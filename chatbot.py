import chainlit as cl
from chainlit.input_widget import Switch, Slider
import os
import sys

sys.path.append("./Src")

#Import from another files
import MyClasses
import constant_value as CONST
from database import *

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
        ]
    ).send()

    # ======================Ảnh bìa======================
    image = cl.Image(path="./Additional/fill_form.jpg", name="image1", display="inline")
    await cl.Message(
        content="Tôi là chatbot có nhiệm vụ chính là điền thông tin vào document.",
        elements=[image],
    ).send()  

    # ======================Insert file need to fullfill======================
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Upload form bạn cần điền thông tin!", accept=["text/plain"]
        ).send()
    text_file = files[0]
    with open(text_file.path, "r", encoding="utf-8") as f:
        text = f.read()  

    # print("text \n:",text)
    await cl.Message(content=f"Content:").send()
    await cl.Message(content=text).send()

    ## ======================Handling======================
    llm = MyClasses.LLM_Gemini(CONST.API_KEY)
    handle_text = MyClasses.Text_Processing()

    Blanked_text, _ = handle_text.generate_uniform(text)
    await cl.Message(content=f"Blanked text: \n {Blanked_text}").send()
    # await cl.Message(content=f"Blanked text: \n {blanked_text}blanked_text, count_blank = handle_text.generate_uniform(text)").send()
    # blank_to_tagnames = llm.blank_to_tagnames(blanked_text, CONST.tag_names) ##**Important**
    # list_tag_names = list(blank_to_tagnames.values())
    # print('list_tag_names: ', list_tag_names)
    # list_values = llm.translate_tag_names(list_tag_names, CONST.translations)
    # print('list_values: ', list_values)

    # ## ======================DATABASE======================
    # if not os.path.isfile("data.db"):
    #     keys = "ID" + CONST.tag_names
    #     create_database(keys)
    # count_id = count_rows()
    # if count_id == 0:
    #     await cl.Message(content = "Chưa có thông tin trong database. Vui lòng đưa context vào.").send()
    #     value = "1"
    # else:
    #     list_name_actions = [cl.Action(name = "New", value = str(count_id + 1), label = "0: New")]
    #     for i in range(count_id):
    #         name = get_value(i+1,"Full_Name")
    #         info = f"{i+1}: {name}"
    #         list_name_actions.append(cl.Action(name = f"Row {i+1}", value = str(i + 1), label = info ))
    #     res = await cl.AskActionMessage(
    #         content=f"Chọn lựa chọn phù hợp.",
    #         actions= list_name_actions
    #     ).send()
    #     value = res.get("value")
    # print(count_id, value)
    # if value != str(count_id + 1): # Điền form bằng cách lấy thông tin từ database
    #     list_info, list_miss_keys, list_miss_items = get_values(value, list_tag_names, CONST.translations)
    #     filled_form = handle_text.fill_form(blanked_text, list_info)
    #     print("filled_form: \n",filled_form)
    #     await cl.Message(
    #         content = f"Filled form: \n {filled_form}"
    #     ).send()

    # # # ---------------------- Save user session ---------------------
    # cl.user_session.set("blank_to_tagnames",blank_to_tagnames)
    # cl.user_session.set("count_blank",count_blank)
    # cl.user_session.set("handle_text",handle_text)
    # cl.user_session.set("llm",llm)
    # cl.user_session.set("blanked_text", blanked_text)
    # cl.user_session.set("list_tag_names", list_tag_names)
    # cl.user_session.set("list_values", list_values)
    # cl.user_session.set("value", value)
    # cl.user_session.set("count_id", count_id)


@cl.on_message
async def main(message: cl.Message):
    # cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
    # # ---------------------- Take again user session ---------------------
    blank_to_tagnames = cl.user_session.get("blank_to_tagnames")
    count_blank = cl.user_session.get("count_blank")
    handle_text = cl.user_session.get("handle_text")
    llm = cl.user_session.get("llm")
    blanked_text = cl.user_session.get("blanked_text")
    list_tag_names = cl.user_session.get("list_tag_names")
    list_values = cl.user_session.get("list_values")
    value = cl.user_session.get("value")
    count_id = cl.user_session.get("count_id")
    # Get response
    context = message.content
    if value == str(count_id + 1): # Điền form bằng context được nhập vào
        #Get infor context by LLM
        value_keys_to_context_value = llm.extract_content(context, list_values) ##**Important**
        await cl.Message(
            content = f"value_keys_to_context_value: \n {value_keys_to_context_value}"
        ).send()
    # List info
    list_info = handle_text.getlistInfo(value_keys_to_context_value, list_values)
    data_to_insert = handle_text.create_tag_info_dict(value, list_tag_names, list_info)
    insert_value_into_database(value, data_to_insert)
    await cl.Message(content = data_to_insert).send()
    # Query user
    list_miss_items, list_miss_keys, list_index = handle_text.getMissItem(value_keys_to_context_value, CONST.translations, list_values)
    # print("LIST_MISS_ITEMS: ", list_miss_items)
    # print("LIST_MISS_KEYS: ", list_miss_keys)
    # print("LIST_INDEX: ", list_index)
    count =  len(list_miss_items)
    data_to_update = {'Empty': '#Empty',}
    while(count):
        miss_item = list_miss_items[len(list_miss_items)-count]
        if miss_item == 'Trống':
            count -= 1
            continue
        query = f"Thông tin về '{miss_item}' hiện đang thiếu, bạn hãy cung cấp thêm thông tin này."
        res = await cl.AskUserMessage(content = query, timeout=30).send()
        if res:
            await cl.Message(content=f"{list_miss_items[len(list_miss_items)-count]}: {res['output']}").send()
        list_info[list_index[len(list_miss_items)-count]] = res['output']
        temp = list_miss_keys[len(list_miss_keys)-count].replace("#","")
        data_to_update[temp] = res['output']
        count -= 1
    await cl.Message(content = data_to_update).send()
    update_value_in_database(value, data_to_update)

    #============================Filled Form============================
    filled_form = handle_text.fill_form(blanked_text, list_info)
    print("filled_form: \n",filled_form)
    await cl.Message(
        content = f"Filled form: \n {filled_form}"
    ).send()
    

# ------------------------------ Stop section ------------------------------
@cl.on_stop
async def on_stop():
    print("Người dùng muốn dừng công việc này!")

# ------------------------------ End section ------------------------------
@cl.on_chat_end
async def on_chat_end():
    print("Người dùng đã ngắt kết nối!")

# --------------------------- Authentication -------------------------------
# @cl.password_auth_callback
# def auth_callback(username: str, password: str):
#     # Fetch the user matching username from your database
#     # and compare the hashed password with the value stored in the database
#     if (username, password) == ("LHH", "1323"):
#         return cl.User(
#             identifier="LHH", metadata={"role": "admin", "provider": "credentials"}
#         )
#     else:
#         return None
    
# ----------------------------- Chat settings update --------------------------
# @cl.on_settings_update
# async def setup_agent(settings):
#     print("on_settings_update", settings)
 