import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import constant_value as CONST
from Prompt import *
from dotenv import load_dotenv


load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")

llm = GoogleGenerativeAI(model = 'gemini-1.5-flash', max_retries= 2, timeout= None, max_tokens = None, google_api_key = gemini_key)

def identify_type_form(llm):
    # Tạo retriever
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key = gemini_key)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    splits = text_splitter.create_documents([residence_identification_tagnames, study_tagnames, health_and_medical_tagnames, vehicle_driver_tagnames, job_tagnames])
    vectostore = FAISS.from_documents(splits, embeddings)
    retriever = vectostore.as_retriever()
    template = """
    You are an expert at classifying documents into their appropriate categories. There are five types of documents you need to distinguish:

    1. Residence and ID Number
    2. Education
    3. Health and Medical
    4. Vehicle and Driving
    5. Employment
    I will provide you with a description of common information typically found in each type of document.

    Context: {context}

    Your task is to analyze the provided form and accurately determine which of the five document types it belongs to.

    Form: {form}
    """

    prompt = PromptTemplate.from_template(template)


    chain = (
        (
            {
                "context" : retriever,
                "form": RunnablePassthrough()
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


form = """
                        TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ

I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): ............................................	[02]. Giới tính: ............................................
[03]. Ngày, tháng, năm sinh: ...../...../......	  [04]. Quốc tịch: ............................................
[05]. Dân tộc: ........................	[06]. Số CCCD/ĐDCN/Hộ chiếu: .........................................	
[07]. Điện thoại: ............................	[08]. Email (nếu có): ............................................	
[09]. Nơi đăng ký khai sinh: [09.1]. Xã: .........................	[09.2]. Huyện: ................................ [09.3]. Tỉnh: ........................
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): ..................................................
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: ............................
[12]. Số nhà, đường/phố, thôn/xóm: ............................................	
[13]. Xã: ..........................	[14]	Huyện: .............................	[15]. Tỉnh: ....................................... 	
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
"""

# chain = identify_type_form(llm)
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
            prompt = PromptTemplate.from_template(health_medical_template_prompt)
            chain = prompt | llm | StrOutputParser()
            try:
                response = chain.invoke({"health_and_medical_tagnames": health_and_medical_tagnames, "remaining_tag_names": remaining_tag_names, "form": text})
                write_file(response_dir, response)
            except Exception as e:
                print("111111111111111111111111111")
            print("End with: ", filename)

auto_generate_tag_names(start = 35, end = 36)

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

