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

def print_tagnames(tagnames):
    print("======Tagnames======")
    for index,tagname in enumerate(tagnames):
        print(tagname + f"_{index}", end=", ")
    print()

def similarity_two_forms(form1, form2):
    # Replace all ".........." by "[#another]"
    form1 = form1.replace("..........","[#another]")
    form2 = form2.replace("..........","[#another]")
    # Find all matches
    pattern = r"\[([^\]]+)\]"
    tagnames1 = re.findall(pattern, form1)
    tagnames2 = re.findall(pattern, form2)
    #print tagnames to check
    print_tagnames(tagnames1)
    print_tagnames(tagnames2)
    # Calculate similarity percentage
    similarity_percentage = calculate_similarity(tagnames1, tagnames2)
    return similarity_percentage

similarity_result_forms = []
nums_copy = 1
index_result = 0

#Run with folder 'Công dân All'/Input/Output
Result_Folder = "Forms/Input/Output/Uniform_Date/Output_Diff"
Data_Folder = "Forms/Input/Data1/Uniform_Date"

Data_Input_Folder = "Forms/Data_Testing/Input"
Data_Label_Folder = "Forms/Data_Testing/Label_Output"
Data_Testing_Folder = "Forms/Data_Testing/Test_Fill_By_Label"

Data_LLM_Filled_Folder = "Forms/Data_Testing/Result_LLM_Filled_Hung"
Data_LLM_Filled_Processed_Folder = "Forms/Data_Testing/Result_LLM_Filled_Hung_Processed"

for index,filename in enumerate(os.listdir(Data_Label_Folder)):
    if filename.endswith(".txt"):
        similarity_result_forms.append([])
        print("========= Index: ",index, "============", filename)
        file_dir_label = Data_Label_Folder + '/' + filename
        file_dir_predict = Data_LLM_Filled_Processed_Folder + '/Output_Diff/' + filename
        #read
        text = read_file(file_dir_label)
        text_predict = read_file(file_dir_predict)
        similarity_result_forms[index_result].append(similarity_two_forms(text, text_predict))
        index_result += 1   

#Save to csv
df_result = pd.DataFrame(similarity_result_forms)
df_result.to_csv("result.csv")
print(df_result)



