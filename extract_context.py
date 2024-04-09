import google.generativeai as genai
 
genai.configure(api_key="AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50")
 
# Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 6144,
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
 
# Root prompt
# prompt_parts = [
# '''
# Your task is to extract model names from machine learning paper abstracts. Your response is an array of the model names in the format [\"model_name\"]. If you don't find model names in the abstract or you are not sure, return [\"NA\"]
# Abstract: Large Language Models (LLMs), such as ChatGPT and GPT-4, have revolutionized natural language processing research and demonstrated potential in Artificial General Intelligence (AGI). However, the expensive training and deployment of LLMs present challenges to transparent and open academic research. To address these issues, this project open-sources the Chinese LLaMA and Alpaca…
# ''']

Abstract = "Tôi tên Văn A, số điện thoại 321, đang mong muốn học bằng lái xe A2, hiện tại đang ở KTX khu B."
Abstract = """
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): Hồ Quý Phi
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Kang
3. Ngày, tháng, năm sinh:27/01/2003; 4. Giới tính (Nam/nữ): Nữ
5. Số CMND/CCCD: 547
6. Dân tộc:Hoa; 7. Tôn giáo:Phật 8. Quốc tịch: Anh
9. Tình trạng hôn nhân: Kết hôn 10. Nhóm máu (nếu có): B
11. Nơi đăng ký khai sinh: USA
12. Quê quán: Bình Định
13. Nơi thường trú: Singapore
"""
# Abstract = """
# TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ

# I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
# [01]. Họ và tên (viết chữ in hoa): LÊ VĂN VIỆT	[02]. Giới tính: Nam
# [03]. Ngày, tháng, năm sinh: 01/12/1993	  [04]. Quốc tịch: Việt Nam
# [05]. Dân tộc: Mường	[06]. Số CCCD/ĐDCN/Hộ chiếu: 05222030	
# [07]. Điện thoại: 01123	[08]. Email (nếu có): levanviet@gmail.com
# [09]. Nơi đăng ký khai sinh: [09.1]. Xã: Hóa Lạc [09.2]. Huyện: Phù Cát [09.3]. Tỉnh: Bình Ka
# [10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): Không
# [11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: Y tế
# [12]. Số nhà, đường/phố, thôn/xóm: 	Hóa Lạc
# [13]. Xã: Cát Thành	[14]	Huyện: Phù Cát	[15]. Tỉnh: Bình Định
# [16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.

# """
# list_keys = ["Họ tên", "Ngày sinh", "Tháng sinh", "Năm sinh", "Ngày tháng năm sinh", "Giới tính", "Số CMND", "Dân tộc", "Tôn giáo", "Quốc tịch", "Tình trạng hôn nhân", "Nhóm máu", "Nơi đăng ký khai sinh", "Quê quán", "Nơi thường trú", "Số điện thoại"]
# Question = """
# Họ tên
# Ngày sinh
# Tháng sinh
# Năm sinh
# Ngày tháng năm sinh
# Giới tính
# Số CMND
# Dân tộc
# Tôn giáo
# Quốc tịch
# Tình trạng hôn nhân
# Nhóm máu
# Nơi đăng ký khai sinh
# Quê quán
# Nơi thường trú
# Số điện thoại"""
results = []

def get_value(data):
  # Find the index of ':'
  colon_index = data.find(':')
  # Extract the value after ':'
  if colon_index != -1:
      value = data[colon_index + 1:].strip(' []')
      # print(value)
  else:
      print("Colon ':' not found in the string.")
  return value

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
    "#Father_name": "Tên cha",
    "#Father_day_of_birth": "Ngày sinh của cha",
    "#Father_month_of_birth": "Tháng sinh của cha",
    "#Father_year_of_birth": "Năm sinh của cha",
    "#Father_date_of_birth": "Ngày tháng năm sinh của cha",
    "#Electronic_invoice_number_tax_code": "Mã số hóa đơn điện tử",
    "#Registration_tax_file_code": "Mã số hồ sơ đăng ký thuế",
    "#E_customs_declaration_number": "Số tờ khai hải quan điện tử",
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
    "#Relationship_to_registrant": "Mối quan hệ với người đăng kí",
    "#Place_of_issue": 'Nơi cấp',
    "#Empty": "Trống"
}

Question = """
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
Ngày tháng năm cấp
Giới tính
Chứng minh nhân dân
Dân tộc
Tôn giáo
Quốc tịch
Tình trạng hôn nhân
Nhóm máu
Nơi đăng ký sinh
Quê quán
Nơi thường trú
Chỗ ở hiện nay
Nghề nghiệp
Trình độ học vấn
Số điện thoại
Email
Chức vụ
Tổ chức
Giờ
Phút
Giây
Mã số thuế doanh nghiệp
Người đại diện pháp luật
Vi phạm hành chính
Quy định tại
(Cá nhân/Tổ chức) bị thiệt hại
Ý kiến từ người vi phạm
Ý kiến từ cơ quan/quan chức/nhân chứng
Ý kiến từ bên bị ảnh hưởng
Yêu cầu gửi đến Ông/Bà
Lý do
Kính thưa
Mối quan hệ với người đăng ký
Tên mẹ
Ngày sinh của mẹ
Tháng sinh của mẹ
Năm sinh của mẹ
Ngày tháng năm sinh của mẹ
Tên cha
Ngày sinh của cha
Tháng sinh của cha
Năm sinh của cha
Ngày tháng năm sinh của cha
Mã số hóa đơn điện tử
Mã số hồ sơ đăng ký thuế
Số tờ khai hải quan điện tử
Động cơ N1
Động cơ N2
Khung xe N0
Nội dung
Số lượng
Tình trạng công việc hiện tại
Xã/Phường
Quận/Huyện
Tỉnh/Thành phố
Dành cho bạn
Hành vi
Giải trình cho đơn xin
Tòa án nhân dân
Mối quan hệ với người đăng kí
Nơi cấp
"""

for key in range(1):
  prompt_parts = [
  f"""
  Give you list of keys. Your task is to extract information from abstract corresponding with this list keys.
  Your response will be a list having have format [key:value]. If this [key] doesn't have info, reply with [key:#Empty].
  <Examples>
  Abstract: '''Tôi tên là Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CMND là 12345.'''
  list_keys = '''
  Họ tên
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
  Quê quán
  Nơi thường trú
  Số điện thoại'''
  Answer: 
  [Họ tên:Lê Hữu Hưng]
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
  [Quê quán:#Empty]
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
  Ngày tháng năm sinh
  Giới tính
  Số CMND
  Dân tộc
  Tôn giáo
  Quốc tịch
  Tình trạng hôn nhân
  Nhóm máu
  Nơi đăng ký khai sinh
  Quê quán
  Nơi thường trú
  Số điện thoại'''
  Answer:
  [Họ tên:Nguyễn Văn Khoa]
  [Ngày sinh:1]
  [Tháng sinh:1]
  [Năm sinh:2011]
  [Ngày tháng năm sinh:1/1/2011]
  [Giới tính:Nữ]
  [Số CMND:052203654]
  [Dân tộc:Kinh]
  [Tôn giáo:Không]
  [Quốc tịch:Việt Nam]
  [Tình trạng hôn nhân:Đã kết hôn]
  [Nhóm máu:A]
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
  Ngày tháng năm cấp
  Giới tính
  Chứng minh nhân dân
  Dân tộc
  Tôn giáo
  Quốc tịch
  Tình trạng hôn nhân
  Nhóm máu
  Nơi đăng ký sinh
  Quê quán
  Nơi thường trú
  Chỗ ở hiện nay
  Nghề nghiệp
  Trình độ học vấn
  Số điện thoại
  Email
  Tên mẹ
  Ngày sinh của mẹ
  Tháng sinh của mẹ
  Năm sinh của mẹ
  Ngày tháng năm sinh của mẹ
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
  [Ngày tháng năm cấp: 08/04/2024]
  [Giới tính: Nam]
  [Chứng minh nhân dân: #Empty]
  [Dân tộc: Kinh]
  [Tôn giáo: #Empty]
  [Quốc tịch: Việt Nam]
  [Tình trạng hôn nhân: #Empty]
  [Nhóm máu: #Empty]
  [Nơi đăng ký sinh: #Empty]
  [Quê quán: Hóa Lạc - Cát Thành]
  [Nơi thường trú: Hóa Lạc - Cát Thành] 
  [Chỗ ở hiện nay: #Empty]
  [Nghề nghiệp: #Empty]
  [Trình độ học vấn: #Empty]
  [Số điện thoại: #Empty]
  [Email: #Empty]
  [Tên mẹ: Dương Thị Thu Vân]
  [Ngày sinh của mẹ: #Empty]
  [Tháng sinh của mẹ: #Empty]
  [Năm sinh của mẹ: 1978]
  [Ngày tháng năm sinh của mẹ: #Empty]
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
  Họ tên
  Họ
  Tên
  Ngày sinh
  Tháng sinh
  Năm sinh
  Ngày tháng năm sinh
  Động cơ N1
  Động cơ N2
  Khung xe N0
  '''
  Answer:
  [Họ tên: Nguyễn Đức Nam]
  [Họ: Nguyễn]
  [Tên: Đức Nam]
  [Ngày sinh: #Empty]
  [Tháng sinh: #Empty]
  [Năm sinh: 2003]
  [Ngày tháng năm sinh: #Empty]
  [Động cơ N1: #Empty]
  [Động cơ N2: #Empty]
  [Khung xe N0: 77O]
  </Examples>
  Abstract: {Abstract}
  Question: {Question}
  """]
 
  response = model.generate_content(prompt_parts)
  print(response.text)
  results.append(get_value(response.text))

# for key in list_keys:
#   Question = key

#   prompt_parts = [
#   f"""
#   Your task is to extract information from abstract, combine with section in Question. Your response is information corresponding to the question with format [Question:Information]. If you don't have answer, reply with [Question:Rỗng]. Only output print out, no additional text.
#   <Examples>
#   Abstract: '''Tôi tên là Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CMND là 12345.'''
#   Question: 'Họ tên'.
#   Answer: [Họ tên: Lê Hữu Hưng]

#   Abstract:'''Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.'''
#   Question: 'Ngày sinh'
#   Answer: [Ngày sinh: 26]

#   Abstract:'''Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.'''
#   Question: 'Số điện thoại'
#   Answer: [Số điện thoại: Rỗng]

#   Abstract:'''Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.
#   Question: "Ngày tháng năm sinh"
#   Answer: [Ngày tháng năm sinh: 26/02/2003]

#   Abstract: '''TỜ KHAI CĂN CƯỚC CÔNG DÂN
#   1. Họ, chữ đệm và tên(1): Nguyễn Văn Khoa
#   2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không
#   3. Ngày, tháng, năm sinh:1/1/2011; 4. Giới tính (Nam/nữ): nữ
#   5. Số CMND/CCCD: 052203654
#   6. Dân tộc:Kinh; 7. Tôn giáo:Không 8. Quốc tịch: Việt Nam
#   9. Tình trạng hôn nhân: Đã kết hôn 10. Nhóm máu (nếu có): A'''
#   Question: 'Số điện thoại'
#   Answer: [Số điện thoại: Rỗng]

#   Abstract: '''TỜ KHAI CĂN CƯỚC CÔNG DÂN
#   1. Họ, chữ đệm và tên(1): Nguyễn Văn Khoa
#   2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không
#   3. Ngày, tháng, năm sinh:1/1/2011; 4. Giới tính (Nam/nữ): nữ
#   5. Số CMND/CCCD: 052203654
#   6. Dân tộc:Kinh; 7. Tôn giáo:Không 8. Quốc tịch: Việt Nam
#   9. Tình trạng hôn nhân: Đã kết hôn 10. Nhóm máu (nếu có): A'''
#   Question: 'Tháng sinh'
#   Answer: [Tháng sinh: 1]
#   </Examples>
#   Abstract: {Abstract}
#   Question: {Question}
#   """]

