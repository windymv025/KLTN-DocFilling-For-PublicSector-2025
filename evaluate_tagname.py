from Evaluate.my_metrics import similarity_result_two_folders
# import pandas as pd
import time

# General
Data_num = 2
Train_Test = "Train"
# Train_Test = "Test"
Output_num = 2

# === Folder Addresses ===
label_folder = f"Temp\Data_{Data_num}\{Train_Test}\Label\Differents"
llm_filled_folder = f"Temp\Data_{Data_num}\{Train_Test}\Output{Output_num}\Processed_Output\Differents"

# ============= Evaluate between label and llm_filled folders=============
df = similarity_result_two_folders(label_folder, llm_filled_folder)
# Save to csv
time_now = time.strftime('%Y-%m-%d-%H-%M-%S')
df.to_csv(f"Temp/Data_{Data_num}/{Train_Test}/Result_{Output_num}_{time_now}.csv", index=False,encoding='utf-8-sig')

print(df)



