personal_information_tagnames = """
[full_name]: Full name of the user.
[alias_name]: Alternate name of the user.
[dob_day]: Day of birth of the user.
[dob_month]: Month of birth of the user.
[dob_year]: Year of birth of the user.
[dob]: Date of birth (day, month, year) of the user.
[dob_text]: Date of birth (day, month, year) of the user is written by text
[gender]: Gender of the user.
[id_number]: ID card number of the user.
[ethnicity]: Ethnicity of the user.
[religion]: Religion of the user.
[nationality]: Nationality of the user.
[marital_status]: Marital status of the user.
[blood_type]: Blood type of the user.
[birth_registration_place]: Birth registration place of the user.
[birth_registration_place_ward]: Birth registration place ward of the user.
[birth_registration_place_district]: Birth registration place district of the user.
[birth_registration_place_province]: Birth registration place province of the user.
[hometown]: Hometown of the user.
[permanent_address]: Permanent address of the user.
[current_address]: Current address of the user.
[current_address_ward]: Current address ward of the user. 
[current_address_district]: Current address ward of the user.
[current_address_province]: Current address ward of the user.
[occupation]: Occupation of the user.
[education_level]: Education level of the user.
[class]: Class name of the user.
[school]:School name of the user.
[course]: Course of the the user.
[faculty]: Faculty of the the user.
[phone]: Phone mobile of the user
[phone_home]: Phone home of the user
[email]: Email of the user
[driving_license_number]: driving license number of the user
"""

remaining_tag_names = """
[receiver]: The individual or organization that will receive or process the form filled out by the user.
[request_content]: The specific content or request made by the user in the form. This could be details about what the form is being submitted for, such as a request for a new ID card, a change in personal information, etc.
[day]: day when the form is filled out by the user.
[month]: month when the form is filled out by the user.
[year]: year the form is filled out by the user.
[place]: Place where the form is filled out by the user.
[reason]: Reason when the user is filled out form.
"""

template_PI_prompt = """
You have been provided with a form that contains placeholders (........) to be filled in with personal information. Below is a list of tag names that represent different types of personal information:

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