import sys
sys.path.append("./Src")
import MyClasses
import constant_value as CONST
import os
import time

LLM_class = MyClasses.LLM_Gemini(api_key = CONST.API_KEY)
Text_Processing_Class = MyClasses.Text_Processing()

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
        
#Run with folder 'Công dân All'/Input
Input_Folder = "Forms\Input"
for index,filename in enumerate(os.listdir(Input_Folder)):
    # if index<=26:
        # continue
    if index==23:
        break
    if filename.endswith(".txt"):
        print("Start with: ", filename)
        file_dir = Input_Folder + '/' + filename
        text = read_file(file_dir)
        processed_text, count = Text_Processing_Class.generate_uniform(text)
        for i in range(5): #Try to generate 5 times
            respones_dir = Input_Folder + '/Output_TEST/' + filename + '_response_' + str(i) + '.txt'
            while True:
                try:
                    response_text = LLM_class.generate_tagname_cccd_passport(processed_text)
                    break
                except Exception as e:
                    print("Error : ", e)
                    time.sleep(2)
            # response_text = LLM_class.generate_tagname_cccd_passport(processed_text)
        # response_text = LLM_class.generate_tagname_cccd_passport(processed_text)
            write_file(respones_dir, response_text)
            time.sleep(0.5)
        # print(processed_text)
        print("End with: ", filename)
    
#This part will try to generate each tagname for each placeholder
# folder_BlankX = "Forms\Input"

        