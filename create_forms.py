# ===== Ask LLM generates form =====
import json
import random
# Get random forms
from Config.tagnames import remaining_tag_names
from Config.LLM import gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Tagnames.get_tagnames import get_tagnames, get_all_tagnames
from Prompts.create_forms import gen_forms_tagnames_label_forms
# Text Processing
from Utils.text_processing import Text_Processing
# os and Time 
import os
import time

# Get list_tagnames
list_tagnames = get_all_tagnames()
formatted_tagnames = "\n".join([f"{key}: {value}" for key, value in list_tagnames.items()])
# print(formatted_tagnames)

# Get filename: form_content
with open("Temp/folder_form.json", "r", encoding="utf-8") as f:
    folder_form = json.load(f)
# print(type_label_form_texts)

type_forms = [
'1. Cư trú và giấy tờ tùy thân',
'2. Giáo dục',
'3. Y tế và sức khỏe',
'4. Phương tiện và lái xe',
'5. Việc làm',
'6. Khác'
]

def generate_form(formatted_tagnames, remaining_tag_names,random_forms_text):
    prompt_gen_forms =  gen_forms_tagnames_label_forms.format(formatted_tagnames = formatted_tagnames, remaining_tag_names=remaining_tag_names,random_forms_text=random_forms_text)
    prompt = PromptTemplate.from_template(prompt_gen_forms)
    chain = prompt | gemini | StrOutputParser()
    response = chain.invoke({})
    return response

Num = 1
num_forms_generate = Num
forms = folder_form[list(folder_form.keys())[0]]
# Create Num label forms --> Save to Temp/Label_time folder
time_now = time.strftime('%Y-%m-%d-%H-%M-%S')
label_folder = f"Temp/Label_{time_now}"
# Ensure the folder exists
os.makedirs(label_folder, exist_ok=True)

for i in range(num_forms_generate):
    try:
        random_forms = []
        # Get N random forms from each type
        N = random.randint(5,10) # In future, get N is random value
        random_files = random.sample(list(forms.items()), N)  # Randomly pick N forms
        for filename, form_content in random_files:
            form_content = form_content.replace("..........", "[#another]")
            random_forms.append(form_content)
        random_forms_text = "\n".join([form for form in random_forms])

        # Generate
        response = generate_form(formatted_tagnames, remaining_tag_names,random_forms_text)
        print(response)
        # Save file
        with open(f"{label_folder}/input_{i}.txt", "w", encoding="utf-8") as f:
            f.write(response)
            print(f"\n==============End of form {i}==============\n")
    except Exception as e:
        print(f"Error: {e} at form {i}")
        continue


# After above code, we have generated label forms, then simply convert them to input forms
# Then run code to generate output forms from above input forms
input_folder = f"Temp/Input_{time_now}"
temp = Text_Processing()
temp.convert_label_form_to_input_form(label_folder, input_folder)