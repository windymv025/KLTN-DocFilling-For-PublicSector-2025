import os
import sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# print(sys.path)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# from identify_form_types import identify_form_type
from Tagnames.identify_form_types import identify_form_type
from Prompts.define_tagnames import (
    residence_identification_template_prompt,
    study_template_prompt,
    health_medical_template_prompt,
    vehicle_driver_template_prompt,
    job_template_prompt,
    tagname_Nam_ver1_prompt
)
from Config.tagnames import (
    residence_identification_tagnames,
    study_tagnames,
    health_and_medical_tagnames,
    vehicle_driver_tagnames,
    job_tagnames,
    remaining_tag_names,
    tagname_Nam_ver1
)
from Config.LLM import gemini
from Utils.text_processing import Text_Processing

def define_tagname(llm, text):
    type = identify_form_type(llm, text)
    if "1" in type:
        template_prompt = residence_identification_template_prompt
        tagnames = residence_identification_tagnames
        name = "residence_identification_tagnames"
    elif "2" in type:
        template_prompt = study_template_prompt
        tagnames = study_tagnames
        name = "study_tagnames"
    elif "3" in type:
        template_prompt = health_medical_template_prompt
        tagnames = health_and_medical_tagnames
        name = "health_and_medical_tagnames"
    elif "4" in type:
        template_prompt = vehicle_driver_template_prompt
        tagnames = vehicle_driver_tagnames
        name = "vehicle_driver_tagnames"
    elif "5" in type:
        template_prompt = job_template_prompt
        tagnames = job_tagnames
        name = "job_tagnames"
    else:
        template_prompt = residence_identification_template_prompt
        tagnames = residence_identification_tagnames
        name = "residence_identification_tagnames"
    prompt = PromptTemplate.from_template(template_prompt)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(
        {name: tagnames, "remaining_tag_names": remaining_tag_names, "form": text}
    )
    return response

def define_tagname_Nam_ver1(llm, text):
    prompt = PromptTemplate.from_template(tagname_Nam_ver1_prompt)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke(
        {"tagname": tagname_Nam_ver1, "form": text}
    )
    return response


def generate_tagnames(input_folder, output_folder):
    T = True
    while T:
        T = False
        files_to_process = [filename for filename in os.listdir(output_folder) if filename.endswith(".txt")]
        for index, filename in enumerate(os.listdir(input_folder)):
            if filename.endswith(".txt"):
                if filename in files_to_process:
                    continue
                else:
                    T = True
                # Read txt
                file_path = input_folder + "/" + filename
                text = Text_Processing().Read_txt_file(file_path)
                try:
                    # llm_filled = define_tagname(gemini, text)
                    llm_filled = define_tagname_Nam_ver1(gemini, text)
                    # Save to output_folder
                    output_path = output_folder + "/" + filename
                    Text_Processing().Save_txt_file(output_path, llm_filled)
                    print(f"File {filename} is generated successfully!!")
                except Exception as e:
                    print(f"Error: {e} at file {filename}")
                    continue


text = """
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: (1)..........
Họ, chữ đệm, tên người yêu cầu: ..........
Nơi cư trú: (2)..........
Giấy tờ tùy thân: (3)..........
Quan hệ với người được khai sinh: ..........
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên:..........
Ngày, tháng, năm sinh: ........../........../..........ghi bằng chữ: ..........
Giới tính:.......... Dân tộc:..........Quốc tịch: ..........
Nơi sinh: (4)..........
Quê quán: ..........
Họ, chữ đệm, tên người mẹ: ..........
Năm sinh: (5)..........Dân tộc:..........Quốc tịch: ..........
Nơi cư trú: (2) ..........
Họ, chữ đệm, tên người cha: ..........
Năm sinh: (5)..........Dân tộc:..........Quốc tịch: ..........
Nơi cư trú: (2) ..........
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: .........., ngày .......... tháng .......... năm ..........
"""

# print(define_tagname(gemini, text))
