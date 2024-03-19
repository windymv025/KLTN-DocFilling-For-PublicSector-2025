from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable, RunnablePassthrough, RunnableConfig, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
# Database
import chromadb
# Agent
from ReAct_Agent import *
from langchain.agents import Tool, AgentExecutor
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.exceptions import OutputParserException
from typing import *
from langchain.tools import BaseTool
from langchain_community.tools import HumanInputRun
# Chainlit
import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider
from chainlit.types import ThreadDict

# Import file khác
from operator import itemgetter
from txt_filling import *

# Biến global
STT = 0

# Prompt
prompt = prompt_query_user() 
template1, prompt1 = txt_prompt() # Fill form
prompt_miss_info =  Identify_missing_info() # Missing Info

# Sau khi hết timeout(user chưa nhập gì cả) thì chạy lại
async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res

# ----------------------- On start -----------------------------
@cl.on_chat_start
async def on_chat_start():
    # Chat setting
    settings = await cl.ChatSettings(
        [
        Select(id="repo_id",label="HuggingFace Repo Id",values=["google/gemma-7b-it", "google/gemma-7b"],initial_index=0,),
        Slider(id="Temperature",label="Temperature",initial=0.01,min=0,max=1,step=0.02,),
        Slider(id="Top-k",label = "Top-k", initial = 30, min = 1, max = 100, step = 1),
        Slider(id="Top-p",label = "Top-p",initial = 0.95, min = 0,max = 1,step = 0.02),
        Slider(id="mnt", label = "Max new tokens", initial = 4000, min = 0, max = 5000, step = 100),
        Switch(id="New", label="New", initial=False),
        ]
    ).send()
    # -............................ Ảnh bìa ............................
    image = cl.Image(path="./fill_form.jpg", name="image1", display="inline")
    await cl.Message(
        content="Tôi là chatbot có nhiệm vụ chính là điền thông tin vào document.",
        elements=[image],
    ).send()
    # ............................. Chat profile ................................
    user = cl.user_session.get("user")
    await cl.Message(
        content=f"Bắt đầu chat user có ID: {user.identifier}"
    ).send()
    # LLM
    llm = HuggingFaceEndpoint(
        repo_id = settings['repo_id'], 
        top_k = settings['Top-k'],
        top_p = settings['Top-p'],
        temperature = settings['Temperature'],
        max_new_tokens = settings['mnt'],
        huggingfacehub_api_token = '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',
    )    
    cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
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
    cl.user_session.set("text",text)
    # Code tiếp tục đoạn chat trước đó
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt1
        | llm
        | StrOutputParser()
    )
    # Missing Information
    miss_info = (
        prompt_miss_info
        | llm
        | StrOutputParser()
    )
    # User session
    cl.user_session.set("runnable", runnable)
    cl.user_session.set('miss_info', miss_info)
    

# ---------------------------------------- On message --------------------------------------
@cl.on_message
async def main(message: cl.Message):
    # # --------------------------- Database --------------------------
    # user = cl.user_session.get("user")

    # client = chromadb.PersistentClient(path="./vectorstore") # path defaults to .chroma
    # collection = client.get_or_create_collection(name="my_programming_" + user.identifier)

    # #Add context to database
    # global STT
    # context = message.content
    # collection.add(
    #     ids=[user.identifier + str(STT)],
    #     documents=[context]
    # )
    # STT += 1

    runnable = cl.user_session.get("runnable")
    text = cl.user_session.get("text")
    msg = cl.Message(content="")
    async for chunk in runnable.astream(
        {
            "context": message.content,
            "question": text,
        },
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
    output = get_output_form(msg.content)
    # Miss information
    miss_info = cl.user_session.get('miss_info')
    msg_miss_info = cl.Message(content="")
    async for chunk in miss_info.astream(
        {
            "output": output,
        },
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg_miss_info.stream_token(chunk)

    list_items = get_output_miss_info(msg_miss_info.content)
    print(list_items)
    # Query user 
    count =  len(list_items)
    while(count):
        query = f"Thông tin về '{list_items[len(list_items)-count]}' hiện đang thiếu, bạn hãy cung cấp thêm thông tin này."
        res = await cl.AskUserMessage(content = query, timeout=30).send()
        if res:
            await cl.Message(content=f"{list_items[len(list_items)-count]}: {res['output']}").send()
        count -= 1
    # Memory
    memory = cl.user_session.get("memory")
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(msg.content)

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
        Select(id="repo_id",label="HuggingFace Repo Id",values=["google/gemma-7b-it", "google/gemma-7b"],initial_index=0,),
        Slider(id="Temperature",label="Temperature",initial=0.01,min=0,max=1,step=0.02,),
        Slider(id="Top-k",label = "Top-k", initial = 30, min = 1, max = 100, step = 1),
        Slider(id="Top-p",label = "Top-p",initial = 0.95, min = 0,max = 1,step = 0.02),
        Slider(id="mnt", label = "Max new tokens", initial = 4000, min = 0, max = 5000, step = 100)
        ]
    ).send()
    await cl.Message(
        content=f"Tiếp tục cuộc hội thoại."
    ).send()
    cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
    # LLM
    llm = HuggingFaceEndpoint(
        repo_id = settings['repo_id'], 
        top_k = settings['Top-k'],
        top_p = settings['Top-p'],
        temperature = settings['Temperature'],
        max_new_tokens = settings['mnt'],
        huggingfacehub_api_token = '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',
    )
    cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
    memory = cl.user_session.get("memory")  # type: ConversationBufferMemory
    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt1
        | llm
        | StrOutputParser()
    )
    cl.user_session.set("runnable", runnable)
    # Missing Info
    miss_info = (
        prompt_miss_info
        | llm
        | StrOutputParser()
    )
    cl.user_session.set('miss_info', miss_info)