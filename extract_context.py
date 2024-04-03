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
Abstract = """
TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ

I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): LÊ VĂN VIỆT	[02]. Giới tính: Nam
[03]. Ngày, tháng, năm sinh: 01/12/1993	  [04]. Quốc tịch: Việt Nam
[05]. Dân tộc: Mường	[06]. Số CCCD/ĐDCN/Hộ chiếu: 05222030	
[07]. Điện thoại: 01123	[08]. Email (nếu có): levanviet@gmail.com
[09]. Nơi đăng ký khai sinh: [09.1]. Xã: Hóa Lạc [09.2]. Huyện: Phù Cát [09.3]. Tỉnh: Bình Ka
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): Không
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: Y tế
[12]. Số nhà, đường/phố, thôn/xóm: 	Hóa Lạc
[13]. Xã: Cát Thành	[14]	Huyện: Phù Cát	[15]. Tỉnh: Bình Định
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.

"""
list_keys = ["Họ tên", "Ngày sinh", "Tháng sinh", "Năm sinh", "Ngày tháng năm sinh", "Giới tính", "Số CMND", "Dân tộc", "Tôn giáo", "Quốc tịch", "Tình trạng hôn nhân", "Nhóm máu", "Nơi đăng ký khai sinh", "Quê quán", "Nơi thường trú", "Số điện thoại"]
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

for key in list_keys:
  Question = key

  prompt_parts = [
  f"""
  Your task is to extract information from abstract, combine with section in Question. Your response is information corresponding to the question with format [Question:Information]. If you don't have answer, reply with [Question:Rỗng]. Only output print out, no additional text.
  <Examples>
  Abstract: '''Tôi tên là Lê Hữu Hưng, giới tính nam, sinh viên năm 3, ngày sinh 01 tháng 03 năm 2003, quê ở Gia Lai (lãnh thổ Việt Nam), số CMND là 12345.'''
  Question: 'Họ tên'.
  Answer: [Họ tên: Lê Hữu Hưng]

  Abstract:'''Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.'''
  Question: 'Ngày sinh'
  Answer: [Ngày sinh: 26]

  Abstract:'''Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.'''
  Question: 'Số điện thoại'
  Answer: [Số điện thoại: Rỗng]

  Abstract:'''Tên của tôi là Nguyễn Đức Nam, là sinh viên năm 3, sinh ngày 26/02/2003, dân tộc Kinh, quê ở Bình Định, quốc tịch Việt Nam, số CMND là 12345.
  Question: "Ngày tháng năm sinh"
  Answer: [Ngày tháng năm sinh: 26/02/2003]

  Abstract: '''TỜ KHAI CĂN CƯỚC CÔNG DÂN
  1. Họ, chữ đệm và tên(1): Nguyễn Văn Khoa
  2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không
  3. Ngày, tháng, năm sinh:1/1/2011; 4. Giới tính (Nam/nữ): nữ
  5. Số CMND/CCCD: 052203654
  6. Dân tộc:Kinh; 7. Tôn giáo:Không 8. Quốc tịch: Việt Nam
  9. Tình trạng hôn nhân: Đã kết hôn 10. Nhóm máu (nếu có): A'''
  Question: 'Số điện thoại'
  Answer: [Số điện thoại: Rỗng]

  Abstract: '''TỜ KHAI CĂN CƯỚC CÔNG DÂN
  1. Họ, chữ đệm và tên(1): Nguyễn Văn Khoa
  2. Họ, chữ đệm và tên gọi khác (nếu có)(1): Không
  3. Ngày, tháng, năm sinh:1/1/2011; 4. Giới tính (Nam/nữ): nữ
  5. Số CMND/CCCD: 052203654
  6. Dân tộc:Kinh; 7. Tôn giáo:Không 8. Quốc tịch: Việt Nam
  9. Tình trạng hôn nhân: Đã kết hôn 10. Nhóm máu (nếu có): A'''
  Question: 'Tháng sinh'
  Answer: [Tháng sinh: 1]
  </Examples>
  Abstract: {Abstract}
  Question: {Question}
  """]
 
  response = model.generate_content(prompt_parts)
  print(response.text)
  results.append(get_value(response.text))

