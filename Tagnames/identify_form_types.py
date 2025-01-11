import sys
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Prompts.identify_form_types import *
from Config.LLM import *


def identify_form_type(llm, form):
    # Tạo retriever
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=gemini_key
    )
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    splits = text_splitter.create_documents([type_form_feature])
    vectostore = FAISS.from_documents(splits, embeddings)
    retriever = vectostore.as_retriever()
    prompt = PromptTemplate.from_template(identify_form_type_template)
    chain = (
        ({"context": retriever, "form": RunnablePassthrough()})
        | prompt
        | llm
        | StrOutputParser()
    )
    form_type = chain.invoke(form)
    return form_type.strip()
