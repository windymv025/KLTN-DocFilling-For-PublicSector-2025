# ===Import===
from Utils.text_processing import Text_Processing
import os
from Config.config import Data_num, Type, Label_Input_num

# Folder - Input folder
label_folder = f"Temp/Data_{Data_num}/{Type}/Label{Label_Input_num}"
input_folder = f"Temp/Data_{Data_num}/{Type}/Input{Label_Input_num}"

# Ensure the folder exists
os.makedirs(input_folder, exist_ok=True)

# Convert label form to input form
temp = Text_Processing()
temp.convert_label_form_to_input_form(label_folder, input_folder)