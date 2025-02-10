import re
import os
from Utils.text_processing import Text_Processing
import pandas as pd


def calculate_similarity(contextual1, contextual2, tagnames1, tagnames2):
    """
    - Hàm kiểm tra độ tương đồng hai list tagname1 (label), tagname2(LLM-filled)
    - Trả về các độ đo:

    + A1-A1: Count of correct matches in subset A.
    + A1-A2: Count of misclassifications in subset A.
    + A1-B: Count of unrecognized subset A tagnames (labeled as #another).
    + B-A1: Count of false positives (LLM incorrectly identifies subset A).
    + B-B: Count of correct non-A tagnames assigned as #another.
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
        }
        return metrics  # Return 0% similarity if lengths are different

    # Initialize counters
    A1_A1, A1_A2, A1_B, B_A1, B_B = 0, 0, 0, 0, 0
    error_A1_A2, error_A1_B, error_B_A1 = [], [], []
    error_A1_A2_detail, error_A1_B_detail, error_B_A1_detail = [], [], []
    count_label = 0  # To track valid tagnames in subset_A

    for index, (tag1, tag2) in enumerate(zip(tagnames1, tagnames2)):
        tag1 = tag1.strip("[]")  # Remove square brackets
        tag2 = tag2.strip("[]")  # Remove square brackets
        # Standardize tagnames by replacng userX with user0
        standardized_tag1 = re.sub(r"user\d+", "user0", tag1)
        standardized_tag2 = re.sub(r"user\d+", "user0", tag2)
        # Standardize tagnames by replacing userX with user0
        standardized_tag1 = re.sub(r"deceased", "user0", standardized_tag1)
        standardized_tag2 = re.sub(r"deceased", "user0", standardized_tag2)
        # Replace "dob_date" with "dob" exactly
        standardized_tag1 = re.sub(r"dob_date", "dob", standardized_tag1)
        standardized_tag2 = re.sub(r"dob_date", "dob", standardized_tag2)
        # Replace "registration" with "birth_registration" exactly
        standardized_tag1 = re.sub(r"user0_birth_registration_place", "user0_birth_registration", standardized_tag1)
        standardized_tag2 = re.sub(r"user0_birth_registration_place", "user0_birth_registration", standardized_tag2)
        # Now if tagname is receiver --> convert to #another
        standardized_tag1 = re.sub(r"receiver", "#another", standardized_tag1)
        standardized_tag2 = re.sub(r"receiver", "#another", standardized_tag2)
        # Check if ground truth tagname is in subset_A
        if standardized_tag1 in our_40_tagnames:
            count_label += 1
            if standardized_tag2 in our_40_tagnames:
                if standardized_tag1 == standardized_tag2:
                    A1_A1 += 1  # Exact match
                else:
                    error_A1_A2.append((tag1, tag2))
                    print(" ".join(contextual1[index]))
                    error_A1_A2_detail.append((' '.join(contextual1[index]), tag1, ' '.join(contextual2[index]), tag2))
                    # print("A1_A2: ", tag1, " - ", tag2)
                    A1_A2 += 1  # Incorrect match within subset A
            else:
                error_A1_B.append((tag1, tag2))
                error_A1_B_detail.append((' '.join(contextual1[index]), tag1, ' '.join(contextual2[index]), tag2))
                # print("A1_B: ", tag1, " - ", tag2)
                A1_B += 1  # Missed, filled with something outside subset A
        else:
            if standardized_tag2 in our_40_tagnames:
                error_B_A1.append((tag1, tag2))
                error_B_A1_detail.append((' '.join(contextual1[index]), tag1, ' '.join(contextual2[index]), tag2))
                # print("B-A1: ", tag1, " - ", tag2)
                B_A1 += 1  # Incorrectly predicted a tagname in subset A
            else:
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
    }

    return metrics



def print_tagnames(tagnames):
    print("======Tagnames======")
    for index, tagname in enumerate(tagnames):
        print(tagname + f"_{index}", end=", ")
    print()


def similarity_two_forms(form1, form2):
    # Replace all ".........." by "[#another]"
    form1 = form1.replace("..........", "[#another]")
    form2 = form2.replace("..........", "[#another]")
    # Find all matches
    # pattern = r"\[(?!\d)([^\]]+)\]"
    # tagnames1 = re.findall(pattern, form1)
    # tagnames2 = re.findall(pattern, form2)
    contextual1, tagnames1 = Text_Processing().get_contextual_tagnames(form1)
    contextual2, tagnames2 = Text_Processing().get_contextual_tagnames(form2)
    
    # print tagnames to check
    # Calculate similarity percentage
    similarity_percentage = calculate_similarity(contextual1, contextual2, tagnames1, tagnames2)
    return similarity_percentage


def similarity_result_two_folders(folder1, folder2):
    similarity_result_forms = []
    form_names = []
    index_result = 0
    for index, filename in enumerate(os.listdir(folder1)):
        if filename.endswith(".txt"):
            similarity_result_forms.append([])
            if (index+1)%10 == 0:
                print("========= Index: ", index+1, "============", filename)
            file_dir_label = folder1 + "/" + filename
            file_dir_predict = folder2 + "/" + filename
            # Read
            text_label = Text_Processing().Read_txt_file(file_dir_label)
            text_predict = Text_Processing().Read_txt_file(file_dir_predict)
            # Result
            similarity_result_forms[index_result].append(
                similarity_two_forms(text_label, text_predict)
            )
            form_names.append(filename)
            index_result += 1
    # print(similarity_result_forms)
    print(similarity_result_forms[-1])
    print(len(similarity_result_forms))
    # Create the DataFrame
    flattened_data = [item[0] for item in similarity_result_forms]
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
        ],
    )
    df["form_name"] = form_names
    return df
