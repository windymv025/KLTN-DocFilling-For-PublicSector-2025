import re
import sys
sys.path.append("./Src")
import MyClasses
import constant_value as CONST
import os

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

# Combine both lists of tagnames
valid_tagnames_general = CONST.list_general_tagnames
valid_tagnames_cccd_passport = CONST.list_cccd_passport_tagnames

def remove_invalid_tagnames(form_text, valid_tagnames_general, valid_tagnames_cccd_passport):
    # Regular expression to match all tagnames (e.g., [user1_full_name], [place], etc.)
    tagname_pattern = re.compile(r'\[.*?\]')

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

#Run with folder 'Công dân All'/Input/Output
folder_BlankX = "Forms\Input\Output_Hung"
for index,filename in enumerate(os.listdir(folder_BlankX)):
    # if index==20:
    #     break
    if filename.endswith(".txt"):
        print("Start with: ", filename)
        file_dir = folder_BlankX + '/' + filename
        respones_dir = folder_BlankX + '/Output_Diff/' + filename
        text = read_file(file_dir)
        cleaned_form = remove_invalid_tagnames(text, valid_tagnames_general, valid_tagnames_cccd_passport)
        print(cleaned_form)
        write_file(respones_dir, cleaned_form)
        print("End with: ", filename)
