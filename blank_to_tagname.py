import google.generativeai as genai
 
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

Abstract = """
Mẫu số 16:  Ban hành kèm theo Thông tư số 28/2015/TT-BLĐTBXH ngày 31 tháng 7 năm 2015 của Bộ trưởng Bộ Lao động-Thương binh và Xã hội
			CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
			    Độc lập - Tự do - Hạnh phúc

THÔNG BÁO VỀ VIỆC TÌM KIẾM VIỆC LÀM
Tháng hưởng trợ cấp thất nghiệp thứ: (Blank1)

Kính gửi:  Trung tâm Dịch vụ việc làm (Blank2)
Tên tôi là: (Blank3)sinh ngày (Blank4) / (Blank5) / (Blank6)
Số chứng minh nhân dân: (Blank7)
Ngày cấp: (Blank8)/(Blank9)/(Blank10) nơi cấp: (Blank11)
Chỗ ở hiện nay: (Blank12)
Số điện thoại :(Blank13)
Theo Quyết định số(Blank14) ngày(Blank15)/(Blank16)/(Blank17) tôi được hưởng trợ cấp thất nghiệp(Blank18)tháng, kể từ ngày(Blank19)/(Blank20)/(Blank21) đến ngày(Blank22)/(Blank23)/(Blank24) tại tỉnh/thành phố(Blank25)
Tôi thông báo kết quả tìm kiếm việc làm theo quy định, cụ thể như sau:
(1) Đơn vị thứ nhất (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
(Blank26)
(2) Đơn vị thứ hai (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
(Blank27)
 ((Blank28)) Tên đơn vị thứ ((Blank29)): (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
(Blank30)
Tình trạng việc làm hiện nay: (Blank31)
"""

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

# Abstract = """
# TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ
# I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
# [01]. Họ và tên (viết chữ in hoa): (Blank1)	[02]. Giới tính: (Blank2)
# [03]. Ngày, tháng, năm sinh: (Blank3)/(Blank4)/(Blank5)	  [04]. Quốc tịch: (Blank6)
# [05]. Dân tộc: (Blank7)	[06]. Số CCCD/ĐDCN/Hộ chiếu: (Blank8)	
# [07]. Điện thoại: (Blank9)	[08]. Email (nếu có): (Blank10)	
# [09]. Nơi đăng ký khai sinh: [09.1]. Xã: (Blank11)	[09.2]. Huyện: (Blank12) [09.3]. Tỉnh: (Blank13)
# [10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): (Blank14)
# [11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: (Blank15)
# [12]. Số nhà, đường/phố, thôn/xóm: (Blank16)	
# [13]. Xã: (Blank17)	[14]	Huyện: (Blank18)	[15]. Tỉnh: (Blank19) 	
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
# GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
# A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
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

# tag_names = """
# #Full_Name
# #Surname
# #Last_Name
# #Day_of_birth
# #Month_of_birth
# #Year_of_birth
# #Date_of_birth
# #Day_of_issue
# #Month_of_issue
# #Year_of_issue
# #Date_of_issue
# #Gender
# #Citizen_identification_card
# #Ethnicity
# #Religion
# #Nationality
# #Marital_status
# #Blood_type
# #Place_of_birth_registration
# #Hometown
# #Permanent_residence
# #Current_address
# #Occupation
# #Educational_level
# #Phone_number
# #Email
# #Position
# #Organization
# #Hour
# #Minute
# #Second
# #Enterprise_Identification_Number
# #Legal_Representative
# #Administrative_violations
# #Regulation_at
# #Individual_or_Organization_suffered_damages
# #Opinions_from_violator
# #Opinions_from_officials_or_witnesses
# #Opinions_from_affected_party
# #Request_to_Mr_Ms
# #Reason
# #Dear
# #Place_of_issue
# #Relationship_to _registrant
# #Mother_name
# #Mother_day_of_birth
# #Mother_month_of_birth
# #Mother_year_of_birth
# #Mother_date_of_birth
# #Father_name
# #Father_day_of_birth
# #Father_month_of_birth
# #Father_year_of_birth
# #Father_date_of_birth
# #Electronic_invoice_number_tax_code
# #Registration_tax_file_code
# #E_customs_declaration_number
# #Engine_N1
# #Engine_N2
# #Chassis_N0
# #Content
# #Quantity
# #Current_employment_status
# #Commune
# #District
# #Province
# #For_you
# #Behavior
# #Explanation_for_the_application
# #People_Court
# #Empty
# """

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
#Empty
"""
list_blanks =["(Blank1)","(Blank2)","(Blank3)","(Blank4)","(Blank5)","(Blank6)","(Blank7)","(Blank8)","(Blank9)","(Blank10)","(Blank11)","(Blank12)","(Blank13)","(Blank14)","(Blank15)","(Blank16)","(Blank17)","(Blank18)","(Blank19)","(Blank20)","(Blank21)","(Blank22)","(Blank23)","(Blank24)","(Blank25)","(Blank26)","(Blank27)","(Blank28)","(Blank29)","(Blank30)","(Blank31)"]

for blank in list_blanks[:1]:
  prompt_parts = [
  f"""
  Give you list of tag names, and Abstract include some [Blankx] to fill in. Your task is to choose right tag names to replace the these [Blankx].
  Your response will be a list having have format [Blankx:#tagname]. If this [Blankx] don't have info, reply with [Blankx:#Empty].
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
  Answer: 
  [Blank1: #Empty]
  [Blank2: #Name]
  [Blank3: #Date_of_birth]
  [Blank4: #Current_address]
  [Blank5: #Phone_number]
  [Blank6: #Empty]
  [Blank7: #Educational_level]
  [Blank8: #Empty]
  [Blank9: #Empty]

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
  Answer: 
  [Blank1: #Name]
  [Blank2: #Empty]
  [Blank3: #Day_of_birth]
  [Blank4: #Month_of_birth]
  [Blank5: #Year_of_birth]
  [Blank6: #Gender]
  [Blank7: #Citizen_identification_card]
  [Blank8: #Ethnicity]
  [Blank9: #Religion]
  [Blank10: #Nationality]
  [Blank11: #Marital_status]
  [Blank12: #Blood_type]
  [Blank13: #Place_of_birth_registration]
  [Blank14: #Hometown]
  [Blank15: #Permanent_residence]
  [Blank16: #Current_address]
  [Blank17: #Occupation]
  [Blank18: #Empty]

  Abstract:'''ĐƠN XIN NGHỈ HỌC

  Tôi tên: (Blank1)	 MSSV:	(Blank2)
  Ngành học: (Blank3)	 Lớp: 	(Blank4)
  Ngày sinh: (Blank5) 	 Nơi sinh: (Blank6)	
  Địa chỉ hộ khẩu thường trú:	(Blank7)
  Điện thoại: (Blank8)
  Nay tôi làm đơn này kính xin Ban Giám Hiệu trường cho tôi được thôi học từ học kỳ: (Blank9) năm học: 20(Blank10) – 20(Blank11)
  Lý do: (Blank12)
  Trong khi chờ đợi sự chấp thuận của nhà trường, tôi xin chân thành cảm ơn.'''
  Answer: 
  [Blank1: #Name]
  [Blank2: #Empty]
  [Blank3: #Empty]
  [Blank4: #Empty]
  [Blank5: #Date_of_birth]
  [Blank6: #Empty]
  [Blank7: #Permanent_residence]
  [Blank8: #Phone_number]
  [Blank9: #Empty]
  [Blank10: #Empty]
  [Blank11: #Empty]
  [Blank12: #Empty]

  Abstract:'''
  Mẫu số 16:  Ban hành kèm theo Thông tư số 28/2015/TT-BLĐTBXH ngày 31 tháng 7 năm 2015 của Bộ trưởng Bộ Lao động-Thương binh và Xã hội
        CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
            Độc lập - Tự do - Hạnh phúc

  THÔNG BÁO VỀ VIỆC TÌM KIẾM VIỆC LÀM
  Tháng hưởng trợ cấp thất nghiệp thứ: (Blank1)

  Kính gửi:  Trung tâm Dịch vụ việc làm (Blank2)
  Tên tôi là: (Blank3)sinh ngày (Blank4) / (Blank5) / (Blank6)
  Số chứng minh nhân dân: (Blank7)
  Ngày cấp: (Blank8)/(Blank9)/(Blank10) nơi cấp: (Blank11)
  Chỗ ở hiện nay: (Blank12)
  Số điện thoại :(Blank13)
  Theo Quyết định số(Blank14) ngày(Blank15)/(Blank16)/(Blank17) tôi được hưởng trợ cấp thất nghiệp(Blank18)tháng, kể từ ngày(Blank19)/(Blank20)/(Blank21) đến ngày(Blank22)/(Blank23)/(Blank24) tại tỉnh/thành phố(Blank25)
  Tôi thông báo kết quả tìm kiếm việc làm theo quy định, cụ thể như sau:
  (1) Đơn vị thứ nhất (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
  (Blank26)
  (2) Đơn vị thứ hai (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
  (Blank27)
  ((Blank28)) Tên đơn vị thứ ((Blank29)): (Tên đơn vị, địa chỉ, người trực tiếp liên hệ, vị trí công việc dự tuyển, kết quả).
  (Blank30)
  Tình trạng việc làm hiện nay: (Blank31)

  Answer:
  [Blank1: #Empty]
  [Blank2: #Empty]
  [Blank3: #Name]
  [Blank4: #Day_of_birth]
  [Blank5: #Month_of_birth]
  [Blank6: #Year_of_birth]
  [Blank7: #Citizen_identification_card]
  [Blank8: #Day_of_issue]
  [Blank9: #Month_of_issue]
  [Blank10: #Year_of_issue]
  [Blank11: #Empty]
  [Blank12: #Current_address]
  [Blank13: #Phone_number]
  [Blank14: #Empty]
  [Blank15: #Day_of_issue]
  [Blank16: #Month_of_issue]
  [Blank17: #Year_of_issue]
  [Blank18: #Empty]
  [Blank19: #Empty]
  [Blank20: #Empty]
  [Blank21: #Empty]
  [Blank22: #Empty]
  [Blank23: #Empty]
  [Blank24: #Empty]
  [Blank25: #Empty]
  [Blank26: #Empty]
  [Blank27: #Empty]
  [Blank28: #Empty]
  [Blank29: #Empty]
  [Blank30: #Empty]
  [Blank31: #Empty]'''

  </Examples>
  Abstract: {Abstract}
  """]

  response = model.generate_content(prompt_parts)
  print(response.text)
