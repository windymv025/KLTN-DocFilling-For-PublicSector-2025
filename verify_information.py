from datetime import datetime
import re

def verify_information(miss_item, input_value):
    if miss_item == "Họ tên":
        # Kiểm tra xem tên có phải là 1 chuỗi chỉ có kí tự và khoảng trắng hay không
        if input_value and all(x.isalpha() or x.isspace() for x in input_value):
            return True

    elif miss_item == "Email":
        # Định nghĩa email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, input_value):
            return True

    elif miss_item == "Số điện thoại":
        # Kiểm tra xem số điện thoại chỉ chứa số hay không
        phone_regex = r'^\d{10}$'
        if re.match(phone_regex, input_value):
            return True
        
    elif miss_item in ["Ngày sinh", "Tháng sinh", "Năm sinh", "Ngày cấp", "Tháng cấp", "Năm cấp", "Giờ", "Phút", "Giây"]:
        regex = r'^\d*$'
        if re.match(regex, input_value):
            return True
        
    elif miss_item == "Ngày tháng năm sinh" or miss_item == "Ngày tháng năm cấp":
        # Kiểm tra định dạng ngày tháng năm theo dd/mm/yyyy
        try:
            datetime.strptime(input_value, '%d/%m/%Y')
            return True
        except ValueError:
            return False
    
    elif miss_item == "Chứng minh nhân dân":
        cccd_regex = r'^\d*$'
        if re.match(cccd_regex, input_value):
            return True
        
    elif miss_item == "Chỗ ở" or miss_item == "Nơi thường trú":
        # Kiểm tra chỗ ở có thể chứa chữ cái, số, khoảng trắng và một số ký tự đặc biệt
        address_regex = r'^[a-zA-Z0-9\s,.-]+$'
        if re.match(address_regex, input_value):
            return True

    else:
        if input_value and all(x.isalpha() or x.isspace() for x in input_value):
            return True


