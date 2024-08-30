import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import constant_value as CONST
from Prompt import *
from dotenv import load_dotenv


load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")

llm = GoogleGenerativeAI(model = 'gemini-1.5-flash', max_retries= 2, timeout= None, max_tokens = None, google_api_key = gemini_key)

# Function to read file contents
def read_file(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    
def write_file(file_path, text):
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    # Write content to the file
    try:
        with open(file_path, 'w',encoding='utf-8') as file:
            file.write(text)
        print(f"File written successfully to '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")
           
        
def auto_generate_tag_names(llm = llm, folder_dir = "Forms/Text/Input/Output", start = 0 , end = 10): # Phải có start và end chứ nếu không nó sẽ lỗi gemini
    for index,filename in enumerate(os.listdir(folder_dir)[start:end]):
        if filename.endswith(".txt"):
            print("Start with: ", filename)
            file_dir = folder_dir + '/' + filename
            response_dir = folder_dir + '/TagName/' + filename
            text = read_file(file_dir)
            prompt = PromptTemplate.from_template(template_PI_prompt)
            chain = prompt | llm | StrOutputParser()
            try:
                response = chain.invoke({"personal_information_tagnames": personal_information_tagnames, "remaining_tag_names": remaining_tag_names, "form": text})
                write_file(response_dir, response)
            except Exception as e:
                print("111111111111111111111111111")
            print("End with: ", filename)

auto_generate_tag_names(start = 0, end = 1)

def auto_identify_relationship(llm = llm, folder_dir = "Forms/Text/Input/Output/TagName", save_dir = "Forms/Text/Input/Output/", start = 0, end = 10):
    for index,filename in enumerate(os.listdir(folder_dir)[start:end]):
        if filename.endswith(".txt"):
            print("Start with: ", filename)
            file_dir = folder_dir + '/' + filename
            respones_dir = save_dir + '/Relationship/' + filename
            text = read_file(file_dir)
            prompt_parts2 = template_identify_relationship_prompt.format(form = text)
            response2 = llm.model.generate_content(prompt_parts2)
            write_file(respones_dir, response2.text)

