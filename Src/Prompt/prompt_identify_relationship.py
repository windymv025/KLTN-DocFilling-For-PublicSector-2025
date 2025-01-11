relationship = """

"""

template_identify_relationship_prompt = """
Instructions for Defining Relationships:
1. Identify Users and Context:

Identify Users: Determine the roles of users based on the tags (e.g., [user1], [user2], [user3]). Ensure that the user indices (X, Y) are sequential and correctly ordered (e.g., 1-2, 1-3, 2-3).
Understand the Context: Analyze the context of the form to understand potential relationships (e.g., "Father," "Mother," "Child").
2. Analyze Potential Relationships:

Assess Relationships: Evaluate whether a direct relationship exists between the identified users based on their roles. For instance, if user1 is the father of user2, the relationship is "child-father."
Consider Relationship Direction: Ensure the relationship is properly ordered. For example:
If user1 is the parent of user2, output [user1_relationship_user2]: [parent-child].
If user1 is the child of user2, output [user1_relationship_user2]: [child-parent].
3. Determine and Specify the Relationship:

Direct Relationship: If a direct relationship is identified, clearly specify it (e.g., "parent-child," "sibling").
No Direct Relationship: If no direct relationship exists between the users, output [userX_relationship_userY]: [not_relationship].
4. Output the Relationships:

Format the Output: For each relationship field, output the determined relationship in the format [userX_relationship_userY]: [relationship].
Single User Case: If only one user is present, output only the user information without relationships.

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: [another]
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
Làm tại: [another], ngày [another] tháng [another] năm [another]
Answer:
[user1_relationship_user2]: [not_relationship]
[user1_relationship_user3]: [not_relationship]
[user1_relationship_user4]: [not_relationship]
[user2_relationship_user3]: [child-mother]
[user2_relationship_user4]: [child-father]
[user3_relationship_user4]: [wife-husband]

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ
Kính gửi(1): [another]
1. Họ, chữ đệm và tên:	[user1_full_name]
2. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/ [user1_dob_year]       3. Giới tính: [user1_gender]
4. Số định danh cá nhân: [user1_id_number]											
5. Số điện thoại liên hệ: [user1_phone] 6. Email:	[user1_email]
7. Họ, chữ đệm và tên chủ hộ: [user2_full_name] 8. Mối quan hệ với chủ hộ: [another]
9. Số định danh cá nhân của chủ hộ:	[user2_id_number]											
10. Nội dung đề nghị(2): [another]
Answer:
[user1_relationship_user2]: [not_relationship]

Form:
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
[another], ngày [another] tháng [another] năm [another]
Answer:
Form has only 1 user

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ HỖ TRỢ HỌC TẬP 
(Dùng cho cha mẹ trẻ mẫu giáo hoặc người chăm sóc trẻ mẫu giáo học tại các cơ sở giáo dục công lập)
Kính gửi: [another] (Cơ sở giáo dục)
Họ và tên cha mẹ (hoặc người chăm sóc): [user1_full_name]
Hộ khẩu thường trú tại: [user1_permanent_address]
Là cha/mẹ (hoặc người chăm sóc) của em: [user2_full_name]
Sinh ngày: [user2_dob]
Dân tộc: [user2_ethnicity]
Hiện đang học tại lớp: [user2_class_name]
Trường: [user2_school_name]
Tôi làm đơn này đề nghị các cấp quản lý xem xét, giải quyết cấp tiền hỗ trợ học tập theo quy định và chế độ hiện hành./.
 
XÁC NHẬN CỦA ỦY BAN NHÂN DÂN CẤP XÃ1
Nơi trẻ mẫu giáo có hộ khẩu thường trú
(Ký tên, đóng dấu)	[another],ngày [another] tháng [another] năm [another]
Người làm đơn
(Ký, ghi rõ họ tên)
Answer:
[user1_relationship_user2]: [parent-child]



Form:
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
     Độc lập - Tự do - Hạnh phúc 

TỜ KHAI ĐĂNG KÝ NHẬN CHA, MẸ, CON

Kính gửi: (1) [another]

Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Ngày, tháng, năm sinh: [user1_dob]
Nơi cư trú: (2) [user1_current_address]

Giấy tờ tùy thân: (3) [user1_id]

Quan hệ với người nhận cha/mẹ/con: (4) [another]
Đề nghị cơ quan công nhận người có tên dưới đây:
Họ, chữ đệm, tên:       [user2_full_name]
Ngày, tháng, năm sinh:  [user2_dob]
Giới tính: (2) [user2_gender] Dân tộc: (2) [user2_ethnicity] Quốc tịch: (2) [user2_nationality]
Nơi cư trú: (2) [user2_current_address]

Giấy khai sinh/Giấy tờ tùy thân: (3) [user2_id]

Là [another] của người có tên dưới đây:
Họ, chữ đệm, tên: [user3_full_name]
Ngày, tháng, năm sinh: [user3_dob]
Giới tính: (2) [user3_gender] Dân tộc: (2) [user3_ethnicity] Quốc tịch: (2) [user3_nationality]
Nơi cư trú: (2) [user3_current_address]

Giấy khai sinh/Giấy tờ tùy thân: (3) [user3_id]

Tôi cam đoan việc nhận [another] nói trên là đúng sự thật, tự nguyện, không có tranh chấp và chịu trách nhiệm trước pháp luật về cam đoan của mình.
Làm tại [another] ngày [another] tháng [another] năm [another]
Người yêu cầu
(Ký, ghi rõ họ, chữ đệm, tên)
Answer:
[user1_relationship_user2]: [not_relationship]
[user1_relationship_user3]: [not_relationship]
[user2_relationship_user3]: [not_relationship]

Form:
I.      Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): [user1_full_name]    [02]. Giới tính: [user1_gender]
[03]. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]   [04]. Quốc tịch: [user1_nationality]
[05]. Dân tộc: [user1_ethnicity]        [06]. Số CCCD/ĐDCN/Hộ chiếu: [user1_id_number]
[07]. Điện thoại: [user1_phone] [08]. Email (nếu có): [user1_email]
[09]. Nơi đăng ký khai sinh: [09.1]. Xã: [user1_birth_registration_place_ward]  [09.2]. Huyện: [user1_birth_registration_place_district] [09.3]. Tỉnh: [user1_birth_registration_place_province]
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): [user2_full_name]
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: [another]
[12]. Số nhà, đường/phố, thôn/xóm: [user1_current_address]
[13]. Xã: [user1_current_address_ward]  [14]    Huyện: [user1_current_address_district] [15]. Tỉnh: [user1_current_address_province]
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
Answer:
[user1_relationship_user2]: [parent-child]

Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI

Kính gửi: [receiver]

Tôi tên là: [user1_full_name]
Cơ quan quản lý trực tiếp (nếu có): [user1_organization]

Quyết định cử đi học số [user1_decision_number] ngày [user1_decision_day] tháng [user1_decision_month] năm [user1_decision_year] của  [user1_decision_issuer]
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
Answer:
Form has only 1 user

Form:
{form}
Answer:
"""