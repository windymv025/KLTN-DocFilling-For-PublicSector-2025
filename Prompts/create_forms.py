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

# Ví dụ:
"""