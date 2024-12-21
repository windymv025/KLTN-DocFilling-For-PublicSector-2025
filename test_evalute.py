import re
import Src.MyClasses as MyClasses
import os
from dotenv import load_dotenv
import pandas as pd
import copy

load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")

LLM_class = MyClasses.LLM_Gemini(api_key = gemini_key)
Text_Processing_Class = MyClasses.Text_Processing()

def read_file(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    
def write_file(file_path, text):
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    try:
        with open(file_path, 'w',encoding='utf-8') as file:
            file.write(text)
        print(f"File written successfully to '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")

pattern = r"\[([^\d].*?)\]"

# Function to calculate similarity percentage if lists have the same length
def calculate_similarity(tagnames1, tagnames2):    
    if len(tagnames1) != len(tagnames2):
        return 0.0

    matching_tagnames = [tag1 for tag1, tag2 in zip(tagnames1, tagnames2) if tag1 == tag2]
    
    similarity_percentage = len(matching_tagnames) / len(tagnames1) * 100
    
    return similarity_percentage

#Run with folder 'Công dân All'/Input/Output
Result_Folder = "Forms/Text/Input_test/Input/TagName1/Output_Diff"
Data_Folder = "Forms/Text/Input_test/Label_Output_NDN1"

overall_result = []
nums_copy = 1
index_temp = 0
for index,filename in enumerate(os.listdir(Data_Folder)[0:]):
    if filename.endswith(".txt"):
        # print(inde, "Start with: ", filename)
        overall_result.append([])
        print("========= Index: ",index, "============", filename)
        file_dir = Data_Folder + '/' + filename
        # respones_dir = folder_BlankX + '/Output/' + filename
        text = read_file(file_dir)
        text = text.replace("..........","[another]")
        # Find all matches
        tagnames = re.findall(pattern, text)
        temp1 = copy.deepcopy(tagnames)
        for index1, tagname in enumerate(temp1):
            temp1[index1] = f'{tagname}_{index1}'
        print(temp1)
        # Check result with predict data
        for index_predict,filename_predict in enumerate(os.listdir(Result_Folder)[index*nums_copy:index*nums_copy+nums_copy]):
            if filename_predict.endswith(".txt"):
                file_dir_predict = Result_Folder + '/' + filename_predict
                print("------- Index: ",index, "-------", filename_predict)
                text_predict = read_file(file_dir_predict)
                text_predict = text_predict.replace("..........","[another]")
                tagnames_predict = re.findall(pattern, text_predict)
                temp2 = copy.deepcopy(tagnames_predict)
                for index1, tagname in enumerate(temp2):
                    temp2[index1] = f'{tagname}_{index1}'
                print(temp2)
                overall_result[index_temp].append(calculate_similarity(tagnames, tagnames_predict))
        index_temp += 1       
        # print("End with: ", filename)
        print()
        print()

df_result = pd.DataFrame(overall_result)
df_result.to_csv("result.csv")

print(df_result)