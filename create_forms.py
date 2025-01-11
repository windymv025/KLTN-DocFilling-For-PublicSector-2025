# ===== Take residence_identification_tagnames tagname =====
# from Config.tagnames import *
# import json

# list_red_iden_tagnames = study_tagnames.split("\n")[1:-1]
# list_tagnames = {}
# for tagname in list_red_iden_tagnames:
#     list_tagnames[tagname.split(":")[0]] = tagname.split(":")[1]
#     # list_tagnames.append(tagname.split(":")[0])
#     # list_meanings.append(tagname.split(":")[1])

# # Save
# with open("list_study_tagnames.json", "w", encoding="utf-8") as f:
#     json.dump(list_tagnames, f, ensure_ascii=False, indent=4)

# print(abc)
# print(list_tagnames)
# Print out
# for index in range(len(list_tagnames)):
#     print(f"{list_tagnames[index]}: {list_meanings[index]}")


# ===== Take forms is residence_identification_tagnames type =====
# from Tagnames.identify_form_types import identify_form_type
# from Config.LLM import gemini
# from Config.folders import *
# from Utils import *
# import os
# ## Check type of 1 form
# input_folders = [input_raw_folder, input_hand_process_folder]
# type1_forms = {}
# for input_folder in input_folders:
#     type1_forms[input_folder] = {}
#     for index,filename in enumerate(os.listdir(input_folder)):
#         if filename.endswith(".txt"):
#             file_dir = input_folder + '/' + filename
#             form_text = Text_Processing().Read_txt_file(file_dir)
#             # Print type
#             # print(f"{filename} content: {form_text}")
#             try:
#                 form_type = identify_form_type(gemini, form_text)
#                 if "2. Giáo dục" in form_type:
#                     print(f"{filename} have type: {form_type}")
#                     type1_forms[input_folder][filename] = form_text
#             except:
#                 pass
#         # print(f"{filename} have type: {identify_form_type(gemini, form_text)}")
# # Save
# import json

# # Save the list to a JSON file
# with open("type2_form_text.json", "w", encoding="utf-8") as f:
#     json.dump(type1_forms, f, ensure_ascii=False, indent=4)

# print("type2_form_text saved successfully!")
# print(abc)

# ===== Ask LLM generates form =====
# import json
# import random

# # Get list_tagnames
# with open("list_study_tagnames.json", "r", encoding="utf-8") as f:
#     list_tagnames = json.load(f)
# formatted_tagnames = "\n".join(
#     [f"- {key}: {value}" for key, value in list_tagnames.items()]
# )

# with open("type2_form_text.json", "r", encoding="utf-8") as f:
#     type1_form_texts = json.load(f)

# Get random forms
import random
from Config.LLM import gemini
from Tagnames import *

for i in range(10):
    random_forms = []
    for form_type, forms in type1_form_texts.items():
        # Get N random forms from each type
        N = 4
        random_files = random.sample(list(forms.items()), N)  # Randomly pick 3 forms
        for filename, form_content in random_files:
            random_forms.append(form_content)

    random_forms_text = "\n".join([form for form in random_forms])
    # print(random_forms_text)

    # Get prompt
    prompt_gen_forms = f"""
    Bạn là một AI được giao nhiệm vụ tạo form tài liệu và điền thông tin bằng các tagnames được cung cấp. 
    Hãy làm theo các bước sau:
    ##**Input**:
    1. **Tôi sẽ cung cấp danh sách các tagnames và ý nghĩa tương ứng**:
    {formatted_tagnames}

    2. **Tôi sẽ cung cấp nhiều form trống như sau**:
    {random_forms_text}

    ##**Yêu cầu**:
    1. **Tạo form tài liệu mới**:
    - Có thể tổng hợp, kết hợp từ các form đã cho, hoặc sáng tạo thêm nội dung mới phù hợp với mục đích tương tự.
    - Form mới phải có cấu trúc hợp lý và bám sát các tagnames đã cung cấp.
    - Các forms nên đa dạng, để tạo thành bộ dữ liệu tốt.
    2. **Điền vào form mới bằng các tagnames đã được cung cấp**:
    - Sử dụng prefix userX để biểu thị thuộc về đối tượng nào, ví dụ: [user1_full_name], [user2_dob_day].
    - Nếu một trường trong form không có tagname tương ứng trong danh sách, hãy để [#another].
    - Chỉ điền khi chắc chắn đúng.
    3. **Chỉ điền tagnames, không điền giá trị cụ thể. Một khi điền phải chính xác**.
    4. **Nếu bạn thêm trường mới hoặc tạo nội dung sáng tạo, đảm bảo rằng các trường đó phù hợp với mục tiêu và có thể sử dụng các tagnames đã cho**.

    ##**Output**:
    - Form mới được tạo ra với nội dung chứa các tagnames.
    - Các trường không có tagnames trong danh sách sẽ được để [#another].

    **Ví dụ output form chứa đầy đủ tagnames**:
    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM  
    Độc lập - Tự do - Hạnh phúc  

    TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ  
    Kính gửi [receiver]  
    1. Họ, chữ đệm và tên [user1_full_name]  
    2. Ngày, tháng, năm sinh [user1_dob_day]/[user1_dob_month]/[user1_dob_year]  
    3. Giới tính [user1_gender]  
    4. Số định danh cá nhân [user1_id_number] Ngày cấp [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year]  
    5. Số điện thoại liên hệ [user1_phone]  
    6. Email [user1_email]  
    7. Họ, chữ đệm và tên chủ hộ [user2_full_name]  
    8. Mối quan hệ với chủ hộ [another]  

    **Ví dụ output form với 25% trường trống**:
    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    Độc lập - Tự do - Hạnh phúc
    ---------------
    ĐƠN ĐĂNG KÝ HỌC SINH
    STUDENT REGISTRATION FORM

    Kính gửi (To): [receiver]
    Họ và tên học sinh (Full name of student): [user1_full_name]
    Ngày sinh (Date of birth): [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
    Giới tính (Gender): [user1_gender]
    Quốc tịch (Nationality): [user1_nationality]
    Nơi sinh (Place of birth): [user1_place_of_birth]
    Họ và tên cha (Father's name): [user2_full_name]
    Ngày sinh của cha (Father's date of birth): [user2_dob_day]/[user2_dob_month]/[user2_dob_year]
    Nơi sinh của cha (Father's place of birth): [another]
    Họ và tên mẹ (Mother's name): [user3_full_name]
    Ngày sinh của mẹ (Mother's date of birth): [user3_dob_day]/[user3_dob_month]/[user3_dob_year]
    Địa chỉ thường trú của học sinh (Student's address): [user1_permanent_address]
    Số điện thoại của học sinh (Student's phone number): [another]
    Trường học (School): [another]
    Lớp học (Class): [another]

    Người làm đơn (Applicant):
    (Ký và ghi rõ họ tên)
    (Signature and Full name)

    **Ví dụ output form với 50% trường trống**:
    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
    Độc lập - Tự do - Hạnh phúc
    ---------------
    ĐƠN ĐĂNG KÝ KHÁM BỆNH
    MEDICAL REGISTRATION FORM

    Kính gửi (To): [receiver]
    Họ và tên bệnh nhân (Full name of patient): [user1_full_name]
    Ngày sinh (Date of birth): [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
    Giới tính (Gender): [user1_gender]
    Số điện thoại (Phone number): [user1_phone]
    Địa chỉ liên lạc (Contact address): [user1_address]
    Số bảo hiểm y tế (Health insurance number): [another]
    Lý do khám bệnh (Reason for medical visit): [another]
    Tiền sử bệnh (Medical history): [another]
    Bác sĩ điều trị (Treating doctor): [another]
    Ngày khám (Examination date): [day]/[month]/[year]
    Chẩn đoán (Diagnosis): [another]

    Người làm đơn (Applicant):
    (Ký và ghi rõ họ tên)
    (Signature and Full name)

    Output:
    """

    # Use gemini

    prompt = PromptTemplate.from_template(prompt_gen_forms)
    chain = prompt | gemini | StrOutputParser()
    response = chain.invoke({})
    print(prompt_gen_forms)
    print(response)

    with open("output_study_forms.txt", "a", encoding="utf-8") as f:
        f.write(response)
