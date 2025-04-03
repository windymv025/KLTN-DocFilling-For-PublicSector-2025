import re
import os
from Utils.text_processing import Text_Processing
import pandas as pd
from collections import Counter
import json
from Config.config import Data_num, Output_num, Type
# Folde address
root_folder = f"Temp\Data_{Data_num}\{Type}"

def analyze_errors_type_1(error_list):
    """
    Phân tích danh sách lỗi, đếm số lần xuất hiện của từng lỗi (tag1, tag2).
    :param error_list: Danh sách chứa tuple (tag1, tag2)
    :return: Danh sách chứa tuple (tag1, tag2, count) sắp xếp theo số lần xuất hiện giảm dần.
    """
    counter = Counter(error_list)
    return sorted([(tag1, tag2, count) for (tag1, tag2), count in counter.items()], key=lambda x: x[2], reverse=True)

def analyze_errors_type_2(error_list):
    """
    Phân tích danh sách lỗi, đếm số lần xuất hiện của từng lỗi (tag1, tag2, context).
    :param error_list: Danh sách chứa tuple (tag1, tag2, context)
    :return: Danh sách chứa tuple (tag1, tag2, context, count) sắp xếp theo số lần xuất hiện giảm dần.
    """
    counter = Counter(error_list)
    return sorted([(tag1, tag2, context, count) for (tag1, tag2, context), count in counter.items()], 
                  key=lambda x: x[3], reverse=True)

def calculate_similarity(contextual1, contextual2, tagnames1, tagnames2, form1, form2, filename, tagnames_truthLLM=None):
    # print("come here? 3")
    """
    - Hàm kiểm tra độ tương đồng hai list tagname1 (label), tagname2(LLM-filled)
    - Trả về các độ đo:

    + A1-A1: Count of correct matches in subset A.
    + A1-A2: Count of misclassifications in subset A.
    + A1-B: Count of unrecognized subset A tagnames (labeled as #another).
    + B-A1: Count of false positives (LLM incorrectly identifies subset A).
    + B-B: Count of correct non-A tagnames assigned as #another.

    tagnames1: List of tagnames from the label.
    tagnames2: List of tagnames from the LLM-filled form.
    """
    our_40_tagnames = Text_Processing().Summary_tagnames()
    # Check if the lengths are different
    if len(tagnames1) != len(tagnames2):
        metrics = {
            "completeness": 0,
            "A1-A1": 0,
            "A1-A2": 0,
            "A1-B": 0,
            "B-A1": 0,
            "B-B": 0,
            "error A1-A2": [],
            "error A1-B": [],
            "error B-A1": [],
            "error A1-A2 detail": [],
            "error A1-B detail": [],
            "error B-A1 detail": [],
            # "form1": form1,
            # "form2": form2,
            "user_X_X": [], # Correct
            "user_X_Y": [], # Wrong
            "debug_user_X_Y_label": [],
            "debug_user_X_Y_predict": [],
        }
        return metrics, metrics  # Return 0% similarity if lengths are different
    # Initialize counters
    A1_A1, A1_A2, A1_B, B_A1, B_B = 0, 0, 0, 0, 0
    error_A1_A2, error_A1_B, error_B_A1 = [], [], []
    error_A1_A2_detail, error_A1_B_detail, error_B_A1_detail = [], [], []
    count_label = 0  # To track valid tagnames in subset_A
    copy_contextual_input_dir = f"{root_folder}/Output{Output_num}/Copy_Contextual_Input/"+ filename + ".json"
    # Read copy_contextual_input
    with open(copy_contextual_input_dir, "r", encoding="utf-8") as f:
        copy_contextual_input = json.load(f)
    num_user_X_X = 0
    num_user_X_Y = 0
    debug_user_X_Y_label = []
    debug_user_X_Y_predict = []
    true_llm_truthLLM = 0
    false_llm_truthLLM = 0
    debug_llm_truthLLM = []
    for index, (tag1, tag2) in enumerate(zip(tagnames1, tagnames2)):
        llm_truthLLM = False
        
        if tagnames_truthLLM is not None:
            tag_truthLLM = tagnames_truthLLM[index]
            if tag_truthLLM != tag2:
                # print("Error: tag_truthLLM != tag2")
                # print(tag_truthLLM, tag2)
                llm_truthLLM = True

        if copy_contextual_input[index][-1][0] != "[":
            debug_contextual_output = " ".join(copy_contextual_input[index]) + " " + "Empty"
        else:
            debug_contextual_output = " ".join(copy_contextual_input[index][:-1]) + " " + copy_contextual_input[index][-1]
        # Normalize
        tag1 = tag1.strip("[]")  # Remove square brackets
        tag2 = tag2.strip("[]")  # Remove square brackets
        # Take value of userX
        def extract_user_number(tagname):
            match = re.search(r'user(\d+)_', tagname)
            if match:
                return int(match.group(1))
            return -1  # Return None if no match is found
        user_tag1 = extract_user_number(tag1)
        user_tag2 = extract_user_number(tag2)
        if user_tag1 == user_tag2:
            num_user_X_X += 1
        elif user_tag1 != -1 and user_tag2 != -1:
            num_user_X_Y += 1
            debug_user_X_Y_label.append(tag1)
            debug_user_X_Y_predict.append(tag2)

        # Standardize tagnames by replacng userX with user0
        standardized_tag1 = re.sub(r"user\d+", "user0", tag1)
        standardized_tag2 = re.sub(r"user\d+", "user0", tag2)
        # Standardize tagnames by replacing userX with user0
        standardized_tag1 = re.sub(r"dob_date", "dob", standardized_tag1)
        standardized_tag2 = re.sub(r"dob_date", "dob", standardized_tag2)
        
        # Check if ground truth tagname is in subset_A
        if standardized_tag1 in our_40_tagnames:
            count_label += 1
            if standardized_tag2 in our_40_tagnames:
                if standardized_tag1 == standardized_tag2:
                    A1_A1 += 1  # Exact match
                    if llm_truthLLM:
                        # print("ADD")
                        # print(true_llm_truthLLM)
                        true_llm_truthLLM += 1
                        # print(true_llm_truthLLM)
                else:
                    if llm_truthLLM:
                        # print("ADD")
                        # print(false_llm_truthLLM)
                        false_llm_truthLLM += 1
                        # print(false_llm_truthLLM)
                        debug_llm_truthLLM.append(('A1-A2: ',' '.join(contextual1[index]), tag1, debug_contextual_output))
                    # error_A1_A2.append((tag1, tag2))
                    error_A1_A2.append((standardized_tag1, standardized_tag2))
                    error_A1_A2_detail.append((' '.join(contextual1[index]), tag1, debug_contextual_output))
                    A1_A2 += 1  # Incorrect match within subset A
            else:
                if llm_truthLLM:
                    # print("ADD")
                    # print(false_llm_truthLLM)
                    false_llm_truthLLM += 1
                    # print(false_llm_truthLLM)
                    debug_llm_truthLLM.append(('A1-B: ',' '.join(contextual1[index]), tag1, debug_contextual_output))
                # error_A1_B.append((tag1, tag2))
                error_A1_B.append((standardized_tag1, standardized_tag2))
                error_A1_B_detail.append((' '.join(contextual1[index]), tag1, debug_contextual_output))
                A1_B += 1  # Missed, filled with something outside subset A
        else:
            if standardized_tag2 in our_40_tagnames:
                if llm_truthLLM:
                    # print("ADD")
                    # print(false_llm_truthLLM)
                    false_llm_truthLLM += 1
                    # print(false_llm_truthLLM)
                    debug_llm_truthLLM.append(('B-A1: ',' '.join(contextual1[index]), tag1, debug_contextual_output))
                error_B_A1.append((standardized_tag1, standardized_tag2))
                error_B_A1_detail.append((' '.join(contextual1[index]), tag1, debug_contextual_output))
                B_A1 += 1  # Incorrectly predicted a tagname in subset A
            else:
                if llm_truthLLM:
                    # print("ADD")
                    # print(true_llm_truthLLM)
                    true_llm_truthLLM += 1
                    # print(true_llm_truthLLM)
                B_B += 1  # Both are outside subset A (#another case)

    # matching_tagnames = [tag1 for tag1, tag2 in zip(tagnames1, tagnames2) if tag1 == tag2]

    # Completeness and accuracy
    completeness = 100.0 if len(tagnames1) == len(tagnames2) else 0.0
    # accuracy = A1_A1 / count_label * 100 if count_label > 0 else 0.0

    # Compile results
    metrics = {
        "completeness": completeness,
        "A1-A1": A1_A1,
        "A1-A2": A1_A2,
        "A1-B": A1_B,
        "B-A1": B_A1,
        "B-B": B_B,
        "error A1-A2": error_A1_A2,
        "error A1-B": error_A1_B,
        "error B-A1": error_B_A1,
        "error A1-A2 detail": error_A1_A2_detail,
        "error A1-B detail": error_A1_B_detail,
        "error B-A1 detail": error_B_A1_detail,
        # "form1": form1,
        # "form2": form2,
        "user_X_X": num_user_X_X, # Correct
        "user_X_Y": num_user_X_Y, #
        "debug_user_X_Y_label": debug_user_X_Y_label,
        "debug_user_X_Y_predict": debug_user_X_Y_predict,
    }

    # Metrics2 (more detail), from above number
    # Total first
    total_A1 = metrics["A1-A1"] + metrics["A1-A2"] + metrics["A1-B"]
    total_B = metrics["B-B"] + metrics["B-A1"]
    metrics_detail={
        "total_A1": total_A1,
        "total_B": total_B,
        # Calculate percentage (P: Percentage)
        "P_A1_A1": metrics["A1-A1"],
        "P_B_B": metrics["B-B"],
        # "P_A1_A2": (metrics["A1-A2"] / total_A1) * 100 if total_A1 > 0 else 0,
        # "P_A1_B": (metrics["A1-B"] / total_A1) * 100 if total_A1 > 0 else 0,
        # "P_B_A1": (metrics["B-A1"] / total_B) * 100 if total_B > 0 else 0,
        "P_A1_A2": metrics["A1-A2"],
        "P_A1_B": metrics["A1-B"],
        "P_B_A1": metrics["B-A1"],
        # Count about wrong metric (C: Count)
        "C_A1_A2": analyze_errors_type_1(metrics["error A1-A2"]),
        "C_A1_B": analyze_errors_type_1(metrics["error A1-B"]),
        "C_B_A1": analyze_errors_type_1(metrics["error B-A1"]),
        # Detail about wrong metric (D: Detail)
        "D_A1_A2": analyze_errors_type_2(metrics["error A1-A2 detail"]),
        "D_A1_B": analyze_errors_type_2(metrics["error A1-B detail"]),
        "D_B_A1": analyze_errors_type_2(metrics["error B-A1 detail"]),
    }

    # Debug truth LLM
    # print(true_llm_truthLLM)
    # print(false_llm_truthLLM)
    debug_llm_truthLLM_dict = {
        "true_llm_truthLLM": true_llm_truthLLM,
        "false_llm_truthLLM": false_llm_truthLLM,
        "debug_llm_truthLLM": debug_llm_truthLLM,
    }
    # print("Test") 
    # print(true_llm_truthLLM, false_llm_truthLLM)
    # print(debug_llm_truthLLM_dict)
    # print()
    return metrics, metrics_detail, debug_llm_truthLLM_dict


def print_tagnames(tagnames):
    print("======Tagnames======")
    for index, tagname in enumerate(tagnames):
        print(tagname + f"_{index}", end=", ")
    print()


def similarity_two_forms(form1, form2, filename, text_truthLLM=None):
    # print("come here? 2")
    # Replace all ".........." by "[#another]"
    form1 = form1.replace("..........", "[#another]")
    form2 = form2.replace("..........", "[#another]")
    if text_truthLLM is not None:
        text_truthLLM = text_truthLLM.replace("..........", "[#another]")
    # Find all matches
    contextual1, tagnames1 = Text_Processing().get_contextual_tagnames(form1)
    contextual2, tagnames2 = Text_Processing().get_contextual_tagnames(form2)   
    tagnames_truthLLM = None
    if text_truthLLM is not None:
        contextual_truthLLM, tagnames_truthLLM = Text_Processing().get_contextual_tagnames(text_truthLLM)
    
    # Calculate similarity percentage
    similarity_percentage, similarity_percentage_detail, debug_llm_truthLLM_dict = calculate_similarity(contextual1, contextual2, tagnames1, tagnames2, form1, form2, filename, tagnames_truthLLM)
    
    return similarity_percentage, similarity_percentage_detail, debug_llm_truthLLM_dict


def similarity_result_two_folders(label_folder1, output_folder2,llm_filled_truthLLM_folder=None):
    '''
    label_folder1: label
    output_folder2: output
    '''
    similarity_result_forms = []
    similarity_result_forms_detail = []
    list_debug_llm_truthLLM_dict = []
    form_names = []
    index_result = 0
    for index, filename in enumerate(os.listdir(output_folder2)):
        if filename.endswith(".txt"):
            similarity_result_forms.append([])
            similarity_result_forms_detail.append([])
            list_debug_llm_truthLLM_dict.append([])
            if (index+1)%5 == 0:
                print("========= Index: ", index+1, "============", filename)
            # if filename == "49_00_TK1-TS.txt":
                # print("debug")
            file_dir_label_process = label_folder1 + "/" + filename
            file_dir_output_process = output_folder2 + "/" + filename
            # Read
            text_label = Text_Processing().Read_txt_file(file_dir_label_process)
            text_predict = Text_Processing().Read_txt_file(file_dir_output_process)
            text_truthLLM = None
            if llm_filled_truthLLM_folder is not None:
                file_dir_output_truthLLM_process = llm_filled_truthLLM_folder + "/" + filename
                text_truthLLM = Text_Processing().Read_txt_file(file_dir_output_truthLLM_process)
                text_truthLLM = text_truthLLM.strip()
            # Strip
            text_label = text_label.strip()
            text_predict = text_predict.strip()
            # Result
            # print("debug1")
            similarity_result, similarity_result_detail, debug_llm_truthLLM_dict = similarity_two_forms(text_label, text_predict, filename, text_truthLLM)
            # print("debug2")
            similarity_result_forms[index_result].append(similarity_result)
            similarity_result_forms_detail[index_result].append(similarity_result_detail)

            # Add debug_llm_truthLLM_dict
            list_debug_llm_truthLLM_dict[index_result].append(debug_llm_truthLLM_dict)

            # Process to get output folder, label folder
            # Now, folder 1 is label, folder 2 is llm_filled
            label_folder = f"{root_folder}/Label{Output_num}"
            output_folder = re.sub(r"\\Processed_Output\\Differents$", "", output_folder2)
            # input_folder = re.sub(r"Label", r"Input", label_folder)
            input_folder = f"{root_folder}/Input{Output_num}"
            # Add form names
            file_dir_label = label_folder + "/" + filename
            file_dir_output = output_folder + "/" + filename
            file_dir_input = input_folder + "/" + filename
            # Create Make clickable hyperlinks for Excel 5 files
            file_dir_input_hyperlink = f'=HYPERLINK("{os.path.abspath(file_dir_input).replace("\\", "/")}","{filename}")'
            file_dir_output_hyperlink = f'=HYPERLINK("{os.path.abspath(file_dir_output).replace("\\", "/")}","{filename}")'
            file_dir_output_process_hyperlink = f'=HYPERLINK("{os.path.abspath(file_dir_output_process).replace("\\", "/")}","{filename}")'
            file_dir_label_hyperlink = f'=HYPERLINK("{os.path.abspath(file_dir_label).replace("\\", "/")}","{filename}")'
            file_dir_label_process_hyperlink = f'=HYPERLINK("{os.path.abspath(file_dir_label_process).replace("\\", "/")}","{filename}")'
            # Add to form_names to store it
            form_names.append([file_dir_input_hyperlink, file_dir_output_hyperlink, file_dir_output_process_hyperlink, file_dir_label_hyperlink, file_dir_label_process_hyperlink])
            index_result += 1
    # Create the DataFrame
    flattened_data = [item[0] for item in similarity_result_forms]
    flattened_data_detail = [item[0] for item in similarity_result_forms_detail]
    flattened_data_debug_llm_truthLLM_dict = [item[0] for item in list_debug_llm_truthLLM_dict]
    # Create the DataFrame
    df = pd.DataFrame(
        flattened_data,
        columns=[
            "completeness",
            "A1-A1",
            "A1-A2",
            "A1-B",
            "B-A1",
            "B-B",
            "error A1-A2",
            "error A1-B",
            "error B-A1",
            "error A1-A2 detail",
            "error A1-B detail",
            "error B-A1 detail",
            # "form1",
            # "form2",
            "user_X_X",
            "user_X_Y",
            "debug_user_X_Y_label",
            "debug_user_X_Y_predict",
        ],
    )
    # Detail dataframe
    df_detail = pd.DataFrame(
        flattened_data_detail,
        columns=[
            "total_A1",
            "total_B",
            "P_A1_A1",
            "P_B_B",
            "P_A1_A2",
            "P_A1_B",
            "P_B_A1",
            "C_A1_A2",
            "C_A1_B",
            "C_B_A1",
            "D_A1_A2",
            "D_A1_B",
            "D_B_A1",
        ],
    )
    # Convert form_names into a DataFrame
    df_form_names = pd.DataFrame(
        form_names, 
        columns=[
            "file_dir_input", 
            "file_dir_output", 
            "file_dir_output_process",
            "file_dir_label", 
            "file_dir_label_process", 
        ]
    )
    # Concatenate both DataFrames side by side
    sub_df = pd.concat([df, df_form_names], axis=1)
    # Add form_names to the end of df detail verison
    df_detail = pd.concat([df_detail, df_form_names], axis=1)
    
    # df debug
    # print(list_debug_llm_truthLLM_dict)
    df_debug_llm_truthLLM_dict = pd.DataFrame(
        flattened_data_debug_llm_truthLLM_dict,
        columns=[
            "true_llm_truthLLM",
            "false_llm_truthLLM",
            "debug_llm_truthLLM",
        ],
    )

    # Concatenate
    # df_detail = pd.concat([df_detail, pd.DataFrame([summary_row])], ignore_index=True)

    return sub_df, df_detail, df_debug_llm_truthLLM_dict
