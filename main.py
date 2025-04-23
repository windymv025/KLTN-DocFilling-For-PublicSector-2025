# Inference to fill tagname to string form
import argparse
import os
from Config.LLM import gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Prompts.define_tagnames import tagname_Nam_ver1_prompt
from Config.tagnames import tagname_Nam_ver1
from Utils.text_processing import Text_Processing
import re

def define_tagname_Nam_ver1(llm, text):
    prompt = PromptTemplate.from_template(tagname_Nam_ver1_prompt)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke(
        {"tagname": tagname_Nam_ver1, "form": text}
    )
    return response

def fix_infinity_space(text):
    '''
    Fix lỗi khi LLM điền vô hạn khoảng trắng
    '''
    # Replace more than 2 consecutive spaces with exactly 2 spaces
    text = re.sub(r' {3,}', '  ', text)
    
    # Replace more than 2 consecutive newlines with exactly 2 newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def process_single_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        string_form = f.read()

    # Inference to fill tagname to string form
    llm_filled = define_tagname_Nam_ver1(gemini, string_form)
    while not llm_filled.strip():  # Check if empty or contains only whitespace
        llm_filled = define_tagname_Nam_ver1(gemini, string_form)

    print("Generated successfully!!")
    print(llm_filled)

    # Post-processing steps
    input_text = string_form
    filled_text = llm_filled
    # Fix infinity space
    input_text = fix_infinity_space(input_text)
    filled_text = fix_infinity_space(filled_text)
    # Replace all ".........." by "[another]"
    input_text = input_text.replace("..........", "[#another]")
    filled_text = filled_text.replace("..........", "[#another]")

    filled_input_text, copy_contextual_input = Text_Processing().fill_input_by_llm_form(
        filled_text, input_text, process_tagname=True
    )
    print("Post-processing successfully!!")

    # Final output
    # print(filled_input_text)

    # Determine the folder of the input file
    input_folder = os.path.dirname(file_path)
    
    # Create the Results folder inside the same folder as the input file
    results_folder = os.path.join(input_folder, "Results")
    
    # Create the Results folder if it doesn't exist
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # Create a file name based on the input file name (adding '_processed' to the original name)
    base_filename = os.path.basename(file_path)
    output_filename = f"{os.path.splitext(base_filename)[0]}.txt"
    output_file_path = os.path.join(results_folder, output_filename)

    # Save the processed content to the new file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(filled_input_text)

    print(f"Processed file saved as {output_file_path}")

def process_multiple_files(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path) and file_path.endswith(".txt"):
            print(f"Processing file: {filename}")
            process_single_file(file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process form data.")
    parser.add_argument("mode", type=int, choices=[1, 2], help="Mode: 1 for single file, 2 for multiple files in a folder")
    parser.add_argument("--file", type=str, help="File path for mode 1", default="")  # New argument for file path
    parser.add_argument("--folder", type=str, help="Folder path for mode 2", default="")
    
    args = parser.parse_args()

    if args.mode == 1:
        # Run for a single file (e.g., main.py 1 --file input_0.txt)
        if not args.file:
            print("Please provide a file path using --file")
        else:
            process_single_file(args.file)

    elif args.mode == 2:
        # Run for multiple files in a folder (e.g., main.py 2 --folder your_folder_path)
        if not args.folder:
            print("Please provide a folder path for mode 2 using --folder")
        else:
            process_multiple_files(args.folder)