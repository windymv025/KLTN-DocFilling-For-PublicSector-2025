import json
import random
import os
from config import folder2, Num_forms, receiver, place_dmy

def load_tagnames(filepath, selection_rate=0.7):
    """Load tagnames from a JSON file and randomly select a subset, ensuring 'full_name' is included."""
    with open(filepath, "r", encoding="utf-8") as f:
        tagnames = json.load(f)
    
    # Ensure 'full_name' is included
    selected_keys = [key for key in tagnames.keys() if 'full_name' in key]
    remaining_keys = [key for key in tagnames.keys() if key not in selected_keys]
    selected_keys += random.sample(remaining_keys, int(len(remaining_keys) * selection_rate))
    
    selected_tagnames = {key: tagnames[key] for key in selected_keys}
    
    return selected_tagnames

def generate_form(selected_tagnames_1, selected_tagnames_2):
    """Generate a combined form for two users, ensuring full names stay at the top and others are shuffled."""
    combined_tagnames = {**selected_tagnames_1, **selected_tagnames_2}
    
    # Extract full names
    full_name_keys = [key for key in combined_tagnames.keys() if "full_name" in key]
    remaining_keys = [key for key in combined_tagnames.keys() if key not in full_name_keys]
    
    random.shuffle(remaining_keys)
    ordered_keys = full_name_keys + remaining_keys
    
    form = {key: random.choice(combined_tagnames[key]) for key in ordered_keys}
    return form

def generate_form_txt(selected_tagnames):
    """Generate a form using the selected tagnames in the required format."""
    form_lines = []
    if random.random() < 0.75:
        form_lines.append(random.choice(receiver))
    for tagname, field_name in selected_tagnames.items():
        # field_name = random.choice(options)  # Pick one random alias
        form_lines.append(f"{field_name}: {tagname}")
    # 75% chance to add a random place_dmy format at the end
    if random.random() < 0.75:
        form_lines.append(random.choice(place_dmy))
    return "\n".join(form_lines)

# Example usage
if __name__ == "__main__":
    filepath_1 = "test_data_1.json"  # Path to your JSON file
    filepath_2 = "test_data_2.json"  # Path to your JSON file
    # Create N forms
    N = Num_forms
    label_folder = folder2
    # Ensure the folder exists
    os.makedirs(label_folder, exist_ok=True)
    for i in range(N):
        selection_rate_1 = random.uniform(0.5, 0.9)
        selection_rate_2 = random.uniform(0.5, 0.9)
        selected_tagnames_1 = load_tagnames(filepath_1, selection_rate=selection_rate_1)
        selected_tagnames_2 = load_tagnames(filepath_2, selection_rate=selection_rate_2)
        form = generate_form(selected_tagnames_1, selected_tagnames_2)
        form = generate_form_txt(form)
        # print(form)
        # Save file
        with open(f"{label_folder}/input_{i}.txt", "w", encoding="utf-8") as f:
            f.write(form)
            print(f"\n==============End of form {i}==============\n")
    # selected_tagnames = load_tagnames(filepath, selection_rate=0.7)
    # print(json.dumps(form, indent=4, ensure_ascii=False))
