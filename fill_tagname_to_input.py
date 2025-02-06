import os
from Tagnames.define_tagnames import generate_tagnames
from Utils.text_processing import Text_Processing

# Folder addresses
input_folder = "Temp/LLM_generate/Input"
input_folders = [input_folder]
label_folder = "Temp/LLM_generate/Label"
output_folder = "Temp/LLM_generate/Output"

# ============= 1. Generates tagnames =============
# for input_folder in input_folders:
#     generate_tagnames(input_folder, output_folder)

# ============= 2. Process the output =============
## 2.1 From forms response by LLM --> get tagnames to input forms --> remove different tagnames

# For filling just some form (Chỉ định chỉ điền một số form để test --> debugging)
list_specific_forms = [
"input_1.txt",
"input_100.txt",
"input_101.txt",
"input_103.txt",
"input_104.txt",
"input_105.txt",
"input_106.txt",
"input_108.txt",
"input_109.txt",
"input_112.txt",
"input_114.txt",
"input_116.txt",
"input_117.txt",
"input_118.txt",
"input_119.txt",
"input_120.txt",
"input_121.txt",
"input_122.txt",
"input_123.txt",
"input_124.txt",
"input_125.txt",
"input_126.txt",
"input_127.txt",
"input_129.txt",
"input_13.txt",
"input_130.txt",
"input_131.txt",
"input_132.txt",
"input_134.txt",
"input_137.txt",
"input_138.txt",
"input_140.txt",
"input_141.txt",
"input_142.txt",
"input_143.txt",
"input_144.txt",
"input_146.txt",
"input_148.txt",
"input_149.txt",
"input_15.txt",
"input_160.txt",
"input_162.txt",
"input_168.txt",
"input_169.txt",
"input_189.txt",
"input_190.txt",
"input_198.txt",
"input_205.txt",
"input_210.txt",
"input_22.txt",
"input_225.txt",
"input_235.txt",
"input_252.txt",
"input_256.txt",
"input_283.txt",
"input_296.txt",
"input_300.txt",
"input_301.txt",
"input_302.txt",
"input_303.txt",
"input_315.txt",
"input_317.txt",
"input_322.txt",
"input_325.txt",
"input_329.txt",
"input_33.txt",
"input_337.txt",
"input_339.txt",
"input_34.txt",
"input_340.txt",
"input_366.txt",
"input_368.txt",
"input_370.txt",
"input_374.txt",
"input_382.txt",
"input_383.txt",
"input_391.txt",
"input_406.txt",
"input_413.txt",
"input_440.txt",
"input_445.txt",
"input_449.txt",
"input_451.txt",
"input_467.txt",
"input_469.txt",
"input_472.txt",
"input_484.txt",
"input_485.txt",
"input_493.txt",
"input_55.txt",
"input_57.txt",
"input_68.txt",
"input_69.txt",
"input_72.txt",
"input_84.txt",
"input_95.txt"
]

def filled_input_from_filled_form(input_folder, filled_folder, output_folder):
    # for index, filename in enumerate(os.listdir(filled_folder)):
    for index, filename in enumerate(list_specific_forms): # Debugging
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
# for input_folder in input_folders:
#     filled_input_from_filled_form(input_folder, output_folder, process_folder)

# 2.2 Remove different tagnames from process output folder
# for index, filename in enumerate(os.listdir(process_folder)):
for index, filename in enumerate(list_specific_forms): # Debugging
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


