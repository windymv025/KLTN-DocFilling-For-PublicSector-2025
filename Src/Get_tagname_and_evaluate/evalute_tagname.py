import re
import sys
sys.path.append("./Src")
import MyClasses
import constant_value as CONST
import os
import pandas as pd

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

# Regular expression to find all occurrences of tagnames in square brackets
pattern = r"\[([^\]]+)\]"

# Function to calculate similarity percentage if lists have the same length
def calculate_similarity(tagnames1, tagnames2):
    # Check if the lengths are different
    if len(tagnames1) != len(tagnames2):
        return 0.0  # Return 0% similarity if lengths are different

    matching_tagnames = [tag1 for tag1, tag2 in zip(tagnames1, tagnames2) if tag1 == tag2]
    
    # Calculate similarity percentage as the ratio of matching tagnames to total tagnames
    similarity_percentage = len(matching_tagnames) / len(tagnames1) * 100
    
    return similarity_percentage

#Run with folder 'Công dân All'/Input/Output
Result_Folder = "Forms\Input\Output_Hung\Output_Diff"
Data_Folder = "Forms\Input\Data1"

overall_result = []
nums_copy = 1
for index,filename in enumerate(os.listdir(Data_Folder)):
    # if index!=3:
    #     continue
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
        print(tagnames)
        # Check result with predict data
        for index_predict,filename_predict in enumerate(os.listdir(Result_Folder)[index*nums_copy:index*nums_copy+nums_copy]):
            if filename_predict.endswith(".txt"):
                file_dir_predict = Result_Folder + '/' + filename_predict
                text_predict = read_file(file_dir_predict)
                text_predict = text_predict.replace("..........","[another]")
                tagnames_predict = re.findall(pattern, text_predict)
                print(tagnames_predict)
                overall_result[index].append(calculate_similarity(tagnames, tagnames_predict))
                
        # print("End with: ", filename)
        print()
        print()

df_result = pd.DataFrame(overall_result)
df_result.to_csv("result.csv")
print(df_result)



