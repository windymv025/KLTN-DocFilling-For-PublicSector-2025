import os
import re
from auto_generate import *
import pickle

def identify_type_key(content):
    llm = GoogleGenerativeAI(model = 'gemini-1.5-flash', timeout= None, max_tokens = 50, temperature = 0, top_k = 1, top_p = 1,  google_api_key = gemini_key)
    chain = identify_type_form(llm)
    type = chain.invoke(content)
    print(type)
    if "Residence" in type:
        return 'residence_identification_tagnames'
    elif "Education" in type:
        return 'study_tagnames'
    elif "Health" in type:
        return 'health_and_medical_tagnames'
    elif "Vehicle" in type:
        return 'vehicle_driver_tagnames'
    elif "Employment" in type:
        return 'job_tagnames'
    else:
        return 'residence_identification_tagnames'

def load_tagname_dict(save_path = 'tagname_dict.pkl'):
    with open(save_path, 'rb') as f:
        return pickle.load(f)
    
def save_tagname_dict(tagname_dict, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(tagname_dict, f)


def extract_tagname(folder_path = 'Forms/Text/Input/Output/TagName/', start = 0, end = 2):
    tagname_dict = {
    'residence_identification_tagnames': {},
    'study_tagnames': {},
    'health_and_medical_tagnames': {},
    'vehicle_driver_tagnames': {},
    'job_tagnames': {}
    }
    if os.path.exists('tagname_dict.pkl'):
        tagname_dict = load_tagname_dict()
    list_file_name = os.listdir(folder_path)
    list_file_path = [os.path.join(folder_path, file_name) for file_name in list_file_name]
    regex = r'\[([^\d].*?)\]'
    for i, file_path in enumerate(list_file_path[start:end]):
        content = read_file(file_path)
        _key = identify_type_key(content)
        list_tag_names = re.findall(regex, content)
        for tag_name in list_tag_names:
            if 'user' in tag_name:
                tag_name = tag_name[6:]
            if tag_name not in tagname_dict[_key].keys():
                tagname_dict[_key][tag_name] = 1
            else:
                tagname_dict[_key][tag_name] += 1
    save_tagname_dict(tagname_dict = tagname_dict, save_path = 'tagname_dict.pkl')
    return tagname_dict

tagname_dict = extract_tagname(start = 0, end = -1)
print(tagname_dict)