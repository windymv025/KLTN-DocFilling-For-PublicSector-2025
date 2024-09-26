import pickle
import copy


def load_tagname_dict(save_path = 'tagname_dict.pkl'):
    with open(save_path, 'rb') as f:
        return pickle.load(f)

def count_summ_tag_names():
    tag_name_dict = load_tagname_dict()
    list_count_tag_name = []
    for key in tag_name_dict.keys():
        type_form = tag_name_dict[key]
        total_count = 0
        for count in type_form.values():
            total_count += count
        list_count_tag_name.append(total_count)
    return tag_name_dict, list_count_tag_name

def tag_name_frequency_each_type():
    tag_name_dict, list_count_tag_name = count_summ_tag_names()
    frequency_tag_name_dict = copy.deepcopy(tag_name_dict)
    for index, key in enumerate(tag_name_dict.keys()):
        type_form = frequency_tag_name_dict[key]
        a = 0.0
        for key1, count in type_form.items():
            frequency_tag_name_dict[key][key1] = count/list_count_tag_name[index]
            a += count/list_count_tag_name[index]
    return frequency_tag_name_dict

frequency_tag_name_dict = tag_name_frequency_each_type()
all_tag_names = []
for type_i_key in frequency_tag_name_dict.keys():
    for tag_name, frequency in frequency_tag_name_dict[type_i_key].items():
        all_tag_names.append(tag_name)
all_tag_names = set(all_tag_names)
print(len(all_tag_names))