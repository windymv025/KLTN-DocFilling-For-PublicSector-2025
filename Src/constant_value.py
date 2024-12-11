# Importing


### 0. ------------------DEFAULT------------------###
API_KEY = "AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50" #Gemini API key
API_KEY1 = "AIzaSyAcW-DBX75FFX-wxaNXqmPZSxQUO7eaDtM" #Gemini API key
API_KEY2 = "AIzaSyBP9ujvSXoHsfCGt7rDS6j39jGZ7AUHe-I" #Gemini API key
API_KEY3 = "AIzaSyBjYscl3MCJtu83WYiqVd9jpp1O6MSUy0M" #Gemini API key
API_KEY4 = "AIzaSyDvaIcGggU8WwH4eiv6b7zny_HEH5QM_uI" #Gemini API key

cccd_passport_tagnames = """
[full_name]: Họ và tên của người dùng.
Sử dụng khi cần điền họ và tên đầy đủ vào biểu mẫu. 
[alias_name]: Tên khác (bí danh) của người dùng.
Sử dụng khi biểu mẫu yêu cầu cung cấp tên gọi khác hoặc bí danh.
[dob_date]: Ngày tháng năm sinh đầy đủ của người dùng (dạng số).
Sử dụng khi biểu mẫu yêu cầu cung cấp ngày tháng năm sinh đầy đủ. Ví dụ như ngày tháng năm sinh: ..../..../...., hay ngày sinh: ..... mà không đề cập tháng, năm.
[dob_text]: Ngày tháng năm sinh của người dùng (dạng chữ). 
Sử dụng khi biểu mẫu yêu cầu viết ngày tháng năm sinh bằng chữ. Ví dụ các chỗ như ngày tháng năm sinh (bằng chữ): .....
[dob_day],[dob_month],[dob_year]: Ngày sinh, tháng sinh, năm sinh riêng của người dùng.
Sử dụng khi cần điền riêng ngày sinh, riêng tháng sinh hoặc riêng năm sinh. Ví dụ như ngày sinh: ..... tháng sinh: ..... năm sinh: .....
Chú ý ngày sinh ở đây nếu đi chung với tháng sinh và năm sinh, thì sẽ là 3 tagname riêng lẻ như trên. 
[gender]: Giới tính của người dùng.
Sử dụng khi biểu mẫu yêu cầu giới tính (nam/nữ). Ví dụ như giới tính (nam/nữ):.....
[id_number]: Số chứng minh nhân dân hoặc căn cước công dân của người dùng. Hay giấy tờ tùy thân
.Sử dụng khi cần điền số CMND/CCCD. Ví dụ: số CMND/CCCD: ....., hay số CCCD: ....., số định danh cá nhân: ...., giấy tờ tùy thân: .....
[id_issue_date]: Ngày tháng năm cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần ghi đầy đủ ngày, tháng, năm cấp CMND/CCCD.
[id_issue_day],[id_issue_month],[id_issue_year]: Ngày cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần điền riêng ngày cấp, riêng tháng cấp, năm cấp CMND/CCCD. Ví dụ như ngày cấp (cccd): ..... tháng cấp (cccd): ..... năm cấp(cccd): .....
[id_issue_place]: Nơi cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần ghi nơi cấp CMND/CCCD (ví dụ: tỉnh/thành phố, cơ quan công an). ví dụ như nơi cấp (cccd): .....
[id_issue_date_place]: Ngày cấp đầy đủ và nơi cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần ghi đầy đủ ngày, tháng, năm cấp CMND/CCCD và nơi cấp. Ví dụ như ngày cấp: ....., nơi cấp: ....., ngày và nơi cấp: .....
[ethnicity]: Dân tộc của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu dân tộc. Ví dụ như dân tộc: .....
[religion]: Tôn giáo của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu tôn giáo. Ví dụ như tôn giáo: .....
[nationality]: Quốc tịch của người dùng. 
.Sử dụng khi cần điền quốc tịch. Ví dụ như quốc tịch: .....
[marital_status]: Tình trạng hôn nhân của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu điền tình trạng hôn nhân (độc thân, đã kết hôn, ly hôn...). Ví dụ như tình trạng hôn nhân: .....
[blood_type]: Nhóm máu của người dùng. 
.Sử dụng khi cần cung cấp nhóm máu (A, B, AB, O). Ví dụ như nhóm máu: .....
[birthplace]: Nơi sinh của người dùng.
.Sử dụng khi biểu mẫu yêu cầu nơi sinh. Ví dụ như nơi sinh: .....
[birth_place_ward], [birth_place_district], [birth_place_province]: Phường/xã, huyện, tỉnh nơi sinh của người dùng. 
.Sử dụng khi cần điền phường/xã, huyện, tỉnh nơi sinh của người dùng. Ví dụ như phường/xã: ...., huyện: ...., tỉnh: ....
[birth_registration_place]: Nơi đăng ký khai sinh (đầy đủ) của người dùng. 
.Sử dụng khi cần điền nơi đăng ký khai sinh (đầy đủ). Ví dụ như nơi đăng ký khai sinh: .....
[birth_registration_place_ward], [birth_registration_place_district], [birth_registration_place_province]: Phường/xã, huyện, tỉnh nơi đăng ký khai sinh của người dùng. 
.Sử dụng khi cần điền phường/xã, huyện, tỉnh đăng ký khai sinh của người dùng. Ví dụ như phường/xã: ...., huyện: ...., tỉnh: ....
[hometown]: Quê quán của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu quê quán. Ví dụ như quê quán: .....
[permanent_address]: Địa chỉ thường trú của người dùng. 
.Sử dụng khi cần cung cấp địa chỉ thường trú. Ví dụ như địa chỉ thường trú: .....
[current_address]: Địa chỉ tạm trú của người dùng. 
.Sử dụng khi cần cung cấp địa chỉ tạm trú hiện tại. Ví dụ như địa chỉ tạm trú: ....., hay địa chỉ hiện tại: ..........
[current_address_ward],[current_address_district],[current_address_province]: Phường/xã, huyện, tỉnh nơi tạm trú của người dùng. 
.Sử dụng khi cần điền phường/xã, huyện, tỉnh tạm trú. Ví dụ như phường/xã: ...., huyện: ...., tỉnh: ....
[occupation]: Nghề nghiệp của người dùng. Hay có thể là hiện trạng hiện nay.
.Sử dụng khi biểu mẫu yêu cầu điền nghề nghiệp hiện tại. Ví dụ như nghề nghiệp: ....., Hiện nay là: .....
[current_status]: Tình trạng hiện tại của người dùng.
.Sử dụng khi biểu mẫu yêu cầu điền tình trạng hiện tại (đang làm việc, đang học, nghỉ hưu...). Ví dụ như tình trạng hiện tại: ....., hiện tại là:.....
[passport_number]: Số hộ chiếu của người dùng.
Ghi rõ số hộ chiếu để xác định danh tính và quốc tịch của người dùng. Ví dụ như số hộ chiếu: .....
[passport_issue_date]: Ngày, tháng, năm cấp hộ chiếu của người dùng.
Ghi đầy đủ ngày cấp hộ chiếu để dễ dàng tham khảo.
[passport_issue_day],[passport_issue_month],[passport_issue_year]: Ngày cấp, tháng cấp, năm cấp hộ chiếu của người dùng.
Ghi ngày cụ thể, tháng cụ thể, năm cụ thể khi hộ chiếu được cấp. Ví dụ như ngày cấp: ...., tháng cấp: ...., năm cấp: ....
[passport_issue_place]: Nơi cấp hộ chiếu của người dùng.
Ghi tên cơ quan hoặc địa điểm nơi cấp hộ chiếu. Ví dụ như nơi cấp: .....
[passport_expiry_day_month_year]: Ngày hết hạn của hộ chiếu.
Ghi rõ ngày mà hộ chiếu sẽ hết hạn để người dùng có thể quản lý và gia hạn khi cần thiết. Ví dụ như ngày hết hạn: ....
"""

list_cccd_passport_tagnames = [
"[full_name]",
"[alias_name]",
"[dob_text]",
"[dob]",
"[dob_date]",
"[dob_day]",
"[dob_month]",
"[dob_year]",
"[gender]",
"[id_number]",
"[id_issue_date]",
"[id_issue_day]",
"[id_issue_month]",
"[id_issue_year]",
"[id_issue_place]",
"[occupation]",
"[ethnicity]",
"[religion]",
"[nationality]",
"[marital_status]",
"[blood_type]",
"[birth_registration_place]",
"[birthplace]",
"[birth_registration_place_ward]",
"[birth_registration_place_district]",
"[birth_registration_place_province]",
"[hometown]",
"[permanent_address]",
"[current_address]",
"[current_address_ward]",
"[current_address_district]",
"[current_address_province]",
"[current_status]",
"[passport_number]",
"[passport_issue_date]",
"[passport_issue_day]",
"[passport_issue_month]",
"[passport_issue_year]",
"[passport_issue_place]"
]

list_general_tagnames = ["[receiver]","[place]","[day]","[month]","[year]"]

general_tagnames = """
[receiver]: Người nhận biểu mẫu. 
.Sử dụng khi biểu mẫu yêu cầu ghi tên người hoặc cơ quan tiếp nhận. Ví dụ như người nhận: ..... hay kính gửi: .....
[place],[day],[month],[year]: Địa điểm, ngày tháng năm điền được điền bởi người dùng.
.Sử dụng khi cần điền nơi điền biểu mẫu, hay ngày tháng năm làm, thường ở đầu trang hay cuối trang,
nơi mà có ....., ngày ..... tháng ..... năm .....
"""

template_generate_id_passport = """
You are tasked with filling in a form using specific tagnames. 
For any sections where no corresponding tagname exists, leave that section as-is and do not modify it.
Make sure that the output text is formatted correctly and that all tagnames are replaced with the correct information, and don't have any extra characters.
And keep retaining the original format of the text. (The output should have number tagname equal to the input text).

Here are the predefined tagnames for filling into forms, along with their explanations:
{cccd_passport_tagnames}
General tagnames (applicable for all users):
{general_tagnames}

Example:
Input:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH   [#another], ngày [#another] tháng [#another] năm [#another]
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
     [#another], ngày [#another] tháng [#another] năm [#another]

Output:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH   [place], ngày [day] tháng [month] năm [year]
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
     [place], ngày [day] tháng [month] năm [year]

Input:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
 
ĐƠN ĐỀ NGHỊ CẤP CHÍNH SÁCH NỘI TRÚ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi: [#another] (Tên cơ sở giáo dục nghề nghiệp công lập)
Họ và tên:	[#another] 
Ngày, tháng, năm sinh:	[#another] /[#another] /[#another] 
Số định danh cá nhân/Chứng minh nhân dân:[#another] cấp ngày[#another] tháng[#another] năm[#another] nơi cấp[#another] 
Lớp: [#another] Khóa: [#another] Khoa: [#another] 
Mã số học sinh, sinh viên: [#another] 
Thuộc đối tượng: [#another] (ghi rõ đối tượng được quy định tại Điều 2 Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp).
Căn cứ Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ, tôi làm đơn này đề nghị được Nhà trường xem xét để cấp chính sách nội trú theo quy định.

Xác nhận của Khoa
(Quản lý học sinh, sinh viên)	      [#another] , ngày [#another]  tháng [#another]  năm [#another] 
Người làm đơn
(Ký và ghi rõ họ tên)

Output:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
 
ĐƠN ĐỀ NGHỊ CẤP CHÍNH SÁCH NỘI TRÚ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi: [receiver]
Họ và tên:	[user1_full_name]
Ngày, tháng, năm sinh:	[user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số định danh cá nhân/Chứng minh nhân dân:[user1_id_number]cấp ngày[user1_id_issue_day]tháng[user1_id_issue_month]năm[user1_id_issue_year]nơi cấp[user1_id_issue_place]
Lớp:  [#another] Khóa:  [#another] Khoa: [#another]
Mã số học sinh, sinh viên:  [#another] 
Thuộc đối tượng:  [#another] (ghi rõ đối tượng được quy định tại Điều 2 Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp).
Căn cứ Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ, tôi làm đơn này đề nghị được Nhà trường xem xét để cấp chính sách nội trú theo quy định.

Xác nhận của Khoa
(Quản lý học sinh, sinh viên)	      [place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)

Input:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BẢN CAM KẾT
THỰC HIỆN TRÁCH NHIỆM CỦA DU HỌC SINH
(dành cho người chưa có cơ quan công tác)

Kính gửi: Bộ Giáo dục và Đào tạo

Tên tôi là: [#another] Sinh ngày [#another] 
Giấy CMND/Căn cước công dân số: [#another] Ngày cấp:[#another]
Nơi cấp:[#another] 
Hộ chiếu số: [#another] Ngày cấp: [#another] 
Nơi cấp:[#another]
Hiện nay là: [#another] 
Khi được Nhà nước cử đi học tại nước ngoài, tôi cam kết thực hiện đúng trách nhiệm của người được cử đi học như sau:
1. Chấp hành nghiêm túc quy định việc công dân Việt Nam ra nước ngoài học tập (Nghị định số 86/2021/NĐ-CP ngày 25/9/2021 của Chính phủ), quyết định cử đi học cử Bộ Giáo dục và Đào tạo và các quy định tài chính hiện hành của Nhà nước. 
2. Cam kết tích cực học tập, nghiên cứu để hoàn thành tốt chương trình đào tạo đúng thời hạn được phép. Nếu phải gia hạn thời gian học tập sẽ tự túc kinh phí trong thời gian gia hạn.
	[#another], ngày [#another] tháng [#another] năm [#another]
Người cam kết
(ký và ghi rõ họ tên)

Output:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BẢN CAM KẾT
THỰC HIỆN TRÁCH NHIỆM CỦA DU HỌC SINH
(dành cho người chưa có cơ quan công tác)

Kính gửi: Bộ Giáo dục và Đào tạo
Tên tôi là: [user1_full_name] Sinh ngày [user1_dob_date] 
Giấy CMND/Căn cước công dân số: [id_number] Ngày cấp:[id_issue_date]
Nơi cấp:[id_issue_place] 
Hộ chiếu số: [passport_number] Ngày cấp: [passport_issue_date] 
Nơi cấp:[passport_issue_place]
Hiện nay là: [current_status] 
Khi được Nhà nước cử đi học tại nước ngoài, tôi cam kết thực hiện đúng trách nhiệm của người được cử đi học như sau:
1. Chấp hành nghiêm túc quy định việc công dân Việt Nam ra nước ngoài học tập (Nghị định số 86/2021/NĐ-CP ngày 25/9/2021 của Chính phủ), quyết định cử đi học cử Bộ Giáo dục và Đào tạo và các quy định tài chính hiện hành của Nhà nước. 
2. Cam kết tích cực học tập, nghiên cứu để hoàn thành tốt chương trình đào tạo đúng thời hạn được phép. Nếu phải gia hạn thời gian học tập sẽ tự túc kinh phí trong thời gian gia hạn.
	[place], ngày [day] tháng [month] năm [year]
Người cam kết
(ký và ghi rõ họ tên)

Input:
Tờ khai thông tin, căn cước và hộ chiếu
         [another], ngày [another] tháng [another] năm [another]
Kính gửi: [another] (1)
Kính gửi: [another] (2)
Họ và tên: [another]
Ngày sinh: [another]
Ngày sinh: [another]/[another]/[another]   
Ngày sinh: [another] tháng [another] năm [another] 
Ngày, tháng, năm sinh: [another]
Ngày, tháng, năm sinh: [another]/[another]/[another]   
Ngày, tháng, năm sinh: [another] tháng [another] năm [another] 
Nghề nghiệp: [another] 
Công tác tại: [another]
Căn cuộc công dân số: [another]
Ngày cấp: [another]
Ngày cấp: [another] tháng [another] năm [another]
Nơi cấp: [another]
Ngày và nơi cấp: [another] 
Hộ chiếu số: [another]
Ngày cấp: [another]
Ngày cấp: [another] tháng [another] năm [another]  
Nơi cấp: [another]
Đây là thông tin của anh/chị [another] (1)  cần điền vào biểu mẫu. Cảm ơn.

Output:
Tờ khai thông tin, căn cước và hộ chiếu
         [place], ngày [day] tháng [month] năm [year]
Kính gửi: [receiver] (1)
Kính gửi: [receiver] (2)
Họ và tên: [user1_full_name]
Ngày sinh: [user1_dob_date]
Ngày sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]   
Ngày sinh: [user1_dob_day] tháng [user1_dob_month] năm [user1_dob_year]
Ngày, tháng, năm sinh: [user1_dob_date]
Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]   
Ngày, tháng, năm sinh: [user1_dob_day] tháng [user1_dob_month] năm [user1_dob_year]
Nghề nghiệp: [user1_occupation]
Công tác tại: [user1_workplace]  
Căn cuộc công dân số: [uesr1_id_number]
Ngày cấp: [user1_is_issue_date]
Ngày cấp: [user1_is_issue_day] tháng [user1_is_issue_month] năm [user1_is_issue_year]
Nơi cấp: [user1_id_issue_place]
Ngày và nơi cấp: [user1_id_issue_date_place] 
Hộ chiếu số: [user1_passport_number]
Ngày cấp: [user1_passport_issue_date]
Ngày cấp: [user1_passport_issue_day] tháng [user1_passport_issue_month] năm [user1_passport_issue_year] 
Nơi cấp: [user1_passport_issue_place]
Đây là thông tin của anh/chị [user1_full_name] (1)  cần điền vào biểu mẫu. Cảm ơn.
{form}    
Output:
"""

mapping_prompt = """
Given an Input Form and an Output Form, fill in the blank fields (e.g., "BlankX") with the corresponding tagnames from the output. 
If the output form contains a tagname with the suffix _date, you can understand that like _day, _month, _year.
If a blank field is not filled in the output (i.e., it contains ".........."), return "..........".

Please ensure you provide only the correct tagname if available, or return ".........." for unfilled fields.

Example 1:

Input and Output Examples:
Input form:
'''
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BÁO CÁO TỐT NGHIỆP

Kính gửi: (Blank1)

1. Họ và tên:   (Blank2)
2. Số định danh cá nhân:        (Blank3)
3. Cơ quan quản lý trực tiếp (nếu có):  (Blank4)
4. Quyết định cử đi học số(Blank5) ngày(Blank6) tháng(Blank7) năm(Blank8) của(Blank9)  
5. Thời gian học tập ở nước ngoài:      (Blank10)
6. Thời gian gia hạn học tập ở nước ngoài: từ tháng(Blank11)/20(Blank12) đến tháng(Blank13)/20(Blank14)
7. Ngày tốt nghiệp:     (Blank15) Ngày về nước: (Blank16)
8. Kết quả học tập ¬2: :
- Văn bằng, chứng chỉ được cấp: (Blank17)
- Kết quả xếp loại học tập:     (Blank18)
9. Tên cơ sở giáo dục nước ngoài (ghi bằng tiếng Việt và tiếng Anh):
(Blank19)
10. Tên đề tài luận văn thạc sĩ (nếu học thạc sĩ coursework không có luận văn thì ghi: không có luận văn), đề tài luận án tiến sĩ, chuyên đề thực tập:
(Blank20)
11. Tên và học hàm, học vị của người hướng dẫn: (Blank21)
12. Đánh giá của cơ sở giáo dục hoặc giáo sư hướng dẫn (nếu có, viết tóm tắt):
(Blank22)
13. Nguyện vọng, đề nghị 3 :    (Blank23)
14. Cơ quan công tác sau khi tốt nghiệp về Việt Nam:    (Blank24)
Địa chỉ:        (Blank25)
15. Địa chỉ liên hệ :   (Blank26)
Điện thoại cố định:     (Blank27)       , Điện thoại di động:(Blank28)
E-mail:  (Blank29)
16. Kiến nghị, đề xuất đối với cơ quan quản lý trực tiếp, cơ quan cử đi học:
(Blank30)

Tôi cam đoan nội dung báo cáo là hoàn toàn trung thực, chính xác và xin chịu trách nhiệm về nội dung báo cáo.

    (Blank31), ngày(Blank32) tháng(Blank33) năm(Blank34)
Người báo cáo
(Ký và ghi rõ họ tên)
'''
Output form:
'''
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BÁO CÁO TỐT NGHIỆP  
 
Kính gửi: [receiver] 

1. Họ và tên:	[user1_full_name]
2. Số định danh cá nhân:	[user1_id_number]
3. Cơ quan quản lý trực tiếp (nếu có): 	..........
4. Quyết định cử đi học số .......... ngày .......... tháng .......... năm .......... của ..........	
5. Thời gian học tập ở nước ngoài:	..........
6. Thời gian gia hạn học tập ở nước ngoài: từ tháng........../20.......... đến tháng........../20 
7. Ngày tốt nghiệp:	.......... Ngày về nước:	..........
8. Kết quả học tập ¬2: : 
- Văn bằng, chứng chỉ được cấp:	..........
- Kết quả xếp loại học tập:	..........
9. Tên cơ sở giáo dục nước ngoài (ghi bằng tiếng Việt và tiếng Anh):	
..........	
10. Tên đề tài luận văn thạc sĩ (nếu học thạc sĩ coursework không có luận văn thì ghi: không có luận văn), đề tài luận án tiến sĩ, chuyên đề thực tập:	
..........	
11. Tên và học hàm, học vị của người hướng dẫn:	..........
12. Đánh giá của cơ sở giáo dục hoặc giáo sư hướng dẫn (nếu có, viết tóm tắt): 
..........
13. Nguyện vọng, đề nghị 3 :	..........	
14. Cơ quan công tác sau khi tốt nghiệp về Việt Nam:	..........
Địa chỉ:	..........	
15. Địa chỉ liên hệ :	..........	
Điện thoại cố định:	..........	, Điện thoại di động:..........		
E-mail:	 ..........	
16. Kiến nghị, đề xuất đối với cơ quan quản lý trực tiếp, cơ quan cử đi học:	
..........	
		
Tôi cam đoan nội dung báo cáo là hoàn toàn trung thực, chính xác và xin chịu trách nhiệm về nội dung báo cáo. 

    [place], ngày[day] tháng[month] năm[year] 
Người báo cáo
(Ký và ghi rõ họ tên)
'''
Requests:

Request: '(Blank1)'
Output: '[receiver]'

Request: '(Blank4)'
Output: '..........'

Request: '(Blank24)'
Output: '..........'

Request: '(Blank32)'
Output: '[day]'

Example 2:
Input and Output Examples:
Input form:
'''
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ CẤP CHÍNH SÁCH NỘI TRÚ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)    
Kính gửi: (Blank1)(Tên cơ sở giáo dục nghề nghiệp công lập)
Họ và tên:      (Blank2)
Ngày, tháng, năm sinh:  (Blank3)/(Blank4)/(Blank5)
Số định danh cá nhân/Chứng minh nhân dân:(Blank6)cấp ngày(Blank7)tháng(Blank8)năm(Blank9)nơi cấp(Blank10)
Lớp: (Blank11)Khóa: (Blank12)Khoa: (Blank13)
Mã số học sinh, sinh viên: (Blank14)
Thuộc đối tượng: (Blank15)(ghi rõ đối tượng được quy định tại Điều 2 Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp).
Căn cứ Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ, tôi làm đơn này đề nghị được Nhà trường xem xét để cấp chính sách nội trú theo quy định.

Xác nhận của Khoa
(Quản lý học sinh, sinh viên)         (Blank16), ngày (Blank17) tháng (Blank18) năm (Blank19)
Người làm đơn
(Ký và ghi rõ họ tên)
'''

Output form:
'''
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
 
ĐƠN ĐỀ NGHỊ CẤP CHÍNH SÁCH NỘI TRÚ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi: [receiver](Tên cơ sở giáo dục nghề nghiệp công lập)
Họ và tên:	[user1_full_name]
Ngày, tháng, năm sinh:	[user1_dob_date]
Số định danh cá nhân/Chứng minh nhân dân:[user1_id_number]cấp ngày[user1_id_issue_day]tháng[user1_id_issue_month]năm[user1_id_issue_year]nơi cấp[user1_id_issue_place]
Lớp:  ..........Khóa:  ..........Khoa: ..........
Mã số học sinh, sinh viên:  ..........
Thuộc đối tượng:  ..........(ghi rõ đối tượng được quy định tại Điều 2 Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp).
Căn cứ Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ, tôi làm đơn này đề nghị được Nhà trường xem xét để cấp chính sách nội trú theo quy định.

Xác nhận của Khoa
(Quản lý học sinh, sinh viên)	      [place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)
'''

Requests:
Request: '(Blank3)'
Output: '[user1_dob_day]'

Request: '(Blank4)'
Output: '[user1_dob_month]'

Request: '(Blank5)'
Output: '[user1_dob_year]'

Input form: 
'''
{input_form}
'''
Output form:
'''
{output_form}
'''
Request: '{request}'

Output:
"""

generate_promt = '''
I am working with a collection of forms, each serving a specific purpose such as residence_identification_tagnames , study_tagnames ,health_and_medical_tagnames ,health_and_medical_tagnames ,resolve_complaints_tagnames ,job_tagnames and another, so much. Currently, I have about 60 different forms stored, and I will randomly select 5 forms as input.
Each time only generate 1 form.

Your task is to use the provided examples to generate new forms. These new forms should:
1. Follow a similar structure, you can add, delete, modify these forms.
2. Be designed for plausible purposes based on the examples (e.g., legal declarations, health forms, applications, etc.).
3. Include placeholders (e.g., "..........") for fields that need to be filled in, reflecting the content style of the given forms.

Here’s an example to guide your work:
Input: 
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM  
Độc lập - Tự do - Hạnh phúc  

TỜ KHAI CĂN CƯỚC CÔNG DÂN  

1. Họ, chữ đệm và tên: ..........  
2. Ngày, tháng, năm sinh: ..........  
3. Số CMND/CCCD: ..........  
4. Giới tính (Nam/Nữ): ..........  
5. Nơi thường trú: ..........  

.........., ngày .......... tháng .......... năm ..........  
Người khai báo  
(Ký và ghi rõ họ tên)  

CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM  
Độc lập - Tự do - Hạnh phúc  

ĐƠN XIN CẤP GIẤY PHÉP LAO ĐỘNG  

1. Họ và tên: ..........  
2. Ngày, tháng, năm sinh: ..........  
3. Quốc tịch: ..........  
4. Số hộ chiếu: ..........  
5. Địa chỉ nơi làm việc: ..........  

.........., ngày .......... tháng .......... năm ..........  
Người làm đơn  
(Ký và ghi rõ họ tên)  
 
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM  
Độc lập - Tự do - Hạnh phúc  

GIẤY XÁC NHẬN ĐỒNG Ý CỦA PHỤ HUYNH  

1. Tên người đồng ý: ..........  
2. Quan hệ với người được đồng ý: ..........  
3. Nội dung đồng ý: ..........  

.........., ngày .......... tháng .......... năm ..........  
Người đồng ý  
(Ký và ghi rõ họ tên)  

Output:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM  
Độc lập - Tự do - Hạnh phúc  

GIẤY ỦY QUYỀN  

1. Người ủy quyền: ..........  
2. Số CMND/CCCD: ..........  
3. Người được ủy quyền: ..........  
4. Nội dung ủy quyền: ..........  
5. Thời hạn ủy quyền: ..........  

.........., ngày .......... tháng .......... năm ..........  
Người ủy quyền  
(Ký và ghi rõ họ tên)  

Input:
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

TỜ KHAI THUẾ THU NHẬP CÁ NHÂN
(Áp dụng đối với cá nhân cư trú và cá nhân không cư trú có thu nhập từ tiền lương,
tiền công khai thuế trực tiếp với cơ quan thuế)

[01] Kỳ tính thuế:      Tháng .......... năm .......... /Quý .......... năm .......... (Từ tháng ........../.......... đến tháng ........../..........)

[04] Tên người nộp thuế:..........
[05] Mã số thuế:..........
[06] Địa chỉ: ..........
[07] Quận/huyện: .......... [08] Tỉnh/thành phố: ..........
[09] Điện thoại:..........[10] Fax:..........[11] Email: ..........
[12] Tên tổ chức trả thu nhập:..........
[13] Mã số thuế:..........
[14] Địa chỉ: ..........
[15] Quận/huyện: .......... [16] Tỉnh/thành phố: ..........
[17] Tên đại lý thuế (nếu có):..........
[18] Mã số thuế:..........
[19] Hợp đồng đại lý thuế: Số: ..........ngày:..........
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
TỜ KHAI ĐỀ NGHỊ HỖ TRỢ CHI PHÍ MAI TÁNG
(Áp dụng đối với đối tượng quy định tại Điều 5, khoản 1 Điều 14 Nghị định số..........)     
I. THÔNG TIN NGƯỜI CHẾT ĐƯỢC MAI TÁNG (Nếu có)
1. Họ và tên (Viết chữ in hoa). ..........
Ngày/tháng/năm sinh: ........../ ........../.......... Giới tính: .......... Dân tộc: ..........
2. Hộ khẩu thường trú: ..........
3. Ngày .......... tháng .......... năm .......... chết
4. Nguyên nhân chết ..........
5. Thời gian mai táng ..........
6. Địa điểm mai táng ..........
II. THÔNG TIN CƠ QUAN, TỔ CHỨC, HỘ GIA ĐÌNH, CÁ NHÂN ĐỨNG RA MAI TÁNG CHO NGƯỜI CHẾT        
1. Trường hợp cơ quan, tổ chức đứng ra mai táng
a) Tên cơ quan, tổ chức: ..........
- Địa chỉ: ..........
b) Họ và tên người đại diện cơ quan: ..........
- Chức vụ: ..........
2. Trường hợp hộ gia đình, cá nhân đứng ra mai táng
a) Họ và tên (Chủ hộ hoặc người đại diện). ..........
Ngày/tháng/năm sinh: ........../ ........../ ..........
Giấy CMND số: .......... cấp ngày .......... Nơi cấp ..........
b) Hộ khẩu thường trú: ..........
Nơi ở: ..........
c) Quan hệ với người chết: ..........
Tôi xin cam đoan những lời khai trên là đúng, nếu có điều gì khai không đúng tôi xin chịu trách nhiệm hoàn toàn.

Ngày.......... tháng..........năm..........
Người khai
(Ký, ghi rõ họ tên. Nếu cơ quan, tổ chức thì ký, đóng dấu)

SOCIALIST REPUBLIC OF VIETNAM
Independent - Freedom - Happiness
Output:
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KẾT HÔN

Thông tin bên nam:

Họ và tên (Viết chữ in hoa): ..........
Ngày, tháng, năm sinh: .......... Giới tính: ..........
Quốc tịch: .......... Dân tộc: ..........
Số CMND/CCCD: .......... Ngày cấp: .......... Nơi cấp: ..........
Nơi đăng ký hộ khẩu thường trú: ..........
Thông tin bên nữ:

Họ và tên (Viết chữ in hoa): ..........
Ngày, tháng, năm sinh: .......... Giới tính: ..........
Quốc tịch: .......... Dân tộc: ..........
Số CMND/CCCD: .......... Ngày cấp: .......... Nơi cấp: ..........
Nơi đăng ký hộ khẩu thường trú: ..........
Lời cam đoan:
Chúng tôi xin cam đoan thông tin khai trên là đúng sự thật. Nếu có sai sót, chúng tôi xin hoàn toàn chịu trách nhiệm.

Ngày .......... tháng .......... năm ..........
Người khai
(Ký và ghi rõ họ tên)

Input:
ĐƠN ĐỀ NGHỊ HỖ TRỢ
(Dùng cho cha, mẹ học sinh tiểu học học bán trú tại các trường phổ thông
ở xã, thôn đặc biệt khó khăn)

Kính gửi Trường : ..........
Họ và tên:..........
Là Cha/mẹ (hoặc người giám hộ, nhận nuôi) của em: ..........
Sinh ngày..........tháng..........năm..........
Dân tộc:.......... thuộc hộ nghèo(có/không):..........
Thường trú tại thôn/bản..........xã ..........
thuộc vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn.
Huyện..........Tỉnh..........
Năm học..........Là học sinh lớp: .......... Trường ..........
Vì lý do (chọn 1 trong 2 lý do sau):
 - Nhà ở xa trường (ghi rõ cách nơi học tập bao nhiêu km): ..........
 - Địa hình giao thông khó khăn(có/không): ..........
 Nên em .......... không thể đi đến trường và trở về nhà trong ngày.
Tôi làm đơn này đề nghị các cấp quản lý xem xét, để em  .......... được hưởng chính sách hỗ trợ tiền và gạo theo quy định tại Nghị định số........../2016/NĐ-CP ngày..........thá      ng..........năm 2016 của Chính phủ, gồm:

1. Tiền ăn (có/không):..........
2. Tiền nhà ở (đối với trường hợp học sinh phải tự lo chỗ ở)(có/không):..........
3. Gạo(có/không):..........
   .........., ngày ..........tháng..........năm 20..........
Người làm đơn
(Ký, ghi rõ họ, tên hoặc điểm chỉ )



CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

Độc lập - Tự do - Hạnh phúc

---------------

GIẤY ĐỀ NGHỊ KHÁM GIÁM ĐỊNH

Kính gửi:..........
Tên tôi là: ..........
Ngày, tháng, năm sinh: ..........
Chỗ ở hiện tại: ..........
Giấy Chứng minh nhân dân/Thẻ căn cước/Hộ chiếu số: ..........
Ngày cấp: ..........Nơi cấp:..........
Số sổ bảo hiểm xã hội/Mã số bảo hiểm xã hội (1): ..........
Nghề/Công việc (2):..........
Điện thoại liên hệ: ..........
Đề nghị được giám định mức độ suy giảm khả năng lao động:

Đề nghị giám định (3): ..........
Loại hình giám định (4): ..........
Nội dung giám định (5): ..........
Đang hưởng chế độ (6): ..........
Xác nhận của UBND hoặc Công an cấp xã (7)

Người đề nghị

(Ký, ghi rõ họ tên)

Output:
(Dùng cho cha, mẹ học sinh tiểu học học bán trú tại các trường phổ thông ở xã, thôn đặc biệt khó khăn)

Kính gửi Trường: ..........
Họ và tên: ..........
Là Cha/mẹ (hoặc người giám hộ, nhận nuôi) của em: ..........
Sinh ngày .......... tháng .......... năm ..........
Dân tộc: .......... thuộc hộ nghèo (có/không): ..........
Thường trú tại thôn/bản .......... xã ..........
thuộc vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn.
Huyện: .......... Tỉnh: ..........
Năm học: .......... Là học sinh lớp: .......... Trường: ..........

Vì lý do (chọn 1 trong 2 lý do sau):

Nhà ở xa trường (ghi rõ cách nơi học tập bao nhiêu km): ..........
Địa hình giao thông khó khăn (có/không): ..........
Nên em .......... không thể đi đến trường và trở về nhà trong ngày.
Tôi làm đơn này đề nghị các cấp quản lý xem xét, để em .......... được hưởng chính sách hỗ trợ tiền và gạo theo quy định tại Nghị định số ........../2016/NĐ-CP ngày .......... tháng .......... năm 2016 của Chính phủ.
.........., ngày .......... tháng .......... năm 20..........

Người làm đơn
(Ký, ghi rõ họ, tên hoặc điểm chỉ)

Input:
{inputs}
Output:

'''

#===============File path==================
# Input File path
Input_Raw_Folder = "Forms/Input/Raw" #Raw input folder
Input_Hand_process_Folder = "Forms/Input/Hand_process" #Hand process input folder

# Output File path (Extracted from LLM filled --> pass to output)
Output_folder = "Forms/Output"
# Evaluate File path
Evaluate_folder = "Forms/Evaluate"
Process_ouput_folder = "Forms/Process_ouput"

# Label by Hand File path Label_Output_By_Hand (label by LLM in future)
Label_by_hand_Raw_Folder = "Forms/Label_Output_By_Hand/Raw"
Label_by_hand_Hand_process_Folder = "Forms/Label_Output_By_Hand/Hand_process"

# LLM filled form File path
LLM_filled_form_1_Folder = "Forms/Result_LLM_Filled/Hung_19_Oct_2024" #Result1
LLM_filled_form_2_Folder = "Forms/Result_LLM_Filled/Hung_04_Nov_2024" #Result1

# Summary
Input_folder = [Input_Raw_Folder, Input_Hand_process_Folder]
Label_folder =[Label_by_hand_Raw_Folder, Label_by_hand_Hand_process_Folder]
LLM_filled_folder = [LLM_filled_form_1_Folder, LLM_filled_form_2_Folder]







a = "hello world"



    