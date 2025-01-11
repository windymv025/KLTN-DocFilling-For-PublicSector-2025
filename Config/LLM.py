import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")

gemini = GoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    timeout=None,
    max_tokens=1000,
    temperature=0,
    top_k=1,
    top_p=1,
    google_api_key=gemini_key,
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=gemini_key
)
