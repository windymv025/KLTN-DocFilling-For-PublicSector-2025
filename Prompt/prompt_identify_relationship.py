relationship = """

"""

template_identify_relationship_prompt = """
Instruction for Defining Relationships:

For each relationship field in the form, follow these steps:

1. Identify Users and Context:

Determine the roles of the users indicated by the tags (e.g., [userX] and [userY]). Understand the context of the form to identify the potential relationships (e.g., "Father," "Mother," "Parent," "Child").
2.Analyze Potential Relationships:

Consider whether a direct relationship exists between the two users based on their roles in the form. For example, if one user is identified as the parent of another, the relationship is "Parent."
3. Determine and Specify the Relationship:

If a direct relationship exists, specify it clearly (e.g., "Parent" for a parent-child relationship).
If no direct relationship exists between the users, write [not_relationship].
4. Output the Relationships:

For each relationship field, output the determined relationship in the format [userX_relationship_userY]: [relationship].

<Example>
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
[user3_relationship_user2]: [mother-child]
[user4_relationship_user2]: [father-child]
</Example>

<Example>
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
</Example>

<Example>
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
[user1_relationship_user2]: Parent
</Example>

<Example>
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
</Example>

Form:
{form}
Answer:
"""