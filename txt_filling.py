from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import GooglePalmEmbeddings
from langchain.docstore.document import Document
import os
import shutil
import re

# prompt cho điền file .txt, đã triển khai theo cấu trúc CoT
def txt_prompt():
    template = """ Dựa vào context cung cấp, trích xuất từng thông tin theo mục có trong Question và điền vào form tương ứng, nếu không có thông tin thì để là Rỗng.:
    <Instruction>
    Đầu tiên xác định các mục cần phải điền vào từ Question, sau đó ứng với mỗi mục, tìm thông tin từ Context và điền vào form.
    </Instruction>
    <start_of_turn>user
    Context: Tôi tên là Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CMND là 12345.
    Question:
    ''' Điền thông tin vào form sau, chưa có thông tin thì giữ nguyên:
    1. Họ, chữ đệm và tên(1):……………………..…………………………..……………………………………………………………..………………… ……..
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1):………………………………………………………………………..…..……………
    3. Ngày, tháng, năm sinh:…….……./…….……./……………….; 4. Giới tính (Nam/nữ):…………....…………..
    5. Số CMND/CCCD: 12345
    6. Dân tộc:…………………….……; 7. Tôn giáo:…………………….……… 8. Quốc tịch: ………………………….………
    9. Tình trạng hôn nhân:……………………………..………… 10. Nhóm máu (nếu có):………………………………
    11. Nơi đăng ký khai sinh:………………………………………………… ………………………………………………………………
    12. Quê quán: ………………………………………………………………………………………………………………………………..………
    13. Nơi thường trú:……………………………… …………………………………………………………………………………..………………
    '''
    <end_of_turn>
    <start_of_turn>model
    - Liệt kê thông tin hiện có trong context:
    + Họ tên: Lê Hữu Hưng
    + Sinh viên năm 3
    + Giới tính: Nam
    + Sinh ngày: 01/03/2003
    + Quê quán: Gia Lai
    + Quốc Tịch: Việt Nam
    + CMND: 12345
    - Liệt kê các mục cần điền trong form:
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
    
    - Ta sẽ tiến hành điền những thông tin hiện có trong context vào những mục cần điền trong form, nếu không có thông tin thì điền Rỗng.
    Kết quả điền vào form:
    1. Họ, chữ đệm và tên(1): Lê Hữu Hưng
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không có
    3. Ngày, tháng, năm sinh: 01/03/2003; 4. Giới tính (Nam/nữ): Nam
    5. Số CMND/CCCD: 12345
    6. Dân tộc: Kinh; 7. Tôn giáo: Không 8. Quốc tịch: Việt Nam
    9. Tình trạng hôn nhân: Rỗng 10. Nhóm máu (nếu có): Rỗng
    11. Nơi đăng ký khai sinh: Rỗng
    12. Quê quán: Rỗng
    13. Nơi thường trú: Rỗng
    <end_of_turn>

    <start_of_turn>user
    Context: Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.
    Question:
    ''' Điền thông tin vào form sau, chưa có thông tin thì giữ nguyên:
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
    '''
    <end_of_turn>
    <start_of_turn>model
    - Liệt kê thông tin hiện có trong context:
    + Họ tên: Nguyễn Đức Nam
    + Sinh viên năm 3
    + Ngày sinh: 26/02/2003
    + Dân tộc: Kinh
    + Quê: Bình Định
    + Quốc tịch: Việt Nam
    + CMND/CCCD: 12345
    Liệt kê các mục cần điền trong form:
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

    - Ta sẽ tiến hành điền những thông tin hiện có trong context vào những mục cần điền trong form, nếu không có thông tin thì điền Rỗng. 
    Kết quả điền vào form:
    1. Họ, chữ đệm và tên(1): Nguyễn Đức Nam
    2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không có
    3. Ngày, tháng, năm sinh: 26/02/2003; 4. Giới tính (Nam/nữ): Rỗng
    5. Số CMND/CCCD: 12345
    6. Dân tộc: Kinh; 7. Tôn giáo: Không 8. Quốc tịch: Việt Nam
    9. Tình trạng hôn nhân: Rỗng 10. Nhóm máu (nếu có): Rỗng
    11. Nơi đăng ký khai sinh: Rỗng
    12. Quê quán: Rỗng
    13. Nơi thường trú: Rỗng
    14. Nơi ở hiện tại: Rỗng
    15. Nghề nghiệp: Rỗng 16. Trình độ học vấn: Rỗng
    <end_of_turn>

    <start_of_turn>user
    Context: Họ và tên: Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CCCD là 12345, đang sống tại KTX B.
    Question:
    ''' Điền thông tin vào form sau, chưa có thông tin thì giữ nguyên:
    Tôi là:......................................................................... Quốc tịch: ......................
    Sinh ngày:........................tháng ..........................năm .......................................
    Nơi đăng ký hộ khẩu thường trú:........................................................................
    Nơi cư trú:...........................................................................................................
    Điện thoại: ............................................
    Số CCCD (hoặc hộ chiếu): .........................................................
    Cấp ngày:.......... tháng........... năm............... Nơi cấp:......................................
    '''
    <end_of_turn>

    <start_of_turn>model
    - Liệt kê thông tin hiện có trong context:
    + Họ tên: Lê Hữu Hưng
    + Sinh viên năm 3
    + Giới tính: Nam
    + Sinh ngày: 01/03/2003
    + Quê quán: Gia Lai
    + Quốc Tịch: Việt Nam
    + CMND: 12345
    + Hiện tại đang ở KTX khu B.
    - Liệt kê các mục cần điền trong form:
    1. Tôi là
    2. Quốc tịch
    3. Sinh ngày   4. tháng     5. năm
    6. Nơi đăng ký hộ khẩu thường trú:
    7. Nơi cư trú
    8. Điện thoại
    9. Số CCCD (hoặc hộ chiếu)
    10. Cấp ngày:   11. tháng  12. năm  13. Nơi cấp:

    - Ta sẽ tiến hành điền những thông tin hiện có trong context vào những mục cần điền trong form, nếu không có thông tin thì điền Rỗng. 
    Kết quả điền vào form:
    Tôi là: Lê Hữu Hưng Quốc tịch: Việt Nam
    Sinh ngày: 01 tháng 03 năm 2003
    Nơi đăng ký hộ khẩu thường trú: Rỗng
    Nơi cư trú: KTX B
    Điện thoại: Rỗng
    Số CCCD (hoặc hộ chiếu): 12345
    Cấp ngày: Rỗng tháng Rỗng năm Rỗng Nơi cấp: Rỗng
    <end_of_turn>

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
    - Liệt kê thông tin hiện có trong context:
    + Họ tên: Lê Văn A
    + Giới tính: Nam
    + Sinh viên năm 2
    + Ngày sinh: 26/04/2007
    + Số điện thoại: 035
    + Quốc tịch: Việt Nam
    + CMND/CCCD: 152255
    - Liệt kê các mục cần điền trong form:
    1. Họ và tên
    2. Địa chỉ
    3. Số điện thoại
    4. Email
    5. Học vấn
    Ta sẽ tiến hành điền những thông tin hiện có trong context vào những mục cần điền trong form, nếu không có thông tin thì điền Rỗng.
    - Kết quả điền vào form:
    1. Họ và tên: Lê Văn A
    2. Địa chỉ: Rỗng
    3. Số điện thoại: 035
    4. Email: Rỗng
    5. Học vấn: sinh viên năm 2
    <end_of_turn>

    <start_of_turn>user
    Context: Tôi tên Nguyễn Văn C, số điện thoại 321, hiện tại đang ở KTX khu B.
    Question:
    ''' Điền thông tin vào form sau, chưa có thông tin thì giữ nguyên:
    1. Họ và tên: ..........................
    2. Số điện thoại: ..........................
    3. Email: ..........................
    4. Bằng hiện tại: ..........................
    5. Cấp độ học: ..........................
    '''
    <end_of_turn>
    <start_of_turn>model
    - Liệt kê thông tin hiện có trong context:
    + Họ và tên: Nguyễn Văn C
    + Số điện thoại: 321
    + Nơi ở hiện tại: KTX B
    - Liệt kê các mục cần điền trong form:
    1. Họ và tên
    2. Số điện thoại
    3. Email
    4. Bằng hiện tại

    - Ta sẽ tiến hành điền những thông tin hiện có trong context vào những mục cần điền trong form, nếu không có thông tin thì điền Rỗng.
    Kết quả điền vào form:
    1. Họ và tên: Nguyễn Văn C
    2. Số điện thoại: 321
    3. Email: Rỗng
    4. Bằng hiện tại: Rỗng
    <end_of_turn>

    <start_of_turn>user
    Context: Tôi tên Đoàn Thị D, MSSV: 21120463, học lớp 21TNT1, ngành Trí tuệ Nhân tạo. Tôi sinh ngày 01/03/2003, số điện thoại là 035589611.
    Question:
    ''' Điền thông tin vào form sau, điền vào sau dấu :
    Tôi tên:	 MSSV:	
    Ngành học:	 Lớp: 	
    Ngày sinh: 	 Nơi sinh: 	
    Địa chỉ hộ khẩu thường trú:	
    Điện thoại: 	
    Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được được nhập học lại từ học kỳ: .......... năm học: 20...... - 20......
    Lý do: 	
    '''
    <end_of_turn>
    <start_of_turn>model
    - Liệt kê thông tin hiện có trong context:
    + Họ tên: Đoàn Thị D
    + MSSV: 21120463
    + Lớp: 21TNT1
    + Ngành: Trí tuệ Nhân tạo
    + Ngành sinh: 01/03/2003
    + Số điện thoại: 0355896611
    - Liệt kê các mục cần điền trong form:
    1. Tôi tên:   2. MSSV
    3. Ngành học  4. Lớp
    5. Ngày sinh  6. Nơi sinh
    7. Địa chỉ hộ khẩu thường chú
    8. Điện thoại
    9. học kỳ   10. năm học
    11. Lý do

    - Ta sẽ tiến hành điền những thông tin hiện có trong context vào những mục cần điền trong form, nếu không có thông tin thì điền Rỗng.
    Kết quả điền vào form:
    Tôi tên: Lê Hữu Hưng	 MSSV:	21120463
    Ngành học: Trí tuệ Nhân tạo	 Lớp: 21TNT1
    Ngày sinh: 01/03/2003	 Nơi sinh: Rỗng
    Địa chỉ hộ khẩu thường trú:	Rỗng
    Điện thoại: 035589611
    Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được được nhập học lại từ học kỳ: Rỗng năm học: 20Rỗng - 20Rỗng
    Lý do: Rỗng
    <end_of_turn>


    <start_of_turn>user
    Chat history: {history}
    Context: {context}
    Question: {question}
    <end_of_turn>
    <start_of_turn>model
    """
    prompt = ChatPromptTemplate.from_template(template)
    return template, prompt

def get_answer(template, result):
    start = len(template.split('\n')) - 4
    text = ('\n').join(result.split('\n')[start:])
    answer = re.findall(r"- Kết quả điền vào form:(.+)", text, re.DOTALL)[0]
    return answer


