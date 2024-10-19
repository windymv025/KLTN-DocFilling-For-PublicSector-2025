import re
import sys
sys.path.append("./Src")
import os

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
        # print(f"File written successfully to '{file_path}'.")
    except Exception as e:
        pass
        # print(f"An error occurred while writing the file: {e}")

#Function test by jupyter
# Function to process a sentence
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
Data_Input_Folder = "Forms/Data_Testing/Input"
Data_Label_Folder = "Forms/Data_Testing/Label_Output"
Data_LLM_Filled_Folder = "Forms/Data_Testing/Result_LLM_Filled_Hung"
Data_LLM_Filled_Processed_Folder = "Forms/Data_Testing/Result_LLM_Filled_Hung_Processed"


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
        # Filling input text from label text
        try:
            filled_text = fill_label_to_input_form(input_text, label_text).replace("[another]","[#another]")
            if filled_text == "wrong something":
                print(f"Error at {index} in {filename}")
                break
            #Save to Test folder
            write_file(Data_LLM_Filled_Processed_Folder + '/' + filename, filled_text)
        except:
            print(f"Error at {index} in {filename}")




