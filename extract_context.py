import re
# 
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_core.prompts import PromptTemplate
 
# # Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4096,
}
  

llm = GoogleGenerativeAI(model="gemini-pro",
                         safety_settings={
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                         },
                         generation_config=generation_config,
                         google_api_key="AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50")

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

Question = ["Họ tên", "Ngày sinh", "Tháng sinh", "Năm sinh", "Ngày tháng năm sinh", "Giới tính", "Số CMND", "Dân tộc", "Tôn giáo", "Quốc tịch", "Tình trạng hôn nhân", "Nhóm máu", "Nơi đăng ký khai sinh", "Quê quán", "Nơi thường trú", "Số điện thoại"]


def extract_info_prompt():
  template ="""
    Give you list of keys. Your task is to extract information from abstract corresponding with this list keys.
    Your response will be a list having have format [key:value]. If this [key] doesn't have info, reply with [key:#Empty]. If key not in tag names, reply with [key:#Empty]
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
    Quê quán
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
    """
  prompt = PromptTemplate.from_template(template)
  return prompt
# ------------------------------------------------------
def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

def get_listInfo_and_missItem(res, list_info, list_miss_items, list_index):
  temp_res = re.search(r'Answer:(.*)', res, re.DOTALL)
  if not temp_res is None:
     res = temp_res.group(1).strip()
  # print("==================RES=====================")
  # print(res)
  pattern = r"\[(.*?):\s*(.*?)\]"

  matches = re.findall(pattern, res)
  # print("Matches: \n", matches)
  for i, match in enumerate(matches):
    info = match[1]
    item = match[0]
    # print("info: \n", info)
    # print("item: \n", item)
    list_info.append(info)
    # print("list_info: \n", list_info)
    list_index.append(i)
    list_miss_items.append(item)
    # if info == "#Empty" and item != "Trống":
    #   list_index.append(i)
    #   list_miss_items.append(item)
  return list_info, list_miss_items, list_index

# ------------------------------------------------------
def create_tag_info_dict(value, list_tag_names, list_info):
  data_to_insert = {"ID": value}
  print("Create tag info dict")

  for i, tag in enumerate(list_tag_names):
    tag = tag.replace("#","")
    data_to_insert[tag] = list_info[i]
  return data_to_insert

# ------------------------------------------------------
def fill_form(text, list_info, count):
  for i in range(1, count+1):
    text = text.replace(f"(Blank{i})", list_info[i-1])
  return text
