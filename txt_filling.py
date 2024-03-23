from langchain.prompts import ChatPromptTemplate
import re
import chromadb
# Agent
from langchain.tools import BaseTool
#
import chainlit as cl
from chainlit.sync import run_sync
# -------------------------- prompt cho điền file .txt, đã triển khai theo cấu trúc CoT ------------------------------------
def txt_prompt():
    template = """
    <start_of_turn>user
    Context: 
    			TỜ KHAI CĂN CƯỚC CÔNG DÂN

        1. Họ, chữ đệm và tên(1): Lê Dũng
        2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không có
        3. Ngày, tháng, năm sinh: 05/09/1964; 4. Giới tính (Nam/nữ): Nam
        5. Số CMND/CCCD: 005568561645
        6. Dân tộc: Kinh; 7. Tôn giáo: Không 8. Quốc tịch: Việt Nam
        9. Tình trạng hôn nhân: Có 10. Nhóm máu (nếu có): O
        11. Nơi đăng ký khai sinh: Gia Lai
        12. Quê quán: Phú Dương, Phú Vang, Thừa Thiên Huế
        13. Nơi thường trú: Phú Túc
        14. Nơi ở hiện tại: Phú Túc
        15. Nghề nghiệp: Bác Sĩ 16. Trình độ học vấn: Đại học

    Question:
                ĐƠN XIN VIỆC

    Kính gửi: Ban lãnh đạo cùng phòng nhân sự Công ty Blank_1
    Tôi tên là: Blank_2
    Sinh ngày: Blank_3
    Chỗ ở hiện nay: Blank_4
    Số điện thoại liên hệ: Blank_5
    Thông qua trang website của công ty, tôi biết được Quý công ty có nhu cầu tuyển dụng vị tríBlank_6Blank_Tôi cảm thấy trình độ và kỹ năng của mình phù hợp với vị trí này. Tôi mong muốn được làm việc và cống hiến cho công ty.

    Tôi đã tốt nghiệp loại Blank_7 tại trường Blank_8
    Bên cạnh đó, tôi có tham gia các khóa học Blank_9
    Ngoài ra, tôi còn sử dụng thành thạo tin học văn phòng, tiếng Anh giao tiếp tốt và biết sử dụng các phần mềm kế toán.

    Tôi thực sự mong muốn được làm việc trong môi trường chuyên nghiệp của Quý công ty. Tôi rất mong nhận được lịch hẹn phỏng vấn trong một ngày gần nhất.<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. After ',' sign or before ':'
    Output1:
    + Họ, chữ đệm và tên(1): Lê Dũng
    + Họ, chữ đệm và tên gọi khác (nếu có)(2): Không có
    + Ngày sinh: 05
    + Tháng sinh: 09
    + Năm sinh: 1964
    + Giới tính (Nam/nữ): Nam
    + Số CMND/CCCD: 005568561645
    + Dân tộc: Kinh
    + Tôn giáo: Không
    + Quốc tịch: Việt Nam
    + Tình trạng hôn nhân: Có
    + Nhóm máu (nếu có): O
    + Nơi đăng ký khai sinh: Gia Lai
    + Quê quán: Phú Dương, Phú Vang, Thừa Thiên Huế
    + Nơi thường trú: Phú Túc
    + Nơi ở hiện tại: Phú Túc
    + Nghề nghiệp: Bác Sĩ
    + Trình độ học vấn: Đại học
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before Blank_x syntax with * as a number, such as: Blank_1, Blank_2.
    Output2:
    1. Ban lãnh đạo cùng phòng nhân sự Công ty: Blank_1
    2. Tôi tên là: Blank_2
    3. Sinh ngày: Blank_3
    4. Chỗ ở hiện nay: Blank_4
    5. Số điện thoại liên hệ: Blank_5
    6. vị trí: Blank_6
    7. tốt nghiệp loại: Blank_7
    8. tại trường: Blank_8
    9. khóa học: Blank_9
    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.
    - Final Result:
    Blank_1: Rỗng
    Blank_2: Lê Dũng
    Blank_3: 05/09/1964
    Blank_4: Phú Túc
    Blank_5: Rỗng
    Blank_6: Rỗng
    Blank_7: Rỗng
    Blank_8: Rỗng
    Blank_9: Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CCCD là 12345.
    Question:
                TỜ KHAI CĂN CƯỚC CÔNG DÂN

                
    1. Họ, chữ đệm và tên(1): Blank_1
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Blank_2
    3. Ngày, tháng, năm sinh:Blank_3/Blank_4/Blank_5; 4. Giới tính (Nam/nữ): Blank_6
    5. Số CMND/CCCD: Blank_7
    6. Dân tộc: Blank_8; 7. Tôn giáo: Blank_9 8. Quốc tịch: Blank_10
    9. Tình trạng hôn nhân: Blank_11 10. Nhóm máu (nếu có): Blank_12
    11. Nơi đăng ký khai sinh: Blank_13
    12. Quê quán: Blank_14
    13. Nơi thường trú: Blank_15
    14. Nơi ở hiện tại: Blank_16
    15. Nghề nghiệp: Blank_17 16. Trình độ học vấn: Blank_18<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. After ',' sign or before ':'
    Output1:
    + Họ tên: Nguyễn Đức Nam
    + Sinh viên năm 3
    + Ngày sinh: 26/02/2003
    + Dân tộc: Kinh
    + Quê: Bình Định
    + Quốc tịch: Việt Nam
    + CCCD: 12345
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before Blank_x syntax with * as a number, such as: Blank_1, Blank_2.
    Output2:
    1. Họ, chữ đệm và tên(1): Blank_1
    2. Họ, chữ đệm và tên gọi khác (nếu có)(2): Blank_2
    3. Ngày sinh: Blank_3
    4. Tháng sinh: Blank_4
    5. Năm sinh: Blank_5
    6. Giới tính (Nam/nữ): Blank_6
    7. Số CMND/CCCD: Blank_7
    8. Dân tộc: Blank_8
    9. Tôn giáo: Blank_9
    10. Quốc tịch: Blank_10
    11. Tình trạng hôn nhân: Blank_11
    12. Nhóm máu (nếu có): Blank_12
    13. Nơi đăng ký khai sinh: Blank_13
    14. Quê quán: Blank_14
    15. Nơi thường trú: Blank_15
    16. Nơi ở hiện tại: Blank_16
    17. Nghề nghiệp: Blank_17
    18. Trình độ học vấn: Blank_18
    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.
    - Final Result:
    Blank_1: Nguyễn Đức Nam
    Blank_2: Rỗng
    Blank_3: 26
    Blank_4: 02
    Blank_5: 2003
    Blank_6: Rỗng
    Blank_7: 12345
    Blank_8: Kinh
    Blank_9: Rỗng
    Blank_10: Việt Nam
    Blank_11: Rỗng 
    Blank_12: Rỗng
    Blank_13: Rỗng
    Blank_14: Bình Định
    Blank_15: Rỗng
    Blank_16: Rỗng
    Blank_17: Rỗng
    Blank_18: Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Họ và tên: Lê Hữu Hưng, giới tính nam, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai, số CCCD là 12345, đang sống tại KTX B, email: lhh@gmail.com.
    Question:
            ĐƠN XIN CẤP LẠI CCCD
    
    Tôi là: Blank_1 Quốc tịch: Blank_2
    Sinh ngày: Blank_3 tháng Blank_4 năm Blank_5
    Nơi đăng ký hộ khẩu thường trú: Blank_6
    Nơi cư trú: Blank_7
    Điện thoại: Blank_8
    Số CCCD (hoặc hộ chiếu): Blank_9
    Cấp ngày: Blank_10 tháng Blank_11 năm Blank_12 Nơi cấp: Blank_13<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. After ',' sign or before ':'
    Output1:
    + Họ tên: Lê Hữu Hưng
    + Giới tính: Nam
    + Sinh ngày: 01/03/2003
    + Quê quán: Gia Lai
    + Quốc Tịch: Việt Nam
    + CMND: 12345
    + Hiện tại đang sống ở KTX khu B.
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before Blank_x syntax with * as a number, such as: Blank_1, Blank_2.
    Output2:
    1. Tôi là: Blank_1
    2. Quốc tịch: Blank_2
    3. Sinh ngày   : Blank_3
    4. tháng     : Blank_4
    5. năm: Blank_5
    6. Nơi đăng ký hộ khẩu thường trú: Blank_6
    7. Nơi cư trú: Blank_7
    8. Điện thoại: Blank_8
    9. Số CCCD (hoặc hộ chiếu): Blank_9
    10. Cấp ngày   : Blank_10
    11. tháng  : Blank_11
    12. năm  : Blank_12
    13. Nơi cấp: Blank_13
    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.
    - Final Result:
    Blank_1: Lê Hữu Hưng
    Blank_2: Việt Nam
    Blank_3: 01
    Blank_4: 03
    Blank_5: 2003
    Blank_6: Rỗng
    Blank_7: KTX Khu B
    Blank_8: Rỗng
    Blank_9: 12345
    Blank_10: Rỗng
    Blank_11: Rỗng
    Blank_12: Rỗng
    Blank_13: Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Tôi tên Đoàn Thị Hoàn, MSSV: 21120463, học lớp 21TNT1, ngành Trí tuệ Nhân tạo. Tôi sinh ngày 19/05/1965, số điện thoại là 035589611.
    Question:
            ĐƠN XIN NGHỈ HỌC

    Tôi tên: Blank_1	 MSSV:	Blank_2
    Ngành học: Blank_3	 Lớp: 	Blank_4
    Ngày sinh: Blank_5 	 Nơi sinh: Blank_6	
    Địa chỉ hộ khẩu thường trú:	Blank_7
    Điện thoại: Blank_8
    Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được thôi học từ học kỳ: Blank_9 năm học: 20Blank_10 – 20Blank_11
    Lý do: Blank_12
    Trong khi chờ đợi sự chấp thuận của nhà trường, tôi xin chân thành cảm ơn.<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. After ',' sign or before ':'
    Output1:
    + Họ tên: Đoàn Thị Hoàn
    + MSSV: 21120463
    + Lớp: 21TNT1
    + Ngành: Trí tuệ Nhân tạo
    + Ngành sinh: 19/05/1965
    + Số điện thoại: 0355896611
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before Blank_x syntax with x as a number, such as: Blank_1, Blank_2.
    Output2:
    1. Tôi tên: Blank_1
    2. MSSV: Blank_2
    3. Ngành học  : Blank_3
    4. Lớp: Blank_4
    5. Ngày sinh  : Blank_5
    6. Nơi sinh: Blank_6
    7. Địa chỉ hộ khẩu thường chú: Blank_7
    8. Điện thoại: Blank_8
    9. 20: Blank_9
    10. 20  : Blank_10
    11. năm học: Blank_11
    12. Lý do: Blank_12
    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.
    - Final Result:
    Blank_1: Đoàn Thị Hoàn
    Blank_2: 21120463
    Blank_3: Trí tuệ Nhân Tạo
    Blank_4: 21TNT1
    Blank_5: 30/08/1968
    Blank_6: Rỗng
    Blank_7: Rỗng
    Blank_8: 035589611
    Blank_9: Rỗng
    Blank_10: Rỗng
    Blank_11: Rỗng
    Blank_12: Rỗng    
    <start_of_turn>user
    Chat history: {history}
    Context: {context}
    Question: {question}<end_of_turn>
    <start_of_turn>model
    """
    prompt = ChatPromptTemplate.from_template(template)
    return template, prompt


def get_output_form(res):
    output_form = re.findall(r"- Final Result:(.+)", res, re.DOTALL)[0]
    output_form = output_form.replace('<eos>','')
    return output_form

# ---------------------------- Missing Information ----------------------
def Identify_missing_info():
    template = """
    <start_of_turn>user
    Identify items with missing information in this following Form:
    Form: 
        Tờ khai căn cước công dân
    1. Họ, chữ đệm và tên(1): Lê Hữu Hưng
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Rỗng
    3. ngày, tháng, năm sinh: 01/03/2003
    4. Giới tính (Nam/nữ): Rỗng
    5. Số CMND/CCCD: Rỗng
    6. Dân tộc: Rỗng
    7. Tôn giáo: Rỗng
    8. Quốc tịch: Việt Nam
    9. Tình trạng hôn nhân: Rỗng
    10. Nhóm máu (nếu có): Rỗng
    11. Nơi đăng ký khai sinh: Rỗng
    12. Quê quán: Rỗng
    13. Nơi thường trú: KTX khu B<end_of_turn>
    <start_of_turn>model
    Items with the word 'Rỗng' after them are items that missing information.
    Result:
    1. Họ, chữ đệm và tên gọi khác (nếu có)(1)
    2. Giới tính (Nam/nữ)
    3. Số CMND/CCCD
    4. Dân tộc
    5. Tôn giáo
    6. Tình trạng hôn nhân
    7. Nhóm máu (nếu có)
    8. Nơi đăng ký khai sinh<end_of_turn>

    
    <start_of_turn>user
    Identify items with missing information in this following Form:
    Form: 
    1. Họ và tên: Nguyễn Văn C
    2. Số điện thoại: 321
    3. Email: Rỗng
    4. Bằng hiện tại: Rỗng<end_of_turn>
    <start_of_turn>model
    Items with the word 'Rỗng' after them are items that missing information.
    Result:
    1. Email
    2. Bằng hiện tại<end_of_turn>

    
    <start_of_turn>user
    Identify items with missing information in this following Form:
    Form: 
    1. Họ và tên: Lê Văn A
    2. Địa chỉ: KTX Khu B
    3. Số điện thoại: 035
    4. Email: lva@gmail.com
    5. Học vấn: sinh viên năm 2<end_of_turn>
    <start_of_turn>model
    Items with the word 'Rỗng' after them are items that miss information.
    Result:
    No item that miss information.<end_of_turn>

    <start_of_turn>user
    Tôi tên là: Lưu Tuấn Khởi
    Sinh ngày: 01/03/2003
    CCCD: Rỗng
    Nhóm máu: Rỗng
    Số điện thoại: 03884569
    Nơi ở hiện tại: KTX UFM
    Học vấn: Rỗng<end_of_turn>
    <start_of_turn>model
    1. CCCD
    2. Nhóm máu
    3. Học vấn: Rỗng<end_of_turn>


    <start_of_turn>user
    Form:
    1. Họ, chữ đệm và tên: Lê Xuân Lĩnh
    2. Ngày, tháng, năm sinh: 27/09/2003
    3. Giới tính: Nam
    4. CCCD: 25778863
    5. Số điện thoại liên hệ: 255783344
    6. Email: lxl@gmail.com
    7. Họ, chữ đệm và tên chủ hộ: Rỗng
    8. Mối quan hệ với chủ hộ: Rỗng
    9. Số định danh cá nhân của chủ hộ: Rỗng
    10. Nội dung đề nghị: Rỗng<end_of_turn>
    <start_of_turn>model
    1. Họ, chữ đệm và tên chủ hộ
    2. Mối quan hệ với chủ hộ
    3. Số định danh cá nhân của chủ hộ
    4. Nội dung đề nghị<end_of_turn>
    
    <start_of_turn>user
    Identify items with missing information in this following Form:
    Form:
    Tôi tên: Đoàn Thị D	 MSSV:	21120463
    Ngành học: Trí tuệ Nhân tạo	 Lớp: 21TNT1
    Ngày sinh: 01/03/2003	 Nơi sinh: Rỗng
    Địa chỉ hộ khẩu thường trú:	Rỗng
    Điện thoại: 035589611
    Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được được nhập học lại từ học kỳ: Rỗng năm học: 20Rỗng - 20Rỗng
    Lý do: Rỗng<end_of_turn>
    <start_of_turn>model
    Items with the word 'Rỗng' after them are items that miss information.
    Result:
    1. Nơi sinh
    2. Địa chỉ hộ khẩu thường trú
    3. 20
    4. 20
    5. Lý do<end_of_turn>


    <start_of_turn>user
    Identify items with missing information in this following Form
    Form: {output}<end_of_turn>
    <start_of_turn>model
 
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt   

def get_output_miss_info(output):
    output_form = re.findall(r"Result:(.+)", output, re.DOTALL)[0]
    miss_info= output_form.replace('<eos>','')
    pattern = r"\d+\.\s*(.*?)(?=\d+\.|\Z)"
    matches = re.findall(pattern, miss_info, re.DOTALL)
    list_items = []
    for match in matches:
        list_items.append(match.strip())
    return list_items