import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# print(sys.path)
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from Prompts.define_tagnames import tagname_Nam_ver1_prompt
from Config.tagnames import tagname_Nam_ver1
# import ollama

from Config.LLM import gemini
from Utils.text_processing import Text_Processing

def define_tagname_Nam_ver1(llm, text):
    prompt = PromptTemplate.from_template(tagname_Nam_ver1_prompt)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke(
        {"tagname": tagname_Nam_ver1, "form": text}
    )
    return response

def generate_tagnames(input_folder, output_folder):
    T = True
    file_to_process = []
    # file_to_process = [
    #     "input_104.txt",
    #     "input_144.txt",
    #     "input_76.txt",
    #     "input_173.txt",
    #     "input_53.txt",
    #     "input_83.txt",
    #     "input_98.txt",
    #     "input_141.txt",
    #     "input_146.txt",
    #     "input_185.txt",
    #     "input_62.txt",
    #     "input_64.txt",
    #     "input_16.txt",
    #     "input_33.txt",
    #     "input_92.txt",
    #     "input_96.txt",
    #     "input_136.txt",
    #     "input_153.txt",
    #     "input_154.txt",
    #     "input_177.txt",
    #     "input_86.txt",
    #     "input_12.txt",
    #     "input_60.txt",
    #     "input_90.txt",
    #     "input_55.txt",
    #     "input_80.txt",
    #     "input_196.txt",
    #     "input_152.txt",
    #     "input_160.txt",
    #     "input_51.txt",
    #     "input_148.txt",
    #     "input_75.txt",
    #     "input_157.txt",
    #     "input_182.txt",
    #     "input_65.txt",
    #     "input_100.txt",
    #     "input_150.txt",
    #     "input_199.txt",
    #     "input_78.txt",
    #     "input_132.txt",
    #     "input_164.txt",
    #     "input_133.txt",
    #     "input_73.txt",
    #     "input_139.txt",
    #     "input_168.txt",
    #     "input_109.txt",
    #     "input_125.txt",
    #     "input_128.txt",
    #     "input_70.txt",
    #     "input_140.txt",
    #     "input_56.txt",
    #     "input_145.txt",
    #     "input_161.txt",
    #     "input_89.txt",
    #     "input_61.txt"
    #     ]
    
    while T:
        T = False  
        files_processed = [filename for filename in os.listdir(output_folder) if (filename.endswith(".txt") and filename not in file_to_process)]
        for index, filename in enumerate(os.listdir(input_folder)):
            if filename.endswith(".txt"):
                if filename in files_processed:
                    continue
                else:
                    T = True
                # Remove in file_to_process
                if filename in file_to_process:
                    file_to_process.remove(filename)
                # Read txt
                file_path = input_folder + "/" + filename
                text = Text_Processing().Read_txt_file(file_path)
                try:
                    llm_filled = define_tagname_Nam_ver1(gemini, text)
                    while not llm_filled.strip():  # Check if empty or contains only whitespace
                        llm_filled = define_tagname_Nam_ver1(gemini, text)
                    # print(llm_filled)
                    # Save to output_folder
                    output_path = output_folder + "/" + filename
                    Text_Processing().Save_txt_file(output_path, llm_filled)
                    print(f"File {filename} is generated successfully!!")
                except Exception as e:
                    print(f"Error: {e} at file {filename}")
                    continue

    print("Done Generate Tagnames")                

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

