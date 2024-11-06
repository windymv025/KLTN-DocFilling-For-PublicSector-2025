import re
import sys
sys.path.append("./Src")
import MyClasses
import constant_value as CONST
import os
import pandas as pd

#Classes
LLM_class = MyClasses.LLM_Gemini(api_key = CONST.API_KEY)
Text_Processing_Class = MyClasses.Text_Processing()

#Path
Data_Input_Folder = "Forms/Data_Testing/Input" #Input folder
Data_Label_Folder = "Forms/Data_Testing/Label_Output" #Label folder
# Data_LLM_Filled_Folder = "Forms/Data_Testing/Result_LLM_Filled_Hung" #Forms filled by LLM
# Data_LLM_Filled_Processed_Folder = "Forms/Data_Testing/Result_LLM_Filled_Hung_Processed" #Processed forms filled by LLM
Data_LLM_Filled_Folder = "Forms/Data_Testing/New_result_Hung" #Forms filled by LLM
Data_LLM_Filled_Processed_Folder = "Forms/Data_Testing/New_result_Hung_Processed" #Processed forms filled by LLM

#read, write file
def read_file(file_path):
    try:
        with open(file_path, 'r',encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    
def write_file(file_path, text):
    #Delete all before create
    if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    # Write content to the file
    try:
        with open(file_path, 'w',encoding='utf-8') as file:
            file.write(text)
        # print(f"File written successfully to '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while writing the file: {e}")

# 1. From forms response by LLM --> get tagnames to input forms
# Function to process a sentence
def fix_place_dmy_error(form_text):
    '''
    - Hàm để đưa chỗ điền ....., ngày.... tháng.... năm về đúng format [place], ngày [day] tháng [month] năm [year]
    '''
    # Define the regex pattern to match the specific date format with optional spaces
    date_pattern = re.compile(r'\s*\[[a-zA-Z0-9_]+?\]\s*,\s*ngày\s*\[.+?\]\s*tháng\s*\[.+?\]\s*năm\s*\[.+?\]')
    
    # Define the replacement format
    replacement_format = '[place], ngày [day] tháng [month] năm [year]'
    
    # Use sub to replace matched dates with the correct format
    fixed_text = date_pattern.sub(replacement_format, form_text)
    
    return fixed_text

def process_sentence(sentence):
    '''
    Function to remove all number, special character.
    Just keep again words.
    Input: sentence.
    Output: sentence without number, special character.
    '''
    # Step 1: Convert to lowercase
    sentence = sentence.lower()
    # # Step 2: Remove all numbers
    # sentence = re.sub(r'\d+', '', sentence)
    # Step 3: Keep only words and numbers (remove punctuation)
    sentence = re.sub(r'[^\w\s\/]', '', sentence)
    # Step 3.1: Add space around slashes
    sentence = re.sub(r'\/(thang|tháng|nam|năm)', r' / \1', sentence)
    # Step 4: Strip leading/trailing whitespace and split by spaces
    words = sentence.strip().split()
    return words

def extract_form(words,pattern,match_index=0):
    '''
    Function to extract form by pattern re, and with match_index is index of result.
    Input: words, re partern, match_index to return.
    Output: apply pattern, take matches[match_index]
    '''
    # Find all matches
    matches = pattern.findall(words)
    # Collecting the sentences
    sentences = []
    for match in matches:
        sentence = match[match_index].strip()  # Get the text before ".........."
        sentences.append(process_sentence(sentence))
    return sentences

def calculate_similarity_two_lists(list1, list2):
    '''
    Function to calculate similarity 2 list.
    EX:['tờ', 'khai', 'căn', 'cước', 'công', 'dân', 'họ', 'chữ', 'đệm', 'và', 'tên']
    ['họ', 'chữ', 'đệm', 'và', 'tên', 'gọi', 'khác', 'nếu', 'có']
    GPT recommend new metrics: jaccard similarity.
    '''
    if len(list1) == len(list2) == 0:
        return {
        'exact_match_percentage': 100.0,
        'jaccard_similarity': 100.0
    }
    # Exact matching
    exact_match_count = sum(1 for a, b in zip(list1, list2) if a == b)
    exact_match_percentage = exact_match_count / max(len(list1), len(list2)) * 100
    
    # Jaccard similarity
    set1, set2 = set(list1), set(list2)
    jaccard_similarity = len(set1.intersection(set2)) / len(set1.union(set2)) * 100
    
    return {
        'exact_match_percentage': exact_match_percentage,
        'jaccard_similarity': jaccard_similarity
    }

def fill_tagname_to_form(form, list_tag_name):
    '''
    Function fill list_tagname to form (here is input form, with all #another).
    Ensure that list_tag_name len is same with len of #another
    Parameters:
    form (str): The input form with #another placeholders.
    list_tag_name (list of lists): The list of tagnames to fill in.
    
    Returns:
    str: The form with tagnames filled in.
    '''
    # Ensure the length matches the number of placeholders
    num_placeholders = form.count('[#another]')
    if len(list_tag_name) != num_placeholders:
        raise ValueError(f"Mismatch: Found {num_placeholders} placeholders, but {len(list_tag_name)} tagnames were provided.")
    
    # Replace each occurrence of [#another] with the corresponding tagname
    for tag in list_tag_name:
        form = form.replace('[#another]', f'[{tag[0]}]', 1)
    
    return form

def fill_label_to_input_form(input_form, label_form):
    '''
    Function to fill from label form to input form (fill tagname into).
    Input: input form with all ......., label form with [#tagname] is placed.
    '''
    pattern = re.compile(r'(.*?)(\[[^\d].+?\])', re.DOTALL)
    # Find all matches input
    input_sentences = extract_form(input_form,pattern)
    # Find all matches label
    label_sentences = extract_form(label_form,pattern)
    label_tagnames = extract_form(label_form,pattern,match_index=1)

    ## Print testing 
    #Filling
    index_label = 0
    tagname_to_fills = []
    
    # Initialize skip counter
    skip_count = 0
    for i_input, input_sentence in enumerate(input_sentences):
        if skip_count > 0:
            # Skip the current iteration and decrement the skip count
            skip_count -= 1
            continue
        while True:
            try:
                jaccard_similarity = calculate_similarity_two_lists(input_sentence,label_sentences[index_label])['jaccard_similarity']
            except:
                return "wrong something"
            if jaccard_similarity > 1.0:
                # Xử lý _dob
                pattern_dob = re.compile(r'(.*?_dob)$', re.DOTALL)
                find_dob = pattern_dob.search(label_tagnames[index_label][0])
                if find_dob is not None:
                    #Check if exist "tháng", "/" in next input_sentence[i+1]... --> wrong dob
                    if ((i_input+2) <= (len(input_sentences))) and ("tháng" in input_sentences[i_input + 1] or "/" in input_sentences[i_input + 1] or "thang" in input_sentences[i_input + 1]):
                        match = find_dob.group(1)
                        for sub_i in ['day', 'month', 'year']:
                            temp_list = [f"{match}_{sub_i}"]
                            tagname_to_fills.append(temp_list)
                        index_label += 1
                        skip_count = 2
                        break
                # Tương tự xử lý _date
                pattern_date = re.compile(r'(.*?_date)$', re.DOTALL)
                find_date = pattern_date.search(label_tagnames[index_label][0])
                if find_date is not None:
                    #Check if exist "tháng", "/" in next input_sentence[i+1]... --> wrong date
                    if ((i_input+2) <= (len(input_sentences))) and ("tháng" in input_sentences[i_input + 1] or "/" in input_sentences[i_input + 1] or "thang" in input_sentences[i_input + 1]):
                        match = find_date.group(1).replace('_date', '')
                        for sub_i in ['day', 'month', 'year']:
                            temp_list = [f"{match}_{sub_i}"]
                            tagname_to_fills.append(temp_list)
                        index_label +=1
                        skip_count = 2
                        break
                # Xử lý _dob_day
                pattern_day = re.compile(r'(.*?_day)$', re.DOTALL)
                find_day = pattern_day.search(label_tagnames[index_label][0])
                
                if find_day is not None:
                    match = find_day.group(1)
                    # Check nếu đứng một mình --> không tồn tại _month, _year phía sau
                    pattern_month = re.compile(r'(.*?_month)$', re.DOTALL)
                    if ((index_label+2)<=len(label_tagnames)) and (pattern_month.search(label_tagnames[index_label+1][0]) is None):
                        # Nếu nó là dob/ date (tức phía sau không có chỗ cho điền ngày tháng) --> replace thành dob, hoặc date
                        # Nếu không thì nó điền sai, phải có đủ ngày tháng năm --> thêm ngày tháng năm vào
                        if ((i_input+2) <= (len(input_sentences))) and ("tháng" not in input_sentences[i_input + 1] and "/" not in input_sentences[i_input + 1] and "thang" not in input_sentences[i_input + 1]):
                            match = match.replace('_day','_date')
                            tagname_to_fills.append([match])
                            index_label +=1
                            break
                        elif ((i_input+2) <= (len(input_sentences))) and ("tháng" in input_sentences[i_input + 1] or "/" in input_sentences[i_input + 1] or "thang" in input_sentences[i_input + 1]):
                            match = match.replace("_day", "")
                            for sub_i in ['day', 'month', 'year']:
                                temp_list = [f"{match}_{sub_i}"]
                                tagname_to_fills.append(temp_list)
                            index_label +=1
                            skip_count = 2
                            break
                    elif ((index_label+2)<=len(label_tagnames)) and (pattern_month.search(label_tagnames[index_label+1][0]) is not None):
                        # Check nếu đứng cả 3 --> có _month, _year phía sau
                        #TH nó sai, tức phải thành date (đúng thì xét làm gì?) --> chuyển thành date (bỏ qua month, year kia)
                        if ((i_input+2) <= (len(input_sentences))) and ("tháng" not in input_sentences[i_input + 1] and "/" not in input_sentences[i_input + 1] and "thang" not in input_sentences[i_input + 1]):
                            match = match.replace("_day", "_date")
                            tagname_to_fills.append([match])
                            index_label +=3
                            break
                    
                tagname_to_fills.append(label_tagnames[index_label])
                index_label +=1
                break
            else:
                index_label += 1
    return fill_tagname_to_form(input_form, tagname_to_fills)

# Regular expression to match text before ".........."
pattern = re.compile(r'(.*?)(\[.+?\])', re.DOTALL)
# Filled input from by LLM forms
for index,filename in enumerate(os.listdir(Data_Input_Folder)):
    if filename.endswith(".txt"):
        file_input_dir = Data_Input_Folder + '/' + filename
        # file_label_dir = Data_Label_Folder + '/' + filename
        file_label_dir = Data_LLM_Filled_Folder + '/' + filename
        # respones_dir = folder_BlankX + '/Output/' + filename
        input_text = read_file(file_input_dir)
        label_text = read_file(file_label_dir)
        #Replace all ".........." by "[another]"
        input_text = input_text.replace("..........","[#another]")
        label_text = label_text.replace("..........","[#another]")
        
        # Xử lý chỗ date thành [place], ngày [day] tháng [month] năm [year]
        # input_text = fix_place_dmy_error(input_text)
        # label_text = fix_place_dmy_error(label_text)
        # Filling input text from label text
        try:
            filled_text = fill_label_to_input_form(input_text, label_text).replace("[another]","[#another]")
            # Xử lý chỗ date thành [place], ngày [day] tháng [month] năm [year]
            filled_text = fix_place_dmy_error(filled_text)
            if filled_text == "wrong something":
                print(f"Error at {index} in {filename}")
                break
            #Save to Test folder
            write_file(Data_LLM_Filled_Processed_Folder + '/' + filename, filled_text)
        except:
            print(f"Error at {index} in {filename}")

# 2. Remove different tagnames in processed forms, and label form
# Combine both lists of tagnames
valid_tagnames_general = CONST.list_general_tagnames
valid_tagnames_cccd_passport = CONST.list_cccd_passport_tagnames

# Function to replace all '_date' tagnames with '_day', '_month', '_year'
def replace_date_tagnames(text):
    # Regular expression to match tagnames like [userX_something_date]
    pattern = re.compile(r'(\[user\d+_[a-zA-Z_]+)_date\]')
    
    # Replace all occurrences of '_date' with '_day', '_month', and '_year'
    def replacement(match):
        base_tag = match.group(1)
        return f"{base_tag}_day]/{base_tag}_month]/{base_tag}_year]"
    
    # Substitute all matched patterns in the text
    updated_text = pattern.sub(replacement, text)
    return updated_text

def remove_invalid_tagnames(form_text, valid_tagnames_general, valid_tagnames_cccd_passport):
    # Regular expression to match all tagnames (e.g., [user1_full_name], [place], etc.)
    tagname_pattern = re.compile(r'\[[^\d].*?\]')

    # Function to replace invalid tagnames
    def replace_invalid_tagname(match):
        tagname = match.group(0)

        # Check if the tagname is a general tagname (direct match)
        if tagname in valid_tagnames_general:
            return tagname  # Keep general tagnames unchanged

        # Check if the tagname is a valid cccd/passport tagname with userX_ prefix (e.g., [user1_full_name])
        for valid_tagname in valid_tagnames_cccd_passport:
            if re.match(r'\[user\d+_' + re.escape(valid_tagname[1:-1]) + r'\]', tagname):
                return tagname  # Keep valid userX_ prefixed tagnames

        # If the tagname is not in the valid lists, remove it
        return ".........."

    # Process the form by replacing invalid tagnames
    cleaned_form = re.sub(tagname_pattern, replace_invalid_tagname, form_text)

    return cleaned_form

def remove_different_tagnames(folder_path):
    for index,filename in enumerate(os.listdir(folder_path)):
        if filename.endswith(".txt"):
            file_dir = folder_path + '/' + filename
            respones_dir = folder_path + '/Output_Diff/' + filename
            # print(file_dir)
            #Read
            text = read_file(file_dir)
            cleaned_form = remove_invalid_tagnames(text, valid_tagnames_general, valid_tagnames_cccd_passport)
            write_file(respones_dir, cleaned_form)

#Apply to label folder, and processed folder
remove_different_tagnames(Data_LLM_Filled_Processed_Folder)
remove_different_tagnames(Data_Label_Folder)

# 3. Evaluate similarity between processed forms and label forms
# Regular expression to find all occurrences of tagnames in square brackets
pattern = r"\[([^\]]+)\]"

# Function to calculate similarity percentage if lists have the same length
def calculate_similarity(tagnames1, tagnames2):
    '''
    - Hàm kiểm tra độ tương đồng hai list tagname1 (label), tagname2
    - Trả về:
    + Độ đủ: điền đủ không (len = len)
    + Độ chính xác (trong X tagnames đó thôi, không xét another)
    + Check xem có sai chỗ nào không.
    '''
    # Check if the lengths are different
    if len(tagnames1) != len(tagnames2):
        return [0,0,0]  # Return 0% similarity if lengths are different

    matching_tagnames = []
    count_label = 0
    count_error = 0
    for tag1,tag2 in zip(tagnames1,tagnames2):
        # Standardize tagnames by replacing userX with user0
        standardized_tag1 = re.sub(r'user\d+', 'user0', tag1)
        standardized_tag2 = re.sub(r'user\d+', 'user0', tag2)
        # Replace "dob_date" with "dob" exactly
        standardized_tag1 = re.sub(r'dob_date', 'dob', standardized_tag1)
        standardized_tag2 = re.sub(r'dob_date', 'dob', standardized_tag2)
        if standardized_tag1 != "#another": #Because tagname 1 is label, so we count it
            count_label += 1
        if standardized_tag1 != "#another" and standardized_tag1 == standardized_tag2:
            matching_tagnames.append(standardized_tag1)
        if standardized_tag1 != "#another" and standardized_tag2 != "#another" and standardized_tag1!=standardized_tag2:
            count_error += 1

    # matching_tagnames = [tag1 for tag1, tag2 in zip(tagnames1, tagnames2) if tag1 == tag2]
    
    # Calculate similarity percentage as the ratio of matching tagnames to total tagnames
    similarity_percentage = len(matching_tagnames) / count_label * 100
    error_percentage = count_error / count_label * 100
    
    return [100.0,similarity_percentage,error_percentage]

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
form_names = []
index_result = 0
for index,filename in enumerate(os.listdir(Data_Label_Folder)):
    if filename.endswith(".txt"):
        similarity_result_forms.append([])
        print("========= Index: ",index, "============", filename)
        file_dir_label = Data_Label_Folder + '/Output_Diff/' + filename
        file_dir_predict = Data_LLM_Filled_Processed_Folder + '/Output_Diff/' + filename
        #read
        text_label = read_file(file_dir_label)
        text_predict = read_file(file_dir_predict)
        similarity_result_forms[index_result].append(similarity_two_forms(text_label, text_predict))
        form_names.append(filename)
        index_result += 1   

#Save to csv
flattened_data = [item[0] for item in similarity_result_forms]
# Create the DataFrame
df = pd.DataFrame(flattened_data, columns=['completeness', 'similarity', 'error'])
df['form_name'] = form_names
df.to_csv("result.csv")
print(df)

