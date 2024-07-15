
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

    else:
        return True


