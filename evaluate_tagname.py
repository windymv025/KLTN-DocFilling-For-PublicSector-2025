from Evaluate.my_metrics import similarity_result_two_folders
import pandas as pd
import time
from Config import Data_num, Output_num

from collections import Counter

# === Folder Addresses ===
label_folder = f"Temp\Data_{Data_num}\Label\Differents"
llm_filled_folder = f"Temp\Data_{Data_num}\Output{Output_num}\Processed_Output\Differents"

# Function to process df_detail
def analyze_errors_type_1(error_list):
    """
    Phân tích danh sách lỗi, đếm số lần xuất hiện của từng lỗi (tag1, tag2).
    :param error_list: Danh sách chứa tuple (tag1, tag2)
    :return: Danh sách chứa tuple (tag1, tag2, count) sắp xếp theo số lần xuất hiện giảm dần.
    """
    counter = Counter(error_list)
    return sorted([(tag1, tag2, count) for (tag1, tag2), count in counter.items()], key=lambda x: x[2], reverse=True)

def analyze_errors_type_2(error_list):
    """
    Phân tích danh sách lỗi, đếm số lần xuất hiện của từng lỗi (tag1, tag2, context).
    :param error_list: Danh sách chứa tuple (tag1, tag2, context)
    :return: Danh sách chứa tuple (tag1, tag2, context, count) sắp xếp theo số lần xuất hiện giảm dần.
    """
    counter = Counter(error_list)
    return sorted([(tag1, tag2, context, count) for (tag1, tag2, context), count in counter.items()], 
                  key=lambda x: x[3], reverse=True)

# ============= Evaluate between label and llm_filled folders=============
df, df_detail = similarity_result_two_folders(label_folder, llm_filled_folder)
# Save to csv
time_now = time.strftime('%Y-%m-%d-%H-%M-%S')
# df.to_csv(f"Temp/Data_{Data_num}/Result_{Output_num}_{time_now}.csv", index=False,encoding='utf-8-sig')
# Process df detail
mean_columns = ["P_A1_A1", "P_B_B"]
sum_columns = ["P_A1_A2", "P_A1_B", "P_B_A1"]
mean_row = df_detail[mean_columns].mean()
sum_row = df_detail[sum_columns].sum()
# Combine mean and sum into a single DataFrame row

summary_row = pd.concat([mean_row, sum_row], axis=0)
summary_row["total_A1"] = "Summary"
print(df["error A1-B"])
print(sum(df["error A1-B"], []))
summary_row["C_A1_A2"] = analyze_errors_type_1(sum(df["error A1-A2"], []))
summary_row["C_A1_B"] = analyze_errors_type_1(sum(df["error A1-B"], []))
summary_row["C_B_A1"] = analyze_errors_type_1(sum(df["error B-A1"], []))
summary_row["D_A1_A2"] = analyze_errors_type_2(sum(df["error A1-A2 detail"], []))
summary_row["D_A1_B"] = analyze_errors_type_2(sum(df["error A1-B detail"], []))
summary_row["D_B_A1"] = analyze_errors_type_2(sum(df["error B-A1 detail"], []))

# Append to df_detail
df_detail = pd.concat([df_detail, pd.DataFrame([summary_row])], ignore_index=True)

# Save detail to csv
df_detail.to_csv(f"Temp/Data_{Data_num}/Result_Detail_{Output_num}_{time_now}.csv", index=False,encoding='utf-8-sig')
# LLM_Generate folder
# df_detail.to_csv(f"Temp/LLM_generate/Result_Detail_{Output_num}_{time_now}.csv", index=False,encoding='utf-8-sig')

# Print
print("Save result successfully!!")



