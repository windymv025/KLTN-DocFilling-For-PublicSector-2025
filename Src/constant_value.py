### 0. ------------------DEFAULT------------------###
API_KEY = "AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50" #Gemini API key

### 1. ------------------Task: BLANK TO TAGNAMES------------------###
tag_names = """
#Full_Name
#Surname
#Last_Name
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
#Place_of_birth
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
#Individual_or_Organization_suffered_damages
#Opinions_from_violator
#Opinions_from_officials_or_witnesses
#Opinions_from_affected_party
#Request_to_Mr_Ms
#Reason
#Dear
#Place_of_issue
#Relationship_to_registrant
#Mother_name
#Mother_day_of_birth
#Mother_month_of_birth
#Mother_year_of_birth
#Mother_date_of_birth
#Mother_Citizen_identification_card
#Mother_Ethnicity
#Mother_Religion
#Mother_Nationality
#Mother_Marital_status
#Mother_Blood_type
#Mother_Place_of_birth
#Mother_Place_of_birth_registration
#Mother_Hometown
#Mother_Permanent_residence
#Mother_Current_address
#Mother_Occupation
#Mother_Educational_level
#Mother_Phone_number
#Mother_Email
#Father_name
#Father_day_of_birth
#Father_month_of_birth
#Father_year_of_birth
#Father_date_of_birth
#Father_Citizen_identification_card
#Father_Ethnicity
#Father_Religion
#Father_Nationality
#Father_Marital_status
#Father_Blood_type
#Father_Place_of_birth
#Father_Place_of_birth_registration
#Father_Hometown
#Father_Permanent_residence
#Father_Current_address
#Father_Occupation
#Father_Educational_level
#Father_Phone_number
#Father_Email
#Electronic_invoice_number_tax_code
#Registration_tax_file_code
#E_customs_declaration_number
#Engine_N1
#Engine_N2
#Chassis_N0
#Content
#Quantity
#Current_employment_status
#Commune
#District
#Province
#For_you
#Behavior
#Explanation_for_the_application
#People_Court
#Relationship
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
"#Place_of_birth": "Nơi sinh",
"#Place_of_birth_registration": "Nơi đăng ký sinh",
"#Hometown": "Quê quán",
"#Permanent_residence": "Nơi thường trú",
"#Current_address": "Chỗ ở hiện nay",
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
"#Mother_Citizen_identification_card": "Chứng minh nhân dân của mẹ",
"#Mother_Ethnicity": "Dân tộc của mẹ", 
"#Mother_Religion": "Tôn giáo của mẹ",
"#Mother_Nationality": "Quốc tịch của mẹ",
"#Mother_Marital_status": "Tình trạng hôn nhân của mẹ",
"#Mother_Blood_type": "Nhóm máu của mẹ",
"#Mother_Place_of_birth": "Nơi sinh của mẹ",
"#Mother_Place_of_birth_registration": "Nơi đăng ký sinh của mẹ",
"#Mother_Hometown": "Quê quán của mẹ",
"#Mother_Permanent_residence": "Nơi thường trú của mẹ",
"#Mother_Current_address": "Chỗ ở hiện nay của mẹ",
"#Mother_Occupation": "Nghề nghiệp của mẹ",
"#Mother_Educational_level": "Trình độ học vấn của mẹ",
"#Mother_Phone_number": "Số điện thoại của mẹ",
"#Mother_Email": "Email của mẹ",
"#Father_name": "Tên cha",
"#Father_day_of_birth": "Ngày sinh của cha",
"#Father_month_of_birth": "Tháng sinh của cha",
"#Father_year_of_birth": "Năm sinh của cha",
"#Father_date_of_birth": "Ngày tháng năm sinh của cha",
"#Father_Citizen_identification_card": "Chứng minh nhân dân của cha",
"#Father_Ethnicity": "Dân tộc của cha",
"#Father_Nationality": "Quốc tịch của cha",
"#Father_Marital_status": "Tình trạng hôn nhân của cha",
"#Father_Blood_type": "Nhóm máu của cha",
"#Father_Place_of_birth_registration": "Nơi đăng ký sinh của cha",
"#Father_Place_of_birth": "Nơi sinh của cha",
"#Father_Hometown": "Quê quán của cha",
"#Father_Permanent_residence": "Nơi thường trú của cha",
"#Father_Current_address": "Chỗ ở hiện nay của cha",
"#Father_Occupation": "Nghề nghiệp của cha",
"#Father_Educational_level": "Trình độ học vấn của cha",
"#Father_Phone_number": "Số điện thoại của cha",
"#Father_Email": "Email của cha",
"#Electronic_invoice_number_tax_code": "Mã số hóa đơn điện tử",
"#Registration_tax_file_code": "Mã số hồ sơ đăng ký thuế",
"#E_customs_declaration_number": "Số tờ khai hải quan điện tử",
"#Engine_N1": "Động cơ N1",
"#Engine_N2": "Động cơ N2",
"#Chassis_N0": "Khung xe N0",
"#Content": "Nội dung",
"#Quantity": "Số lượng",
"#Current_employment_status": "Tình trạng công việc hiện tại",
"#Commune": "Xã/Phường",
"#District": "Quận/Huyện",
"#Province": "Tỉnh/Thành phố",
"#For_you": "Dành cho bạn",
"#Behavior": "Hành vi",
"#Explanation_for_the_application": "Giải trình cho đơn xin",
"#People's_Court": "Tòa án nhân dân",
"#Relationship_to_registrant": "Mối quan hệ với người đăng kí",
"#Place_of_issue": 'Nơi cấp',
"#Relationship": "Mối quan hệ",
"#Empty": "Trống"
}

#{tag_names} and {Abstract} will be replaced
template_blank_to_tagname = """
Give you list of tag names, and Abstract include some [Blankx] to fill in. Your task is to choose right tag names to replace the these [Blankx]. Your response will be a list having have format [Blankx:#tagname]. If this [Blankx] don't have info, reply with [Blankx:#Empty].
List of task names: {tag_names}

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
[Blank2: #Full_Name]
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
[Blank1: #Full_Name]
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
[Blank18: #Educational_level]

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
[Blank1: #Full_Name]
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
Tình trạng việc làm hiện nay: (Blank31)'''

Answer:
[Blank1: #Empty]
[Blank2: #Empty]
[Blank3: #Full_Name]
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
[Blank31: #Empty]

Abstract:'''
    CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

        Độc lập - Tự do - Hạnh phúc

            --------------

ĐƠN TỐ CÁO

Kính gửi: (Blank1)

Họ và tên tôi: (Blank2) Sinh ngày: (Blank3)

Chứng minh nhân dân số: (Blank4)

Ngày cấp: (Blank5)/(Blank6)/(Blank7) Nơi cấp: (Blank8)
Hộ khẩu thường trú: (Blank9)

Chỗ ở hiện tại: (Blank10)

Số điện thoại liên hệ: (Blank11)

Tôi làm đơn này tố cáo và đề nghị Quý cơ quan tiến hành điều tra, xử lý đối với hành vi vi phạm pháp luật của:

Anh: (Blank12) Sinh ngày: (Blank13)

CMND/CCCD: (Blank14)
Ngày cấp: (Blank15) Nơi cấp: (Blank16)

Hộ khẩu thường trú: (Blank17)

Chỗ ở hiện tại: (Blank18)

Vì anh  (Blank19) đã có hành vi(Blank20)

Sự việc cụ thể như sau:

(Blank21)

(Blank22)

(Blank23)

Từ những sự việc trên, tôi cho rằng hành vi của anh (Blank24) có dấu hiệu vi phạm pháp luật.

Tôi cam kết toàn bộ nội dung đã trình bày trên là hoàn toàn đúng sự thật và chịu trách nhiệm trước pháp luật về những điều trình bày trên. Kính mong Quý cơ quan xem xét và giải quyết theo đúng quy định pháp luật.

Tôi xin chân thành cảm ơn!'''

Answer:
[Blank1: #Empty]
[Blank2: #Full_Name]
[Blank3: #Date_of_birth]
[Blank4: #Citizen_identification_card]
[Blank5: #Date_of_issue]
[Blank6: #Month_of_issue]
[Blank7: #Year_of_issue]
[Blank8: #Place_of_issue]
[Blank9: #Permanent_residence]
[Blank10: #Current_address]
[Blank11: #Phone_number]
[Blank12: #Full_Name]
[Blank13: #Date_of_birth]
[Blank14: #Citizen_identification_card]
[Blank15: #Date_of_issue]
[Blank16: #Place_of_issue]
[Blank17: #Permanent_residence]
[Blank18: #Current_address]
[Blank19: #Last_Name]
[Blank20: #Empty]
[Blank21: #Content]
[Blank22: #Content]
[Blank23: #Content]
[Blank24: #Last_Name]

Abstract: {Abstract}
"""

### 2. ------------------Task: EXTRACT CONTENT------------------###
#{Abstract} and {Question} will be replaced
template_extract_content ="""
Give you list of keys. Your task is to extract information from abstract corresponding with this list keys.
Your response will be a list having have format [key:value]. If this [key] doesn't have info, reply with [key:#Empty]. If key not in tag names, reply with [key:#Empty], example, if key is Trống, reply [Trống: #Empty]
<Examples>
Abstract: '''Tôi tên là Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CMND là 12345.'''
list_keys = '''
Họ tên
Trống
Ngày sinh
Tháng sinh
Năm sinh
Ngày tháng năm sinh
Giới tính
Số CMND
Dân tộc
Tôn giáo
Quốc tịch
Tình trạng hôn nhân
Nhóm máu
Nơi đăng ký khai sinh
Trống
Quê quán
Trống
Trống
Trống
Nơi thường trú
Số điện thoại'''
Answer: 
[Họ tên:Lê Hữu Hưng]
[Trống: #Empty]
[Ngày sinh:01]
[Tháng sinh:03]
[Năm sinh:2003]
[Ngày tháng năm sinh:01/03/2003]
[Giới tính:Nam]
[Số CMND:12345]
[Dân tộc:#Empty]
[Tôn giáo:#Empty]
[Quốc tịch:#Empty]
[Tình trạng hôn nhân:#Empty]
[Nhóm máu:#Empty]
[Nơi đăng ký khai sinh:#Empty]
[Trống: #Empty]
[Quê quán:#Empty]
[Trống: #Empty]
[Trống: #Empty]
[Trống: #Empty]
[Nơi thường trú:#Empty]
[Số điện thoại:#Empty]

Abstract:'''Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.'''
list_keys = '''
Họ tên
Ngày sinh
Tháng sinh
Năm sinh
Ngày tháng năm sinh
Số CMND
Số điện thoại
Trình độ học vấn
'''
Answer:
[Họ tên:Nguyễn Đức Nam]
[Ngày sinh:26]
[Tháng sinh:02]
[Năm sinh:2003]
[Ngày tháng năm sinh:26/02/2003]
[Số CMND:12345]
[Số điện thoại:#Empty]
[Trình độ học vấn:#Empty]


Abstract: '''TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): Nguyễn Văn Khoa
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không
3. Ngày, tháng, năm sinh:1/1/2011; 4. Giới tính (Nam/nữ): nữ
5. Số CMND/CCCD: 052203654
6. Dân tộc:Kinh; 7. Tôn giáo:Không 8. Quốc tịch: Việt Nam
9. Tình trạng hôn nhân: Đã kết hôn 10. Nhóm máu (nếu có): A'''
list_keys = '''
Họ tên
Ngày sinh
Tháng sinh
Năm sinh
Trống
Ngày tháng năm sinh
Giới tính
Số CMND
Dân tộc
Tôn giáo
Quốc tịch
Tình trạng hôn nhân
Nhóm máu
Trống
Trống
Nơi đăng ký khai sinh
Quê quán
Nơi thường trú
Số điện thoại'''
Answer:
[Họ tên:Nguyễn Văn Khoa]
[Ngày sinh:1]
[Tháng sinh:1]
[Năm sinh:2011]
[Trống: #Empty]
[Ngày tháng năm sinh:1/1/2011]
[Giới tính:Nữ]
[Số CMND:052203654]
[Dân tộc:Kinh]
[Tôn giáo:Không]
[Quốc tịch:Việt Nam]
[Tình trạng hôn nhân:Đã kết hôn]
[Nhóm máu:A]
[Trống: #Empty]
[Trống: #Empty]
[Nơi đăng ký khai sinh:#Empty]
[Quê quán:#Empty]
[Nơi thường trú:#Empty]
[Số điện thoại:#Empty]

Abstract: '''
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: (1) Công an Xã Cát Thành
Họ, chữ đệm, tên người yêu cầu: Nguyễn Đức Phép
Nơi cư trú: (2)Hóa Lạc - Cát Thành
Giấy tờ tùy thân: (3)Giấy khai sinh
Quan hệ với người được khai sinh: Cha
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: Nguyễn Đức Nam
Ngày, tháng, năm sinh: 26/02/2003 ghi bằng chữ: Ngày 26 tháng 02 năm 2003
Giới tính: Nam Dân tộc:  Kinh Quốc tịch: Việt Nam
Nơi sinh: (4)Hóa Lạc - Cát Thành
Quê quán: Hóa Lạc - Cát Thành
Họ, chữ đệm, tên người mẹ: Dương Thị Thu Vân
Năm sinh: (5)1978 Dân tộc: Kinh Quốc tịch: Việt Nam
Nơi cư trú: (2) Hóa Lạc - Cát Thành
Họ, chữ đệm, tên người cha: Nguyễn Đức Phép
Năm sinh: (5)1976 Dân tộc: Kinh Quốc tịch: Việt Nam
Nơi cư trú: (2) Hóa Lạc - Cát Thành
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: Cát Thành, ngày 08 tháng 04 năm 2024
'''
list_keys = '''
Họ tên
Họ
Tên
Ngày sinh
Tháng sinh
Năm sinh
Ngày tháng năm sinh
Ngày cấp
Tháng cấp
Năm cấp
Trống
Ngày tháng năm cấp
Trống
Giới tính
Chứng minh nhân dân
Dân tộc
Tôn giáo
Quốc tịch
Tình trạng hôn nhân
Trống
Nhóm máu
Nơi đăng ký sinh
Quê quán
Nơi thường trú
Chỗ ở hiện nay
Nghề nghiệp
Trống
Trống
Trống
Trình độ học vấn
Số điện thoại
Email
Tên mẹ
Ngày sinh của mẹ
Tháng sinh của mẹ
Năm sinh của mẹ
Ngày tháng năm sinh của mẹ
Trống
Trống
Tên cha
Ngày sinh của cha
Tháng sinh của cha
Năm sinh của cha
Ngày tháng năm sinh của cha'''
Answer:
[Họ tên: Nguyễn Đức Nam]
[Họ: Nguyễn]
[Tên: Đức Nam]
[Ngày sinh: 26]
[Tháng sinh: 02]
[Năm sinh: 2003]
[Ngày tháng năm sinh: 26/02/2003]
[Ngày cấp: 08]
[Tháng cấp: 04]
[Năm cấp: 2024]
[Trống: #Empty]
[Ngày tháng năm cấp: 08/04/2024]
[Trống: #Empty]
[Giới tính: Nam]
[Chứng minh nhân dân: #Empty]
[Dân tộc: Kinh]
[Tôn giáo: #Empty]
[Quốc tịch: Việt Nam]
[Tình trạng hôn nhân: #Empty]
[Trống: #Empty]
[Nhóm máu: #Empty]
[Nơi đăng ký sinh: #Empty]
[Quê quán: Hóa Lạc - Cát Thành]
[Nơi thường trú: Hóa Lạc - Cát Thành] 
[Chỗ ở hiện nay: #Empty]
[Nghề nghiệp: #Empty]
[Trống: #Empty]
[Trống: #Empty]
[Trống: #Empty]
[Trình độ học vấn: #Empty]
[Số điện thoại: #Empty]
[Email: #Empty]
[Tên mẹ: Dương Thị Thu Vân]
[Ngày sinh của mẹ: #Empty]
[Tháng sinh của mẹ: #Empty]
[Năm sinh của mẹ: 1978]
[Ngày tháng năm sinh của mẹ: #Empty]
[Trống: #Empty]
[Trống: #Empty]
[Tên cha: Nguyễn Đức Phép]
[Ngày sinh của cha: #Empty]
[Tháng sinh của cha: #Empty]
[Năm sinh của cha: 1976]
[Ngày tháng năm sinh của cha: #Empty]

Abstract: '''
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
Tên chủ xe : Nguyễn Đức Nam
Năm sinh: 2003
Địa chỉ : KTX B
Số CCCD/CMND/Hộ chiếu của chủ xe: 05220
cấp ngày 05/05/2018 tại Bình Định
Số CCCD/CMND/Hộ chiếu của người làm thủ tục 05220
cấp ngày 05/05/2018 tại Bình Định
Điện thoại của chủ xe : 035
Điện thoại của người làm thủ tục : 035
Số hóa đơn điện tử mã số thuế: 054
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp: 047
Số tờ khai hải quan điện tử cơ quan cấp: 064
Số sêri Phiếu KTCLXX Cơ quan cấp 065
Số giấy phép kinh doanh vận tải cấp ngày 7/8/2019 tại TPHCM
Số máy 1 (Engine N0): 77E1
Số máy 2 (Engine N0): 77H1
Số khung (Chassis N0): 77O'''
list_keys = '''
Trống
Trống
Họ tên
Họ
Tên
Ngày sinh
Tháng sinh
Năm sinh
Ngày tháng năm sinh
Trống
Trống
Trống
Động cơ N1
Động cơ N2
Khung xe N0
'''
Answer:
[Trống: #Empty]
[Trống: #Empty]
[Họ tên: Nguyễn Đức Nam]
[Họ: Nguyễn]
[Tên: Đức Nam]
[Ngày sinh: #Empty]
[Tháng sinh: #Empty]
[Năm sinh: 2003]
[Ngày tháng năm sinh: #Empty]
[Trống: #Empty]
[Trống: #Empty]
[Trống: #Empty]
[Động cơ N1: #Empty]
[Động cơ N2: #Empty]
[Khung xe N0: 77O]
</Examples>
Abstract: {Abstract}
Question: {Question}
"""

### 3. ------------------Task: FILL IN BLANKS WITH TAGNAME LLM------------------###
#{tag_names} and {Abstract} will be replaced
template_llm_auto_blanks_to_tagnames = """
You will be given an abstract containing placeholders in the form of [Blankx].
Your task is to identify the appropriate tag names that should replace these placeholders. 
Provide your response as a list with the format [Blankx: #tagname]. 
If you cannot determine a suitable tag name, reply with [Blankx: #Empty].
Your response only contain Answer, not include Chain of Thought.

For each abstract, follow these steps:
1. Determine how much blanks need to be filled. Ensure that you fill in all blanks.
2. Break down the abstract and analyze the context around each [Blankx].
3. Determine the appropriate tag name based on the context.
4. Document your reasoning for each determination.
5. Provide the final list of tags.

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

Chain of Thought:
We have 9 blanks that need to be filled.
Blank1: This is the recipient of the letter, which is the company's HR department. Thus, the tag should be #company_name.
Blank2: This is the name of the applicant, so the tag should be #applicant_name.
Blank3: This is the birth date of the applicant, so the tag should be #date_of_birth.
Blank4: This is the current address of the applicant, so the tag should be #current_address.
Blank5: This is the contact number of the applicant, so the tag should be #contact_number.
Blank6: This is the position the applicant is applying for, so the tag should be #position.
Blank7: This refers to the type of degree the applicant has graduated with, so the tag should be #degree.
Blank8: This is the university the applicant graduated from, so the tag should be #university.
Blank9: This refers to additional courses the applicant has taken, so the tag should be #courses

Answer:
[Blank1: #company_name]
[Blank2: #applicant_name]
[Blank3: #date_of_birth]
[Blank4: #current_address]
[Blank5: #contact_number]
[Blank6: #position]
[Blank7: #degree]
[Blank8: #university]
[Blank9: #courses]

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

Chain of Thought:
We have 18 blanks that need to be filled.
Blank1: This is the full name of the individual, so the tag should be #full_name.
Blank2: This is another name the individual goes by, so the tag should be #other_name.
Blank3, Blank4, Blank5: These are the day, month, and year of birth, so the tags should be #day_of_birth, #month_of_birth, and #year_of_birth respectively.
Blank6: This indicates the gender of the individual, so the tag should be #gender.
Blank7: This is the ID number of the individual, so the tag should be #ID_number.
Blank8: This refers to the individual's ethnicity, so the tag should be #ethnicity.
Blank9: This refers to the individual's religion, so the tag should be #religion.
Blank10: This is the individual's nationality, so the tag should be #nationality.
Blank11: This refers to the marital status of the individual, so the tag should be #marital_status.
Blank12: This indicates the blood type of the individual, so the tag should be #blood_type.
Blank13: This is the place where the individual’s birth was registered, so the tag should be #place_of_birth_registration.
Blank14: This is the hometown of the individual, so the tag should be #hometown.
Blank15: This is the permanent residence of the individual, so the tag should be #permanent_residence.
Blank16: This is the current address of the individual, so the tag should be #current_address.
Blank17: This is the occupation of the individual, so the tag should be #occupation.
Blank18: This is the educational level of the individual, so the tag should be #educational_level.

Answer: 
[Blank1: #full_name]
[Blank2: #other_name]
[Blank3: #day_of_birth]
[Blank4: #month_of_birth]
[Blank5: #year_of_birth]
[Blank6: #gender]
[Blank7: #ID_number]
[Blank8: #ethnicity]
[Blank9: #religion]
[Blank10: #nationality]
[Blank11: #marital_status]
[Blank12: #blood_type]
[Blank13: #place_of_birth_registration]
[Blank14: #hometown]
[Blank15: #permanent_residence]
[Blank16: #current_address]
[Blank17: #occupation]
[Blank18: #educational_level]

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
Tình trạng việc làm hiện nay: (Blank31)'''

Chain of Thought:
We have 31 blanks that need to be filled.
Blank1: This refers to the month of receiving unemployment benefits. The tag should be #unemployment_benefit_month.
Blank2: This is addressed to the job service center. The tag should be #job_service_center.
Blank3: This is the name of the individual. The tag should be #full_name.
Blank4, Blank5, Blank6: These are the day, month, and year of birth respectively. The tags should be #day_of_birth, #month_of_birth, and #year_of_birth.
Blank7: This is the individual's CCCD number. The tag should be #CCCD_number.
Blank8, Blank9, Blank10: These refer to the day, month, and year of ID issuance respectively. The tags should be #issue_day, #issue_month, and #issue_year.
Blank11: This is the place where the ID was issued. The tag should be #issue_place.
Blank12: This is the current residence of the individual. The tag should be #current_residence.
Blank13: This is the phone number of the individual. The tag should be #phone_number.
Blank14: This is the decision number related to unemployment benefits. The tag should be #decision_number.
Blank15, Blank16, Blank17: These refer to the day, month, and year the unemployment benefits start. The tags should be #start_day, #start_month, and #start_year.
Blank18: This indicates the duration of unemployment benefits in months. The tag should be #unemployment_benefit_duration.
Blank19, Blank20, Blank21: These refer to the day, month, and year the unemployment benefits end. The tags should be #end_day, #end_month, and #end_year.
Blank22, Blank23, Blank24: These are additional references to the end day, month, and year of the benefits. They can also be tagged as #end_day, #end_month, and #end_year to maintain consistency, assuming this section refers to the same dates.
Blank25: This refers to the province or city. The tag should be #province_city.
Blank26, Blank27, Blank28, Blank29, Blank30: These blanks seem to refer to details of job search results and can be complex to determine without additional context. The safe approach is to tag them as #Empty unless more context is provided.
Blank31: This refers to the current employment status of the individual. The tag should be #current_employment_status.

Answer:
[Blank1: #unemployment_benefit_month]
[Blank2: #job_service_center]
[Blank3: #full_name]
[Blank4: #day_of_birth]
[Blank5: #month_of_birth]
[Blank6: #year_of_birth]
[Blank7: #CCCD_number]
[Blank8: #issue_day]
[Blank9: #issue_month]
[Blank10: #issue_year]
[Blank11: #issue_place]
[Blank12: #current_residence]
[Blank13: #phone_number]
[Blank14: #decision_number]
[Blank15: #start_day]
[Blank16: #start_month]
[Blank17: #start_year]
[Blank18: #unemployment_benefit_duration]
[Blank19: #end_day]
[Blank20: #end_month]
[Blank21: #end_year]
[Blank22: #end_day]
[Blank23: #end_month]
[Blank24: #end_year]
[Blank25: #province_city]
[Blank26: #Empty]
[Blank27: #Empty]
[Blank28: #Empty]
[Blank29: #Empty]
[Blank30: #Empty]
[Blank31: #current_employment_status]
</Examples>

Abstract: {Abstract}
"""


form_stt = {
    '0001':'TỜ KHAI CĂN CƯỚC CÔNG DÂN',
    '0002':'TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ',
    '0003':'GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)'
}


### -1. ------------------Task: EXAMPLE ------------------###
cccd_form = """
			TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): ..............................................
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): ..............................................
3. Ngày, tháng, năm sinh:......./......../............; 4. Giới tính (Nam/nữ): .............
5. Số CMND/CCCD: ..................................................................
6. Dân tộc: .............; 7. Tôn giáo: ............ 8. Quốc tịch: ................
9. Tình trạng hôn nhân: ................... 10. Nhóm máu (nếu có): ...........
11. Nơi đăng ký khai sinh: ..............................................
12. Quê quán: ..............................................
13. Nơi thường trú: ..............................................
.................................................................
14. Nơi ở hiện tại: ..............................................
.................................................................
15. Nghề nghiệp: ............ 16. Trình độ học vấn: ................
"""

cccd_form_blankx = """
TỜ KHAI CĂN CƯỚC CÔNG DÂN
Họ, chữ đệm và tên(1): (Blank1)
Họ, chữ đệm và tên gọi khác (nếu có)(1): (Blank2)
Ngày, tháng, năm sinh:(Blank3)/(Blank4)/(Blank5); 4. Giới tính (Nam/nữ): (Blank6)
Số CMND/CCCD: (Blank7)
Dân tộc: (Blank8); 7. Tôn giáo: (Blank9) 8. Quốc tịch: (Blank10)
Tình trạng hôn nhân: (Blank11) 10. Nhóm máu (nếu có): (Blank12)
Nơi đăng ký khai sinh: (Blank13)
Quê quán: (Blank14)
Nơi thường trú: (Blank15)
Nơi ở hiện tại: (Blank16)
Nghề nghiệp: (Blank17) 16. Trình độ học vấn: (Blank18)
"""

TK1_TS_form_blankx = """
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

DK_xe_form_blankx = """
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
Tên chủ xe :(Blank1)
Năm sinh:(Blank2)
Địa chỉ : (Blank3)
Số CCCD/CMND/Hộ chiếu của chủ xe:(Blank4)
cấp ngày (Blank5)/(Blank6)/(Blank7) tại (Blank8)
Số CCCD/CMND/Hộ chiếu của người làm thủ tục (Blank9)
cấp ngày (Blank10)/(Blank11) /(Blank12) tại(Blank13)
Điện thoại của chủ xe :(Blank14)
Điện thoại của người làm thủ tục :(Blank15)
Số hóa đơn điện tử mã số thuế:(Blank16)
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp:(Blank17)
Số tờ khai hải quan điện tử cơ quan cấp:(Blank18)
Số sêri Phiếu KTCLXX Cơ quan cấp (Blank19)
Số giấy phép kinh doanh vận tải cấp ngày (Blank20)/(Blank21) / (Blank22)tại(Blank23)
Số máy 1 (Engine N0):(Blank24)
Số máy 2 (Engine N0):(Blank25)
Số khung (Chassis N0):(Blank26)
"""

cccd_keys = ['#Full_Name', '#Empty', '#Day_of_birth', '#Month_of_birth', '#Year_of_birth', '#Gender', '#Citizen_identification_card', '#Ethnicity', '#Religion', '#Nationality', '#Marital_status', '#Blood_type', '#Place_of_birth_registration', '#Hometown', '#Permanent_residence', '#Current_address', '#Occupation', '#Educational_level']
cccd_values =  ['Họ tên', 'Trống', 'Ngày sinh', 'Tháng sinh', 'Năm sinh', 'Giới tính', 'Chứng minh nhân dân', 'Dân tộc', 'Tôn giáo', 'Quốc tịch', 'Tình trạng hôn nhân', 'Nhóm máu', 'Nơi đăng ký sinh', 'Quê quán', 'Nơi thường trú', 'Chỗ ở hiện nay', 'Nghề nghiệp', 'Trình độ học vấn']

cccd_filled_form = """
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): Nguyễn Văn Khoa
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không
3. Ngày, tháng, năm sinh:1/1/2011; 4. Giới tính (Nam/nữ): nữ
5. Số CMND/CCCD: 052203654
6. Dân tộc:Kinh; 7. Tôn giáo:Không 8. Quốc tịch: Việt Nam
9. Tình trạng hôn nhân: Đã kết hôn 10. Nhóm máu (nếu có): A
11. Nơi đăng ký khai sinh: Bình Định
12. Quê quán: Phù Cát
13. Nơi thường trú: Cát Thánh
14. Nơi ở hiện tại: Khu B
15. Nghề nghiệp: ITE 16. Trình độ học vấn: Master
"""

TK1_TS_filled_form = """
TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ
I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): NGUYỄN ĐỨC NAM	[02]. Giới tính: Nam
[03]. Ngày, tháng, năm sinh: 26/02/2003	  [04]. Quốc tịch: Việt Nam
[05]. Dân tộc: Kinh	[06]. Số CCCD/ĐDCN/Hộ chiếu: 05203
[07]. Điện thoại: 035	[08]. Email (nếu có): nam@gmail.com
[09]. Nơi đăng ký khai sinh: [09.1]. Xã: CT	[09.2]. Huyện: PC [09.3]. Tỉnh: BD
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): Không
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: ABC
[12]. Số nhà, đường/phố, thôn/xóm: (Blank16)
[13]. Xã: KHU B	[14]	Huyện: DIAN	[15]. Tỉnh: BD
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
"""

DK_xe_filled_form = """
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
Tên chủ xe : NGUYỄN ĐỨC NAM
Năm sinh: 2002
Địa chỉ : KB
Số CCCD/CMND/Hộ chiếu của chủ xe: 0520
cấp ngày 2/3/4 tại BD
Số CCCD/CMND/Hộ chiếu của người làm thủ tục 0420
cấp ngày 5/6/7 tại BD
Điện thoại của chủ xe : 035
Điện thoại của người làm thủ tục : 035
Số hóa đơn điện tử mã số thuế: 12345
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp: 67854
Số tờ khai hải quan điện tử cơ quan cấp: #123
Số sêri Phiếu KTCLXX Cơ quan cấp #652
Số giấy phép kinh doanh vận tải cấp ngày 1/1/1111 tại HCM
Số máy 1 (Engine N0): N1_541
Số máy 2 (Engine N0): N2_874
Số khung (Chassis N0): C0_123
"""

LHH_content = """Tôi tên là Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CMND là 12345. Học tại trường HCMUS, và có số điện thoại là 037."""


