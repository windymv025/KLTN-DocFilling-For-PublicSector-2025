import re
import subprocess
import pandas as pd
# Define the path to config.py
from Config import Data_num, Type

config_file = "Config/config.py"
root_folder = f"Temp\Data_{Data_num}\{Type}"


# Define the test cases for output_label_input_num and Data_num
output_label_input_nums = [11,12,13,21,22,23]

for output_label_input_num in output_label_input_nums:
    print(f"\nTesting with output_label_input_num={output_label_input_num}")

    # Read config.py content
    with open(config_file, "r") as file:
        content = file.read()

    # Modify the variables
    content = re.sub(r'output_label_input_num\s*=\s*\d+', f'output_label_input_num = {output_label_input_num}', content)
    # print(content)

    # Write back the modified content
    with open(config_file, "w") as file:
        file.write(content)

    print("Updated config.py ✅")

    # Run fill.py
    subprocess.run(["python", "fill_tagname_to_input.py"])
    print("Executed fill.py ✅")

    # Run evaluate.py
    subprocess.run(["python", "evaluate_tagname.py"])
    print("Executed evaluate.py ✅")

sum_df = pd.read_csv(f"{root_folder}/Result_statis_{output_label_input_nums[0]}.csv")
for output_label_input_num in output_label_input_nums[1:]:
    df = pd.read_csv(f"{root_folder}/Result_statis_{output_label_input_num}.csv")
    sum_df = pd.concat([sum_df, df], ignore_index=True)

df_reordered = pd.concat([sum_df.iloc[0::2], sum_df.iloc[1::2]]).reset_index(drop=True)

df_reordered.to_csv(f"{root_folder}/C_result.csv", index=False)
