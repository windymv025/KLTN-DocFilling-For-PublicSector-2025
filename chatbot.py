import chainlit as cl
from chainlit.input_widget import Switch, Slider
import os
from dotenv import load_dotenv

#Import from another files
import Src.MyClasses as MyClasses
from Src.database import *


load_dotenv()
gemini_api_key = os.getenv('GEMINI_KEY')

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
    image = cl.Image(path="./fill_form.jpg", name="image1", display="inline")
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

    await cl.Message(f'**Content:**\n{text}').send()

    ## ======================EXTRACT LIST TAG NAME FROM FORM======================
    llm = MyClasses.LLM_Gemini(gemini_api_key)
    # handle_text = MyClasses.Text_Processing()
    # edited_text, count_blank = handle_text.generate_uniform(text)
    # await cl.Message(content=f"Text: \n {edited_text}").send()
    form_with_tag_name, list_tag_names, type = llm.blank_to_tagnames(text)
    # await cl.Message("List tag name: ", list_tag_names).send()

    ## ======================DATABASE======================

    ## ======================FILL FORM=====================

    ## =================== Save user session =======================
    cl.user_session.set("llm",llm)
    cl.user_session.set("form_with_tag_name", form_with_tag_name)
    cl.user_session.set("list_tag_names", list_tag_names)


@cl.on_message
async def main(message: cl.Message):
    # cl.user_session.set("memory", ConversationBufferMemory(return_messages=True))
    # # ---------------------- Take again user session ---------------------
    llm = cl.user_session.get("llm")
    form_with_tag_name = cl.user_session.get("form_with_tag_name")
    list_tag_names = cl.user_session.get("list_tag_names")
    # Get response
    context = message.content
    
    

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
 