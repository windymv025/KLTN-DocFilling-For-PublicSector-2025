# Import
import re
import sys
sys.path.append("./Src")
import os
import pandas as pd
import joblib

# Import Classes
import MyClasses
import constant_value as CONST

#Classes
LLM_class = MyClasses.LLM_Gemini(api_key = CONST.API_KEY)
Text_Processing_Class = MyClasses.Text_Processing()

# 1. From forms response by LLM --> get tagnames to input forms
def filled_input_from_filled_form(input_folder, filled_folder):
    for index,filename in enumerate(os.listdir(input_folder)):
        if filename.endswith(".txt"):
            #Input - filled
            file_input_dir = input_folder + '/' + filename
            file_filled_dir = filled_folder + '/' + filename
            # Read
            input_text = Text_Processing_Class.Read_txt_file(file_input_dir)
            filled_text = Text_Processing_Class.Read_txt_file(file_filled_dir)
            #Replace all ".........." by "[another]"
            input_text = input_text.replace("..........","[#another]")
            filled_text = filled_text.replace("..........","[#another]")

            #Print debug
            try:
                filled_input_text = Text_Processing_Class.fill_input_by_llm_form(filled_text, input_text)
                #Save
                output_dir = CONST.Output_folder+ '/' + filled_folder.split("/")[-1] + "/" + input_folder.split("/")[-1] + "/" + filename
                Text_Processing_Class.Save_txt_file(output_dir, filled_input_text)

                # Save to Process_ouput folder
                process_output_dir = CONST.Process_ouput_folder + '/' + filled_folder.split("/")[-1] + "/" + input_folder.split("/")[-1] + "/" + filename
                remove_filled_text = Text_Processing_Class.remove_different_tagnames(filled_input_text)
                Text_Processing_Class.Save_txt_file(process_output_dir, remove_filled_text)
            except Exception as e:
                print(filename)
                print(e)
                break

# File paths
input_dirs = CONST.Input_folder
filled_dirs = CONST.LLM_filled_folder
label_firs = CONST.Label_folder


# Pass values from llm filled file to input --> Output
for input_dir in input_dirs:
    for filled_dir in filled_dirs:
        filled_input_from_filled_form(input_dir, filled_dir)
        

# 2. Add file to process_output_dir folder (remove different tagnames in processed forms, and label form)
# Add label file to process_output_dir folder
for label_dir in label_firs:
    for index,filename in enumerate(os.listdir(label_dir)):
        if filename.endswith(".txt"):
            file_dir = label_dir + '/' + filename
            # Read
            label_text = Text_Processing_Class.Read_txt_file(file_dir)
            # Remove different tagnames
            label_text = Text_Processing_Class.remove_different_tagnames(label_text)
            # Save to evaluate folder
            output_dir = CONST.Process_ouput_folder + '/' + label_dir.split("Forms/",1)[1] + "/" + filename
            Text_Processing_Class.Save_txt_file(output_dir, label_text)

# 3. Evaluate similarity between processed forms and label forms
# Function to calculate similarity percentage if lists have the same length
def calculate_similarity(tagnames1, tagnames2):
    '''
    - Hàm kiểm tra độ tương đồng hai list tagname1 (label), tagname2(LLM-filled)
    - Trả về các độ đo:

    + Độ đủ: điền đủ không (len = len)
    + A1-A1: Count of correct matches in subset A.
    + A1-A2: Count of misclassifications in subset A.
    + A1-B: Count of unrecognized subset A tagnames (labeled as #another). 
    + B-A1: Count of false positives (LLM incorrectly identifies subset A).
    + B-B: Count of correct non-A tagnames assigned as #another.
    '''
    our_40_tagnames = Text_Processing_Class.Summary_tagnames()
    # Check if the lengths are different
    if len(tagnames1) != len(tagnames2):
        metrics = {
            "completeness": 0,
            "A1-A1": 0,
            "A1-A2": 0,
            "A1-B": 0,
            "B-A1": 0,
            "B-B": 0,
        }
        return metrics  # Return 0% similarity if lengths are different

    # Initialize counters
    A1_A1, A1_A2, A1_B, B_A1, B_B = 0, 0, 0, 0, 0
    count_label = 0  # To track valid tagnames in subset_A

    for tag1,tag2 in zip(tagnames1,tagnames2):
        # Standardize tagnames by replacing userX with user0
        standardized_tag1 = re.sub(r'user\d+', 'user0', tag1)
        standardized_tag2 = re.sub(r'user\d+', 'user0', tag2)
        # Replace "dob_date" with "dob" exactly
        standardized_tag1 = re.sub(r'dob_date', 'dob', standardized_tag1)
        standardized_tag2 = re.sub(r'dob_date', 'dob', standardized_tag2)
        # Check if ground truth tagname is in subset_A
        if standardized_tag1 in our_40_tagnames:
            count_label += 1
            if standardized_tag2 in our_40_tagnames:
                if standardized_tag1 == standardized_tag2:
                    A1_A1 += 1  # Exact match
                else:
                    A1_A2 += 1  # Incorrect match within subset A
            else:
                A1_B += 1  # Missed, filled with something outside subset A
        else:
            if standardized_tag2 in our_40_tagnames:
                B_A1 += 1  # Incorrectly predicted a tagname in subset A
            else:
                B_B += 1  # Both are outside subset A (#another case)

    # matching_tagnames = [tag1 for tag1, tag2 in zip(tagnames1, tagnames2) if tag1 == tag2]
    
    # Completeness and accuracy
    completeness = 100.0 if len(tagnames1) == len(tagnames2) else 0.0
    accuracy = A1_A1 / count_label * 100 if count_label > 0 else 0.0
    
    # Compile results
    metrics = {
        "completeness": completeness,
        "A1-A1": A1_A1,
        "A1-A2": A1_A2,
        "A1-B": A1_B,
        "B-A1": B_A1,
        "B-B": B_B,
    }

    return metrics

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
    # Calculate similarity percentage
    similarity_percentage = calculate_similarity(tagnames1, tagnames2)
    if similarity_percentage["A1-A2"] != 0:
        print(similarity_percentage["A1-A2"])
        print_tagnames(tagnames1)
        print_tagnames(tagnames2)
        return similarity_percentage
        # print("Lengths are different")
    return similarity_percentage

def similarity_result_two_folders(folder1, folder2):
    similarity_result_forms = []
    form_names = []
    index_result = 0
    for index, filename in enumerate(os.listdir(folder1)):
        if filename.endswith(".txt"):
            similarity_result_forms.append([])
            print("========= Index: ",index, "============", filename)
            file_dir_label = folder1 + '/' + filename
            file_dir_predict = folder2 + '/' + filename
            # Read
            text_label = Text_Processing_Class.Read_txt_file(file_dir_label)
            text_predict = Text_Processing_Class.Read_txt_file(file_dir_predict)
            # Result
            similarity_result_forms[index_result].append(similarity_two_forms(text_label, text_predict))
            form_names.append(filename)
            index_result += 1
    # Create the DataFrame
    flattened_data = [item[0] for item in similarity_result_forms]
    df = pd.DataFrame(flattened_data, columns=['completeness', 'A1-A1', 'A1-A2', 'A1-B','B-A1','B-B'])
    df['form_name'] = form_names
    return df

# Evaluate similarity between processed forms and label forms
folder1 = "Forms\Process_ouput\Label_Output_By_Hand\Raw"
folder2 = "Forms\Process_ouput\Hung_04_Nov_2024\Raw"
df = similarity_result_two_folders(folder1, folder2)
df.to_csv("./Result/result_11_12_20h_20.csv")
print(df)
