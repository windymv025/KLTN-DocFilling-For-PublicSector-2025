import MyClasses
import constant_value as CONST
import pandas as pd
import os

def create_dataset(input_folder_path, output_path):
    llm = MyClasses.LLM_Gemini(CONST.API_KEY) # Khởi tạo Gemini
    list_file_name = os.listdir(input_folder_path) # Lấy tên của file
    list_file_path = [os.path.join(input_folder_path, file_name) for file_name in list_file_name] # Đường dẫn đến file đó
    data = []
    for idx, file_path in enumerate(list_file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            file = f.read()

        handle_text = MyClasses.Text_Processing()
        blanked_text, _ = handle_text.generate_uniform(file)


        prompt_parts = CONST.template_blank_to_tagname2.format(personal_information_tag_names=CONST.personal_information_tag_names, Abstract = blanked_text)
        response = llm.model.generate_content(prompt_parts)
        response = response.text
        # Còn 1 bước tiền sử lí response trước khi thành Answer(chờ prompt đầy đủ rồi chỉnh sửa sau)
        data.append([idx, blanked_text, response])

    # Tạo DataFrame
    df = pd.DataFrame(data, columns=['id', 'Form', 'Answer'])

    # Lưu DataFrame thành file CSV
    df.to_csv(output_path, index=False, encoding='utf-8')