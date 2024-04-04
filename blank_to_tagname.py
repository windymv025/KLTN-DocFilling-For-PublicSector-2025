import google.generativeai as genai
import re
from extract_context import *
from uniform_text import *

 
genai.configure(api_key="AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50")
 
# Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4096,
}
 
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]
 
model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

##=========================promp=========================##
# Root prompt
# prompt_parts = [
# '''
# Your task is to extract model names from machine learning paper abstracts. Your response is an array of the model names in the format [\"model_name\"]. If you don't find model names in the abstract or you are not sure, return [\"NA\"]
# Abstract: Large Language Models (LLMs), such as ChatGPT and GPT-4, have revolutionized natural language processing research and demonstrated potential in Artificial General Intelligence (AGI). However, the expensive training and deployment of LLMs present challenges to transparent and open academic research. To address these issues, this project open-sources the Chinese LLaMA and Alpaca…
# ''']

# Abstract = "Tôi tên Văn A, số điện thoại 321, đang mong muốn học bằng lái xe A2, hiện tại đang ở KTX khu B."
# Abstract = """
# TỜ KHAI CĂN CƯỚC CÔNG DÂN
# 1. Họ, chữ đệm và tên(1): Hồ Quý Phi
# 2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Kang
# 3. Ngày, tháng, năm sinh:27/01/2003; 4. Giới tính (Nam/nữ): Nữ
# 5. Số CMND/CCCD: 547
# 6. Dân tộc:Hoa; 7. Tôn giáo:Phật 8. Quốc tịch: Anh
# 9. Tình trạng hôn nhân: Kết hôn 10. Nhóm máu (nếu có): B
# 11. Nơi đăng ký khai sinh: USA
# 12. Quê quán: Bình Định
# 13. Nơi thường trú: Singapore
# """

# Abstract = """
# TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ
# I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
# [01]. Họ và tên (viết chữ in hoa): (Blank1)	[02]. Giới tính: (Blank2)
# [03]. Ngày, tháng, năm sinh: (Blank3)/(Blank4)/(Blank5)	  [04]. Quốc tịch: (Blank6)
# [05]. Dân tộc: (Blank7)	[06]. Số CCCD/ĐDCN/Hộ chiếu: (Blank8)	
# [07]. Điện thoại: (Blank9)	[08]. Email (nếu có): (Blank10)	
# [09]. Nơi đăng ký khai sinh: (Blank11) [09.1]. Xã: (Blank12)	[09.2]. Huyện: (Blank13) [09.3]. Tỉnh: (Blank14)
# [10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): (Blank15)
# [11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: (Blank16)
# [12]. Số nhà, đường/phố, thôn/xóm: (Blank17)	
# [13]. Xã: (Blank18)	[14]	Huyện: (Blank19)	[15]. Tỉnh: (Blank20) 	
# [16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
# """

# Abstract = """
# Mẫu số 16:  Ban hành kèm theo Thông tư số 28/2015/TT-BLĐTBXH ngày 31 tháng 7 năm 2015 của Bộ trưởng Bộ Lao động-Thương binh và Xã hội
# 			CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
# 			    Độc lập - Tự do - Hạnh phúc

# THÔNG BÁO VỀ VIỆC TÌM KIẾM VIỆC LÀM
# Tháng hưởng trợ cấp thất nghiệp thứ: (Blank1)

# Kính gửi:  Trung tâm Dịch vụ việc làm (Blank2)
# Tên tôi là: (Blank3)sinh ngày (Blank4) / (Blank5) / (Blank6)
# Số chứng minh nhân dân: (Blank7)
# Ngày cấp: (Blank8)/(Blank9)/(Blank10) nơi cấp: (Blank11)
# Chỗ ở hiện nay: (Blank12)
# Số điện thoại :(Blank13)
# Theo Quyết định số(Blank14) ngày(Blank15)/(Blank16)/(Blank17) tôi được hưởng trợ cấp thất nghiệp(Blank18)tháng, kể từ ngày(Blank19)/(Blank20)/(Blank21) đến ngày(Blank22)/(Blank23)/(Blank24) tại tỉnh/thành phố(Blank25)
# Tôi thông báo kết quả tìm kiếm việc làm theo quy định, cụ thể như sau:
# (1) Đơn vị thứ nhất (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
# (Blank26)
# (2) Đơn vị thứ hai (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
# (Blank27)
#  ((Blank28)) Tên đơn vị thứ ((Blank29)): (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
# (Blank30)
# Tình trạng việc làm hiện nay: (Blank31)
# """

# Abstract = """TỜ KHAI CĂN CƯỚC CÔNG DÂN           
#     1. Họ, chữ đệm và tên(1): (Blank1)
#     2. Họ, chữ đệm và tên gọi khác (nếu có)(1): (Blank2)
#     3. Ngày, tháng, năm sinh:(Blank3)/(Blank4)/(Blank5); 4. Giới tính (Nam/nữ): (Blank6)
#     5. Số CMND/CCCD: (Blank7)
#     6. Dân tộc: (Blank8); 7. Tôn giáo: (Blank9) 8. Quốc tịch: (Blank10)
#     9. Tình trạng hôn nhân: (Blank11) 10. Nhóm máu (nếu có): (Blank12)
#     11. Nơi đăng ký khai sinh: (Blank13)
#     12. Quê quán: (Blank14)
#     13. Nơi thường trú: (Blank15)
#     14. Nơi ở hiện tại: (Blank16)
#     15. Nghề nghiệp: (Blank17) 16. Trình độ học vấn: (Blank18)"""

Abstract = """
TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ
I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): (Blank1)	[02]. Giới tính: (Blank2)
[03]. Ngày, tháng, năm sinh: (Blank3)/(Blank4)/(Blank5)	  [04]. Quốc tịch: (Blank6)
[05]. Dân tộc: (Blank7)	[06]. Số CCCD/ĐDCN/Hộ chiếu: (Blank8)	
[07]. Điện thoại: (Blank9)	[08]. Email (nếu có): (Blank10)	
[09]. Nơi đăng ký khai sinh: [09.1]. Xã: (Blank11)	[09.2]. Huyện: (Blank12) [09.3]. Tỉnh: (Blank13)
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): (Blank14)
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: (Blank15)
[12]. Số nhà, đường/phố, thôn/xóm: (Blank16)	
[13]. Xã: (Blank17)	[14]	Huyện: (Blank18)	[15]. Tỉnh: (Blank19) 	
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
"""

# Abstract = """
# Mẫu số 16:  Ban hành kèm theo Thông tư số 28/2015/TT-BLĐTBXH ngày 31 tháng 7 năm 2015 của Bộ trưởng Bộ Lao động-Thương binh và Xã hội
# 			CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
# 			    Độc lập - Tự do - Hạnh phúc

# THÔNG BÁO VỀ VIỆC TÌM KIẾM VIỆC LÀM
# Tháng hưởng trợ cấp thất nghiệp thứ: (Blank1)

# Kính gửi:  Trung tâm Dịch vụ việc làm (Blank2)
# Tên tôi là: (Blank3)sinh ngày (Blank4) / (Blank5) / (Blank6)
# Số chứng minh nhân dân: (Blank7)
# Ngày cấp: (Blank8)/(Blank9)/(Blank10) nơi cấp: (Blank11)
# Chỗ ở hiện nay: (Blank12)
# Số điện thoại :(Blank13)
# Theo Quyết định số(Blank14) ngày(Blank15)/(Blank16)/(Blank17) tôi được hưởng trợ cấp thất nghiệp(Blank18)tháng, kể từ ngày(Blank19)/(Blank20)/(Blank21) đến ngày(Blank22)/(Blank23)/(Blank24) tại tỉnh/thành phố(Blank25)
# Tôi thông báo kết quả tìm kiếm việc làm theo quy định, cụ thể như sau:
# (1) Đơn vị thứ nhất (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
# (Blank26)
# (2) Đơn vị thứ hai (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
# (Blank27)
#  ((Blank28)) Tên đơn vị thứ ((Blank29)): (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
# (Blank30)
# Tình trạng việc làm hiện nay: (Blank31)
# """

# Abstract = """
# CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
#                 Độc lập - Tự do - Hạnh phúc    
#             TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ
#     Kính gửi(1):(Blank1)
# 1. Họ, chữ đệm và tên: (Blank2)
# 2. Ngày, tháng, năm sinh:(Blank3)/(Blank4)/ (Blank5)       3. Giới tính: (Blank6)
# 4. CCCD: (Blank7)
# 5. Số điện thoại liên hệ:(Blank8)  6. Email: (Blank9)
# 7. Họ, chữ đệm và tên chủ hộ:(Blank10) 8. Mối quan hệ với chủ hộ:(Blank11)
# 9.Số định danh cá nhân của chủ hộ: (Blank12)
# 10. Nội dung đề nghị(2): (Blank13)
# """


# Abstract = """
# GIẤY KHAI ĐĂNG KÝ XE 
# A. PHẦN CHỦ XE TỰ KÊ KHAI
# Tên chủ xe :(Blank1)
# Năm sinh:(Blank2)
# Địa chỉ : (Blank3)
# Số CCCD/CMND/Hộ chiếu của chủ xe:(Blank4)
# cấp ngày (Blank5)/(Blank6)/(Blank7) tại (Blank8)
# Số CCCD/CMND/Hộ chiếu của người làm thủ tục (Blank9)
# cấp ngày (Blank10)/(Blank11) /(Blank12) tại(Blank13)
# Điện thoại của chủ xe :(Blank14)
# Điện thoại của người làm thủ tục :(Blank15)
# Số hóa đơn điện tử mã số thuế:(Blank16)
# Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp:(Blank17)
# Số tờ khai hải quan điện tử cơ quan cấp:(Blank18)
# Số sêri Phiếu KTCLXX Cơ quan cấp (Blank19)
# Số giấy phép kinh doanh vận tải cấp ngày (Blank20)/(Blank21) / (Blank22)tại(Blank23)
# Số máy 1 (Engine N0):(Blank24)
# Số máy 2 (Engine N0):(Blank25)
# Số khung (Chassis N0):(Blank26)
# """

Question = "(Blank1)"
tag_names = """
#Name
#Day_of_birth
#Month_of_birth
#Year_of_birth
#Date_of_birth
#Day_of_issue
#Month_of_issue
#Year_of_issue
#Date_of_issue
#Gender
#Citizen_identification_card
#Ethnicity
#Religion
#Nationality
#Marital_status
#Blood_type
#Place_of_birth_registration
#Hometown
#Permanent_residence
#Current_address
#Occupation
#Educational_level
#Phone_number
#Email
#Position
#Organization
#Hour
#Minute
#Second
#Enterprise_Identification_Number
#Legal_Representative
#Administrative_violations
#Regulation_at
#(Individual/Organization)_suffered_damages
#Opinions_from_violator
#Opinions_from_officials/witnesses
#Opinions_from_affected_party
#Request_to_Mr._(Ms.)
#Reason
#Dear
#Relationship to registrant
#Mother_name
#Mother_day_of_birth
#Mother_month_of_birth
#Mother_year_of_birth
#Mother_date_of_birth
#Father_name
#Father_day_of_birth
#Father_month_of_birth
#Father_year_of_birth
#Father_date_of_birth
#Electronic_invoice_number_tax_code
#Registration_tax_file_code
#E-customs_declaration_number.
#Engine_N1
#Engine_N2
#Chassis_N0
#Content/Specific_incident
#Quantity
#Current_employment_status
#Commune
#District
#Province
#For_you
#Behavior
#Explanation_for_the_application
#People's_Court
#Empty
"""


translations = {
    "#Full_Name": "Họ tên",
    "#Surname": "Họ",
    "#Last_Name": "Tên",
    "#Day_of_birth": "Ngày sinh",
    "#Month_of_birth": "Tháng sinh",
    "#Year_of_birth": "Năm sinh",
    "#Date_of_birth": "Ngày tháng năm sinh",
    "#Day_of_issue": "Ngày cấp",
    "#Month_of_issue": "Tháng cấp",
    "#Year_of_issue": "Năm cấp",
    "#Date_of_issue": "Ngày tháng năm cấp",
    "#Gender": "Giới tính",
    "#Citizen_identification_card": "Chứng minh nhân dân",
    "#Ethnicity": "Dân tộc",
    "#Religion": "Tôn giáo",
    "#Nationality": "Quốc tịch",
    "#Marital_status": "Tình trạng hôn nhân",
    "#Blood_type": "Nhóm máu",
    "#Place_of_birth_registration": "Nơi đăng ký sinh",
    "#Hometown": "Quê quán",
    "#Permanent_residence": "Nơi thường trú",
    "#Current_address": "Địa chỉ hiện nay",
    "#Occupation": "Nghề nghiệp",
    "#Educational_level": "Trình độ học vấn",
    "#Phone_number": "Số điện thoại",
    "#Email": "Email",
    "#Position": "Chức vụ",
    "#Organization": "Tổ chức",
    "#Hour": "Giờ",
    "#Minute": "Phút",
    "#Second": "Giây",
    "#Enterprise_Identification_Number": "Mã số thuế doanh nghiệp",
    "#Legal_Representative": "Người đại diện pháp luật",
    "#Administrative_violations": "Vi phạm hành chính",
    "#Regulation_at": "Quy định tại",
    "#(Individual/Organization)_suffered_damages": "(Cá nhân/Tổ chức) bị thiệt hại",
    "#Opinions_from_violator": "Ý kiến từ người vi phạm",
    "#Opinions_from_officials/witnesses": "Ý kiến từ cơ quan/quan chức/nhân chứng",
    "#Opinions_from_affected_party": "Ý kiến từ bên bị ảnh hưởng",
    "#Request_to_Mr._(Ms.)": "Yêu cầu gửi đến Ông/Bà",
    "#Reason": "Lý do",
    "#Dear": "Kính thưa",
    "#Relationship to registrant": "Mối quan hệ với người đăng ký",
    "#Mother_name": "Tên mẹ",
    "#Mother_day_of_birth": "Ngày sinh của mẹ",
    "#Mother_month_of_birth": "Tháng sinh của mẹ",
    "#Mother_year_of_birth": "Năm sinh của mẹ",
    "#Mother_date_of_birth": "Ngày tháng năm sinh của mẹ",
    "#Father_name": "Tên cha",
    "#Father_day_of_birth": "Ngày sinh của cha",
    "#Father_month_of_birth": "Tháng sinh của cha",
    "#Father_year_of_birth": "Năm sinh của cha",
    "#Father_date_of_birth": "Ngày tháng năm sinh của cha",
    "#Electronic_invoice_number_tax_code": "Mã số hóa đơn điện tử",
    "#Registration_tax_file_code": "Mã số hồ sơ đăng ký thuế",
    "#E-customs_declaration_number": "Số tờ khai hải quan điện tử",
    "#Engine_N1": "Động cơ N1",
    "#Engine_N2": "Động cơ N2",
    "#Chassis_N0": "Khung xe N0",
    "#Content/Specific_incident": "Nội dung",
    "#Quantity": "Số lượng",
    "#Current_employment_status": "Tình trạng công việc hiện tại",
    "#Commune": "Xã/Phường",
    "#District": "Quận/Huyện",
    "#Province": "Tỉnh/Thành phố",
    "#For_you": "Dành cho bạn",
    "#Behavior": "Hành vi",
    "#Explanation_for_the_application": "Giải trình cho đơn xin",
    "#People's_Court": "Tòa án nhân dân",
    "#Empty": "Trống"
}

def blank_to_tagname(form, tag_names):
  Abstract, count = generate_uniform(form)
  list_outputs = []
  for i in range(1, count+1): 
    Question = f"(Blank{i})"
    prompt_parts = [
    f"""
    Give you list of tag names. Your task is to choose a right tag name to replace the (Blankx) gived by Question in the Abstract. Your response only has format (Blankx:#tagname). If you don't have answer, reply with [Blankx:#Empty].
    List of task names: {tag_names}
    <Examples>
      Abstract: '''ĐƠN XIN VIỆC

      Kính gửi: Ban lãnh đạo cùng phòng nhân sự Công ty (Blank1)
      Tôi tên là: (Blank2)
      Sinh ngày: (Blank3)
      Chỗ ở hiện nay: (Blank4)
      Số điện thoại liên hệ: (Blank5)
      Thông qua trang website của công ty, tôi biết được Quý công ty có nhu cầu tuyển dụng vị trí (Blank6). Tôi cảm thấy trình độ và kỹ năng của mình phù hợp với vị trí này. Tôi mong muốn được làm việc và cống hiến cho công ty.

      Tôi đã tốt nghiệp loại (Blank7) tại trường (Blank8)
      Bên cạnh đó, tôi có tham gia các khóa học(Blank9)
      Ngoài ra, tôi còn sử dụng thành thạo tin học văn phòng, tiếng Anh giao tiếp tốt và biết sử dụng các phần mềm kế toán.

      Tôi thực sự mong muốn được làm việc trong môi trường chuyên nghiệp của Quý công ty. Tôi rất mong nhận được lịch hẹn phỏng vấn trong một ngày gần nhất.'''
    Question: (Blank2).
    Answer: (Blank2: #Full_Name)

      Abstract:'''TỜ KHAI CĂN CƯỚC CÔNG DÂN
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
      15. Nghề nghiệp: (Blank17) 16. Trình độ học vấn: (Blank18)'''
    Question: (Blank13)
    Answer: (Blank13: #Place_of_birth_registration)

    Abstract:'''TỜ KHAI CĂN CƯỚC CÔNG DÂN

                  
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
      15. Nghề nghiệp: (Blank17) 16. Trình độ học vấn: (Blank18)'''
    Question: (Blank6)
    Answer: (Blank6: #Gender)

    Abstract:'''ĐƠN XIN NGHỈ HỌC

      Tôi tên: (Blank1)	 MSSV:	(Blank2)
      Ngành học: (Blank3)	 Lớp: 	(Blank4)
      Ngày sinh: (Blank5) 	 Nơi sinh: (Blank6)	
      Địa chỉ hộ khẩu thường trú:	(Blank7)
      Điện thoại: (Blank8)
      Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được thôi học từ học kỳ: (Blank9) năm học: 20(Blank10) – 20(Blank11)
      Lý do: (Blank12)
      Trong khi chờ đợi sự chấp thuận của nhà trường, tôi xin chân thành cảm ơn.'''
    Question: (Blank7)
    Answer: (Blank7: #Permanent_residence)

    Abstract:'''TỜ KHAI CĂN CƯỚC CÔNG DÂN       
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
      15. Nghề nghiệp: (Blank17) 16. Trình độ học vấn: (Blank18)'''
    Question: (Blank18)
    Answer: (Blank18: #Empty)  
    </Examples>
    Abstract: {Abstract}
    Question: {Question}
    """]
    output = model.generate_content(prompt_parts)
    print(output.text)
    list_outputs.append(output.text)
  return list_outputs, Abstract, count
  
with open('Forms\Text\TK1-TS.txt','r',encoding='utf-8') as f:
  text = f.read()

list_tag_names, form, count = blank_to_tagname(text, tag_names)

def get_list_keys(list_tag_names, translations):
  list_keys = []
  pattern = r'#(\w+)'
  for tag_name in list_tag_names:
    match = re.search(pattern, tag_name)
    # text = match.group(0).replace(")","")
    print(translations[match.group(0)])
    list_keys.append(translations[match.group(0)])
  return list_keys

list_keys = get_list_keys(list_tag_names, translations)

def fill_form(context, form, count):
  list_info = extract_info(context, list_keys)
  for i in range(1, count+1):
    form = form.replace(f"(Blank{i})", list_info[i-1])
  return form


context = """
    TỜ KHAI CĂN CƯỚC CÔNG DÂN

1. Họ, chữ đệm và tên(1): Hồ Quý Phi
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Kang
3. Ngày, tháng, năm sinh:27/01/2003; 4. Giới tính (Nam/nữ): Nữ
5. Số CMND/CCCD: 547
6. Dân tộc:Hoa; 7. Tôn giáo:Phật 8. Quốc tịch: Anh
9. Tình trạng hôn nhân: Kết hôn 10. Nhóm máu (nếu có): B
11. Nơi đăng ký khai sinh: USA
12. Quê quán:  Huyện Krông Pa, Tỉnh Bình Định
13. Nơi thường trú: Singapore
"""

print(form)

print(fill_form(context, form, count))