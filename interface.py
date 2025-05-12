# Inference to fill tagname to string form
import gradio as gr
import os
from Config.LLM import gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Prompts.define_tagnames import tagname_Nam_ver1_prompt
from Config.tagnames import tagname_Nam_ver1
from Utils.text_processing import Text_Processing
from datetime import datetime
import re

def define_tagname_Nam_ver1(llm, text):
    prompt = PromptTemplate.from_template(tagname_Nam_ver1_prompt)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke(
        {"tagname": tagname_Nam_ver1, "form": text}
    )
    return response

def fix_infinity_space(text):
    '''
    Fix lỗi khi LLM điền vô hạn khoảng trắng
    '''
    # Replace more than 2 consecutive spaces with exactly 2 spaces
    text = re.sub(r' {3,}', '  ', text)
    
    # Replace more than 2 consecutive newlines with exactly 2 newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def generate_tagnames(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        string_form = f.read()

    # Inference to fill tagname to string form
    llm_filled = define_tagname_Nam_ver1(gemini, string_form)
    while not llm_filled.strip():  # Check if empty or contains only whitespace
        llm_filled = define_tagname_Nam_ver1(gemini, string_form)

    # Post-processing steps
    input_text = string_form
    filled_text = llm_filled
    # Fix infinity space
    input_text = fix_infinity_space(input_text)
    filled_text = fix_infinity_space(filled_text)
    # Replace all ".........." by "[another]"
    input_text = input_text.replace("..........", "[#another]")
    filled_text = filled_text.replace("..........", "[#another]")

    # print("Filled text:\n", filled_text)

    filled_input_text, copy_contextual_input = Text_Processing().fill_input_by_llm_form(
        filled_text, input_text, process_tagname=True
    )

    # print("Filled text 2:\n", filled_input_text)
    print("Post-processing successfully!!")

    # Final output
    # print(filled_input_text)

    # Determine the folder of the input file
    input_folder = os.path.dirname(file_path)
    
    # Create the Results folder inside the same folder as the input file
    results_folder = os.path.join(input_folder, "Results")
    
    # Create the Results folder if it doesn't exist
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # Create a file name based on the input file name (adding '_processed' to the original name)
    base_filename = os.path.basename(file_path)
    output_filename = f"{os.path.splitext(base_filename)[0]}.txt"
    output_file_path = os.path.join(results_folder, output_filename)

    # Save the processed content to the new file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(filled_input_text)

    print(f"Processed file saved as {output_file_path}")
    return filled_input_text


# --- Simulated Database ---
user_db = {
    "u001": {
        "full_name": "Nguyễn Văn A",
        "last_name": "Nguyễn",
        "middle_and_first_name": "Văn A",
        "alias_name": "",
        "dob_text": "01 tháng 01 năm 1990",
        "dob": "01/01/1990",
        "dob_day": "01",
        "dob_month": "01",
        "dob_year": "1990",
        "gender": "Nam",
        "id_number": "0123456789",
        "id_issue_date": "01/01/2010",
        "id_issue_day": "01",
        "id_issue_month": "01",
        "id_issue_year": "2010",
        "id_issue_place": "Cục Cảnh sát QLHC về TTXH",
        "occupation": "Kỹ sư phần mềm",
        "ethnicity": "Kinh",
        "religion": "Không",
        "nationality": "Việt Nam",
        "marital_status": "Độc thân",
        "blood_type": "O",
        "birthplace": "Hà Nội",
        "birthplace_ward": "Phường Thanh Xuân Trung",
        "birthplace_district": "Quận Thanh Xuân",
        "birthplace_province": "Hà Nội",
        "birth_registration_place": "UBND Quận Thanh Xuân",
        "birth_registration_place_ward": "Phường Thanh Xuân Trung",
        "birth_registration_place_district": "Quận Thanh Xuân",
        "birth_registration_place_province": "Hà Nội",
        "hometown": "Nam Định",
        "hometown_ward": "Xã Yên Trung",
        "hometown_district": "Huyện Ý Yên",
        "hometown_province": "Nam Định",
        "permanent_address": "123 Nguyễn Trãi, Hà Nội",
        "permanent_address_village": "",
        "permanent_address_ward": "Phường Thanh Xuân Trung",
        "permanent_address_district": "Quận Thanh Xuân",
        "permanent_address_province": "Hà Nội",
        "current_address": "123 Nguyễn Trãi, Hà Nội",
        "current_address_village": "",
        "current_address_ward": "Phường Thanh Xuân Trung",
        "current_address_district": "Quận Thanh Xuân",
        "current_address_province": "Hà Nội",
        "passport_number": "C1234567",
        "passport_issue_date": "01/01/2020",
        "passport_issue_day": "01",
        "passport_issue_month": "01",
        "passport_issue_year": "2020",
        "passport_issue_place": "Cục Quản lý Xuất nhập cảnh",
        "passport_expiry_date": "01/01/2030",
        "passport_expiry_day": "01",
        "passport_expiry_month": "01",
        "passport_expiry_year": "2030",
        "email": "vana@example.com",
        "home_phone": "0243-123456",
        "phone": "0912345678",
        "health_insurance_number": "HN123456789",
        "social_insurance_number": "SI987654321",
        "education_level": "Đại học"
    },
    "u002": {
        "full_name": "Trần Thị B",
        "last_name": "Trần",
        "middle_and_first_name": "Thị B",
        "alias_name": "",
        "dob_text": "15 tháng 03 năm 1992",
        "dob": "15/03/1992",
        "dob_day": "15",
        "dob_month": "03",
        "dob_year": "1992",
        "gender": "Nữ",
        "id_number": "2233445566",
        "id_issue_date": "10/04/2011",
        "id_issue_day": "10",
        "id_issue_month": "04",
        "id_issue_year": "2011",
        "id_issue_place": "Công an TP. Hồ Chí Minh",
        "occupation": "Giáo viên",
        "ethnicity": "Kinh",
        "religion": "Phật giáo",
        "nationality": "Việt Nam",
        "marital_status": "Đã kết hôn",
        "blood_type": "A",
        "birthplace": "Đà Nẵng",
        "birthplace_ward": "Phường Hải Châu I",
        "birthplace_district": "Quận Hải Châu",
        "birthplace_province": "Đà Nẵng",
        "birth_registration_place": "UBND Quận Hải Châu",
        "birth_registration_place_ward": "Phường Hải Châu I",
        "birth_registration_place_district": "Quận Hải Châu",
        "birth_registration_place_province": "Đà Nẵng",
        "hometown": "Quảng Nam",
        "hometown_ward": "Xã Duy Trung",
        "hometown_district": "Huyện Duy Xuyên",
        "hometown_province": "Quảng Nam",
        "permanent_address": "456 Lê Lợi, Đà Nẵng",
        "permanent_address_ward": "Phường Hải Châu I",
        "permanent_address_district": "Quận Hải Châu",
        "permanent_address_province": "Đà Nẵng",
        "current_address": "456 Lê Lợi, Đà Nẵng",
        "current_address_ward": "Phường Hải Châu I",
        "current_address_district": "Quận Hải Châu",
        "current_address_province": "Đà Nẵng",
        "passport_number": "B7654321",
        "passport_issue_date": "20/05/2018",
        "passport_issue_day": "20",
        "passport_issue_month": "05",
        "passport_issue_year": "2018",
        "passport_issue_place": "Phòng Quản lý Xuất nhập cảnh Đà Nẵng",
        "passport_expiry_date": "20/05/2028",
        "passport_expiry_day": "20",
        "passport_expiry_month": "05",
        "passport_expiry_year": "2028",
        "email": "thib@example.com",
        "home_phone": "0236-987654",
        "phone": "0987123456",
        "health_insurance_number": "HN987654321",
        "social_insurance_number": "SI123456789",
        "education_level": "Thạc sĩ"
    },
    "u003": {
        "full_name": "Lê Văn C",
        "last_name": "Lê",
        "middle_and_first_name": "Văn C",
        "alias_name": "",
        "dob_text": "22 tháng 07 năm 1988",
        "dob": "22/07/1988",
        "dob_day": "22",
        "dob_month": "07",
        "dob_year": "1988",
        "gender": "Nam",
        "id_number": "3344556677",
        "id_issue_date": "15/06/2008",
        "id_issue_day": "15",
        "id_issue_month": "06",
        "id_issue_year": "2008",
        "id_issue_place": "Công an tỉnh Bình Dương",
        "occupation": "Kỹ thuật viên",
        "ethnicity": "Kinh",
        "religion": "Không",
        "nationality": "Việt Nam",
        "marital_status": "Độc thân",
        "blood_type": "B",
        "birthplace": "TP.HCM",
        "birthplace_ward": "Phường Bến Nghé",
        "birthplace_district": "Quận 1",
        "birthplace_province": "TP.HCM",
        "birth_registration_place": "UBND Quận 1",
        "birth_registration_place_ward": "Phường Bến Nghé",
        "birth_registration_place_district": "Quận 1",
        "birth_registration_place_province": "TP.HCM",
        "hometown": "Bình Dương",
        "hometown_ward": "Xã An Phú",
        "hometown_district": "TP. Thuận An",
        "hometown_province": "Bình Dương",
        "permanent_address": "789 Pasteur, Quận 1, TP.HCM",
        "permanent_address_ward": "Phường Bến Nghé",
        "permanent_address_district": "Quận 1",
        "permanent_address_province": "TP.HCM",
        "current_address": "789 Pasteur, Quận 1, TP.HCM",
        "current_address_ward": "Phường Bến Nghé",
        "current_address_district": "Quận 1",
        "current_address_province": "TP.HCM",
        "passport_number": "A9876543",
        "passport_issue_date": "10/09/2015",
        "passport_issue_day": "10",
        "passport_issue_month": "09",
        "passport_issue_year": "2015",
        "passport_issue_place": "Cục Quản lý Xuất nhập cảnh TP.HCM",
        "passport_expiry_date": "10/09/2025",
        "passport_expiry_day": "10",
        "passport_expiry_month": "09",
        "passport_expiry_year": "2025",
        "email": "levanc@example.com",
        "home_phone": "0283-567890",
        "phone": "0934567890",
        "health_insurance_number": "HN555888333",
        "social_insurance_number": "SI333888555",
        "education_level": "Cao đẳng"
    }
}


provinces = [
    "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu", "Bắc Ninh",
    "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước", "Bình Thuận", "Cà Mau",
    "Cần Thơ", "Cao Bằng", "Đà Nẵng", "Đắk Lắk", "Đắk Nông", "Điện Biên",
    "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội",
    "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên",
    "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn",
    "Lào Cai", "Long An", "Nam Định", "Nghệ An", "Ninh Bình", "Ninh Thuận",
    "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh",
    "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên",
    "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "TP. Hồ Chí Minh", "Trà Vinh",
    "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
]

def detect_user_tags(form_text):
    tags = re.findall(r'\[user(\d+)_\w+\]', form_text)
    unique_userx = sorted(set(f"user{num}" for num in tags), key=lambda x: int(x[4:]))
    return unique_userx

def fill_user_data(form_text, user_id, user_tag):
    user_data = user_db.get(user_id, {})

    def replace(match):
        tag = match.group(1)
        if tag.startswith(user_tag + "_"):
            field = tag.split("_", 1)[-1]
            return user_data.get(field, match.group(0))
        return match.group(0)

    return re.sub(r"\[([a-zA-Z0-9_#]+)\]", replace, form_text)

def update_userx_dropdowns(form_text):
    userx_list = detect_user_tags(form_text)
    updates = []
    for i in range(5):
        if i < len(userx_list):
            updates.append(gr.update(visible=True, label=f"👤 Select {userx_list[i]}", value=None))
        else:
            updates.append(gr.update(visible=False, value=None))
    return updates

def fill_all_users(form_text, receiver, place, *user_names):
    userx_list = detect_user_tags(form_text)
    filled = form_text
    for i, name in enumerate(user_names):
        if i >= len(userx_list) or not name:
            continue
        user_id = next((uid for uid, info in user_db.items() if info["full_name"] == name), None)
        if user_id:
            filled = fill_user_data(filled, user_id, userx_list[i])

    today = datetime.today()
    extra_fields = {
        "receiver": receiver,
        "place": place,
        "day": today.strftime("%d"),
        "month": today.strftime("%m"),
        "year": today.strftime("%Y")
    }

    def replace_extra(match):
        tag = match.group(1)
        if tag in extra_fields:
            return extra_fields[tag]
        else:
            return ".........."

    final = re.sub(r"\[([a-zA-Z0-9_#]+)\]", replace_extra, filled)
    return final

# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 📋 Fill Form")
    gr.Markdown("Upload form ➔ Generate tagnames ➔ Select users ➔ Fill form")

    with gr.Column():
        with gr.Row():
            form_file = gr.File(label="📌 Upload Form (.txt)")
            load_btn = gr.Button("📄 Generate tagnames")

        form_text = gr.Textbox(label="📑 Form with Tagnames", lines=15)
        load_btn.click(fn=generate_tagnames, inputs=form_file, outputs=form_text)

        form_text.change(fn=update_userx_dropdowns, inputs=form_text, outputs=[])

        receiver_input = gr.Textbox(label="📝 Receiver")
        place_input = gr.Dropdown(choices=provinces, label="🌐 Place")

        gr.Markdown("### 👥 Select users for each [userX] tag:")
        userx_dropdowns = []
        for i in range(5):  # max 5 userX
            dropdown = gr.Dropdown(
                choices=[user["full_name"] for user in user_db.values()],
                label=f"user{i+1}",
                visible=False
            )
            userx_dropdowns.append(dropdown)

        fill_btn = gr.Button("📝 Fill Form")

        output_textbox = gr.Textbox(label="📨 Filled Form Output", lines=20)

        form_text.change(fn=update_userx_dropdowns, inputs=form_text, outputs=userx_dropdowns)

        fill_btn.click(
            fn=fill_all_users,
            inputs=[form_text, receiver_input, place_input] + userx_dropdowns,
            outputs=output_textbox
        )




if __name__ == "__main__":
    demo.launch(share=True)