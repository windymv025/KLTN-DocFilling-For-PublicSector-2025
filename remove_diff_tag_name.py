import re
import Src.MyClasses as MyClasses
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv("GEMINI_KEY")


LLM_class = MyClasses.LLM_Gemini(api_key = gemini_key)

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
valid_tagnames_general = ["[receiver]","[place]","[day]","[month]","[year]"]
valid_tagnames_cccd_passport = list_cccd_passport_tagnames = [
"[full_name]",
"[alias_name]",
"[dob]",
"[dob_text]",
"[dob_day]",
"[dob_month]",
"[dob_year]",
"[gender]",
"[id_number]",
"[id_issue_date]",
"[id_issue_day]",
"[id_issue_month]",
"[id_issue_year]",
"[id_issue_place]",
"[ethnicity]",
"[religion]",
"[nationality]",
"[marital_status]",
"[blood_type]",
"[birth_registration_place]",
"[birthplace]",
"[birth_registration_place_village]"
"[birth_registration_place_ward]",
"[birth_registration_place_district]",
"[birth_registration_place_province]",
"[hometown]",
"[permanent_address]",
"[current_address]",
"[current_address_ward]",
"[current_address_district]",
"[current_address_province]",
"[occupation]",
"[passport_number]",
"[passport_issue_date]",
"[passport_issue_day]",
"[passport_issue_month]",
"[passport_issue_year]",
"[passport_issue_place]",
"[passport_expiry_date]"
]

def remove_invalid_tagnames(form_text, valid_tagnames_general, valid_tagnames_cccd_passport):
    # Regular expression to match all tagnames (e.g., [user1_full_name], [place], etc.)
    tagname_pattern = re.compile(r'\[[^0-9].*?\]')

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
folder_BlankX = "Forms/Text/Input_test/Input/TagName1"
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





