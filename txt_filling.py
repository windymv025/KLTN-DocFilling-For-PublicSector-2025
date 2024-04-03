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
    Context: Tôi là Nguyễn Văn A, số điện thoại là 034887774, hiện đại ở KTX UFM, số CCCD: 97785674, email: jjjjff@gmail.com
    Question:
                ĐƠN XIN VIỆC

    Kính gửi: Ban lãnh đạo cùng phòng nhân sự Công ty (Blank1)
    Tôi tên là: (Blank2)
    Sinh ngày: (Blank3)
    Chỗ ở hiện nay: (Blank4)
    Số điện thoại liên hệ: (Blank5)
    Thông qua trang website của công ty, tôi biết được Quý công ty có nhu cầu tuyển dụng vị trí (Blank6). Tôi cảm thấy trình độ và kỹ năng của mình phù hợp với vị trí này. Tôi mong muốn được làm việc và cống hiến cho công ty.

    Tôi đã tốt nghiệp loại (Blank7) tại trường (Blank8)
    Bên cạnh đó, tôi có tham gia các khóa học(Blank9)
    Ngoài ra, tôi còn sử dụng thành thạo tin học văn phòng, tiếng Anh giao tiếp tốt và biết sử dụng các phần mềm kế toán.

    Tôi thực sự mong muốn được làm việc trong môi trường chuyên nghiệp của Quý công ty. Tôi rất mong nhận được lịch hẹn phỏng vấn trong một ngày gần nhất.<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. Information is separated by commas. Information is listed below:
    + Họ và tên: Nguyễn Văn A
    + Số điện thoại(SDT): 034887774
    + Nơi ở hiện tại: KTX UFM
    + CCCD: 97785674
    + email: jjjjff@gmail.com
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before (Blankx) syntax with * as a number, such as: (Blank1), (Blank2). The items are listed below:
    1. Ban lãnh đạo cùng phòng nhân sự Công ty: (Blank1)
    2. Tôi tên là: (Blank2)
    3. Sinh ngày: (Blank3)
    4. Chỗ ở hiện nay: (Blank4)
    5. Số điện thoại liên hệ: (Blank5)
    6. vị trí: (Blank6)
    7. tốt nghiệp loại: (Blank7)
    8. tại trường: (Blank8)
    9. khóa học: (Blank9)

    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.
    Final Result:
    (Blank1): Rỗng
    (Blank2): Nguyễn Văn A
    (Blank3): Rỗng
    (Blank4): KTX UFM
    (Blank5): 034887774
    (Blank6): Rỗng
    (Blank7): Rỗng
    (Blank8): Rỗng
    (Blank9): Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CCCD là 12345.
    Question:
                TỜ KHAI CĂN CƯỚC CÔNG DÂN

                
    1. Họ, chữ đệm và tên(1): (Blank1)
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1): (Blank2)
    3. Ngày, tháng, năm sinh:(Blank3)/(Blank4)/(Blank5); 4. Giới tính (Nam/nữ): (Blank6)
    5. Số CMND/CCCD: (Blank7)
    6. Dân tộc: (Blank8); 7. Tôn giáo: (Blank9) 8. Quốc tịch: (Blank10)
    9. Tình trạng hôn nhân: (Blank11) 10. Nhóm máu (nếu có): (Blank12)
    11. Nơi đăng ký khai sinh: (Blank13)
    12. Quê quán: (Blank14)
    13. Nơi thường trú: (Blank15)
    14. Nơi ở hiện tại: (Blank16)
    15. Nghề nghiệp: (Blank17) 16. Trình độ học vấn: (Blank18)<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. Information is separated by commas. Information is listed below:
    + Họ tên: Nguyễn Đức Nam
    + Sinh viên năm 3
    + Ngày sinh: 26/02/2003
    + Dân tộc: Kinh
    + Quê: Bình Định
    + Quốc tịch: Việt Nam
    + CCCD: 12345
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before (Blankx) syntax with * as a number, such as: (Blank1), (Blank2). The items are listed below:
    1. Họ, chữ đệm và tên(1): (Blank1)
    2. Họ, chữ đệm và tên gọi khác (nếu có)(2): (Blank2)
    3. Ngày sinh: (Blank3)
    4. Tháng sinh: (Blank4)
    5. Năm sinh: (Blank5)
    6. Giới tính (Nam/nữ): (Blank6)
    7. Số CMND/CCCD: (Blank7)
    8. Dân tộc: (Blank8)
    9. Tôn giáo: (Blank9)
    10. Quốc tịch: (Blank10)
    11. Tình trạng hôn nhân: (Blank11)
    12. Nhóm máu (nếu có): (Blank12)
    13. Nơi đăng ký khai sinh: (Blank13)
    14. Quê quán: (Blank14)
    15. Nơi thường trú: (Blank15)
    16. Nơi ở hiện tại: (Blank16)
    17. Nghề nghiệp: (Blank17)
    18. Trình độ học vấn: (Blank18)

    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.
    Final Result:
    (Blank1): Nguyễn Đức Nam
    (Blank2): Rỗng
    (Blank3): 26
    (Blank4): 02
    (Blank5): 2003
    (Blank6): Rỗng
    (Blank7): 12345
    (Blank8): Kinh
    (Blank9): Rỗng
    (Blank10): Việt Nam
    (Blank11): Rỗng 
    (Blank12): Rỗng
    (Blank13): Rỗng
    (Blank14): Bình Định
    (Blank15): Rỗng
    (Blank16): Rỗng
    (Blank17): Rỗng
    (Blank18): Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Họ và tên: Lê Hữu Hưng, giới tính nam, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai, số CCCD là 12345, đang sống tại KTX B, email: lhh@gmail.com.
    Question:
            ĐƠN XIN CẤP LẠI CCCD
    
    Tôi là: (Blank1) Quốc tịch: (Blank2)
    Sinh ngày: (Blank3) tháng (Blank4) năm (Blank5)
    Nơi đăng ký hộ khẩu thường trú: (Blank6)
    Nơi cư trú: (Blank7)
    Điện thoại: (Blank8)
    Số CCCD (hoặc hộ chiếu): (Blank9)
    Cấp ngày: (Blank10) tháng (Blank11) năm (Blank12) Nơi cấp: (Blank13)<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. Information is separated by commas. Information is listed below:
    + Họ tên: Lê Hữu Hưng
    + Giới tính: Nam
    + Sinh ngày: 01/03/2003
    + Quê quán: Gia Lai
    + Quốc Tịch: Việt Nam
    + CMND: 12345
    + Hiện tại đang sống ở KTX khu B.
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before (Blankx) syntax with * as a number, such as: (Blank1), (Blank2). The items are listed below: 
    1. Tôi là: (Blank1)
    2. Quốc tịch: (Blank2)
    3. Sinh ngày   : (Blank3)
    4. tháng     : (Blank4)
    5. năm: (Blank5)
    6. Nơi đăng ký hộ khẩu thường trú: (Blank6)
    7. Nơi cư trú: (Blank7)
    8. Điện thoại: (Blank8)
    9. Số CCCD (hoặc hộ chiếu): (Blank9)
    10. Cấp ngày   : (Blank10)
    11. tháng  : (Blank11)
    12. năm  : (Blank12)
    13. Nơi cấp: (Blank13)

    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.
    Final Result:
    (Blank1): Lê Hữu Hưng
    (Blank2): Việt Nam
    (Blank3): 01
    (Blank4): 03
    (Blank5): 2003
    (Blank6): Rỗng
    (Blank7): KTX Khu B
    (Blank8): Rỗng
    (Blank9): 12345
    (Blank10): Rỗng
    (Blank11): Rỗng
    (Blank12): Rỗng
    (Blank13): Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Tôi tên Đoàn Thị Hoàn, MSSV: 21120463, học lớp 21TNT1, ngành Trí tuệ Nhân tạo. Tôi sinh ngày 19/05/1965, số điện thoại là 035589611.
    Question:
            ĐƠN XIN NGHỈ HỌC

    Tôi tên: (Blank1)	 MSSV:	(Blank2)
    Ngành học: (Blank3)	 Lớp: 	(Blank4)
    Ngày sinh: (Blank5) 	 Nơi sinh: (Blank6)	
    Địa chỉ hộ khẩu thường trú:	(Blank7)
    Điện thoại: (Blank8)
    Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được thôi học từ học kỳ: (Blank9) năm học: 20(Blank10) – 20(Blank11)
    Lý do: (Blank12)
    Trong khi chờ đợi sự chấp thuận của nhà trường, tôi xin chân thành cảm ơn.<end_of_turn>
    <start_of_turn>model
    Extract information from the Context. Information is separated by commas. Information is listed below:
    + Họ tên: Đoàn Thị Hoàn
    + MSSV: 21120463
    + Lớp: 21TNT1
    + Ngành: Trí tuệ Nhân tạo
    + Ngành sinh: 19/05/1965
    + Số điện thoại: 0355896611
    List the items that need to be filled in in the Question. The item that needs to be filled in is the part before (Blankx) syntax with x as a number, such as: (Blank1), (Blank2). The items are listed below:
    1. Tôi tên: (Blank1)
    2. MSSV: (Blank2)
    3. Ngành học  : (Blank3)
    4. Lớp: (Blank4)
    5. Ngày sinh  : (Blank5)
    6. Nơi sinh: (Blank6)
    7. Địa chỉ hộ khẩu thường chú: (Blank7)
    8. Điện thoại: (Blank8)
    9. 20: (Blank9)
    10. 20  : (Blank10)
    11. năm học: (Blank11)
    12. Lý do: (Blank12)

    Check the information that needs to be filled in the Question in the information extracted from the Context. If so, write that information in. If not, fill in 'Rỗng'.:
    (Blank1): Đoàn Thị Hoàn
    (Blank2): 21120463
    (Blank3): Trí tuệ Nhân Tạo
    (Blank4): 21TNT1
    (Blank5): 30/08/1968
    (Blank6): Rỗng
    (Blank7): Rỗng
    (Blank8): 035589611
    (Blank9): Rỗng
    (Blank10): Rỗng
    (Blank11): Rỗng
    (Blank12): Rỗng    
    <start_of_turn>user
    Chat history: {history}
    Context: {context}
    Question: {question}<end_of_turn>
    <start_of_turn>model
    """
    prompt = ChatPromptTemplate.from_template(template)
    return template, prompt


def get_output_form(res):
    try:
        output_form = re.findall(r"Final Result:(.+)", res, re.DOTALL)[0]
    except:
        output_form = re.findall(r"\*\*Final Result:\*\*(.+)", res, re.DOTALL)[0]
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