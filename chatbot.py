from langchain_community.llms import HuggingFaceEndpoint
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
# Database
from langchain_community.utilities import SQLDatabase
# Chainlit
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider
from chainlit.types import ThreadDict
# Import file khác
from operator import itemgetter
from uniform_text import *
from txt_filling import *
from blank_to_tagname import *
from extract_context import *
from database import *
import os.path

# Prompt
blank_to_tagname_prompt, tag_names, translations = blank_to_tagname_prompt()
extract_info_prompt = extract_info_prompt()
prompt_miss_info =  Identify_missing_info()

# check exist database
if not os.path.isfile("data.db"):
    keys = "ID" + tag_names
    create_database(keys)


# ----------------------- On start -----------------------------
@cl.on_chat_start
async def on_chat_start():
    # Chat setting
    settings = await cl.ChatSettings(
        [
        Slider(id="Temperature",label="Temperature",initial=0,min=0,max=1,step=0.02,),
        Slider(id="Top-k",label = "Top-k", initial = 1, min = 1, max = 100, step = 1),
        Slider(id="Top-p",label = "Top-p",initial = 1, min = 0,max = 1,step = 0.02),
        Slider(id="mnt", label = "Max new tokens", initial = 4000, min = 0, max = 8000, step = 100),
        Switch(id="New", label="New", initial=True),
        Switch(id="Database", label = "Database", initial=False)
        ]
    ).send()
    #
    generation_config = {
        "temperature": settings['Temperature'],
        "top_p": settings['Top-p'],
        "top_k": settings['Top-k'],
        "max_output_tokens": settings['mnt'],
    }
    isGetInfoFromDatabase = settings['Database']
    cl.user_session.set('isGetInfoFromDatabase', isGetInfoFromDatabase)
    # ................................ LLM ......................................
    llm = GoogleGenerativeAI(
        model="gemini-pro",
        safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        },
        generation_config=generation_config,
        google_api_key="AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50")
    cl.user_session.set('llm',llm)
    blank_to_tagname_chain = (
        blank_to_tagname_prompt
        | llm
        | StrOutputParser()
    )
    # -............................ Ảnh bìa ............................
    image = cl.Image(path="./fill_form.jpg", name="image1", display="inline")
    await cl.Message(
        content="Tôi là chatbot có nhiệm vụ chính là điền thông tin vào document.",
        elements=[image],
    ).send()  
    # ................................ Đưa form vào chatbot bất cứ khi nào cũng được................................
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Upload form bạn cần điền thông tin!", accept=["text/plain"]
        ).send()
    text_file = files[0]
    with open(text_file.path, "r", encoding="utf-8") as f:
        text = f.read()  
    await cl.Message(content=f"`{text_file.name}` uploaded, it contains {len(text)} characters!").send() # Thông báo cho người dùng biết đã up file thành công
    text, count_blank = generate_uniform(text)
    await cl.Message(content=text).send()
    list_tag_names = blank_to_tagname(blank_to_tagname_chain, text, count_blank, tag_names)
    await cl.Message(content=list_tag_names).send()
    list_cols, list_keys = get_list_keys(list_tag_names, translations)
    cl.user_session.set('list_keys', list_keys)
    cl.user_session.set('list_cols',list_cols)
    # --------------------------- Database --------------------------
    count_id = count_rows()
    if count_id == 0:
        await cl.Message(content = "Chưa có thông tin trong database. Vui lòng đưa context vào.").send()
        value = "1"
    else:
        list_name_actions = [cl.Action(name = "New", value = str(count_id + 1), label = "0: New")]
        for i in range(count_id):
            name = get_value(i+1,"Full_Name")
            info = f"{i+1}: {name}"
            list_name_actions.append(cl.Action(name = f"Row {i+1}", value = str(i + 1), label = info ))
        res = await cl.AskActionMessage(
            content=f"Chọn lựa chọn phù hợp.",
            actions= list_name_actions
        ).send()
        value = res.get("value")
    print(count_id, value)
    if value != str(count_id + 1): # Điền form bằng cách lấy thông tin từ database
        list_info, list_miss_keys, list_miss_items = get_values(value, list_cols, translations)
        print("11111111111111111111111111111111111")
        print("LIST_INFO:", list_info)
        print("LIST_MISS_KEYS:", list_miss_keys)
        print("LIST_MISS_ITEMS:", list_miss_items)   
    # ---------------------- Lưu user session ---------------------
    cl.user_session.set("value", value)
    cl.user_session.set('list_tag_names', list_tag_names)
    cl.user_session.set("text",text)
    cl.user_session.set("count_blank", count_blank)
    cl.user_session.set("count_id", count_id)


# ---------------------------------------- On message --------------------------------------
@cl.on_message
async def main(message: cl.Message):   
    cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
    # Code tiếp tục đoạn chat trước đó
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    # Tag name cần điền từ form:
    list_tag_names = cl.user_session.get('list_tag_names')
    # ---------------------- Người dùng chọn việc load thông tin từ database hay điền người mới------------------------------
    count_id = cl.user_session.get("count_id")
    value = cl.user_session.get("value")
    list_cols = cl.user_session.get("list_cols")
    list_keys = cl.user_session.get("list_keys")
    list_info = []
    list_miss_items = []
    list_miss_keys = []
    list_index = []
    if value == str(count_id + 1): # Điền form bằng context được nhập vào
        print("22222222222222222222222222222222222")
        # ----------------- Extract information ----------------------------------
        llm = cl.user_session.get('llm')
        extract_info_chain = (
            RunnablePassthrough.assign(
                history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
            )
            | extract_info_prompt
            | llm
            | StrOutputParser()
        )
        print("COLS:", list_cols)
        print("LIST_KEYS: ", list_keys)
        for i, Question in enumerate(list_keys):
            count_miss_items1 = len(list_miss_items)
            res = await extract_info_chain.ainvoke({
                "Abstract": message.content, 
                "Question": Question
            })
            list_info, list_miss_items = get_listInfo_and_missItem(res, list_info, list_miss_items)
            count_miss_items2 = len(list_miss_items)
            if count_miss_items1 != count_miss_items2:
                list_index.append(i)
                list_miss_keys.append(list_tag_names[i])
        await cl.Message(content = f"Thông tin phù hợp với từng Blank: {list_info}").send()
        await cl.Message(content = f"Thông tin còn thiếu: {list_miss_items}").send()
        print("LIST_INFO:", list_info)
        print("LIST_MISS_KEYS:", list_miss_keys)
        print("LIST_MISS_ITEMS:", list_miss_items)
        # Thêm thông tin vào database
        data_to_insert = create_tag_info_dict(value, list_cols, list_info)
        print("DATA_TO_INSERT", data_to_insert)
        insert_value_into_database(data_to_insert)

    # Query user 
    count =  len(list_miss_items)
    data_to_insert = {}
    while(count):
        query = f"Thông tin về '{list_miss_items[len(list_miss_items)-count]}' hiện đang thiếu, bạn hãy cung cấp thêm thông tin này."
        res = await cl.AskUserMessage(content = query, timeout=30).send()
        if res:
            await cl.Message(content=f"{list_miss_items[len(list_miss_items)-count]}: {res['output']}").send()
        list_info[list_index[len(list_miss_items)-count]] = res['output']
        data_to_insert[list_miss_keys[len(list_miss_keys)-count]] = res['output']
        count -= 1
    # Fill Form
    text = cl.user_session.get("text")
    count_blank = cl.user_session.get("count_blank")
    output_form = fill_form(text, list_info, count_blank)
    await cl.Message(content = output_form).send()
    with open('./Output/result.txt','w',encoding='utf-8') as file:
        file.write(output_form)
    # Memory
    memory = cl.user_session.get("memory")
    memory.chat_memory.add_user_message(message.content)

# ------------------------------ Câu lệnh in ra khi user dừng -------------------------------
@cl.on_stop
async def on_stop():
    print("Người dùng muốn dừng công việc này!")

# ------------------ Câu lệnh in ra khi người dùng ngắt kết nối ------------------------------
@cl.on_chat_end
async def on_chat_end():
    print("Người dùng đã ngắt kết nối!")


# --------------------------- Xác thực -------------------------------
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("LHH", "1323"):
        return cl.User(
            identifier="LHH", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
    
# ---------------------------- Chat profile ---------------------------------
@cl.set_chat_profiles
async def chat_profile(current_user: cl.User):
    if current_user.metadata["role"] != "admin":
        return None

    return [
        cl.ChatProfile(
            name="Gemma-7b-it",
            markdown_description="Gemma is a family of lightweight, state-of-the-art open models from Google, built from the same research and technology used to create the Gemini models.",
        ),
    ]    

# ----------------------------- Chat settings update --------------------------
@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)


# --------------------------- Resume ------------------------------------------
@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    memory = ConversationBufferMemory(return_messages=True)
    root_messages = [m for m in thread["steps"] if m["parentId"] == None]
    for message in root_messages:
        if message["type"] == "USER_MESSAGE":
            memory.chat_memory.add_user_message(message["output"])
        else:
            memory.chat_memory.add_ai_message(message["output"])

    cl.user_session.set("memory", memory)

    # Setting
    settings = await cl.ChatSettings(
        [
        Slider(id="Temperature",label="Temperature",initial=0.01,min=0,max=1,step=0.02,),
        Slider(id="Top-k",label = "Top-k", initial = 20, min = 1, max = 100, step = 1),
        Slider(id="Top-p",label = "Top-p",initial = 0.95, min = 0,max = 1,step = 0.02),
        Slider(id="mnt", label = "Max new tokens", initial = 4000, min = 0, max = 5000, step = 100),
        Switch(id="New", label="New", initial=True),
        ]
    ).send()
        #
    generation_config = {
        "temperature": settings['Temperature'],
        "top_p": settings['Top-p'],
        "top_k": settings['Top-k'],
        "max_output_tokens": settings['mnt'],
    }
    # ................................ LLM ......................................
    llm = GoogleGenerativeAI(
        model="gemini-pro",
        safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        },
        generation_config=generation_config,
        google_api_key="AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50")
    await cl.Message(content=f"Tiếp tục cuộc hội thoại.").send()