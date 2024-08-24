import constant_value as CONST
import MyClasses
import os
import time

llm = MyClasses.LLM_Gemini(CONST.API_KEY)

with open('Forms/Text/Công dân/Học tập/bao_cao_tot_nghiep_du_hoc_sinh.txt', 'r', encoding='utf-8') as f:
    doc = f.read()

handle_text = MyClasses.Text_Processing()
blanked_text, count_blank = handle_text.generate_uniform(doc)

print(blanked_text)

prompt_parts = CONST.form_tagging_prompt.format(main_tag_names= CONST.main_tag_names, relationship_tag_names = CONST.relationship_tag_names, remaining_tag_names = CONST.remaining_tag_names, Form = blanked_text)
response = llm.model.generate_content(prompt_parts)
response = response.text

print(response)

# folder_BlankX = "Forms\Text\Công dân"
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

# #Run with folder "Cong dan"
# for index,filename in enumerate(os.listdir(folder_BlankX)):
#     print(filename)
#     sub_folder = folder_BlankX + '/' + filename
#     for sub_filename in os.listdir(sub_folder):
#         if sub_filename.endswith(".txt"):
#             print("Start with: ", sub_filename)
#             file_dir = folder_BlankX + '/' + filename + '/' +  sub_filename
#             respones_dir = folder_BlankX  + '/' + filename + '/Response1/' + sub_filename
#             # print(file_dir)
#             # print(respones_dir)
#             text = read_file(file_dir)
#             handle_text = MyClasses.Text_Processing()
#             blanked_text, count_blank = handle_text.generate_uniform(text)
#             prompt_parts = CONST.form_tagging_prompt.format(main_tag_names= CONST.main_tag_names, relationship_tag_names = CONST.relationship_tag_names, remaining_tag_names = CONST.remaining_tag_names, Form = blanked_text)
#             response = llm.model.generate_content(prompt_parts)
#             try:
#                 response_text = response.text
#                 write_file(respones_dir, response_text)
#             except:
#                 print(11111111111111111111111111)
#                 pass
#             print("End with: ", sub_filename)
#             time.sleep(5)
