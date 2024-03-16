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
from chainlit.sync import run_sync
from chainlit.input_widget import Select, Switch, Slider
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider
from chainlit.types import ThreadDict

# Import file khác
from operator import itemgetter
from txt_filling import *


# Template để chatbot có thể hỏi lại User nếu cần thêm thông tin
template1 = '''
    <start_of_turn>user
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    <end_of_turn>
    <start_of_turn>model
    ''' 

prompt = ChatPromptTemplate.from_template(template1) # Agent
template1, prompt1 = txt_prompt()

# Sau khi hết timeout(user chưa nhập gì cả) thì chạy lại
async def ask_helper(func, **kwargs):
    res = await func(**kwargs).send()
    while not res:
        res = await func(**kwargs).send()
    return res

# ------------------------------------- Tool to ask user ------------------------------------------

class HumanInputChainlit(BaseTool):
    """Tool that adds the capability to ask user for input."""

    name = "Human"
    description = ( # You can provide few-shot examples as a part of the description.
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )

    def _run(self, query: str, run_manager=None) -> str:
        """Use the Human input tool."""
        res = run_sync(ask_helper(cl.AskUserMessage, content=query).send())
        return res["content"]
    
    async def _arun(self, query: str, run_manager=None) -> str:
        """Use the Human input tool."""
        res = await ask_helper(cl.AskUserMessage, content=query).send()
        return res["output"]


# ----------------------- On start -----------------------------
@cl.on_chat_start
async def on_chat_start():
    # Chat setting
    settings = await cl.ChatSettings(
        [
        Select(id="repo_id",label="HuggingFace Repo Id",values=["google/gemma-7b-it", "google/gemma-7b"],initial_index=0,),
        Slider(id="Temperature",label="Temperature",initial=0.1,min=0,max=1,step=0.05,),
        Slider(id="Top-k",label = "Top-k", initial = 30, min = 1, max = 100, step = 1),
        Slider(id="Top-p",label = "Top-p",initial = 0.95, min = 0,max = 1,step = 0.05),
        Slider(id="mnt", label = "Max new tokens", initial = 3000, min = 0, max = 5000, step = 100)
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
    chat_profile = cl.user_session.get("chat_profile")
    await cl.Message(
        content=f"Bắt đầu chat với {user.identifier} dùng {chat_profile} chat profile"
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
    llm_chat = ChatHuggingFace(llm=llm)
    # Agent
    tools = [  
    HumanInputChainlit(),
    Tool(
        name = "Agent",
        func = llm_chat.invoke,
        description = "I will query you if I need additional information",
        coroutine = llm_chat.ainvoke,
    )]
    agent = create_react_agent(tools = tools, llm = llm, prompt = prompt) # Create an agent that uses ReAct prompting.
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, memory=memory
    )
    cl.user_session.set("agent", agent_executor)  
    cl.user_session.set("runnable", runnable)

# ---------------------------------------- On message --------------------------------------
@cl.on_message
async def main(message: cl.Message):
    # # Agent
    # agent = cl.user_session.get("agent")  # type: AgentExecutor
    # res_agent = await agent.ainvoke(
    # {
    #     "input": message.content,
    # }, 
    # callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=["FINAL","ANSWER"])]
    # )
    # await cl.Message(content=res_agent).send()
    # Runnable
    client = chromadb.PersistentClient(path="./vectorstore") # path defaults to .chroma
    collection = client.get_or_create_collection(name="my_programming_collection")
    runnable = cl.user_session.get("runnable")
    text = cl.user_session.get("text")
    res = await runnable.ainvoke(
        {
            "context": message.content,
            "question": text,
        },
        callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True, answer_prefix_tokens=["FINAL","ANSWER"])]
    )
    await cl.Message(content = res).send()
    # Memory
    memory = cl.user_session.get("memory")
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(res)

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
        Slider(id="Temperature",label="Temperature",initial=0.1,min=0,max=1,step=0.05,),
        Slider(id="Top-k",label = "Top-k", initial = 30, min = 1, max = 100, step = 1),
        Slider(id="Top-p",label = "Top-p",initial = 0.8,min = 0,max = 1,step = 0.05),
        Slider(id="mnt", label = "Max new tokens", initial = 0.8, min = 0, max = 1, step = 0.05)
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
