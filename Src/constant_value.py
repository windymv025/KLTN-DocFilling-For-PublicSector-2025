### 0. ------------------DEFAULT------------------###
API_KEY = "AIzaSyBRWVbQgcq1F5-1jXqIGC30MQ1ASMSaM50" #Gemini API key

#abc
template_generate_tagname_without_predefined_tagname = """
You are tasked with filling out various forms using predefined tagnames, replacing all placeholders (..........) with the correct tagname. The tagnames will follow a specific pattern.
But if you encounter new fields that don't have predefined tagnames, design a new tagname based on the field’s context.  
There are two important rules:
1. User-specific tagnames: If a tagname follows the format userX_tagname (e.g., user1_full_name, user2_dob_day,...), use the corresponding user-specific information.
2. General tagnames: If the tagname does not belong to a user (such as day, month, year, or receiver,...), fill in that tagname directly without associating it with any user.
3. Replace all placeholders: Every occurrence of ".........." must be replaced with an appropriate tagname, whether it is user-specific or a general tagname.
<Example>
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
</Example>
Form:
{form}
Answer:

"""

specific_tagnames = """
[full_name]: Họ và tên của người dùng.
Sử dụng khi cần điền họ và tên đầy đủ vào biểu mẫu.
[alias_name]: Tên khác (bí danh) của người dùng.
Sử dụng khi biểu mẫu yêu cầu cung cấp tên gọi khác hoặc bí danh.
[dob]: Ngày tháng năm sinh của người dùng.
Sử dụng khi cần điền ngày tháng năm sinh đầy đủ dạng số (ngày, tháng, năm).
[dob_text]: Ngày tháng năm sinh của người dùng (dạng chữ).
Sử dụng khi biểu mẫu yêu cầu viết ngày tháng năm sinh bằng chữ.
[dob_day]: Ngày sinh của người dùng.
Sử dụng khi cần điền riêng ngày sinh.
[dob_month]: Tháng sinh của người dùng.
Sử dụng khi cần điền riêng tháng sinh.
[dob_year]: Năm sinh của người dùng.
Sử dụng khi cần điền riêng năm sinh.
[gender]: Giới tính của người dùng.
Sử dụng khi biểu mẫu yêu cầu giới tính (nam/nữ).
[id_number]: Số chứng minh nhân dân hoặc căn cước công dân của người dùng. 
.Sử dụng khi cần điền số CMND/CCCD.
[id_issue_date]: Ngày tháng năm cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần ghi đầy đủ ngày, tháng, năm cấp CMND/CCCD.
[id_issue_day]: Ngày cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần điền riêng ngày cấp CMND/CCCD.
[id_issue_month]: Tháng cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần điền riêng tháng cấp CMND/CCCD.
[id_issue_year]: Năm cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần điền riêng năm cấp CMND/CCCD.
[id_issue_place]: Nơi cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần ghi nơi cấp CMND/CCCD (ví dụ: tỉnh/thành phố, cơ quan công an).
[ethnicity]: Dân tộc của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu dân tộc.
[religion]: Tôn giáo của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu tôn giáo.
[nationality]: Quốc tịch của người dùng. 
.Sử dụng khi cần điền quốc tịch.
[marital_status]: Tình trạng hôn nhân của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu điền tình trạng hôn nhân (độc thân, đã kết hôn, ly hôn...).
[blood_type]: Nhóm máu của người dùng. 
.Sử dụng khi cần cung cấp nhóm máu (A, B, AB, O).
[birth_registration_place]: Nơi đăng ký khai sinh của người dùng. 
.Sử dụng khi cần điền nơi đăng ký khai sinh.
[birth_registration_place_ward]: Phường/xã nơi đăng ký khai sinh của người dùng. 
.Sử dụng khi cần điền phường/xã đăng ký khai sinh.
[birth_registration_place_district]: Quận/huyện nơi đăng ký khai sinh của người dùng. 
.Sử dụng khi cần điền quận/huyện đăng ký khai sinh.
[birth_registration_place_province]: Tỉnh/thành phố nơi đăng ký khai sinh của người dùng. 
.Sử dụng khi cần điền tỉnh/thành phố đăng ký khai sinh.
[hometown]: Quê quán của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu quê quán.
[permanent_address]: Địa chỉ thường trú của người dùng. 
.Sử dụng khi cần cung cấp địa chỉ thường trú.
[current_address]: Địa chỉ tạm trú của người dùng. 
.Sử dụng khi cần cung cấp địa chỉ tạm trú hiện tại.
[current_address_ward]: Phường/xã nơi tạm trú của người dùng. 
.Sử dụng khi cần điền phường/xã tạm trú.
[current_address_district]: Quận/huyện nơi tạm trú của người dùng. 
.Sử dụng khi cần điền quận/huyện tạm trú.
[current_address_province]: Tỉnh/thành phố nơi tạm trú của người dùng. 
.Sử dụng khi cần điền tỉnh/thành phố tạm trú.
[occupation]: Nghề nghiệp của người dùng. 
.Sử dụng khi biểu mẫu yêu cầu điền nghề nghiệp hiện tại.
[passport_number]: Số hộ chiếu của người dùng.
Ghi rõ số hộ chiếu để xác định danh tính và quốc tịch của người dùng.
[passport_issue_day]: Ngày cấp hộ chiếu của người dùng.
Ghi ngày cụ thể khi hộ chiếu được cấp.
[passport_issue_month]: Tháng cấp hộ chiếu của người dùng.
Ghi tháng khi hộ chiếu được cấp.
[passport_issue_year]: Năm cấp hộ chiếu của người dùng.
Ghi năm khi hộ chiếu được cấp.
[passport_issue_date]: Ngày, tháng, năm cấp hộ chiếu của người dùng.
Ghi đầy đủ ngày cấp hộ chiếu để dễ dàng tham khảo.
[passport_issue_place]: Nơi cấp hộ chiếu của người dùng.
Ghi tên cơ quan hoặc địa điểm nơi cấp hộ chiếu.
[passport_expiry_date]: Ngày hết hạn của hộ chiếu.
Ghi rõ ngày mà hộ chiếu sẽ hết hạn để người dùng có thể quản lý và gia hạn khi cần thiết.
[social_insurance_number]: Số sổ bảo hiểm xã hội của người dùng.
Dùng để xác định quyền lợi và nghĩa vụ của người dùng trong hệ thống bảo hiểm xã hội.
[health_insurance_card_number]: Số thẻ bảo hiểm y tế của người dùng.
Ghi rõ số thẻ bảo hiểm y tế để quản lý các dịch vụ chăm sóc sức khỏe của người dùng.
[health_insurance_registration_place]: Nơi đăng ký bảo hiểm y tế của người dùng.
Ghi tên cơ quan hoặc địa điểm nơi người dùng đã đăng ký bảo hiểm y tế.
[phone_number]: Số điện thoại của người dùng.
Sử dụng khi cần ghi số điện thoại di động hoặc chính của người dùng.
[phone_home_number]: Số điện thoại nhà của người dùng.
Sử dụng khi cần ghi số điện thoại cố định tại nhà.
[email]: Địa chỉ email của người dùng.
Sử dụng khi cần ghi địa chỉ email liên hệ của người dùng.
[fax_number]: Số fax của người dùng.
Sử dụng khi cần ghi số fax của người dùng.
[relationship_user2]: Mối quan hệ với người dùng.
.Sử dụng khi cần điền mối quan hệ với người dùng khác (ở đây là user2)
[academic_level]: Trình độ học tập hiện tại của người dùng (ví dụ: sinh viên năm nhất, năm hai, năm ba, năm tư).
Sử dụng khi cần ghi rõ cấp độ học tập theo hệ thống năm học.
[school_year]: Năm học của người dùng (ví dụ: 2024-2025).
Sử dụng khi cần ghi rõ năm học cụ thể mà sinh viên hoặc học sinh đang theo học.
[enrollment_year]: Năm nhập học của sinh viên.
Sử dụng khi bạn cần ghi rõ năm mà sinh viên bắt đầu học tại cơ sở giáo dục, giúp phân biệt các khóa khác nhau (ví dụ: khóa 2021, khóa 2022, v.v.). Thường để trả lời sinh viên khóa nào?
[class]: Lớp học của người dùng.
Sử dụng khi cần ghi tên hoặc mã lớp mà sinh viên hoặc học sinh đang học.
[school]: Trường học của người dùng.
Sử dụng khi cần ghi tên trường mà sinh viên hoặc học sinh đang theo học.
[course]: Khóa học mà người dùng đang tham gia.
Sử dụng khi cần ghi tên hoặc mã khóa học cụ thể mà sinh viên hoặc học sinh đăng ký.
[faculty]: Khoa hoặc bộ môn của người dùng.
Sử dụng khi cần ghi khoa hoặc bộ môn mà sinh viên đang theo học.
[student_id_number]: Mã số sinh viên của người dùng.
Sử dụng khi cần ghi mã số sinh viên do trường cấp.
[education_level]: Trình độ giáo dục của người dùng.
Sử dụng khi cần ghi trình độ học vấn (ví dụ: đại học, thạc sĩ, tiến sĩ).
[duration_of_course]: Thời gian học của khóa học.
Sử dụng khi cần ghi tổng thời gian học tập của một khóa học (ví dụ: 4 năm).
[graduation_date]: Ngày tốt nghiệp của người dùng.
Sử dụng khi cần ghi rõ ngày tốt nghiệp của sinh viên hoặc học sinh.
[degree]: Bằng cấp mà người dùng đang theo đuổi hoặc đã đạt được.
Sử dụng khi cần ghi rõ loại bằng cấp (ví dụ: Cử nhân, Thạc sĩ).
[grade]: Điểm số hoặc thành tích mà người dùng đạt được.
Sử dụng khi cần ghi điểm hoặc xếp hạng học tập.

[semester]: Học kỳ mà người dùng đang tham gia hoặc đang nói đến.
Sử dụng khi cần ghi rõ học kỳ cụ thể (ví dụ: Học kỳ 1, Học kỳ 2).

[supervisor_name]: Tên giảng viên hướng dẫn của người dùng.
Sử dụng khi cần ghi rõ tên giảng viên hướng dẫn hoặc cố vấn học tập.

[school_address]: Địa chỉ của trường mà người dùng đang theo học.
Sử dụng khi cần ghi rõ địa chỉ của trường học.

[school_phone]: Số điện thoại của trường mà người dùng đang theo học.
Sử dụng khi cần ghi số điện thoại liên hệ của trường học.

[policy_object]: Đối tượng chính sách của người dùng.
Sử dụng khi cần ghi rõ đối tượng thuộc chính sách nào (ví dụ: học bổng, chính sách xã hội).

[direct_management_agency]: Cơ quan quản lý trực tiếp của người dùng (nếu có).
Ghi cơ quan quản lý trực tiếp người dùng.

[study_decision_number]: Số quyết định cử đi học.
Ghi số quyết định liên quan đến việc cử đi học.

[study_decision_day], [study_decision_month], [study_decision_year]: Ngày, tháng, năm của quyết định cử đi học.
Ghi ngày tháng năm quyết định được ban hành.

[study_decision_issuer]: Cá nhân hoặc tổ chức ký quyết định cử đi học.
Ghi tên người/tổ chức có thẩm quyền ký quyết định.

[study_abroad_duration]: Thời gian học tập ở nước ngoài.
Ghi tổng thời gian học tại nước ngoài.

[extension_start_month], [extension_start_year], [extension_end_month], [extension_end_year]: Thời gian gia hạn học tập ở nước ngoài.
Ghi rõ thời gian bắt đầu và kết thúc gia hạn.

[graduation_date]: Ngày tốt nghiệp.
Ghi ngày tháng năm tốt nghiệp của người dùng.

[return_date]: Ngày về nước.
Ghi ngày tháng năm về nước.

[foreign_institution_name]: Tên cơ sở giáo dục nước ngoài.
Ghi tên trường hoặc tổ chức giáo dục nước ngoài mà người dùng đã học.

[thesis_title]: Tên đề tài luận văn thạc sĩ hoặc luận án tiến sĩ.
Ghi tên đề tài nghiên cứu của người dùng.

[supervisor_info]: Tên và học hàm, học vị của người hướng dẫn.
Ghi thông tin về giảng viên hướng dẫn của người dùng.

[supervisor_evaluation]: Đánh giá của cơ sở giáo dục hoặc giáo sư hướng dẫn.
Ghi ý kiến đánh giá của giảng viên hoặc trường học.

[user1_discipline] : Ghi rõ mức độ kỷ luật nếu có của người dùng.
Dùng để ghi rõ kỷ luật của người người dùng, cũng như xác định xem họ có bị kỷ luật nào hay không.

[total_modules_or_credits]: Tổng số môn học hoặc tín chỉ của người dùng.
Ghi tổng số môn học hoặc tín chỉ mà người dùng cần hoàn thành trong chương trình học.

[modules_or_credits_first_semester_year1]: Số môn học hoặc tín chỉ trong học kỳ đầu năm thứ nhất của người dùng.
Ghi số môn học hoặc tín chỉ mà người dùng trong học kỳ đầu tiên của năm học đầu tiên.

[modules_or_credits_second_semester_year1]: Số môn học hoặc tín chỉ trong học kỳ thứ hai năm thứ nhất của người dùng.
Ghi số môn học hoặc tín chỉ mà người dùng trong học kỳ thứ hai của năm học đầu tiên.

[request]: Nguyện vọng hoặc đề nghị của người dùng.
Ghi rõ nguyện vọng hoặc yêu cầu của người dùng trong báo cáo.

[workplace]: Cơ quan công tác.
Ghi tên cơ quan làm việc của người dùng.

[workplace_address]: Địa chỉ của cơ quan công tác.
Ghi rõ địa chỉ nơi làm việc.

[recommendation]: Kiến nghị, đề xuất.
Ghi rõ các kiến nghị hoặc đề xuất của người dùng.

[reason]: Lý do đề nghị.
Ghi rõ lý do mà người dùng đề nghị.

[bank_account]: Số tài khoản ngân hàng của người dùng.
Ghi số tài khoản để thực hiện các giao dịch tài chính và thanh toán.

[bank_name]: Tên ngân hàng của người dùng.
Ghi tên ngân hàng nơi người dùng có tài khoản.

[parent_name]: Tên phụ huynh của người dùng.
Dùng để ghi rõ thông tin về phụ huynh, có thể cần cho các thủ tục hành chính hoặc liên hệ.

[driving_license_number]: Số giấy phép lái xe của người dùng.
Ghi rõ số giấy phép lái xe mà người dùng đã được cấp.

[driving_license_issuer]: Cơ quan cấp giấy phép lái xe.
Tên tổ chức hoặc cơ quan đã cấp giấy phép lái xe cho người dùng.

[driving_license_place]: Nơi cấp giấy phép lái xe.
Địa điểm cụ thể nơi người dùng đã nhận giấy phép lái xe.

[driving_license_issue_day], [driving_license_issue_month], [driving_license_issue_year]: Ngày, tháng, năm cấp giấy phép lái xe.
Thông tin ngày cấp giấy phép lái xe, cần ghi rõ từng phần để tránh nhầm lẫn.

[driving_license_category]: Loại giấy phép lái xe (A, B, C,...).
Chỉ rõ loại giấy phép mà người dùng đã được cấp, giúp phân loại theo quy định giao thông.
"""

cccd_passport_tagnames = """
[full_name]: Họ và tên của người dùng.
Sử dụng khi cần điền họ và tên đầy đủ vào biểu mẫu. 
[alias_name]: Tên khác (bí danh) của người dùng.
Sử dụng khi biểu mẫu yêu cầu cung cấp tên gọi khác hoặc bí danh.
[dob]: Ngày tháng năm sinh của người dùng.
Sử dụng khi cần điền ngày tháng năm sinh đầy đủ dạng số (ngày, tháng, năm). Ví dụ các chỗ như ngày tháng năm sinh: .....
[dob_text]: Ngày tháng năm sinh của người dùng (dạng chữ). 
Sử dụng khi biểu mẫu yêu cầu viết ngày tháng năm sinh bằng chữ. Ví dụ các chỗ như ngày tháng năm sinh (bằng chữ): .....
[dob_day],[dob_month],[dob_year]: Ngày sinh, tháng sinh, năm sinh riêng của người dùng.
Sử dụng khi cần điền riêng ngày sinh, riêng tháng sinh hoặc riêng năm sinh. Ví dụ như ngày sinh: ..... tháng sinh: ..... năm sinh: .....
[gender]: Giới tính của người dùng.
Sử dụng khi biểu mẫu yêu cầu giới tính (nam/nữ). Ví dụ như giới tính (nam/nữ):.....
[id_number]: Số chứng minh nhân dân hoặc căn cước công dân của người dùng. Hay giấy tờ tùy thân
.Sử dụng khi cần điền số CMND/CCCD. Ví dụ: số CMND/CCCD: ....., hay số CCCD: ....., số định danh cá nhân: ...., giấy tờ tùy thân: .....
[id_issue_date]: Ngày tháng năm cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần ghi đầy đủ ngày, tháng, năm cấp CMND/CCCD. Ví dụ như ngày cấp (cccd): ..... đứng một mình (sau đó không có tháng, năm), thì hiểu là cần điền date (đầy đủ). 
[id_issue_day],[id_issue_month],[id_issue_year]: Ngày cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần điền riêng ngày cấp, riêng tháng cấp, năm cấp CMND/CCCD. Ví dụ như ngày cấp (cccd): ..... tháng cấp (cccd): ..... năm cấp(cccd): .....
[id_issue_place]: Nơi cấp số chứng minh nhân dân hoặc căn cước công dân.
Sử dụng khi cần ghi nơi cấp CMND/CCCD (ví dụ: tỉnh/thành phố, cơ quan công an). ví dụ như nơi cấp (cccd): .....
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
.Sử dụng khi cần cung cấp địa chỉ tạm trú hiện tại. Ví dụ như địa chỉ tạm trú: .....
[current_address_ward],[current_address_district],[current_address_province]: Phường/xã, huyện, tỉnh nơi tạm trú của người dùng. 
.Sử dụng khi cần điền phường/xã, huyện, tỉnh tạm trú. Ví dụ như phường/xã: ...., huyện: ...., tỉnh: ....
[occupation]: Nghề nghiệp của người dùng. Hay có thể là hiện trạng hiện nay.
.Sử dụng khi biểu mẫu yêu cầu điền nghề nghiệp hiện tại. Ví dụ như nghề nghiệp: ....., Hiện nay là: .....
[passport_number]: Số hộ chiếu của người dùng.
Ghi rõ số hộ chiếu để xác định danh tính và quốc tịch của người dùng. Ví dụ như số hộ chiếu: .....
[passport_issue_date]: Ngày, tháng, năm đầy đủ hộ chiếu của người dùng.
Ghi đầy đủ ngày cấp hộ chiếu để dễ dàng tham khảo. Ví dụ như ngày cấp: .... đứng một mình (sau đó không có tháng, năm), thì hiểu là cần điền date (đầy đủ).
[passport_issue_day],[passport_issue_month],[passport_issue_year]: Ngày cấp, tháng cấp, năm cấp hộ chiếu của người dùng.
Ghi ngày cụ thể, tháng cụ thể, năm cụ thể khi hộ chiếu được cấp. Ví dụ như ngày cấp: ...., tháng cấp: ...., năm cấp: ....
[passport_issue_place]: Nơi cấp hộ chiếu của người dùng.
Ghi tên cơ quan hoặc địa điểm nơi cấp hộ chiếu. Ví dụ như nơi cấp: .....
[passport_expiry_date]: Ngày hết hạn của hộ chiếu.
Ghi rõ ngày mà hộ chiếu sẽ hết hạn để người dùng có thể quản lý và gia hạn khi cần thiết. Ví dụ như ngày hết hạn: ....
"""

list_cccd_passport_tagnames = [
"[full_name]",
"[alias_name]",
"[dob]",
"[dob_text]",
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
"[occupation]",
"[passport_number]",
"[passport_issue_date]",
"[passport_issue_day]",
"[passport_issue_month]",
"[passport_issue_year]",
"[passport_issue_place]",
"[passport_expiry_date]"
]

list_general_tagnames = ["[receiver]","[place]","[day]","[month]","[year]"]

general_tagnames = """
[receiver]: Người nhận biểu mẫu. 
.Sử dụng khi biểu mẫu yêu cầu ghi tên người hoặc cơ quan tiếp nhận. Ví dụ như người nhận: ..... hay kính gửi: .....
[place],[day],[month],[year]: Địa điểm, ngày tháng năm điền được điền bởi người dùng.
.Sử dụng khi cần điền nơi điền biểu mẫu, hay ngày tháng năm làm, thường ở đầu trang hay cuối trang,
nơi mà có ....., ngày ..... tháng ..... năm .....
"""

template_generate_tagname_with_predefined_tagname = """
Bạn chịu trách nhiệm xác định tên thẻ (tagname) chính xác cho mỗi chỗ trống trong biểu mẫu. Nhiệm vụ của bạn là đảm bảo rằng mọi chỗ trống trong biểu mẫu đều được thay thế chính xác bằng tên thẻ tương ứng, dựa trên các tagnames của userX và các tagnames chung được cung cấp. Nếu một chỗ trống không khớp với bất kỳ tên thẻ nào đã được định nghĩa, hãy tạo một tên thẻ mới phù hợp.

Hãy tuân theo các quy tắc sau:
1. Tagnames cho từng người dùng: Nếu tagname theo định dạng userX_tagname (ví dụ: user1_full_name, user2_dob_day,...), hãy sử dụng thông tin cụ thể tương ứng với người dùng đó. 
Một số ví dụ về tagnames cho từng người dùng và giải thích của nó: 
{specific_tagnames}
2. Tagnames chung: Nếu tagname không thuộc về một người dùng cụ thể (như day, month, year, hoặc receiver,...), hãy điền trực tiếp tên thẻ đó mà không cần liên kết với bất kỳ người dùng nào. 
Một số ví dụ về tagnames chung và giải thích của nó: 
{general_tagnames}
3. Đề xuất tagnames mới: Nếu không có tagname phù hợp từ danh sách cho một phần nào đó, hãy đề xuất một tagname mới theo cùng mẫu và ngữ cảnh. Đề xuất của bạn phải rõ ràng và dựa trên mục đích của trường dữ liệu.
4. Thay thế tất cả chỗ trống: Mọi sự xuất hiện của "#another" phải được thay thế bằng một tagname phù hợp, dù đó là tên thẻ cho người dùng cụ thể hay tên thẻ chung.
Example:
Input:
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): #another
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): #another
3. Ngày, tháng, năm sinh: #another/#another/#another; 4. Giới tính (Nam/nữ): #another
5. Số CMND/CCCD: #another
6. Dân tộc: #another; 7. Tôn giáo: #another 8. Quốc tịch: #another
9. Tình trạng hôn nhân: #another 10. Nhóm máu (nếu có): #another
11. Nơi đăng ký khai sinh: #another
12. Quê quán: #another
13. Nơi thường trú: #another
14. Nơi ở hiện tại: #another
15. Nghề nghiệp: #another 16. Trình độ học vấn: #another
#another, ngày #another tháng#another năm#another
Output:
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày sinh: [user1_dob]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id_number]
6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Quê quán: [user1_hometown]
13. Nơi thường trú: [user1_permanent_address]
14. Nơi ở hiện tại: [user1_current_address]
15. Nghề nghiệp: [user1_occupation] 16. Trình độ học vấn: [user1_education_level]
[place], ngày [day] tháng [month] năm [year]

Input:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: #another
Họ, chữ đệm, tên người yêu cầu: #another
Nơi cư trú: #another
Giấy tờ tùy thân: #another
Quan hệ với người được khai sinh: #another
Đề nghị cơ quan đăng ký khai sinh cho người dưới đây:
Họ, chữ đệm, tên: #another
Ngày, tháng, năm sinh: #another/#another/#another ghi bằng chữ: #another
Giới tính: #another Dân tộc: #another Quốc tịch: #another
Nơi sinh: #another
Quê quán: #another
Họ, chữ đệm, tên người mẹ: #another
Năm sinh: #another Dân tộc: #another Quốc tịch: #another
Nơi cư trú: #another
Họ, chữ đệm, tên người cha: #another
Năm sinh: #another Dân tộc: #another Quốc tịch: #another
Nơi cư trú: #another
Tôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.
Tôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.
     #another, ngày #another tháng #another năm #another

Output:
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
     [place], ngày [day] tháng [month] năm [year]
Input:
{form}
Output:
"""

template_generate_id_passport = """
You are tasked with filling in a form using specific tagnames. 
For any sections where no corresponding tagname exists, leave that section as-is and do not modify it.

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
{form}
Output:
"""

template_generate_each_placeholder = """
You will be provided with a form containing multiple blanks labeled (BlankX), and a list of two types of tagnames: User Tagnames and General Tagnames. 
After that, you will be asked to process a specific (BlankX) following the steps below:
Steps for Filling a Blank:
1. Check if the blank corresponds to user information:
- If it matches a userX_tagname from the list, return the correct user tagname.
2. If the blank does not correspond to user information, check if it matches a general tagname:
- If it matches, return the general tagname.
3. If the blank does not match any user or general tagname, return [another].

** Form:
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
BÁO CÁO TỐT NGHIỆP  
Kính gửi: (Blank1) 
1. Họ và tên:   (Blank2)
2. Số định danh cá nhân:        (Blank3)
3. Cơ quan quản lý trực tiếp (nếu có):  (Blank4)
4. Quyết định cử đi học số(Blank5) ngày(Blank6) tháng(Blank7) năm(Blank8) của(Blank9)
5. Thời gian học tập ở nước ngoài:      (Blank10)
....

List of Available Tagnames:
** User Tagnames (for specific users):
{cccd_passport_tagnames}
** General Tagnames (for general use):
{general_tagnames}

Example:
Input: Please process (Blank2) using the steps outlined above:
Output: 
For (Blank2):
Step 1: Does this correspond to user information? → Yes, it corresponds to [user1_full_name].
Result: (Blank2) => [user1_full_name]

Input: Please process (Blank4) using the steps outlined above:
Output:
For (Blank4):
Step 1: Check if it's user information (userX_tagname). → No
Step 2: Check if it's a general tagname. → No
Step 3: Return [another]
Result: (Blank4) => [another]

Form: 
{form}
Input:
{input}
Output:

"""

a = "hello world"

