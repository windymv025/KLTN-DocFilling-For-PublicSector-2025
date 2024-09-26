import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from Prompt import *
from dotenv import load_dotenv


load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")

llm = GoogleGenerativeAI(model = 'gemini-1.5-flash', timeout= None, max_tokens = 2000, temperature = 0, top_k = 1, top_p = 1,  google_api_key = gemini_key)

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
    I will provide a description, and you must respond with only the document type in one word (no spaces, no explanations, no extra characters). The answer should be exactly one of the five options above.

    Example:
    Form:
                    TỜ KHAI CĂN CƯỚC CÔNG DÂN
        1. Họ, chữ đệm và tên(1): ..........
        2. Họ, chữ đệm và tên gọi khác (nếu có)(1): ..........
        3. Ngày, tháng, năm sinh:........../........../..........; 4. Giới tính (Nam/nữ): ..........
        5. Số CMND/CCCD: ..........
        6. Dân tộc: ..........; 7. Tôn giáo: .......... 8. Quốc tịch: ..........
        9. Tình trạng hôn nhân: .......... 10. Nhóm máu (nếu có): ..........
        11. Nơi đăng ký khai sinh: ..........
        12. Quê quán: ..........
        13. Nơi thường trú: ..........
        14. Nơi ở hiện tại: ..........
        15. Nghề nghiệp: .......... 16. Trình độ học vấn: ..........
    Answer: Residence and ID Number
    
    Example:
    Form:
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
    Answer: Health and Medical

    Example:
    Form:
        CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    Độc lập - Tự do - Hạnh phúc

    ĐƠN ĐỀ NGHỊ HỖ TRỢ HỌC TẬP 
    (Dùng cho cha mẹ trẻ mẫu giáo hoặc người chăm sóc trẻ mẫu giáo học tại các cơ sở giáo dục công lập)
    Kính gửi: ..........(Cơ sở giáo dục)
    Họ và tên cha mẹ (hoặc người chăm sóc): ..........
    Hộ khẩu thường trú tại:..........
    Là cha/mẹ (hoặc người chăm sóc) của em:..........
    Sinh ngày:..........
    Dân tộc:..........
    Hiện đang học tại lớp:..........
    Trường:..........
    Tôi làm đơn này đề nghị các cấp quản lý xem xét, giải quyết cấp tiền hỗ trợ học tập theo quy định và chế độ hiện hành.

    XÁC NHẬN CỦA ỦY BAN NHÂN DÂN CẤP XÃ1
    Nơi trẻ mẫu giáo có hộ khẩu thường trú
    (Ký tên, đóng dấu)	..........,ngày..........tháng..........năm..........
    Người làm đơn
    (Ký, ghi rõ họ tên)
    Answer: Education

    Example:
    Form: {form}
    Answer:
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
			TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): ..........
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): ..........
3. Ngày, tháng, năm sinh:........../........../..........; 4. Giới tính (Nam/nữ): ..........
5. Số CMND/CCCD: ..........
6. Dân tộc: ..........; 7. Tôn giáo: .......... 8. Quốc tịch: ..........
9. Tình trạng hôn nhân: .......... 10. Nhóm máu (nếu có): ..........
11. Nơi đăng ký khai sinh: ..........
12. Quê quán: ..........
13. Nơi thường trú: ..........
14. Nơi ở hiện tại: ..........
15. Nghề nghiệp: .......... 16. Trình độ học vấn: ..........
"""

# chain = identify_type_form(llm)

# print(chain.invoke(form))
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
    for index, filename in enumerate(os.listdir(folder_dir)[start:end]):
        chain = identify_type_form(llm)
        template_prompt = None
        tagnames = None
        name = None
        if filename.endswith(".txt"):
            print("Start with: ", filename)
            file_dir = folder_dir + '/' + filename
            response_dir = folder_dir + '/TagName/' + filename
            text = read_file(file_dir)
            type = chain.invoke(text)
            print(type.strip())
            if "Residence" in type:
                print("111111111111111111111111111")
                template_prompt = residence_identification_template_prompt
                tagnames = residence_identification_tagnames
                name = "residence_identification_tagnames"
            elif "Education" in type:
                print("222222222222222222")
                template_prompt = study_template_prompt
                tagnames = study_tagnames
                name = "study_tagnames"
            elif "Health" in type:
                print("333333333333333333333")
                template_prompt = health_medical_template_prompt
                tagnames = health_and_medical_tagnames
                name = "health_and_medical_tagnames"
            elif "Vehicle" in type:
                print("44444444444444444444")
                template_prompt = vehicle_driver_template_prompt
                tagnames = vehicle_driver_tagnames
                name = "vehicle_driver_tagnames"
            elif "Employment" in type:
                print("55555555555555555555")
                template_prompt = job_template_prompt
                tagnames = job_tagnames
                name = "job_tagnames"
            else:
                template_prompt = residence_identification_template_prompt
                tagnames = residence_identification_tagnames
                name = "residence_identification_tagnames"
            prompt = PromptTemplate.from_template(template_prompt)
            chain = prompt | llm | StrOutputParser()
            try:
                response = chain.invoke({name: tagnames, "remaining_tag_names": remaining_tag_names, "form": text})
                write_file(response_dir, response)
            except Exception as e:
                print(e)
            print("End with: ", filename)

# auto_generate_tag_names(start = 50, end = -1)

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

