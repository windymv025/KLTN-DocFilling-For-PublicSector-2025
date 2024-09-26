import re
import sys
sys.path.append("./Src")
import constant_value as CONST

# Lists of valid tagnames
list_cccd_passport_tagnames = CONST.list_cccd_passport_tagnames
list_general_tagnames = CONST.list_general_tagnames

# Combine both lists of tagnames
valid_tagnames_general = list_general_tagnames
valid_tagnames_cccd_passport = list_cccd_passport_tagnames

def remove_invalid_tagnames(form_text, valid_tagnames_general, valid_tagnames_cccd_passport):
    # Regular expression to match all tagnames (e.g., [user1_full_name], [place], etc.)
    tagname_pattern = re.compile(r'\[.*?\]')

    # Function to replace invalid tagnames
    def replace_invalid_tagname(match):
        tagname = match.group(0)

        # Check if the tagname is a general tagname (direct match)
        if tagname in valid_tagnames_general:
            return tagname  # Keep general tagnames unchanged

        # Check if the tagname is a valid cccd/passport tagname with userX_ prefix (e.g., [user1_full_name])
        for valid_tagname in valid_tagnames_cccd_passport:
            if re.match(r'\[user\d+_' + re.escape(valid_tagname[1:-1]) + r'\]', tagname):
                return tagname  # Keep valid userX_ prefixed tagnames

        # If the tagname is not in the valid lists, remove it
        return ".........."

    # Process the form by replacing invalid tagnames
    cleaned_form = re.sub(tagname_pattern, replace_invalid_tagname, form_text)

    return cleaned_form

# Example form with tagnames (some are valid, others are not)
form = """
Mẫu số 10: Ban hành kèm theo Thông t¬ư số 15/2023/TT-BLĐTBXH ngày 29 tháng 12 năm 2023 của Bộ trưởng Bộ Lao động - Th¬ươngbinh và Xã hội.

CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc


ĐỀ NGHỊ CHUYỂN NƠI H¬ƯỞNG TRỢ CẤP THẤT NGHIỆP
Kính gửi: Trung tâm Dịch vụ việc làm [receiver]
Tên tôi là: [user1_full_name] sinh ngày[user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number]cấp ngày[user1_id_number_issue_day]tháng[user1_id_number_issue_month]năm[user1_id_number_issue_year]    Nơi cấp[user1_id_number_issue_place]
Số sổ BHXH:[user1_id]
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú):[user1_current_address]
Hiện nay, tôi đang hưởng trợ cấp thất nghiệp theo Quyết định số [user1_id] ngày [user1_id_number_issue_day]/[user1_id_number_issue_month]/[user1_id_number_issue_year] của Giám đốc Sở Lao động - Thương binh và Xã hội tỉnh/thành phố[user1_id_number_issue_place]
Tổng số tháng được hưởng trợ cấp thất nghiệp:[user1_id]tháng
Đã hưởng trợ cấp thất nghiệp: [user1_id]tháng
Nhưng vì lý do: [user1_id]
tôi đề nghị quý Trung tâm chuyển nơi hưởng trợ cấp thất nghiệp đến tỉnh/thành phố[user1_id]để tôi được tiếp tục hưởng các chế độ bảo hiểm thất nghiệp theo quy định./.
		[place], ngày [day] tháng [month] năm [year]
"""

# Call the function to clean the form
cleaned_form = remove_invalid_tagnames(form, valid_tagnames_general, valid_tagnames_cccd_passport)

# Output the cleaned form
print(cleaned_form)
