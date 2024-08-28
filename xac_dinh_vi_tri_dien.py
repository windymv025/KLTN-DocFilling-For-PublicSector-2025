import sys
sys.path.append("./Src")
import MyClasses
import constant_value as CONST
import os
import pandas as pd

LLM_class = MyClasses.LLM_Gemini(api_key = CONST.API_KEY)
Text_Processing_Class = MyClasses.Text_Processing()

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
           
#Run with folder 'Công dân All\Input'
foldel_dir = "Forms\Text\Công dân All\Input"
for index,filename in enumerate(os.listdir(foldel_dir)):
    if filename.endswith(".txt"):
        file_dir = foldel_dir + '/' + filename
        respones_dir = foldel_dir + '/Output/' + filename
        text = read_file(file_dir)
        processed_text = Text_Processing_Class.generate_uniform(text)[0]
        write_file(respones_dir, processed_text)

#Save to check
counts = []
folder_dir = "Forms\Text\Công dân All\Input\Output"
#Rename file in folder 'Công dân All'
for index,filename in enumerate(os.listdir(folder_dir)):
    if filename.endswith(".txt"):
        print("SST: ", index, "file_name: ", filename)
        file_dir = folder_dir + '/' + filename
        text = read_file(file_dir)
        # Count the occurrences of ".........."
        count = text.count("..........")
        #Save to dataframe
        counts.append(count)

#Save to csv file
df = pd.DataFrame(counts, columns = ['Count'])
df.to_csv('count_fullfill_place.csv', index=False)