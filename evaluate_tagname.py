from Evaluate.my_metrics import similarity_result_two_folders
# import pandas as pd
import time

# === Folder Addresses Train ===
label_folder = "Temp\Data_2\Train\Label2\Differents"
llm_filled_folder = "Temp\Data_2\Train\Output2\Processed_Output\Differents"

# Test data
# label_folder = "Temp\Data_1\Test_data\Label\Differents"
# llm_filled_folder = "Temp\Data_1\Test_data\Output3\Processed_Output\Differents"

# ============= Evaluate between label and llm_filled folders=============
df = similarity_result_two_folders(label_folder, llm_filled_folder)
# Save to csv
time_now = time.strftime('%Y-%m-%d-%H-%M-%S')
df.to_csv(f"Temp/Data_2/Train/Result_{time_now}.csv", index=False)

# Save to test csv
# time_now = time.strftime('%Y-%m-%d-%H-%M-%S')
# df.to_csv(f"Temp/Data_1/Test_data/Result_3_{time_now}.csv", index=False)
print(df)



