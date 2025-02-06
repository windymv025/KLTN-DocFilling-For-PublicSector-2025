create_forms_template_prompt = """
Hãy tạo một form mới sử dụng các thông tin và tag name đã được cung cấp. 
- Tag name:  {tag_names}
- Các đặc trưng của form: {form_features}

# Yêu cầu
1 .Tính hợp lý:
- Form phải được thiết kế với bố cục rõ ràng, logic, phù hợp với mục đích sử dụng.
- Nội dung cần đảm bảo tính chính xác, phù hợp với các tình huống thực tế.

2. Sử dụng đúng tag name:
- Tích hợp các tag name đã được cung cấp vào các vị trí thích hợp trong form.
- Nếu cần thông tin mà chưa có tag name tương ứng, hãy bổ sung thêm tag mới với ý nghĩa rõ ràng, phù hợp với ngữ cảnh.

3. Tích hợp đặc trưng:
- Đảm bảo sử dụng các đặc trưng của form đã được liệt kê.
- Trong trường hợp không sử dụng hết các đặc trưng, hãy bổ sung nội dung mới nhưng phải liên quan và phù hợp với mục đích của form.

4. Ngữ pháp và định dạng:
- Nội dung form phải được trình bày ngắn gọn, mạch lạc, đúng ngữ pháp.
- Sử dụng định dạng chuyên nghiệp, dễ đọc, dễ hiểu.

5. Tính sáng tạo:
- Tạo ra các form có nội dung đa dạng, phù hợp với các tình huống thực tế như: yêu cầu cấp giấy tờ, thông báo thay đổi thông tin, khai báo bảo hiểm, đăng ký học tập, làm việc, v.v.
- Nội dung nên mang tính mới mẻ, hữu ích và có thể áp dụng được trong các trường hợp cụ thể.


# Ví dụ
```
			TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày, tháng, năm sinh: [user1_dob]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id_number]
6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Nơi thường trú: [user1_permanent_address]
13. Nơi ở hiện tại: [user1_current_address]
14. Nghề nghiệp: [user1_occupation] 15. Trình độ học vấn: [user1_education_level]
```

# Ví dụ
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
 
ĐƠN ĐỀ NGHỊ CẤP CHÍNH SÁCH NỘI TRÚ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi: [receiver] (Tên cơ sở giáo dục nghề nghiệp công lập)
Họ và tên:	[user1_full_name]
Ngày, tháng, năm sinh:	[user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number] cấp ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year] nơi cấp [user1_id_issue_place]
Lớp: [user1_class] Khóa: [user1_course] Khoa: [user1_faculty]
Mã số học sinh, sinh viên: [user1_student_id]
Thuộc đối tượng: [user1_student_type] (ghi rõ đối tượng được quy định tại Điều 2 Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp).
Căn cứ Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ, tôi làm đơn này đề nghị được Nhà trường xem xét để cấp chính sách nội trú theo quy định.

Xác nhận của Khoa
(Quản lý học sinh, sinh viên)	      [place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)

```

# Form mới:
"""

gen_forms_tagnames_label_forms = """
Bạn là một AI chuyên hỗ trợ xử lý các form tài liệu và điền thông tin vào form bằng các tagnames đã chọn trước. 
Dưới đây là danh sách các tagnames và ý nghĩa tương ứng:

Đầu tiên là danh sách tagnames ứng với user, được điền vào form theo dạng [userX_tagname]:
{formatted_tagnames}
Tiếp theo là các tagnames chung, được điền vào form theo dạng [tagname]:
{remaining_tag_names}

**Nhiệm vụ của bạn:**
1. Dựa trên danh sách tagnames và một số form đã được cung cấp (các form này có nhãn sẵn và những chỗ trống được thay bằng tagname [#another]), bạn sẽ:
- Tổng hợp lại các thông tin từ nhiều form để tạo thành một form mới, có sự khác biệt so với các form gốc.
- Có thể sáng tạo thêm nội dung, thêm bớt hoặc xóa bỏ một số phần để tạo ra sự đa dạng.
- Các mục trống không khớp với tagname có sẵn phải được thay bằng [#another]. Nếu phù hợp, bạn có thể tự đề xuất thêm tagnames mới.
- Một khi điền tagname vào thì phải đúng dạng [userX_tagname] nếu tagname thuộc đối tượng, [tagname] nếu là tagname chung, nếu không, hãy để là [#another].
2. Kết quả đầu ra (Output):
- Một form mới duy nhất được tạo ra, tổng hợp từ các form đã cung cấp.
- Form mới phải giữ cấu trúc hợp lý, sáng tạo và có nhãn đầy đủ (dùng các tagnames từ danh sách hoặc thêm hoặc [#another]).
	
Input:
'TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ\n(Dùng cho công dân Việt Nam định cư ở nước ngoài \nkhông có hộ chiếu Việt Nam còn giá trị sử dụng) \n\nKính gửi (1):[receiver]\n1. Họ, chữ đệm và tên Việt t Nam:[user1_full_name]\n2. Họ, chữ đệm và tên trong hộ chiếu/giấy tờ do nước ngoài cấp:\t[user1_foreign_name]\n3. Ngày, tháng, năm sinh:[user1_dob_day]/[user1_dob_month]/ [user1_dob_year]     4. Giới tính:\t[user1_gender]\n5. Dân tộc:[user1_ethnicity]     6. Tôn giáo:\t[user1_religion]\n7. Số định danh cá nhân/CMND: [user1_id_number]\t\t\t\t\t\t\t\t\t\n8. Số điện thoại (nếu có):[user1_phone]\t 9. E-mail (nếu có):[user1_email]\n10. Quốc tịch nước ngoài (nếu có):[user1_foreign_nationality]\n11. Số hộ chiếu/ Giấy tờ đi lại quốc tế do nước ngoài cấp/ Giấy tờ do cơ quan có thẩm quyền Việt Nam cấp:\nSố:\t[user1_passport_number] Ngày cấp: [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]\nCó giá trị đến ngày:[user1_passport_expiry_date] Do: [user1_passport_issue_place]\n12. Nghề nghiệp, nơi làm việc ở nước ngoài trước khi nhập cảnh Việt Nam:[user1_foreign_occupation]\n13. Họ, chữ đệm và tên, năm sinh, quốc tịch, nghề nghiệp, nơi làm việc, chỗ ở hiện nay của cha, mẹ, vợ, chồng, con:\n[user1_family_info]\n14. Nơi cư trú ở nước ngoài trước khi nhập cảnh Việt Nam:\t\n[user1_foreign_address]\n15. Nơi ở hiện tại ở Việt Nam:\t\n[user1_current_address]\n16. Nội dung đề nghị (2):\t\n[user1_request_content]\n17. Họ và tên chủ hộ:[user2_full_name]18. Quan hệ với chủ hộ:[user1_relationship_user2]\n19. Số định danh cá nhân/ CMND của chủ hộ:[user2_id_number]\t\t\t\t\t\t\t\t\t\t\n\n\t\n', '\t\t\tTỜ KHAI CĂN CƯỚC CÔNG DÂN\n1. Họ, chữ đệm và tên(1): [user1_full_name]\n2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]\n3. Ngày, tháng, năm sinh:[user1_dob_day]/[user1_dob_month]/[user1_dob_year]; 4. Giới tính (Nam/nữ): [user1_gender]\n5. Số CMND/CCCD: [user1_id_number]\n6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]\n9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]\n11. Nơi đăng ký khai sinh: [user1_birth_registration_place]\n12. Nơi thường trú: [user1_permanent_address]\n13. Nơi ở hiện tại: [user1_current_address]\n14. Nghề nghiệp: [user1_occupation] 15. Trình độ học vấn: [user1_education_level]'
Output:
TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ
(Dùng cho công dân Việt Nam định cư ở nước ngoài không có hộ chiếu Việt Nam còn giá trị sử dụng)

Kính gửi (1): [receiver]

Họ, chữ đệm và tên Việt Nam: [user1_full_name]
Họ, chữ đệm và tên trong hộ chiếu/giấy tờ do nước ngoài cấp: [user1_foreign_name]
Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
4. Giới tính: [user1_gender]
Dân tộc: [user1_ethnicity]
6. Tôn giáo: [user1_religion]
Số định danh cá nhân/CMND: [user1_id_number]
Số điện thoại (nếu có): [user1_phone]
9. Email (nếu có): [user1_email]
Quốc tịch nước ngoài (nếu có): [user1_foreign_nationality]
Số hộ chiếu/Giấy tờ đi lại quốc tế do nước ngoài cấp/Giấy tờ do cơ quan có thẩm quyền Việt Nam cấp:
Số: [user1_passport_number]
Ngày cấp: [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]
Có giá trị đến ngày: [user1_passport_expiry_date]
Do: [user1_passport_issue_place]
Nghề nghiệp, nơi làm việc ở nước ngoài trước khi nhập cảnh Việt Nam: [user1_foreign_occupation]
Họ, chữ đệm và tên, năm sinh, quốc tịch, nghề nghiệp, nơi làm việc, chỗ ở hiện nay của cha, mẹ, vợ, chồng, con: [user1_family_info]
Nơi cư trú ở nước ngoài trước khi nhập cảnh Việt Nam: [user1_foreign_address]
Nơi ở hiện tại ở Việt Nam: [user1_current_address]
Nội dung đề nghị: [user1_request_content]
Họ và tên chủ hộ: [user2_full_name]
Quan hệ với chủ hộ: [user1_relationship_user2]
Số định danh cá nhân/CMND của chủ hộ: [user2_id_number]

Input:
'CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM\n     Độc lập - Tự do - Hạnh phúc \n  \t\t\t    \t\nTỜ KHAI ĐĂNG KÝ CHẤM DỨT GIÁM HỘ\n\nKính gửi: (1) \t[receiver]\nHọ, chữ đệm, tên người yêu cầu:\t[user1_full_name]\nNgày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]\nNơi cư trú: (2)\t[user1_current_address]\nGiấy tờ tùy thân: (3)\t[user1_id_number]\nĐề nghị cơ quan đăng ký chấm dứt việc giám hộ giữa:\nNgười giám hộ: \nHọ, chữ đệm, tên: \t[user2_full_name]\nNgày, tháng, năm sinh:\t[user2_dob_day]/[user2_dob_month]/[user2_dob_year]\nGiới tính: (2)[user2_gender]Dân tộc: (2)[user2_ethnicity] Quốc tịch: (2)\t[user2_nationality]\nNơi cư trú(2): \t[user2_current_address]\nGiấy tờ tùy thân: (3) \t\t\n[user2_id_number]\t\nNgười được giám hộ: \nHọ, chữ đệm, tên: \t[user3_full_name]\nNgày, tháng, năm sinh: \t[user3_dob]\nGiới tính: (2)[user3_gender]Dân tộc: (2)[user3_ethnicity] Quốc tịch: (2)\t[user3_nationality]\nNơi cư trú (2): [user3_current_address]\t\n\t\nGiấy khai sinh/Giấy tờ tùy thân (3): \t[user3_id_number]\nĐã đăng ký giám hộ tại (4) \t[user1_guardianship_registration_place]\nngày [user1_guaardianship_registration_day] tháng [user1_guardianship_registration_month] năm [user1_guardianship_registration_year] số[user1_guardianship_registration_number]quyển số: [user1_guardianship_registration_volume]\t\nLý do chấm dứt việc giám hộ: \t[user1_reason]\nTôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.\n   Làm tại:[place], ngày [day] tháng [month] năm [year]', 'CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\nTỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH,\nBỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC\nKính gửi: [receiver]\nHọ, chữ đệm, tên người yêu cầu: [user1_full_name]\nNgày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]\nNơi cư trú: [user1_current_address]\nGiấy tờ tùy thân: [user1_id_number]\nQuan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch:[user1_relationship_user2]\nĐề nghị cơ quan đăng ký việc [user1_request_content]cho người có tên dưới đây:\nHọ, chữ đệm, tên: [user2_full_name]\nNgày, tháng, năm sinh: [user2_dob]\nGiới tính:[user2_gender]Dân tộc:[user2_ethnicity]Quốc tịch: [user2_nationality]\nNơi cư trú:  [user2_current_address]\nGiấy tờ tùy thân: [user2_id_number]\nĐã đăng ký  [user2_registration_type]tại[user2_registration_place] ngày[user2_registration_date]  số: [user2_registration_number] Quyển số:[user2_registration_volume]\nNội dung: [user2_request_content]\nLý do:[user2_reason]\nTôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.\nĐề nghị cấp bản sao: Có , Không ; số lượng:[user1_copy_request]bản\nLàm tại:[place], ngày [day] tháng [month] năm [year]\nNgười yêu cầu\n(Ký, ghi rõ họ, chữ đệm, tên)', 'TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ\n(Dùng cho công dân Việt Nam định cư ở nước ngoài \nkhông có hộ chiếu Việt Nam còn giá trị sử dụng) \n\nKính gửi (1):[receiver]\n1. Họ, chữ đệm và tên Việt Nam:[user r1_full_name]\n2. Họ, chữ đệm và tên trong hộ chiếu/giấy tờ do nước ngoài cấp:\t[user1_foreign_name]\n3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/ [user1_dob_year]     4. Giới tính:[user1_gender]\n5. Dân tộc:[user1_ethnicity]     6. Tôn giáo:[user1_religion]\n7. Số định danh cá nhân/CMND: [user1_id_number]\tNơi cấp: [user1_id_issue_place]\t\t\t\t\t\t\t\t\n8. Số điện thoại (nếu có):[user1_phone]\t 9. E-mail (nếu có):[user1_email]\n10. Quốc tịch nước ngoài (nếu có):[user1_foreign_nationality]\n11. Số hộ chiếu/ Giấy tờ đi lại quốc tế do nước ngoài cấp/ Giấy tờ do cơ quan có thẩm quyền Việt Nam cấp:\nSố:\t[user1_passport_number] Ngày cấp: [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]\nCơ quan cấp:[user1_passport_issue_place]\t Có giá trị đến ngày:[user1_passport_expiry_date]\n12. Nghề nghiệp, nơi làm việc ở nước ngoài trước khi nhập cảnh Việt Nam:[user1_foreign_occupation]\n13. Họ, chữ đệm và tên, năm sinh, quốc tịch, nghề nghiệp, nơi làm việc, chỗ ở hiện nay của cha, mẹ, vợ, chồng, con:[user1_family_info]\n14. Nơi cư trú ở nước ngoài trước khi nhập cảnh Việt Nam:[user1_foreign_address]\n15. Nơi ở hiện tại ở Việt Nam:[user1_current_address]\n16. Nội dung đề nghị (2):[user1_request_content]\n17. Họ và tên chủ hộ:[user2_full_name]18. Quan hệ với chủ hộ:[user1_relationship_user2]\n19. Số định danh cá nhân/ CMND của chủ hộ:[user2_id_number]\t\t\t\t\t\t\t\t\t\t\n\n\t\n'

Output:
TỜ KHAI ĐĂNG KÝ CẢI CHÍNH HỌ TÊN
Kính gửi (1): [receiver]

Họ, chữ đệm và tên hiện tại: [user1_full_name]
Họ, chữ đệm và tên đề nghị thay đổi: [user1_name_change]
Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Giới tính: [user1_gender]
Dân tộc: [user1_ethnicity]
Quốc tịch: [user1_nationality]
Nơi cư trú: [user1_current_address]
Giấy tờ tùy thân (Số CMND/CCCD): [user1_id_number]
Lý do thay đổi tên: [user1_name_change_reason]
Thông tin người khai: [user2_full_name]
Quan hệ với người yêu cầu thay đổi tên: [user2_relationship_user1]
Đề nghị cơ quan đăng ký thực hiện việc thay đổi tên cho người yêu cầu.
Nơi đăng ký: [place]
Ngày: [day] tháng: [month] năm: [year]

Input:
'TỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH, \nBỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC\n\nKính gửi: (1) [receiver]\nHọ, chữ đệm, tên người yêu cầu: [user1_full_name] \t\nNgày, tháng, năm sinh: [user1_dob_day] /[user1_dob_month]/[user1_dob_year]\t\nNơi cư trú: (2) [user1_current_address]\t\n\t\nGiấy tờ tùy thân: (3) [user1_id_number]\t\n\t\nQuan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch:[user1_relationship_user2].\t\nĐề nghị cơ quan đăng ký việc (4)[user1_request_content] \t\t\ncho người có tên dưới đây:\nHọ, chữ đệm, tên: [user2_full_name]\t\nNgày, tháng, năm sinh:[user2_dob] \t\nGiới tính: (2)[user2_gender]Dân tộc: (2)[user2_ethnicity]Quốc tịch: (2)[user2_nationality]\t\nNơi cư trú: (2)[user2_current_address]\t\n\t\nGiấy tờ tùy thân: (3)[user2_id_number]\t\n\t\nĐã đăng ký (5)  [user2_registration_type]\ntại[user2_registration_place]\nngày[user2_registration_date] số: [user2_registration_number] Quyển số:[user2_registration_volume] \t\nNội dung: (6)[user2_request_content].\t\nLý do:\t[user2_reason].\t\nTôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.  \nLàm tại:[place], ngày [day] tháng [month] năm [year]\t\nNgười yêu cầu\n(Ký, ghi rõ họ, chữ đệm, tên)                                     
																								
	\n', '\t\t\tTỜ KHAI CĂN CƯỚC CÔNG DÂN\n1. Họ, chữ đệm và tên(1): [user1_full_name]\n2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]\n3. Ngày, tháng, năm sinh:[user1_dob]; 4. Giới tính (Nam/nữ): [user1_gender]\n5. Số CMND/CCCD: [user1_id_number]\n6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]\n9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]\n11. Nơi đăng ký khai sinh: [user1_birth_registration_place]\n12. Nơi thường trú: [user1_permanent_address]\n13. Nơi ở hiện tại: [user1_current_address]\n14. Nghề nghiệp: [user1_occupation] 15. Trình độ học vấn: [user1_education_level]', 'Độc lập - Tự do - Hạnh phúc\n\n\nTỜ KHAI ĐĂNG KÝ GIÁM HỘ\n\nKính gửi: (1)[receiver]\t\n\nHọ, chữ đệm, tên người yêu cầu: [user1_full_name]\t\nNgày, tháng, năm sinh: [user1_dob]\nNơi cư trú: (2) [user1_current_address]\t\n\t\nGiấy tờ tùy thân: (3) \t[user1_id_number]\nĐề nghị cơ quan đăng ký việc giám hộ giữa: \nNgười giám hộ:\nHọ, chữ đệm, tên: [user1_full_name]\t\nNgày, tháng, năm sinh:\t[user1_dob_day]/[user1_dob_month]/[user1_dob_year]\nGiới tính:(2) [user1_gender]Dân tộc: (2)[user1_ethnicity] Quốc tịch: (2) \t[user1_nationality]\nNơi cư trú: (2)\t[user1_current_address]\nGiấy tờ tùy thân: (3)[user1_id_number]\t\n\t\nNgười được giám hộ:\nHọ, chữ đệm, tên: \t[user2_full_name]\nNgày, tháng, năm sinh: \t[user2_dob]\nNơi cư trú: (2) [user2_current_address]\nGiấy khai sinh/Giấy tờ tùy thân: (3)[user1_id_number]\nLý do đăng ký giám hộ: \t[user1_reason]\t\nTôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.\n   Làm tại:[place], ngày [day] tháng [month] năm [year]\t\n\n\tNgười yêu cầu \n(Ký, ghi rõ họ, chữ đệm, tên)\n\n\n', 'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\nTỜ KHAI ĐĂNG KÝ KHAI SINH\nHọ, chữ đệm, tên người yêu cầu: [user1_full_name]\nNơi cư trú: (2)[user1_current_address]\nGiấy tờ tùy thân: (3)[user1_id_number]\nQuan hệ với người được khai sinh: [user1_relationship_user2]\nĐề nghị cơ quan đăng ký khai sinh cho người dưới đây:\nHọ, chữ đệm, tên:[user2_full_name]\nNgày, tháng, năm sinh: [user2_dob_day]/[user2_dob_month]/[user2_dob_year]ghi bằng chữ: [user2_dob_text]\nGiới tính:[user2_gender] Dân tộc:[user2_ethnicity]Quốc tịch: [user2_nationality]\nNơi sinh: (4)[user2_birthplace]\nQuê quán: [user2_hometown]\nHọ, chữ đệm, tên người mẹ: [user3_full_name]\nNăm sinh: (5)[user3_dob_year]Dân tộc:[user3_ethnicity]Quốc tịch: [user3_nationality]\nNơi cư trú: (2) [user3_current_address]\nHọ, chữ đệm, tên người cha: [user4_full_name]\nNăm sinh: (5)[user4_dob_year]Dân tộc:[user4_ethnicity]Quốc tịch: [user4_nationality]\nNơi cư trú: (2) [user4_current_address]\nTôi cam đoan nội dung đề nghị đăng ký khai sinh trên đây là đúng sự thật, được sự thỏa thuận nhất trí của các bên liên quan theo quy định pháp luật.\nTôi chịu hoàn toàn trách nhiệm trước pháp luật về nội dung cam đoan của mình.\nLàm tại:[place], ngày [day] tháng [month] năm [year]'
Output:
Tờ Khai Đăng Ký Thay Đổi Địa Chỉ Thường Trú
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM  
Độc lập - Tự do - Hạnh phúc  
---------------  
TỜ KHAI ĐĂNG KÝ THAY ĐỔI ĐỊA CHỈ THƯỜNG TRÚ  

Kính gửi: (1) [receiver]  
Họ, chữ đệm, tên: [user1_full_name]  
Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]  
Giới tính: [user1_gender]  
Số CMND/CCCD: [user1_id_number]  
Dân tộc: [user1_ethnicity]  
Quốc tịch: [user1_nationality]  

Địa chỉ thường trú hiện tại: [user1_current_address]  
Địa chỉ thường trú mới: [user1_new_address]  

Lý do thay đổi địa chỉ: [user1_reason]  

Tôi cam đoan những thông tin đã khai là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.  

Làm tại: [place], ngày [day] tháng [month] năm [year]  

Người khai  
(Ký, ghi rõ họ, chữ đệm, tên)  
Input:
{random_forms_text}
Output:
"""