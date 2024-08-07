import sys
sys.path.append("./Src")
import MyClasses
import constant_value as CONST
import os

LLM_class = MyClasses.LLM_Gemini(api_key = CONST.API_KEY)
Text_Processing_Class = MyClasses.Text_Processing()

folder_BlankX = "Forms\Text\Công dân\Có con nhỏ"
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
    
for index,filename in enumerate(os.listdir(folder_BlankX)):
    # if index==5:
    #     break
    if filename.endswith(".txt"):
        print("Start with: ", filename)
        file_dir = folder_BlankX + '/' + filename
        respones_dir = folder_BlankX + '/Response/' + filename
        text = read_file(file_dir)
        processed_text = Text_Processing_Class.generate_uniform(text)[0]
        # print(text)
        # print("Processing....")
        # print(processed_text)
        response_text = LLM_class.generate_user_tagname_from_blankX_form(processed_text)
        # print(response_text)
        write_file(respones_dir, response_text)
        print("End with: ", filename)
        print("=====================================")

        


"""
Process txt scratch into Blankx txt
# folder = "./Forms/Text"
# folder_BlankX = "./Forms/Text/BlankX"
# # Function to read file contents
# def read_file(file_path):
#     try:
#         with open(file_path, 'r',encoding='utf-8') as file:
#             return file.read()
#     except FileNotFoundError:
#         print(f"The file {file_path} does not exist.")
#         return None
    
# def write_file(file_path, text):
#     os.makedirs(os.path.dirname(file_path),exist_ok=True)
    
#     # Write content to the file
#     try:
#         with open(file_path, 'w',encoding='utf-8') as file:
#             file.write(text)
#         print(f"File written successfully to '{file_path}'.")
#     except Exception as e:
#         print(f"An error occurred while writing the file: {e}")
    
# for filename in os.listdir(folder):
#     if filename.endswith(".txt"):
#         file_dir = folder + '/' + filename
#         text = read_file(file_dir)
#         processed_text = Text_Processing_Class.generate_uniform(text)
#         file_BlankX_dir = folder_BlankX + '/' + filename
#         # print(processed_text[0])
#         write_file(file_BlankX_dir, processed_text[0])
#         # break
"""
