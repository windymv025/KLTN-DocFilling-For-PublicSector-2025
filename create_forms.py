# ===== Ask LLM generates form =====
import json
import random
# Get random forms
from Config.LLM import gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Text Processing
from Utils.text_processing import Text_Processing
# os and Time 
import os
import time

from Config.config import Data_num, Type, Label_Input_num

# Folder
label_folder = f"Temp/Data_{Data_num}/{Type}/Label{Label_Input_num}"
input_folder = f"Temp/Data_{Data_num}/{Type}/Input{Label_Input_num}"

# Ensure the folder exists
os.makedirs(input_folder, exist_ok=True)

temp = Text_Processing()
temp.convert_label_form_to_input_form(label_folder, input_folder)