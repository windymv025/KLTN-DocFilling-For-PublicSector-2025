import os
from Tagnames.define_tagnames import generate_tagnames
from Utils.text_processing import Text_Processing

# General
Data_num = 2
Train_Test = "Train"
# Train_Test = "Test"
Output_num = 2

# Folder addresses train
input_folder = f"Temp/Data_{Data_num}/{Train_Test}/Input"
input_folders = [input_folder]
label_folder = f"Temp/Data_{Data_num}/{Train_Test}/Label"
output_folder = f"Temp/Data_{Data_num}/{Train_Test}/Output{Output_num}"

# Ensuse output folder exists
os.makedirs(output_folder, exist_ok=True)

# ============= 1. Generates tagnames =============
for input_folder in input_folders:
    generate_tagnames(input_folder, output_folder)



# ============= 2. Process the output =============
## 2.1 From forms response by LLM --> get tagnames to input forms --> remove different tagnames

# For filling just some form (Chỉ định chỉ điền một số form để test --> debugging)
def filled_input_from_filled_form(input_folder, filled_folder, output_folder):
    for index, filename in enumerate(os.listdir(filled_folder)):
    # for index, filename in enumerate(list_specific_forms): # Debugging
        if index%5==0:
            print(f"Process until {index}")
        if filename.endswith(".txt") :
            # Input - filled
            file_input_dir = input_folder + "/" + filename
            file_filled_dir = filled_folder + "/" + filename
            # Read
            input_text = Text_Processing().Read_txt_file(file_input_dir)
            filled_text = Text_Processing().Read_txt_file(file_filled_dir)
            # Replace all ".........." by "[another]"
            input_text = input_text.replace("..........", "[#another]")
            filled_text = filled_text.replace("..........", "[#another]")

            # Print debug
            try:
                # Fill input by LLM form
                filled_input_text = Text_Processing().fill_input_by_llm_form(
                    filled_text, input_text
                )
                # Remove different tagnames
                filled_input_text_different = (
                    Text_Processing().remove_different_tagnames(filled_input_text)
                )
                # Save 2 versions
                output_path = output_folder + "/" + filename
                output_path_different = output_folder + "/Differents/" + filename
                Text_Processing().Save_txt_file(output_path, filled_input_text)
                Text_Processing().Save_txt_file(
                    output_path_different, filled_input_text_different
                )

            except Exception as e:
                print(f"Error: {e} at file {filename}")
                break

process_folder = f"{output_folder}\Processed_Output"
os.makedirs(process_folder, exist_ok=True)
for input_folder in input_folders:
    filled_input_from_filled_form(input_folder, output_folder, process_folder)

# 2.2 Remove different tagnames from process output folder
for index, filename in enumerate(os.listdir(process_folder)):
# for index, filename in enumerate(list_specific_forms): # Debugging
    if filename.endswith(".txt"):
        # Input - filled
        file_process_output_dir = process_folder + "/" + filename
        # Read
        process_output_text = Text_Processing().Read_txt_file(file_process_output_dir)
        # Print debug
        try:
            # Remove different tagnames
            process_output_text_different = Text_Processing().remove_different_tagnames(
                process_output_text
            )
            # Save
            output_path_different = process_folder + "/Differents/" + filename
            Text_Processing().Save_txt_file(output_path_different, process_output_text_different)

        except Exception as e:
            print(f"Error: {e} at file {filename}")
            break


# 2.2 Remove different tagnames from label folder
for index, filename in enumerate(os.listdir(label_folder)):
    if filename.endswith(".txt"):
        # Input - filled
        file_label_dir = label_folder + "/" + filename
        # Read
        label_text = Text_Processing().Read_txt_file(file_label_dir)
        # Print debug
        try:
            # Remove different tagnames
            label_text_different = Text_Processing().remove_different_tagnames(
                label_text
            )
            # Save
            output_path_different = label_folder + "/Differents/" + filename
            Text_Processing().Save_txt_file(output_path_different, label_text_different)

        except Exception as e:
            print(f"Error: {e} at file {filename}")
            break


