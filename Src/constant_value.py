### 0. ------------------DEFAULT------------------###
API_KEY = "AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50" #Gemini API key

### 1. ------------------Task: BLANK TO TAGNAMES------------------###
tag_names = """
#full_name: Họ, chữ đệm và tên
#alias_name: Họ, chữ đệm và tên gọi khác 
#dob_day, #dob_month, #dob_year: Ngày sinh
#gender: Giới tính
#id_number: Số CMND/CCCD
#CCCD_number: Số CCCD
#CMND_Number: Số CMND
#religion: Tôn giáo
#nationality: Quốc tịch
#marital_status: Tình trạng hôn nhân
#blood_type: Nhóm máu 
#birth_registration_place: Nơi đăng ký khai sinh
#hometown: Quê quán
#permanent_address: Nơi thường trú
#current_address: Nơi ở hiện tại
#occupation: Nghề nghiệp
#education_level: Trình độ học vấn
#place: Địa điểm khai tờ khai
#day, #month, #year: Ngày, tháng, năm khai tờ khai
#receiver: Kính gửi
#relationship: Quan hệ với người được khai sinh
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
form_tagging_prompt = """
Bạn được cung cấp một form cần điền thông tin.
Nhiệm vụ của bạn là gán các tên tag thích hợp cho từng trường dữ liệu liên quan đến người dùng hoặc cơ quan/tổ chức với định dạng [userX_tagname] hoặc [orgX_tagname]. 
Đối với các trường không liên quan đến bất kỳ người dùng hay cơ quan/tổ chức nào, sử dụng tag name [#another].
<Instruction>
Trước tiên, hãy xác định có bao nhiêu người dùng và cơ quan/tổ chức trong form này.
Sau đó, xác định các tag name phù hợp cho từng trường dữ liệu trong form dựa trên ngữ cảnh và dữ liệu người dùng hoặc cơ quan/tổ chức.
Nếu không có tag name phù hợp, hãy tạo tag name mới dựa trên quy tắc chuẩn hóa đã đề ra.
</Instruction>
<Examples>
Form:
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): ..........
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): ..........
3. Ngày, tháng, năm sinh: ........../........../..........; 4. Giới tính (Nam/nữ): ..........
5. Số CMND/CCCD: ..........
6. Dân tộc: ..........; 7. Tôn giáo: .......... 8. Quốc tịch: ..........
9. Tình trạng hôn nhân: .......... 10. Nhóm máu (nếu có): ..........
11. Nơi đăng ký khai sinh: ..........
12. Quê quán: ..........
13. Nơi thường trú: ..........
14. Nơi ở hiện tại: ..........
15. Nghề nghiệp: .......... 16. Trình độ học vấn: ..........
.........., ngày ..........tháng..........năm..........
Answer:
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id]
6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Quê quán: [user1_hometown]
13. Nơi thường trú: [user1_permanent_address]
14. Nơi ở hiện tại: [user1_current_address]
15. Nghề nghiệp: [user1_occupation] 16. Trình độ học vấn: [user1_education_level]
[user1_place], ngày [user1_day] tháng [user1_month] năm [user1_year]
Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: ..........
Họ, chữ đệm, tên người yêu cầu: ..........
Nơi cư trú: ..........
Giấy tờ tùy thân: ..........
Quan hệ với người được khai sinh: ..........
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: ..........
Ngày, tháng, năm sinh: ........../........../.......... ghi bằng chữ: ..........
Giới tính: .......... Dân tộc: .......... Quốc tịch: ..........
Nơi sinh: ..........
Quê quán: ..........
Họ, chữ đệm, tên người mẹ: ..........
Năm sinh: .......... Dân tộc: .......... Quốc tịch: ..........
Nơi cư trú: ..........
Họ, chữ đệm, tên người cha: ..........
Năm sinh: .......... Dân tộc: .......... Quốc tịch: ..........
Nơi cư trú: ..........
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: .........., ngày .......... tháng .......... năm ..........
Answer:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: [org1_name]
Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Nơi cư trú: [user1_address]
Giấy tờ tùy thân: [user1_id]
Quan hệ với người được khai sinh: [user1_relationship_user2]
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: [user2_full_name]
Ngày, tháng, năm sinh: [user2_dob_day]/[user2_dob_month]/[user2_dob_year] ghi bằng chữ: [user2_dob_text]
Giới tính: [user2_gender] Dân tộc: [user2_ethnicity] Quốc tịch: [user2_nationality]
Nơi sinh: [user2_birthplace]
Quê quán: [user2_hometown]
Họ, chữ đệm, tên người mẹ: [user3_full_name]
Năm sinh: [user3_dob_year] Dân tộc: [user3_ethnicity] Quốc tịch: [user3_nationality]
Nơi cư trú: [user3_address]
Họ, chữ đệm, tên người cha: [user4_full_name]
Năm sinh: [user4_dob_year] Dân tộc: [user4_ethnicity] Quốc tịch: [user4_nationality]
Nơi cư trú: [user4_address]
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: [user1_place], ngày [user1_day] tháng [user1_month] năm [user1_year]
</Examples>

Form: {Abstract}
Answer:
"""

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


#Hung
personal_information_tagnames = """
# [full_name]: Full name of the user.
# [alias_name]: Alternate name of the user.
# [dob_day]: Day of birth of the user.
# [dob_month]: Month of birth of the user.
# [dob_year]: Year of birth of the user.
# [dob]: Date of birth (day, month, year) of the user.
# [dob_text]: Date of birth (day, month, year) of the user is written by text
# [gender]: Gender of the user.
# [id_number]: ID card number of the user.
# [ethnicity]: Ethnicity of the user.
# [religion]: Religion of the user.
# [nationality]: Nationality of the user.
# [marital_status]: Marital status of the user.
# [blood_type]: Blood type of the user.
# [birth_registration_place]: Birth registration place of the user.
# [birth_registration_place_ward]: Birth registration place ward of the user.
# [birth_registration_place_district]: Birth registration place district of the user.
# [birth_registration_place_province]: Birth registration place province of the user.
# [hometown]: Hometown of the user.
# [permanent_address]: Permanent address of the user.
# [current_address]: Current address of the user.
# [current_address_ward]: Current address ward of the user. 
# [current_address_district]: Current address ward of the user.
# [current_address_province]: Current address ward of the user.
# [occupation]: Occupation of the user.
# [education_level]: Education level of the user.
# [class]: Class name of the user.
# [school]:School name of the user.
# [course]: Course of the the user.
# [faculty]: Faculty of the the user.
# [phone]: Phone mobile of the user
# [phone_home]: Phone home of the user
# [email]: Email of the user
# [driving_license_number]: driving license number of the user
# """

remaining_tag_names = """
# [receiver]: The individual or organization that will receive or process the form filled out by the user.
# [request_content]: The specific content or request made by the user in the form. This could be details about what the form is being submitted for, such as a request for a new ID card, a change in personal information, etc.
# [day]: day when the form is filled out by the user.
# [month]: month when the form is filled out by the user.
# [year]: year the form is filled out by the user.
# [place]: Place where the form is filled out by the user.
# [reason]: Reason when the user is filled out form.
# """

'''
template_PI_prompt = """
You have been provided with a form that contains placeholders (........) to be filled in with personal information.
Below is a list of tag names that represent different types of personal information:

{personal_information_tagnames}

Instructions:

Your task is to accurately identify and replace the placeholders in the form with the appropriate tag names. Follow these steps:

Identify Users: Determine the number of unique users mentioned in the form. Assign each user a unique identifier (e.g., user1, user2, etc.).

Match Personal Information: For each placeholder (........), check if it corresponds to a personal information tag name from the provided list. If it does, replace the placeholder with the appropriate tag name in the format [userX_tagname], where X is the identifier of the user. If the placeholder does not match any tag from the personal_information_tagnames, replace it with [another].

Handle Non-Personal Information: If a placeholder does not correspond to any known personal information tag name, check the {remaining_tag_names}. Replace it with the appropriate tag name from the list if a match is found.
If the placeholder does not match any tag from the remaining_tag_names, replace it with [another].

Ensure that each placeholder is correctly replaced according to the user's unique identifier and the nature of the information.

Form:
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): ..........
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): ..........
3. Ngày, tháng, năm sinh: ........../........../..........; 4. Giới tính (Nam/nữ): ..........
5. Số CMND/CCCD: ..........
6. Dân tộc: ..........; 7. Tôn giáo: .......... 8. Quốc tịch: ..........
9. Tình trạng hôn nhân: .......... 10. Nhóm máu (nếu có): ..........
11. Nơi đăng ký khai sinh: ..........
12. Quê quán: ..........
13. Nơi thường trú: ..........
14. Nơi ở hiện tại: ..........
15. Nghề nghiệp: .......... 16. Trình độ học vấn: ..........
.........., ngày ..........tháng..........năm..........
Answer:
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id]
6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Quê quán: [user1_hometown]
13. Nơi thường trú: [user1_permanent_address]
14. Nơi ở hiện tại: [user1_current_address]
15. Nghề nghiệp: [user1_occupation] 16. Trình độ học vấn: [user1_education_level]
[place], ngày [day] tháng [month] năm [year]

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: ..........
Họ, chữ đệm, tên người yêu cầu: ..........
Nơi cư trú: ..........
Giấy tờ tùy thân: ..........
Quan hệ với người được khai sinh: ..........
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: ..........
Ngày, tháng, năm sinh: ........../........../.......... ghi bằng chữ: ..........
Giới tính: .......... Dân tộc: .......... Quốc tịch: ..........
Nơi sinh: ..........
Quê quán: ..........
Họ, chữ đệm, tên người mẹ: ..........
Năm sinh: .......... Dân tộc: .......... Quốc tịch: ..........
Nơi cư trú: ..........
Họ, chữ đệm, tên người cha: ..........
Năm sinh: .......... Dân tộc: .......... Quốc tịch: ..........
Nơi cư trú: ..........
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: .........., ngày .......... tháng .......... năm ..........
Answer:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: [receiver]
Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Nơi cư trú: [user1_current_address]
Giấy tờ tùy thân: [user1_id]
Quan hệ với người được khai sinh: [user1_relationship_user2]
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: [user2_full_name]
Ngày, tháng, năm sinh: [user2_dob_day]/[user2_dob_month]/[user2_dob_year] ghi bằng chữ: [user2_dob_text]
Giới tính: [user2_gender] Dân tộc: [user2_ethnicity] Quốc tịch: [user2_nationality]
Nơi sinh: [user2_birthplace]
Quê quán: [user2_hometown]
Họ, chữ đệm, tên người mẹ: [user3_full_name]
Năm sinh: [user3_dob_year] Dân tộc: [user3_ethnicity] Quốc tịch: [user3_nationality]
Nơi cư trú: [user3_current_address]
Họ, chữ đệm, tên người cha: [user4_full_name]
Năm sinh: [user4_dob_year] Dân tộc: [user4_ethnicity] Quốc tịch: [user4_nationality]
Nơi cư trú: [user4_current_address]
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: [place], ngày [day] tháng [month] năm [year]

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI

Kính gửi: ..........

Tôi tên là: ..........
Cơ quan quản lý trực tiếp (nếu có): ..........

Quyết định cử đi học số .......... ngày .......... tháng .......... năm .......... của        ..........
Tên trường đến học, nước:       ..........
Trình độ đào tạo:       ..........
Ngành/nghề đào tạo:     ..........
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo:     ..........
Ngày nhập học:  ..........
Lý do đề nghị gia hạn:..........

Thời gian đề nghị gia hạn: từ tháng ........../năm 20.......... đến tháng ........../năm 20..........
Kinh phí trong thời gian gia hạn :      ..........
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập.

Địa chỉ liên lạc của tôi:       ..........
E-mail: ..........
Điện thoại cố định:..........    Điện thoại di động:..........

                .........., ngày.......... tháng.......... năm..........
Người làm đơn
(Ký và ghi rõ họ tên)
Answer:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI

Kính gửi: [receiver]

Tôi tên là: [user1_full_name]
Cơ quan quản lý trực tiếp (nếu có): [user1_organization]

Quyết định cử đi học số [user1_decision_number] ngày [user1_decision_day] tháng [user1_decision_month] năm [user1_decision_year] của  [user1_decis sion_issuer]
Tên trường đến học, nước:       [user1_school]
Trình độ đào tạo:       [user1_education_level]
Ngành/nghề đào tạo:     [user1_course]
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo:     [another]
Ngày nhập học:  [another]
Lý do đề nghị gia hạn:[reason]

Thời gian đề nghị gia hạn: từ tháng [another]/năm 20[another] đến tháng [another]/năm 20[another]
Kinh phí trong thời gian gia hạn :      [another]
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập.

Địa chỉ liên lạc của tôi:       [user1_current_address]
E-mail: [user1_email]
Điện thoại cố định: [user1_phone_home]   Điện thoại di động: [user1_phone]



                [place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ HỖ TRỢ HỌC TẬP 
(Dùng cho cha mẹ trẻ mẫu giáo hoặc người chăm sóc trẻ mẫu giáo học tại các cơ sở giáo dục công lập)
Kính gửi: ................(Cơ sở giáo dục)
Họ và tên cha mẹ (hoặc người chăm sóc): ................
Hộ khẩu thường trú tại:................
Là cha/mẹ (hoặc người chăm sóc) của em:................
Sinh ngày:................
Dân tộc:................
Hiện đang học tại lớp:................
Trường:................
Tôi làm đơn này đề nghị các cấp quản lý xem xét, giải quyết cấp tiền hỗ trợ học tập theo quy định và chế độ hiện hành./.
 
XÁC NHẬN CỦA ỦY BAN NHÂN DÂN CẤP XÃ1
Nơi trẻ mẫu giáo có hộ khẩu thường trú
(Ký tên, đóng dấu)	................,ngày....tháng................năm................
Người làm đơn
(Ký, ghi rõ họ tên)
Answer:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ HỖ TRỢ HỌC TẬP 
(Dùng cho cha mẹ trẻ mẫu giáo hoặc người chăm sóc trẻ mẫu giáo học tại các cơ sở giáo dục công lập)
Kính gửi: [receiver] (Cơ sở giáo dục)
Họ và tên cha mẹ (hoặc người chăm sóc): [user1_full_name]
Hộ khẩu thường trú tại: [user1_permanent_address]
Là cha/mẹ (hoặc người chăm sóc) của em: [user2_full_name]
Sinh ngày: [user2_dob]
Dân tộc: [user2_ethnicity]
Hiện đang học tại lớp: [user2_class]
Trường: [user2_school]
Tôi làm đơn này đề nghị các cấp quản lý xem xét, giải quyết cấp tiền hỗ trợ học tập theo quy định và chế độ hiện hành./.
 
XÁC NHẬN CỦA ỦY BAN NHÂN DÂN CẤP XÃ1
Nơi trẻ mẫu giáo có hộ khẩu thường trú
(Ký tên, đóng dấu)	[place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký, ghi rõ họ tên)

Form:
{form}
Answer:
"""
'''

template_PI_prompt = """
You have been provided with a form where all placeholders have been initially replaced with [#another]. 
Your task is to identify and replace [#another] with the most appropriate tag names from the provided list or suggest a new tag name if necessary.

Below is a list of tag names that represent different types of personal information:

{personal_information_tagnames}

Instructions:

1. **Identify Users**: Determine the number of unique users mentioned in the form. Assign each user a unique identifier (e.g., user1, user2, etc.).

2. **Replace [#another] with Tag Names**: For each occurrence of [#another], check if it corresponds to a personal information tag name from the provided list. If it does, replace [#another] with the appropriate tag name in the format [userX_tagname], where X is the identifier of the user.

3. **Handle Non-Personal Information**: If [#another] does not correspond to any known personal information tag name, check the {remaining_tag_names}. Replace it with the appropriate tag name from the list if a match is found.

4. **Suggest New Tags**: If no existing tag name matches, suggest a new tag name that could be added to the list. If no suitable tag name is suggested, leave it as [#another].

Ensure that each placeholder is correctly replaced according to the user's unique identifier and the nature of the information.

Form:
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [#another]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [#another]
3. Ngày, tháng, năm sinh: [#another]/[#another]/[#another]; 4. Giới tính (Nam/nữ): [#another]
5. Số CMND/CCCD: [#another]
6. Dân tộc: [#another]; 7. Tôn giáo: [#another] 8. Quốc tịch: [#another]
9. Tình trạng hôn nhân: [#another] 10. Nhóm máu (nếu có): [#another]
11. Nơi đăng ký khai sinh: [#another]
12. Quê quán: [#another]
13. Nơi thường trú: [#another]
14. Nơi ở hiện tại: [#another]
15. Nghề nghiệp: [#another] 16. Trình độ học vấn: [#another]
[#another], ngày [#another]tháng[#another]năm[#another]
Answer:
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id]
6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Quê quán: [user1_hometown]
13. Nơi thường trú: [user1_permanent_address]
14. Nơi ở hiện tại: [user1_current_address]
15. Nghề nghiệp: [user1_occupation] 16. Trình độ học vấn: [user1_education_level]
[place], ngày [day] tháng [month] năm [year]

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: [#another]
Họ, chữ đệm, tên người yêu cầu: [#another]
Nơi cư trú: [#another]
Giấy tờ tùy thân: [#another]
Quan hệ với người được khai sinh: [#another]
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: [#another]
Ngày, tháng, năm sinh: [#another]/[#another]/[#another] ghi bằng chữ: [#another]
Giới tính: [#another] Dân tộc: [#another] Quốc tịch: [#another]
Nơi sinh: [#another]
Quê quán: [#another]
Họ, chữ đệm, tên người mẹ: [#another]
Năm sinh: [#another] Dân tộc: [#another] Quốc tịch: [#another]
Nơi cư trú: [#another]
Họ, chữ đệm, tên người cha: [#another]
Năm sinh: [#another] Dân tộc: [#another] Quốc tịch: [#another]
Nơi cư trú: [#another]
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: [#another], ngày [#another] tháng [#another] năm [#another]
Answer:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: [receiver]
Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Nơi cư trú: [user1_current_address]
Giấy tờ tùy thân: [user1_id]
Quan hệ với người được khai sinh: [user1_relationship_user2]
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: [user2_full_name]
Ngày, tháng, năm sinh: [user2_dob_day]/[user2_dob_month]/[user2_dob_year] ghi bằng chữ: [user2_dob_text]
Giới tính: [user2_gender] Dân tộc: [user2_ethnicity] Quốc tịch: [user2_nationality]
Nơi sinh: [user2_birthplace]
Quê quán: [user2_hometown]
Họ, chữ đệm, tên người mẹ: [user3_full_name]
Năm sinh: [user3_dob_year] Dân tộc: [user3_ethnicity] Quốc tịch: [user3_nationality]
Nơi cư trú: [user3_current_address]
Họ, chữ đệm, tên người cha: [user4_full_name]
Năm sinh: [user4_dob_year] Dân tộc: [user4_ethnicity] Quốc tịch: [user4_nationality]
Nơi cư trú: [user4_current_address]
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
Làm tại: [place], ngày [day] tháng [month] năm [year]

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI

Kính gửi: [#another]

Tôi tên là: [#another]
Cơ quan quản lý trực tiếp (nếu có): [#another]

Quyết định cử đi học số [#another] ngày [#another] tháng [#another] năm [#another] của        [#another]
Tên trường đến học, nước:       [#another]
Trình độ đào tạo:       [#another]
Ngành/nghề đào tạo:     [#another]
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo:     [#another]
Ngày nhập học:  [#another]
Lý do đề nghị gia hạn:[#another]

Thời gian đề nghị gia hạn: từ tháng [#another]/năm 20[#another] đến tháng [#another]/năm 20[#another]
Kinh phí trong thời gian gia hạn :      [#another]
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập.

Địa chỉ liên lạc của tôi:       [#another]
E-mail: [#another]
Điện thoại cố định:[#another]    Điện thoại di động:[#another]

                [#another], ngày[#another] tháng[#another] năm[#another]
Người làm đơn
(Ký và ghi rõ họ tên)
Answer:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI

Kính gửi: [receiver]

Tôi tên là: [user1_full_name]
Cơ quan quản lý trực tiếp (nếu có): [user1_organization]

Quyết định cử đi học số [user1_decision_number] ngày [user1_decision_day] tháng [user1_decision_month] năm [user1_decision_year] của  [user1_decis sion_issuer]
Tên trường đến học, nước:       [user1_school]
Trình độ đào tạo:       [user1_education_level]
Ngành/nghề đào tạo:     [user1_course]
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo:     [another]
Ngày nhập học:  [another]
Lý do đề nghị gia hạn:[reason]

Thời gian đề nghị gia hạn: từ tháng [another]/năm 20[another] đến tháng [another]/năm 20[another]
Kinh phí trong thời gian gia hạn :      [another]
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập.

Địa chỉ liên lạc của tôi:       [user1_current_address]
E-mail: [user1_email]
Điện thoại cố định: [user1_phone_home]   Điện thoại di động: [user1_phone]



                [place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)
Form:
{form}
Answer:
"""