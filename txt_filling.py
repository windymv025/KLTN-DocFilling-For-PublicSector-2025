from langchain.prompts import ChatPromptTemplate
import re
import chromadb

# -------------------------- prompt cho điền file .txt, đã triển khai theo cấu trúc CoT ------------------------------------
def txt_prompt():
    template = """
    <start_of_turn>user
    Context: Tôi tên là Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai , quốc tịch Việt Nam, số CMND là 12345.
    Question:
    '''
    ĐƠN XIN VIỆC

    Kính gửi: Ban lãnh đạo cùng phòng nhân sự Công ty ...................................................

    Tôi tên là: ......................................................................................................................

    Sinh ngày: ....................................................................................................................

    Chỗ ở hiện nay: ............................................................................................................

    Số điện thoại liên hệ: ...................................................................................................

    Thông qua trang website của công ty, tôi biết được Quý công ty có nhu cầu tuyển dụng vị trí ……….. Tôi cảm thấy trình độ và kỹ năng của mình phù hợp với vị trí này. Tôi mong muốn được làm việc và cống hiến cho công ty.

    Tôi đã tốt nghiệp loại …… tại trường ......................................................................
    Ngoài ra, tôi còn sử dụng thành thạo tin học văn phòng, tiếng Anh giao tiếp tốt và biết sử dụng các phần mềm kế toán.
    
    Tôi thực sự mong muốn được làm việc trong môi trường chuyên nghiệp của Quý công ty. Tôi rất mong nhận được lịch hẹn phỏng vấn trong một ngày gần nhất.
    '''<end_of_turn>
    <start_of_turn>model
    Extract information separated by , in the Context section.
    Result:
    + Họ tên: Lê Hữu Hưng
    + Sinh viên năm 3
    + Giới tính: Nam
    + Sinh ngày: 01/03/2003
    + Quê quán: Gia Lai
    + Quốc Tịch: Việt Nam
    + CMND: 12345
    List the items that need to be filled in in the Question section (the item that needs to be filled in is the part before '.......' or the sign ':').
    Require: Keep the correct structure in the Question section, do not arbitrarily break the line.
    Result:
    1. Ban lãnh đạo cùng phòng nhân sự Công ty
    2. Tôi tên là
    3. Sinh ngày
    4. Chỗ ở hiện nay
    5. Số điện thoại liên hệ
    6. vị trí
    7. tốt nghiệp loại
    8. tại trường
    
    We will proceed to fill in the information available in the context section into the fields that need to be filled in the Question section. 
    If there is no information, fill in 'Rỗng'.
    - Final Result:
    ĐƠN XIN VIỆC

    Kính gửi: Ban lãnh đạo cùng phòng nhân sự Công ty Rỗng

    Tôi tên là: Lê Hữu Hưng

    Sinh ngày: 01/03/2003

    Chỗ ở hiện nay: .KTX Khu B

    Số điện thoại liên hệ: Rỗng

    Thông qua trang website của công ty, tôi biết được Quý công ty có nhu cầu tuyển dụng vị trí Rỗng. Tôi cảm thấy trình độ và kỹ năng của mình phù hợp với vị trí này. Tôi mong muốn được làm việc và cống hiến cho công ty.

    Tôi đã tốt nghiệp loại Rỗng tại trường Rỗng
    Ngoài ra, tôi còn sử dụng thành thạo tin học văn phòng, tiếng Anh giao tiếp tốt và biết sử dụng các phần mềm kế toán.

    Tôi thực sự mong muốn được làm việc trong môi trường chuyên nghiệp của Quý công ty. Tôi rất mong nhận được lịch hẹn phỏng vấn trong một ngày gần nhất.<end_of_turn>

    
    <start_of_turn>user
    Context: Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.
    Question:
    '''
    1. Họ, chữ đệm và tên(1):……………………..…………………………..……………………………………………………………..………………… ……..
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1):………………………………………………………………………..…..……………
    3. Ngày, tháng, năm sinh:…….……./…….……./……………….; 4. Giới tính (Nam/nữ):…………....…………..
    5. Số CMND/CCCD: ..................................................................
    6. Dân tộc:…………………….……; 7. Tôn giáo:…………………….……… 8. Quốc tịch: ………………………….………
    9. Tình trạng hôn nhân:……………………………..………… 10. Nhóm máu (nếu có):………………………………
    11. Nơi đăng ký khai sinh:………………………………………………… ………………………………………………………………
    12. Quê quán: ………………………………………………………………………………………………………………………………..………
    13. Nơi thường trú:……………………………… …………………………………………………………………………………..………………
    …………………………………………………………………………………………………………………………………………………………………………………………………………….
    14. Nơi ở hiện tại:……………………………… ………………………………………………………….………………………
    …………………………………………………………………………………………………………………………………………………………………………………………………………….
    15. Nghề nghiệp:………………………………… 16. Trình độ học vấn:……………………………………………….………
    '''<end_of_turn>
    <start_of_turn>model
    Extract information separated by , in the Context section.
    Output:
    + Họ tên: Nguyễn Đức Nam
    + Sinh viên năm 3
    + Ngày sinh: 26/02/2003
    + Dân tộc: Kinh
    + Quê: Bình Định
    + Quốc tịch: Việt Nam
    + CMND/CCCD: 12345
    List the items that need to be filled in in the Question section (the item that needs to be filled in is the part before the sign ':' or '.......').
    Output:
    1. Họ, chữ đệm và tên(1)
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1)
    3. Ngày, tháng, năm sinh
    4. Giới tính (Nam/nữ)
    5. Số CMND/CCCD
    6. Dân tộc
    7. Tôn giáo
    8. Quốc tịch
    9. Tình trạng hôn nhân
    10. Nhóm máu (nếu có)
    11. Nơi đăng ký khai sinh
    12. Quê quán
    13. Nơi thường trú
    14. Nơi ở hiện tại
    15. Nghề nghiệp
    16. Trình độ học vấn

    We will proceed to fill in the information available in the context section into the fields that need to be filled in the Question section. 
    If there is no information, fill in 'Rỗng'.
    - Final Result:
    1. Họ, chữ đệm và tên(1): Nguyễn Đức Nam
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không có
    3. Ngày, tháng, năm sinh: 26/02/2003; 4. Giới tính (Nam/nữ): Rỗng
    5. Số CMND/CCCD: 12345
    6. Dân tộc: Kinh;  7. Tôn giáo: Không  8. Quốc tịch: Việt Nam
    9. Tình trạng hôn nhân: Rỗng    10. Nhóm máu (nếu có): Rỗng
    11. Nơi đăng ký khai sinh: Rỗng
    12. Quê quán: Rỗng
    13. Nơi thường trú: Rỗng
    14. Nơi ở hiện tại: Rỗng
    15. Nghề nghiệp: Rỗng 16. Trình độ học vấn: Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Họ và tên: Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CCCD là 12345, đang sống tại KTX B.
    Question:
    ''' 
    Tôi là:......................................................................... Quốc tịch: ......................
    Sinh ngày:........................tháng ..........................năm .......................................
    Nơi đăng ký hộ khẩu thường trú:........................................................................
    Nơi cư trú:...........................................................................................................
    Điện thoại: ............................................
    Số CCCD (hoặc hộ chiếu): .........................................................
    Cấp ngày:.......... tháng........... năm............... Nơi cấp:......................................
    '''<end_of_turn>

    <start_of_turn>model
    Extract information separated by , in the Context section.
    Output:
    + Họ tên: Lê Hữu Hưng
    + Sinh viên năm 3
    + Giới tính: Nam
    + Sinh ngày: 01/03/2003
    + Quê quán: Gia Lai
    + Quốc Tịch: Việt Nam
    + CMND: 12345
    + Hiện tại đang ở KTX khu B.
    List the items that need to be filled in in the Question section (the item that needs to be filled in is the part before the sign ':' or '.......').
    Output:
    1. Tôi là
    2. Quốc tịch
    3. Sinh ngày   
    4. tháng     
    5. năm
    6. Nơi đăng ký hộ khẩu thường trú:
    7. Nơi cư trú
    8. Điện thoại
    9. Số CCCD (hoặc hộ chiếu)
    10. Cấp ngày:   
    11. tháng  
    12. năm  
    13. Nơi cấp:

    We will proceed to fill in the information available in the context section into the fields that need to be filled in the Question section. 
    If there is no information, fill in 'Rỗng'.
    - Final Result:
    Tôi là: Lê Hữu Hưng Quốc tịch: Việt Nam
    Sinh ngày: 01 tháng 03 năm 2003
    Nơi đăng ký hộ khẩu thường trú: Rỗng
    Nơi cư trú: KTX B
    Điện thoại: Rỗng
    Số CCCD (hoặc hộ chiếu): 12345
    Cấp ngày: Rỗng tháng Rỗng năm Rỗng Nơi cấp: Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Họ tên của tôi Lê Văn A, giới tính Nam, sinh viên năm 2, sinh ngày 26/04/2007, dân tộc Kinh, quê ở Bình Định, số điện thoại 035, quốc tịch Việt Nam, số CMND là 152255.
    Question:
    ''' Điền thông tin vào form sau, chưa có thông tin thì giữ nguyên:
    1. Họ và tên: ..........................
    2. Địa chỉ: ..........................
    3. Số điện thoại: ..........................
    4. Email: ..........................
    5. Học vấn: ..........................
    '''
    <end_of_turn>
    <start_of_turn>model
    Extract information separated by , in the Context section.
    Output:
    + Họ tên: Lê Văn A
    + Giới tính: Nam
    + Sinh viên năm 2
    + Ngày sinh: 26/04/2007
    + Số điện thoại: 035
    + Quốc tịch: Việt Nam
    + CMND/CCCD: 152255
    List the items that need to be filled in in the Question section (the item that needs to be filled in is the part before the sign ':' or '.......').
    Output:
    1. Họ và tên
    2. Địa chỉ
    3. Số điện thoại
    4. Email
    5. Học vấn
    We will proceed to fill in the information available in the context section into the fields that need to be filled in the Question section. 
    If there is no information, fill in 'Rỗng'.

    - Final Result:
    1. Họ và tên: Lê Văn A
    2. Địa chỉ: Rỗng
    3. Số điện thoại: 035
    4. Email: Rỗng
    5. Học vấn: sinh viên năm 2<end_of_turn>

    <start_of_turn>user
    Context: Tôi tên Nguyễn Văn C, số điện thoại 321, hiện tại đang ở KTX khu B.
    Question:
    '''
    1. Họ và tên: ..........................
    2. Số điện thoại: ..........................
    3. Email: ..........................
    4. Bằng hiện tại: ..........................
    5. Cấp độ học: ..........................
    '''<end_of_turn>
    <start_of_turn>model
    Extract information separated by , in the Context section.
    Output:
    + Họ và tên: Nguyễn Văn C
    + Số điện thoại: 321
    + Nơi ở hiện tại: KTX B
    List the items that need to be filled in in the Question section (the item that needs to be filled in is the part before the sign ':' or '.......').
    Output:
    1. Họ và tên
    2. Số điện thoại
    3. Email
    4. Bằng hiện tại

    We will proceed to fill in the information available in the context section into the fields that need to be filled in the Question section. 
    If there is no information, fill in 'Rỗng'.

    - Final Result:
    1. Họ và tên: Nguyễn Văn C
    2. Số điện thoại: 321
    3. Email: Rỗng
    4. Bằng hiện tại: Rỗng<end_of_turn>

    <start_of_turn>user
    Context: Tôi tên Đoàn Thị D, MSSV: 21120463, học lớp 21TNT1, ngành Trí tuệ Nhân tạo. Tôi sinh ngày 01/03/2003, số điện thoại là 035589611.
    Question:
    '''
    Tôi tên:	 MSSV:	
    Ngành học:	 Lớp: 	
    Ngày sinh: 	 Nơi sinh: 	
    Địa chỉ hộ khẩu thường trú:	
    Điện thoại: 	
    Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được được nhập học lại từ học kỳ: .......... năm học: 20...... - 20......
    Lý do: 	
    '''<end_of_turn>
    <start_of_turn>model
    Extract information separated by , in the Context section.
    Output:
    + Họ tên: Đoàn Thị D
    + MSSV: 21120463
    + Lớp: 21TNT1
    + Ngành: Trí tuệ Nhân tạo
    + Ngành sinh: 01/03/2003
    + Số điện thoại: 0355896611
    List the items that need to be filled in in the Question section (the item that needs to be filled in is the part before the sign ':' or '.......').
    Output:
    1. Tôi tên:   
    2. MSSV
    3. Ngành học  
    4. Lớp
    5. Ngày sinh  
    6. Nơi sinh
    7. Địa chỉ hộ khẩu thường chú
    8. Điện thoại
    9. học kỳ   
    10. năm học
    11. Lý do

    We will proceed to fill in the information available in the context section into the fields that need to be filled in the Question section. 
    If there is no information, fill in 'Rỗng'.

    - Final Result:
    Tôi tên: Đoàn Thị D	 MSSV:	21120463
    Ngành học: Trí tuệ Nhân tạo	 Lớp: 21TNT1
    Ngày sinh: 01/03/2003	 Nơi sinh: Rỗng
    Địa chỉ hộ khẩu thường trú:	Rỗng
    Điện thoại: 035589611
    Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được được nhập học lại từ học kỳ: Rỗng năm học: 20Rỗng - 20Rỗng
    Lý do: Rỗng<end_of_turn>

    
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
    2. Địa chỉ: Rỗng
    3. Số điện thoại: 035
    4. Email: lva@gmail.com
    5. Học vấn: sinh viên năm 2<end_of_turn>
    <start_of_turn>model
    Items with the word 'Rỗng' after them are items that miss information.
    Result:
    No item that miss information.<end_of_turn>

    
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
    5. Lý do 
    <end_of_turn>


    <start_of_turn>user
    Identify items with missing information in this following Form
    Form: {output}<end_of_turn>
    <start_of_turn>model
 
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt   

def get_output_miss_info(output):
    output_form = re.findall(r"Result:(.+)", output, re.DOTALL)[0]
    output_form = output_form.replace('<eos>','')
    return output_form

# # ---------------------------- Database -----------------------------
# # in disk client
# client = chromadb.PersistentClient(path="./vectorstore")
# collection = client.get_or_create_collection(name="my_programming_collection")



