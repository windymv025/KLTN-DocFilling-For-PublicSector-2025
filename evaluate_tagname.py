from Evaluate.my_metrics import similarity_result_two_folders
# import pandas as pd
import time

# === Folder Addresses ===
label_folder = "Temp\LLM_generate\Label\Differents"
llm_filled_folder = "Temp\LLM_generate\Output\Processed_Output\Differents"

# ============= Evaluate between label and llm_filled folders=============
df = similarity_result_two_folders(label_folder, llm_filled_folder)
# Save to csv
time_now = time.strftime('%Y-%m-%d-%H-%M-%S')
df.to_csv(f"Temp/Result_{time_now}.csv", index=False)
print(df)



