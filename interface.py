# Inference to fill tagname to string form
import os
import re
from datetime import datetime

import gradio as gr
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from Config.LLM import gemini
from Config.tagnames import tagname_Nam_ver1
from Prompts.define_tagnames import tagname_Nam_ver1_prompt
from Utils.text_processing import Text_Processing

# --- Global variables to store generated content ---
generated_tagnames = None
detected_user_tags = None
current_file = None
role_dict = None


def reset_global_variables():
    global generated_tagnames, detected_user_tags, current_file, role_dict
    generated_tagnames = None
    detected_user_tags = None
    role_dict = None
    current_file = None


def define_tagname_Nam_ver1(llm, text):
    prompt = PromptTemplate.from_template(tagname_Nam_ver1_prompt)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"tagname": tagname_Nam_ver1, "form": text})


def map_roles_to_dict(roles_text):
    role_dict = {}

    # Split the input text into lines
    lines = roles_text.strip().split("\n")

    for role in lines:
        # Remove leading "- " and any extra spaces
        role = role.lstrip("- ").strip()

        # Check if the line has the valid format "userX: description"
        if ": " in role:
            user, description = role.split(": ", 1)
            role_dict[user] = description.strip()  # Store the description as a string

    return role_dict


def define_name_of_user(llm, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        form = f.read()

    prompt_template = """
    Dựa vào nội dung biểu mẫu dưới đây, hãy xác định vai trò của từng cá nhân được đề cập và ánh xạ họ với định danh người dùng tương ứng (nếu có).
    Trả về kết quả dưới dạng format sau:

    - user1: vai trò của user1
    - user2: vai trò của user2
    - user3: vai trò của user3
    - user4: vai trò của user4

    Lưu ý: Chỉ liệt kê vai trò và ánh xạ tương ứng nếu có thông tin về người dùng (user). Nếu không có thông tin về người dùng nào, không cần đưa vào ánh xạ.

    ---

    Ví dụ:

    Biểu mẫu:
    ```
        CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
        
    Độc lập - Tự do - Hạnh phúc
    TỜ KHAI ĐĂNG KÝ KHAI SINH
    Kính gửi: (1)..........
    Họ, chữ đệm, tên người yêu cầu: ..........
    Nơi cư trú: (2)..........
    Giấy tờ tùy thân: (3)..........
    Quan hệ với người được khai sinh: ..........
    Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
    Họ, chữ đệm, tên:..........
    Ngày, tháng, năm sinh: ........../........../..........ghi bằng chữ: ..........
    Giới tính:.......... Dân tộc:..........Quốc tịch: ..........
    Nơi sinh: (4)..........
    Quê quán: ..........
    Họ, chữ đệm, tên người mẹ: ..........
    Năm sinh: (5)..........Dân tộc:..........Quốc tịch: ..........
    Nơi cư trú: (2) ..........
    Họ, chữ đệm, tên người cha: ..........
    Năm sinh: (5)..........Dân tộc:..........Quốc tịch: ..........
    Nơi cư trú: (2) ..........
    Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
    Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
    Làm tại: .........., ngày .......... tháng .......... năm ..........
    ```
    Kết quả:
    ```
    - user1: Người đi khai (người yêu cầu đăng ký khai sinh)
    - user2: Người được khai sinh
    - user3: Mẹ của người được khai sinh
    - user4: Cha của người được khai sinh
    ```

    Biểu mẫu: {form}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"form": form})
    print("Debug - LLM result:", result)
    role_dict = map_roles_to_dict(result)
    print("Debug - Mapped role_dict:", role_dict)
    return role_dict


def fix_infinity_space(text):
    """
    Fix lỗi khi LLM điền vô hạn khoảng trắng
    """
    # Replace more than 2 consecutive spaces with exactly 2 spaces
    text = re.sub(r" {3,}", "  ", text)

    # Replace more than 2 consecutive newlines with exactly 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def generate_tagnames(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
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

    filled_input_text, copy_contextual_input = Text_Processing().fill_input_by_llm_form(
        filled_text, input_text, process_tagname=True
    )
    # print(copy_contextual_input)
    print("Post-processing successfully!!")

    # Final output
    # print(filled_input_text)

    # Determine the folder of the input file
    input_folder = os.path.dirname(file_path)

    # Create the Results folder inside the same folder as the input file
    results_folder = os.path.join(input_folder, "Results")

    # Create the Results folder if it doesn't exist
    os.makedirs(results_folder, exist_ok=True)

    # Create a file name based on the input file name (adding '_processed' to the original name)
    base_filename = os.path.basename(file_path)
    output_filename = f"{os.path.splitext(base_filename)[0]}.txt"
    output_file_path = os.path.join(results_folder, output_filename)

    # Save the processed content to the new file
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(filled_input_text)

    print(f"Processed file saved as {output_file_path}")
    return filled_input_text


# --- Simulated Database ---
user_db = {
    "u001": {
        "full_name": "Nguyễn Văn A",
        "last_name": "Nguyễn",
        "middle_and_first_name": "Văn A",
        "alias_name": "NVA",
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
        "education_level": "Đại học",
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
        "education_level": "Thạc sĩ",
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
        "education_level": "Cao đẳng",
    },
}


provinces = [
    "An Giang",
    "Bà Rịa - Vũng Tàu",
    "Bắc Giang",
    "Bắc Kạn",
    "Bạc Liêu",
    "Bắc Ninh",
    "Bến Tre",
    "Bình Định",
    "Bình Dương",
    "Bình Phước",
    "Bình Thuận",
    "Cà Mau",
    "Cần Thơ",
    "Cao Bằng",
    "Đà Nẵng",
    "Đắk Lắk",
    "Đắk Nông",
    "Điện Biên",
    "Đồng Nai",
    "Đồng Tháp",
    "Gia Lai",
    "Hà Giang",
    "Hà Nam",
    "Hà Nội",
    "Hà Tĩnh",
    "Hải Dương",
    "Hải Phòng",
    "Hậu Giang",
    "Hòa Bình",
    "Hưng Yên",
    "Khánh Hòa",
    "Kiên Giang",
    "Kon Tum",
    "Lai Châu",
    "Lâm Đồng",
    "Lạng Sơn",
    "Lào Cai",
    "Long An",
    "Nam Định",
    "Nghệ An",
    "Ninh Bình",
    "Ninh Thuận",
    "Phú Thọ",
    "Phú Yên",
    "Quảng Bình",
    "Quảng Nam",
    "Quảng Ngãi",
    "Quảng Ninh",
    "Quảng Trị",
    "Sóc Trăng",
    "Sơn La",
    "Tây Ninh",
    "Thái Bình",
    "Thái Nguyên",
    "Thanh Hóa",
    "Thừa Thiên Huế",
    "Tiền Giang",
    "TP. Hồ Chí Minh",
    "Trà Vinh",
    "Tuyên Quang",
    "Vĩnh Long",
    "Vĩnh Phúc",
    "Yên Bái",
]


def detect_user_tags(form_text):
    tags = re.findall(r"\[user(\d+)_\w+\]", form_text)
    return sorted(set(f"user{num}" for num in tags), key=lambda x: int(x[4:]))


def fill_user_data(form_text, user_id, user_tag):
    user_data = user_db.get(user_id, {})

    def replace(match):
        tag = match.group(1)
        if tag.startswith(user_tag + "_"):
            field = tag.split("_", 1)[-1]
            return user_data.get(field, match.group(0))
        return match.group(0)

    return re.sub(r"\[([a-zA-Z0-9_#]+)\]", replace, form_text)


def fill_extra_fields(form_text, receiver, place):
    today = datetime.today()
    extra_fields = {
        "receiver": receiver if receiver else "[receiver]",
        "place": place if place else "[place]",
        "day": today.strftime("%d"),
        "month": today.strftime("%m"),
        "year": today.strftime("%Y"),
    }

    def replace_extra(match):
        tag = match.group(1)
        return extra_fields.get(tag, f"[{tag}]")

    return re.sub(r"\[([a-zA-Z0-9_#]+)\]", replace_extra, form_text)


def generate_tagnames_and_fill_form(file_obj, receiver, place, *user_names):
    global generated_tagnames, detected_user_tags, current_file, role_dict

    if file_obj is None:
        return "Please upload a form file first."

    # Generate tagnames and detect user tags only if not already done or if file changed
    if generated_tagnames is None or current_file != file_obj.name:
        generated_tagnames = generate_tagnames(file_obj.name)
        detected_user_tags = detect_user_tags(generated_tagnames)
        if len(detected_user_tags) > 1:
            role_dict = define_name_of_user(gemini, file_obj.name)
        current_file = file_obj.name

    form_text = generated_tagnames
    userx_list = detected_user_tags

    # Fill data for each user
    for i, user_name in enumerate(user_names):
        if i >= len(userx_list) or not user_name:
            continue

        # Find user ID from the selected name
        user_id = next(
            (uid for uid, info in user_db.items() if info["full_name"] == user_name),
            None,
        )
        if user_id:
            form_text = fill_user_data(form_text, user_id, userx_list[i])

    return fill_extra_fields(form_text, receiver, place)


def update_ui(file_obj):
    global generated_tagnames, detected_user_tags, current_file, role_dict

    if file_obj is None:
        reset_global_variables()
        return [gr.update(visible=False) for _ in range(4)] + [gr.update(visible=False)]

    # Generate tagnames and detect user tags only if not already done or if file changed
    if generated_tagnames is None or current_file != file_obj.name:
        generated_tagnames = generate_tagnames(file_obj.name)
        detected_user_tags = detect_user_tags(generated_tagnames)
        if len(detected_user_tags) > 1:
            role_dict = define_name_of_user(gemini, file_obj.name)
        current_file = file_obj.name

    userx_list = detected_user_tags

    print("Debug - userx_list:", userx_list)
    print("Debug - role_dict:", role_dict)

    if len(userx_list) == 1:
        return [gr.update(visible=False) for _ in range(4)] + [gr.update(visible=False)]

    updates = []
    for i in range(4):
        if i < len(userx_list):
            if i == 0:  # Show dropdown for user1 with first user as default
                first_user = list(user_db.values())[0]["full_name"]
                try:
                    role_label = (
                        role_dict[userx_list[i]]
                        if role_dict
                        else f"Select {userx_list[i]}"
                    )
                    updates.append(
                        gr.update(
                            visible=True, label=f"👤{role_label}", value=first_user
                        )
                    )
                except KeyError as e:
                    print(f"Debug - KeyError for {userx_list[i]}: {e}")
                    updates.append(
                        gr.update(
                            visible=True,
                            label=f"👤Select {userx_list[i]}",
                            value=first_user,
                        )
                    )
            else:  # Show dropdowns for user2 onwards
                try:
                    role_label = (
                        role_dict[userx_list[i]]
                        if role_dict
                        else f"Select {userx_list[i]}"
                    )
                    updates.append(gr.update(visible=True, label=f"👤{role_label}"))
                except KeyError as e:
                    print(f"Debug - KeyError for {userx_list[i]}: {e}")
                    updates.append(
                        gr.update(visible=True, label=f"👤Select {userx_list[i]}")
                    )
        else:
            updates.append(gr.update(visible=False))
    updates.append(gr.update(visible=True))
    return updates


# --- Gradio UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 📋 Form Filling Interface")
    gr.Markdown("Upload your form and fill it with user data")

    with gr.Column():
        with gr.Row():
            form_file = gr.File(label="📂 Upload Form (.txt)")
            gen_btn = gr.Button("🔍 Generate Tagnames")
            gen_and_fill_btn = gr.Button("🔍 & ✍️ Generate & Fill Form")

        receiver_input = gr.Textbox(label="📥 Receiver Name")
        place_input = gr.Dropdown(choices=provinces, label="📍 Select Place")

        # User selection section
        user_section = gr.Column(visible=False)
        with user_section:
            gr.Markdown("### 👥 Select Users for Each [userX] Tag:")
            userx_dropdowns = []
            for i in range(4):  # max 4 userX
                dropdown = gr.Dropdown(
                    choices=[user["full_name"] for user in user_db.values()],
                    label=f"User {i+1}",
                    visible=False,
                )
                userx_dropdowns.append(dropdown)
        fill_btn = gr.Button("✍️ Fill Form")
        output_textbox = gr.Textbox(label="📄 Filled Form Output", lines=20)

        form_file.change(
            fn=update_ui, inputs=form_file, outputs=userx_dropdowns + [user_section]
        )
        # Generate tagnames
        gen_btn.click(fn=generate_tagnames, inputs=form_file, outputs=output_textbox)
        # Generate tagnames and fill form
        gen_and_fill_btn.click(
            fn=generate_tagnames_and_fill_form,
            inputs=[form_file, receiver_input, place_input] + userx_dropdowns,
            outputs=output_textbox,
        )
        # Fill form
        fill_btn.click(
            fn=generate_tagnames_and_fill_form,
            inputs=[form_file, receiver_input, place_input] + userx_dropdowns,
            outputs=output_textbox,
        )

if __name__ == "__main__":
    demo.launch(share=True)
