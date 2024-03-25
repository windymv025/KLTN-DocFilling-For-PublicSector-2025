#Now, I'm having txt to full fill in question
import re

Question1 ='''TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1):……………………..…………………………..……………………………………………………………..………………………..
2. Họ, chữ đệm và tên gọi khác (nếu có)(1):………………………………………………………………………..…..……………
3. Ngày, tháng, năm sinh:…….……./…….……./……………….; 4. Giới tính (Nam/nữ):…………....…………..
5. Số CMND/CCCD: ..................................................................
6. Dân tộc:…………………….……; 7. Tôn giáo:…………………….……; 8. Quốc tịch: ………………………….………
9. Tình trạng hôn nhân:……………………………..………… 10. Nhóm máu (nếu có):………………………………
11. Nơi đăng ký khai sinh:…………………………………………………………………………………………………………………
12. Quê quán: ………………………………………………………………………………………………………………………………..………
13. Nơi thường trú:…………………………………………………………………………………………………………………..………………
…………………………………………………………………………………………………………………………………………………………………………………………………………….
14. Nơi ở hiện tại:………………………………………………………………………………………….………………………
…………………………………………………………………………………………………………………………………………………………………………………………………………….
15. Nghề nghiệp:………………………………… 16. Trình độ học vấn:……………………………………………………'''

Question2 ='''GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
Tên chủ xe :…………………..
Năm sinh:…………………..
Địa chỉ : ………………….
Số CCCD/CMND/Hộ chiếu của chủ xe:…………………..
cấp ngày .../.../.... tại …………………..
Số CCCD/CMND/Hộ chiếu của người làm thủ tục …………………..
cấp ngày …………………../………………….. /………………….. tại…………………..
Điện thoại của chủ xe :…………………..
Điện thoại của người làm thủ tục :…………………..
Số hóa đơn điện tử mã số thuế:…………………..
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp:…………………..
Số tờ khai hải quan điện tử cơ quan cấp:…………………..
Số sêri Phiếu KTCLXX Cơ quan cấp …………………………………………..…….
Số giấy phép kinh doanh vận tải cấp ngày …………………../………………….. / …………………..tại…………………..
Số máy 1 (Engine N0):…………………..
Số máy 2 (Engine N0):…………………..
Số khung (Chassis N0):…………………..'''

Question ='''ĐƠN XIN VIỆC

Kính gửi: Ban lãnh đạo cùng phòng nhân sự Công ty ...................................................

Tôi tên là: ......................................................................................................................

Sinh ngày: ....................................................................................................................

Chỗ ở hiện nay: ............................................................................................................

Số điện thoại liên hệ: ...................................................................................................

Thông qua trang website của công ty, tôi biết được Quý công ty có nhu cầu tuyển dụng vị trí……….. Tôi cảm thấy trình độ và kỹ năng của mình phù hợp với vị trí này. Tôi mong muốn được làm việc và cống hiến cho công ty.

Tôi đã tốt nghiệp loại …… tại trường ......................................................................

Bên cạnh đó, tôi có tham gia các khóa học…………………………………………

Ngoài ra, tôi còn sử dụng thành thạo tin học văn phòng, tiếng Anh giao tiếp tốt và biết sử dụng các phần mềm kế toán.

Tôi thực sự mong muốn được làm việc trong môi trường chuyên nghiệp của Quý công ty. Tôi rất mong nhận được lịch hẹn phỏng vấn trong một ngày gần nhất.
'''

Question4 = """
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1):……………………..…………………………..……………………………………………………………..………………………..
2. Họ, chữ đệm và tên gọi khác (nếu có)(1):………………………………………………………………………..…..……………
3. Ngày, tháng, năm sinh:…….……./…….……./……………….; 4. Giới tính (Nam/nữ):…………....…………..
5. Số CMND/CCCD: ..................................................................
6. Dân tộc:…………………….……; 7. Tôn giáo:…………………….……… 8. Quốc tịch: ………………………….………
9. Tình trạng hôn nhân:……………………………..………… 10. Nhóm máu (nếu có):………………………………
11. Nơi đăng ký khai sinh:…………………………………………………………………………………………………………………
12. Quê quán: ………………………………………………………………………………………………………………………………..………
13. Nơi thường trú:…………………………………………………………………………………………………………………..………………
…………………………………………………………………………………………………………………………………………………………………………………………………………….
14. Nơi ở hiện tại:………………………………………………………………………………………….………………………
…………………………………………………………………………………………………………………………………………………………………………………………………………….
15. Nghề nghiệp:………………………………… 16. Trình độ học vấn:……………………………………………….……… 
"""

#Write min function
def min(a, b):
    if a == -1 and b != -1:
        return b
    if b == -1 and a != -1:
        return a
    if a == -1 and b == -1:
        return -1
    if a < b:
        return a
    else:
        return b

def generate_uniform(Question):
    # Initialize a counter for numbering the placeholders
    placeholder_counter = 1

    type1 = ".."
    type2 = "…"
    first_index = min(Question.find(type1), Question.find(type2))
    # Loop through the question and replace the placeholders with the numbered placeholders
    while first_index != -1:
        # Replace the first occurrence of the placeholder with the formatted numbered placeholder
        Question = Question[:first_index] + "{" + str(placeholder_counter) + "}" + Question[first_index:]
        #Index }
        start_index = first_index+2+(len(str(placeholder_counter)))
        end_index = start_index
        # Increment the counter
        placeholder_counter += 1

        while (end_index < (len(Question))) and (Question[end_index] == "…" or Question[end_index] == "."):
            end_index  += 1

        if (end_index+1 < (len(Question))) and (Question[end_index] == "\n") and (Question[end_index+1] == "…" or Question[end_index+1] == "."):
            end_index  += 1

        while (end_index < (len(Question))) and (Question[end_index] == "…" or Question[end_index] == "."):
            end_index  += 1
        
        if end_index == 212:
            a = 2+3
        try:
            Question = Question[:start_index] + Question[end_index:]
        except:
            Question = Question[:start_index]

        # Find the indices of the next placeholders
        first_index = min(Question.find(type1), Question.find(type2))

    return Question


def fill_form(data, form):
    data_dict = dict(re.findall(r'\(Blank_(\d+)\): (.+)', data))
    def replace(match):
        blank_number = match.group(1)
        return data_dict.get(blank_number, '')

    form = re.sub(r'\(Blank(\d+)\)', replace, form)
    return form
