# import os
# from Config.folders import (
#     input_raw_folder,
#     input_hand_process_folder,
#     label_by_hand_folder,
# )
# from Evaluate.my_metrics import similarity_result_two_folders
# from Utils.text_processing import Text_Processing
# from Tagnames.define_tagnames import generate_tagnames

# input = "Forms\LLM_generate\Temp_Input"
# input_folders = [input]
# version_llm_filled = "Hung_19_Oct_2024"
# version_llm_filled = time.strftime("Ver_%Y-%m-%d-%H-%M-%S")
# ============= 1. Generates tagnames =============

# version_llm_filled = time.strftime("Ver_%Y-%m-%d-%H-%M-%S")
# input_folders = [input_raw_folder, input_hand_process_folder]
# output_folder = "Forms\LLM_generate\Output2"
# for input_folder in input_folders:
#     print(input_folder)
#     generate_tagnames(input_folder, output_folder)

# print(ducnam)
# ============= 2. Process the output =============

## 2.1 From forms response by LLM --> get tagnames to input forms --> remove different tagnames

# def filled_input_from_filled_form(input_folder, filled_folder, output_folder):
#     for index, filename in enumerate(os.listdir(filled_folder)):
#         if filename.endswith(".txt"):
#             # Input - filled
#             file_input_dir = input_folder + "/" + filename
#             file_filled_dir = filled_folder + "/" + filename
#             # Read
#             input_text = Text_Processing().Read_txt_file(file_input_dir)
#             filled_text = Text_Processing().Read_txt_file(file_filled_dir)
#             # Replace all ".........." by "[another]"
#             input_text = input_text.replace("..........", "[#another]")
#             filled_text = filled_text.replace("..........", "[#another]")

#             # Print debug
#             try:
#                 # Fill input by LLM form
#                 filled_input_text = Text_Processing().fill_input_by_llm_form(
#                     filled_text, input_text
#                 )
#                 # Remove different tagnames
#                 filled_input_text_different = (
#                     Text_Processing().remove_different_tagnames(filled_input_text)
#                 )
#                 # Save 2 versions
#                 output_path = output_folder + "/" + filename
#                 output_path_different = output_folder + "/Differents/" + filename
#                 Text_Processing().Save_txt_file(output_path, filled_input_text)
#                 Text_Processing().Save_txt_file(
#                     output_path_different, filled_input_text_different
#                 )

#             except Exception as e:
#                 print(f"Error: {e} at file {filename}")
#                 break

# input = "Forms\LLM_generate\Input"
# input_folders = [input]
# llm_filled_folder = "Forms\LLM_generate\Output"
# output_folder = "Forms\LLM_generate\Output\Processed_Output"
# for input_folder in input_folders:
#     filled_input_from_filled_form(input_folder, llm_filled_folder, output_folder)

# print(ducnam)
## 2.2 Remove different tagnames from label folder
# label_folder = "Forms\LLM_generate\Label"
# for index, filename in enumerate(os.listdir(label_folder)):
#     if filename.endswith(".txt"):
#         # Input - filled
#         file_label_dir = label_folder + "/" + filename
#         # Read
#         label_text = Text_Processing().Read_txt_file(file_label_dir)
#         # Print debug
#         try:
#             # Remove different tagnames
#             label_text_different = Text_Processing().remove_different_tagnames(
#                 label_text
#             )
#             # Save
#             output_path_different = label_folder + "/Differents/" + filename
#             Text_Processing().Save_txt_file(output_path_different, label_text_different)

#         except Exception as e:
#             print(f"Error: {e} at file {filename}")
#             break

# ============= 3. Evaluate =============

# label_folder = "Forms\LLM_generate\Label\Differents"
# llm_filled_folder = "Forms\LLM_generate\Output\Processed_Output\Differents"
# df = similarity_result_two_folders(label_folder, llm_filled_folder)
# # Save to csv
# df.to_csv("Results/Result_25_1_19_30.csv", index=False)
# print(df)
