import json
import random
import os
import re
from config import folder4, Num_forms, receiver, place_dmy

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

def merge_tagnames(selected_tagnames_1, selected_tagnames_2):
    """Merge two sets of tagnames, ensuring 'full_name' appears first."""
    combined_tagnames = {**selected_tagnames_1, **selected_tagnames_2}
    
    # Extract full name fields
    full_name_keys = [key for key in combined_tagnames.keys() if "full_name" in key]
    remaining_keys = [key for key in combined_tagnames.keys() if key not in full_name_keys]
    
    # Shuffle remaining keys but keep full_name first
    random.shuffle(remaining_keys)
    ordered_keys = full_name_keys + remaining_keys
    
    # Select a random alias for each field
    form_tagnames = {key: random.choice(combined_tagnames[key]) for key in ordered_keys}
    
    return form_tagnames

def generate_form(selected_tagnames, user_index=1):
    """Generate a form for a single user, ensuring full_name appears at the top."""
    form_lines = []
    for tagname, field_name in selected_tagnames.items():
        # Replace user1 with userX
        tagname = re.sub(r"user1", f"user{user_index}", tagname)
        form_lines.append(f"{field_name}: {tagname}")
    
    return "\n".join(form_lines)


def create_multi_user_form(filepath_1, filepath_2, num_users=None):
    """Generate a multi-user form with tags from both data sources."""
    num_users = num_users or random.randint(2, 4)  # Randomly pick 2 or 3 users
    users_data = []
    
    for _ in range(num_users):
        selection_rate_1 = random.uniform(0.5, 0.9)
        selection_rate_2 = random.uniform(0.5, 0.9)
        selected_tagnames_1 = load_tagnames(filepath_1, selection_rate=selection_rate_1)
        selected_tagnames_2 = load_tagnames(filepath_2, selection_rate=selection_rate_2)
        merged_tagnames = merge_tagnames(selected_tagnames_1, selected_tagnames_2)
        users_data.append(merged_tagnames)
    
    format_type = random.choice([1, 2, 3])  # Randomly pick a format
    form_sections = []
    # 75% chance to add a receiver format at the start
    if random.random() < 0.75:
        form_sections.append(random.choice(receiver))
    if format_type == 1:
        # Format 1: User 1, User 2...
        for i, user_data in enumerate(users_data, 1):
            form_sections.append(f"--- User {i} ---\n" + generate_form(user_data, i))
    elif format_type == 2:
        # Format 2: Bản thông tin thành viên 1, 2...
        for i, user_data in enumerate(users_data, 1):
            form_sections.append(f"Bảng thông tin thành viên {i}:\n" + generate_form(user_data, i))
    else:
        # Format 3: Thành viên một, mối quan hệ với thành viên hai...
        for i, user_data in enumerate(users_data, 1):
            relation = f"Mối quan hệ với thành viên {i + 1}:\n" if i < len(users_data) else ""
            form_sections.append(f"Thành viên {i}:\n" + generate_form(user_data, i) + f"\n{relation}")
    # 75% chance to add a place_dmy format at the end
    if random.random() < 0.75:
        form_sections.append(random.choice(place_dmy))
    return "\n\n".join(form_sections)

# Example usage
if __name__ == "__main__":
    filepath_1 = "test_data_1.json"  # Path to first JSON file
    filepath_2 = "test_data_2.json"  # Path to second JSON file
    
    N = Num_forms  # Number of forms to generate
    label_folder = folder4
    os.makedirs(label_folder, exist_ok=True)
    
    for i in range(N*3):
        form = create_multi_user_form(filepath_1, filepath_2)
        
        # Save file
        with open(f"{label_folder}/input_{i+N}.txt", "w", encoding="utf-8") as f:
            f.write(form)
            print(f"\n============== End of form {i} ==============\n")
