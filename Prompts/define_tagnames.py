residence_identification_template_prompt = """
# Instruction: Residence and Identification Form

# Goal:
The purpose of this form is to accurately capture and store essential personal identification and residence-related details of users. The data collected includes vital information required for legal and government documentation, ensuring that each individual is correctly identified and located. The form covers personal identification (name, birth details, ID numbers), residence information (permanent, current addresses), and additional details such as nationality and marital status. Your task is to ensure each placeholder is replaced with the correct tag name to reflect the user's information. If a placeholder does not match any defined tag, generate a new tag name.

# Your Task:

You are responsible for determining the correct tag name for each placeholder in a residence and identification form. Your task is to ensure that every placeholder in the form is accurately replaced with the corresponding tag name, based on the user's personal information and the tag names provided. If a placeholder does not match any defined tag, generate a new tag name accordingly.

- Input Format:

The input is a sample form containing placeholders (..........) for collecting information.
Each placeholder represents a piece of information that needs to be mapped to a specific tag name, depending on the type of information it corresponds to.

- Output Format:

The output should be a standardized version of the form, where placeholders have been replaced by tags in the format [userX_tagname] or [tagname].
The placeholder tags should be replaced based on a set of predefined tag names for various types of personal and academic information.
Example output should include accurately mapped tags for each type of information required in the form, ensuring clarity and consistency.

Input and output are placed in ``` ```

1. Identify Unique Users

Task: Determine the number of unique users mentioned in the form. Action: Assign a unique identifier to each user (e.g., user1, user2, etc.).

Match and Replace Personal Information Placeholders

Task: For each placeholder (..........), check if it corresponds to a residence or identification tag name from the provided list {residence_identification_tagnames}.

Action 1: If a match is found, replace the placeholder with the corresponding tag name in the format [userX_tagname], where X is the user identifier.

Action 2: If a single placeholder should represent multiple related tags (e.g., Ngày, tháng, năm sinh: ......... or Ngày sinh: .........), combine these related tags into a single tag name (e.g., [userX_dob] for date of birth). Avoid splitting into multiple placeholders.

Action 3: If a placeholder requires multiple pieces of information (e.g., Ngày và nơi cấp: ..........), ensure to create separate tags for each specific detail within the same square brackets separated by commas (e.g., [user1_id_issue_date, user1_id_issue_place] for id issue date and id issue place)

Action 4: If the placeholder implies multiple details (e.g., "Hiện đang (làm gì, ở đâu)"), generate separate tags for each detail within the same set of square brackets and separate them using a comma. For example: [user1_occupation, user1_current_address].

Action 5: If no match is found, generate a new tag name in the format [userX_new_tagname] and replace the placeholder with this generated tag name.


2. Handle Non-Personal Information Placeholders

Task: If the placeholder does not correspond to any known residence or identification tag name:

Action 1: Check against the {remaining_tag_names}.

Action 2: If a match is found, replace the placeholder with the corresponding tag name from this list.

Action 3: If no match is found, generate a new tag name in the format [new_tagname] and replace the placeholder with this generated tag name.

3. Ensure Consistency and Accuracy

Task: Ensure that each placeholder is accurately replaced according to the user's unique identifier and the nature of the information provided.

Action: Review the form to confirm that all placeholders are correctly replaced, maintaining the integrity of the user information and the form structure.

Output only.

## Example:
Input:
```
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
```
Output:
```
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id_number]
6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Quê quán: [user1_hometown]
13. Nơi thường trú: [user1_permanent_address]
14. Nơi ở hiện tại: [user1_current_address]
15. Nghề nghiệp: [user1_occupation] 16. Trình độ học vấn: [user1_education_level]
[place], ngày [day] tháng [month] năm [year]
```

## Example:
Input:
```
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): ..........
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): ..........
3. Ngày, tháng, năm sinh: ..........; 4. Giới tính (Nam/nữ): ..........
5. Số CMND/CCCD: ..........
6. Dân tộc: ..........; 7. Tôn giáo: .......... 8. Quốc tịch: ..........
9. Tình trạng hôn nhân: .......... 10. Nhóm máu (nếu có): ..........
11. Nơi đăng ký khai sinh: ..........
12. Quê quán: ..........
```
Output:
```
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày, tháng, năm sinh: [user1_dob]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id_number]
6. Dân tộc và tôn giáo: [user1_ethnicity, user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Quê quán: [user1_hometown]
```



## Example:
Input:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH,
BỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC
Kính gửi: ..........
Họ, chữ đệm, tên người yêu cầu: ..........
Nơi cư trú: ..........
Giấy tờ tùy thân: ..........
Cấp ngày: ........../........./.........
Quan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch:..........
Đề nghị cơ quan đăng ký việc ..........cho người có tên dưới đây:
Họ, chữ đệm, tên: ..........
Ngày, tháng, năm sinh: ..........
Giới tính:..........Dân tộc:..........Quốc tịch: ..........
Nơi cư trú:  ..........
Giấy tờ tùy thân: ..........
Đã đăng ký  ..........tại.......... ngày.......... tháng .......... năm .......... số: .......... Quyển số:..........
Nội dung: ..........
Lý do:..........
Tôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.
Đề nghị cấp bản sao: Có , Không ; số lượng:..........bản
Làm tại: .......... , ngày ..........  tháng ..........  năm ..........
Người yêu cầu
(Ký, ghi rõ họ, chữ đệm, tên)

```
Output:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH,
BỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC
Kính gửi: [receiver]
Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Nơi cư trú: [user1_current_address]
Giấy tờ tùy thân: [user1_id_number]
Cấp ngày: [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year]
Quan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch: [user1_relationship_user2]
Đề nghị cơ quan đăng ký việc [user1_request_content] cho người có tên dưới đây:
Họ, chữ đệm, tên: [user2_full_name]
Ngày, tháng, năm sinh: [user2_dob]
Giới tính: [user2_gender] Dân tộc: [user2_ethnicity] Quốc tịch: [user2_nationality]
Nơi cư trú:  [user2_current_address]
Giấy tờ tùy thân: [user2_id_number]
Đã đăng ký  [user2_registration_type] tại [user2_registration_place] ngày [user2_registration_day] tháng [user2_registration_month] năm [user2_registration_year] số: [user2_registration_number] Quyển số: [user2_registration_volume]
Nội dung: [user2_request_content]
Lý do: [user2_reason]
Tôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.
Đề nghị cấp bản sao: Có , Không ; số lượng: [user1_copy_request] bản
Làm tại: [place] , ngày [day]  tháng [month]  năm [year]
Người yêu cầu
(Ký, ghi rõ họ, chữ đệm, tên) 

```

## Example
Input:
```
			TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ và tên: ..........
2. Ngày sinh:..........; 3. Giới tính (Nam/nữ): ..........
4. Số CMND/CCCD: ..........
5. Cấp ngày: ........../........../.......... 
6. Dân tộc: ..........; 
9. Tình trạng hôn nhân: .......... 10. Nhóm máu (nếu có): ..........
11. Nơi đăng ký khai sinh: ..........
12. Nơi thường trú: ..........
13. Nghề nghiệp: ..........
```
Ouput:
```
			TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ và tên: [user1_full_name]
2. Ngày sinh: [user1_dob]; 3. Giới tính (Nam/nữ): [user1_gender]
4. Số CMND/CCCD: [user1_id_number]
5. Cấp ngày: [user1_id_issue_date] 
6. Dân tộc: [user1_ethnicity];
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Nơi thường trú: [user1_permanent_address]
13. Nghề nghiệp: [user1_occupation]
```

## Example:
Input:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH,
BỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC
Kính gửi: ..........
Họ, chữ đệm, tên người yêu cầu: ..........
Nơi cư trú: ..........
Giấy tờ tùy thân: ..........
Quan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch:..........
Đề nghị cơ quan đăng ký việc ..........cho người có tên dưới đây:
Họ, chữ đệm, tên: ..........
Ngày, tháng, năm sinh: ........../........../..........
Giới tính:..........Dân tộc:..........Quốc tịch: ..........
Nơi cư trú:  ..........
Giấy tờ tùy thân: ..........
Đã đăng ký  ..........tại.......... ngày.......... tháng .......... năm .......... số: .......... Quyển số:..........
Nội dung: ..........
Lý do:..........
Tôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.
Đề nghị cấp bản sao: Có , Không ; số lượng:..........bản
Làm tại: .......... , ngày ..........  tháng ..........  năm ..........
Người yêu cầu
(Ký, ghi rõ họ, chữ đệm, tên)

```
Output:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH,
BỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC
Kính gửi: [receiver]
Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Nơi cư trú: [user1_current_address]
Giấy tờ tùy thân: [user1_id_number]
Quan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch: [user1_relationship_user2]
Đề nghị cơ quan đăng ký việc [user1_request_content] cho người có tên dưới đây:
Họ, chữ đệm, tên: [user2_full_name]
Ngày, tháng, năm sinh: [user2_dob_day]/[user2_dob_month]/[user2_dob_year]
Giới tính: [user2_gender] Dân tộc: [user2_ethnicity] Quốc tịch: [user2_nationality]
Nơi cư trú:  [user2_current_address]
Giấy tờ tùy thân: [user2_id_number]
Đã đăng ký  [user2_registration_type] tại [user2_registration_place] ngày [user2_registration_day] tháng [user2_registration_month] năm [user2_registration_year] số: [user2_registration_number] Quyển số: [user2_registration_volume]
Nội dung: [user2_request_content]
Lý do: [user2_reason]
Tôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.
Đề nghị cấp bản sao: Có , Không ; số lượng: [user1_copy_request] bản
Làm tại: [place] , ngày [day]  tháng [month]  năm [year]
Người yêu cầu
(Ký, ghi rõ họ, chữ đệm, tên) 

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc


TỜ KHAI 
Đề nghị khôi phục giá trị sử dụng hộ chiếu phổ thông


1. Họ..........Chữ đệm và tên..........(1) 2. Giới tính(Nam/Nữ):..........
3. Sinh ngày.......... tháng.......... năm..........Nơi sinh (tỉnh, thành phố) (2)..........
4. Số định danh cá nhân hoặc CCCD:..........                                                   Ngày cấp:........../........../..........
5. Nơi cư trú hiện tại ..........
6. Số điện thoại: ..........
7. Thông tin về hộ chiếu đề nghị khôi phục:
    Số hộ chiếu:.......... ngày cấp........../........../..........
    Thời hạn:........../........../..........Cơ quan cấp:..........
    8. Thông tin thị thực do nước ngoài cấp: 
	Số thị thực:..........Quốc gia cấp..........Thời hạn..........
    9. Lý do đề nghị khôi phục hộ chiếu(3) ..........
Tôi xin cam đoan những thông tin trên là đúng sự thật./.
                                                  

           Làm tại.........., ngày..........tháng..........năm..........
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc


TỜ KHAI 
Đề nghị khôi phục giá trị sử dụng hộ chiếu phổ thông


1. Họ [user1_last_name] Chữ đệm và tên [user1_first_name] (1) 2. Giới tính(Nam/Nữ): [user1_gender]
3. Sinh ngày [user1_dob_day] tháng [user1_dob_month] năm [user1_dob_year] Nơi sinh (tỉnh, thành phố) (2) [user1_birthplace]
4. Số định danh cá nhân hoặc CCCD: [user1_id_number]                                         Ngày cấp: [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year]
5. Nơi cư trú hiện tại [user1_current_address]
6. Số điện thoại: [user1_phone_number]
7. Thông tin về hộ chiếu đề nghị khôi phục:
    Số hộ chiếu: [user1_passport_number] ngày cấp [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]
    Thời hạn: [user1_passport_expiry_day]/[user1_passport_expiry_month]/[user1_passport_expiry_year] Cơ quan cấp: [user1_passport_issue_place]
    8. Thông tin thị thực do nước ngoài cấp: 
	Số thị thực: [user1_visa_number] Quốc gia cấp [user1_visa_country] Thời hạn [user1_visa_expiry_date]
    9. Lý do đề nghị khôi phục hộ chiếu(3) [user1_reason]
Tôi xin cam đoan những thông tin trên là đúng sự thật./.
                                                  

           Làm tại [place], ngày [day] tháng [month] năm [year]
```


## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc


TỜ KHAI 
Đề nghị khôi phục giá trị sử dụng hộ chiếu phổ thông


1. Họ..........Chữ đệm và tên..........(1) 2. Giới tính(Nam/Nữ):..........
3. Sinh ngày.......... tháng.......... năm..........Nơi sinh (tỉnh, thành phố) (2)..........
4. Số định danh cá nhân hoặc CCCD:..........                                                   Ngày cấp:..........
5. Nơi cư trú hiện tại ..........
6. Số điện thoại: ..........
7. Thông tin về hộ chiếu đề nghị khôi phục:
    Số hộ chiếu:.......... ngày cấp........../........../..........
    Thời hạn: .......... Cơ quan cấp:..........
    8. Thông tin thị thực do nước ngoài cấp: 
	Số thị thực:..........Quốc gia cấp..........Thời hạn..........
    9. Lý do đề nghị khôi phục hộ chiếu(3) ..........
Tôi xin cam đoan những thông tin trên là đúng sự thật./.
                                                  

           Làm tại.........., ngày..........tháng..........năm..........
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc


TỜ KHAI 
Đề nghị khôi phục giá trị sử dụng hộ chiếu phổ thông


1. Họ [user1_last_name] Chữ đệm và tên [user1_first_name] (1) 2. Giới tính(Nam/Nữ): [user1_gender]
3. Sinh ngày [user1_dob_day] tháng [user1_dob_month] năm [user1_dob_year] Nơi sinh (tỉnh, thành phố) (2) [user1_birthplace]
4. Số định danh cá nhân hoặc CCCD: [user1_id_number]                                         Ngày cấp: [user1_id_issue_date]
5. Nơi cư trú hiện tại [user1_current_address]
6. Số điện thoại: [user1_phone_number]
7. Thông tin về hộ chiếu đề nghị khôi phục:
    Số hộ chiếu: [user1_passport_number] ngày cấp [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]
    Thời hạn: [user1_passport_expiry_date] Cơ quan cấp: [user1_passport_issue_place]
    8. Thông tin thị thực do nước ngoài cấp: 
	Số thị thực: [user1_visa_number] Quốc gia cấp [user1_visa_country] Thời hạn [user1_visa_expiry_date]
    9. Lý do đề nghị khôi phục hộ chiếu(3) [user1_reason]
Tôi xin cam đoan những thông tin trên là đúng sự thật./.
                                                  

           Làm tại [place], ngày [day] tháng [month] năm [year]
```

## Example: 
Input:
```
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
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ KHAI SINH
Kính gửi: [receiver]
Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Nơi cư trú: [user1_current_address]
Giấy tờ tùy thân: [user1_id_number]
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
```


## Example:
Input:
```
TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ
(Dùng cho công dân Việt Nam định cư ở nước ngoài 
không có hộ chiếu Việt Nam còn giá trị sử dụng) 

Kính gửi (1):..........
1. Họ, chữ đệm và tên Việt Nam:..........
2. Họ, chữ đệm và tên trong hộ chiếu/giấy tờ do nước ngoài cấp:	..........
3. Ngày, tháng, năm sinh:........../........../ ..........     4. Giới tính:..........
5. Dân tộc:..........     6. Tôn giáo:..........
7. Số định danh cá nhân/CMND: ..........									
8. Số điện thoại (nếu có):..........	 9. E-mail (nếu có):..........
10. Quốc tịch nước ngoài (nếu có):..........
11. Số hộ chiếu/ Giấy tờ đi lại quốc tế do nước ngoài cấp/ Giấy tờ do cơ quan có thẩm quyền Việt Nam cấp:
Số:	.......... Ngày cấp: ........../........../..........
Cơ quan cấp:..........	 Có giá trị đến ngày:........../........../..........
12. Nghề nghiệp, nơi làm việc ở nước ngoài trước khi nhập cảnh Việt Nam:..........
13. Họ, chữ đệm và tên, năm sinh, quốc tịch, nghề nghiệp, nơi làm việc, chỗ ở hiện nay của cha, mẹ, vợ, chồng, con:..........
14. Nơi cư trú ở nước ngoài trước khi nhập cảnh Việt Nam:..........
15. Nơi ở hiện tại ở Việt Nam:..........
16. Nội dung đề nghị (2):..........
17. Họ và tên chủ hộ:..........18. Quan hệ với chủ hộ:..........
19. Số định danh cá nhân/ CMND của chủ hộ:..........
```									
Output:
```
TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ
(Dùng cho công dân Việt Nam định cư ở nước ngoài 
không có hộ chiếu Việt Nam còn giá trị sử dụng) 

Kính gửi (1): [receiver]
1. Họ, chữ đệm và tên Việt Nam: [user1_full_name]
2. Họ, chữ đệm và tên trong hộ chiếu/giấy tờ do nước ngoài cấp:	[user1_foreign_name]
3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]     4. Giới tính: [user1_gender]
5. Dân tộc: [user1_ethnicity]     6. Tôn giáo: [user1_religion]
7. Số định danh cá nhân/CMND: [user1_id_number]									
8. Số điện thoại (nếu có): [user1_phone]	 9. E-mail (nếu có): [user1_email]
10. Quốc tịch nước ngoài (nếu có): [user1_foreign_nationality]
11. Số hộ chiếu/ Giấy tờ đi lại quốc tế do nước ngoài cấp/ Giấy tờ do cơ quan có thẩm quyền Việt Nam cấp:
Số:	[user1_passport_number] Ngày cấp: [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]
Cơ quan cấp: [user1_passport_issue_place]	 Có giá trị đến ngày: [user1_passport_expiry_day]/[user1_passport_expiry_month]/[user1_passport_expiry_year]
12. Nghề nghiệp, nơi làm việc ở nước ngoài trước khi nhập cảnh Việt Nam: [user1_foreign_occupation]
13. Họ, chữ đệm và tên, năm sinh, quốc tịch, nghề nghiệp, nơi làm việc, chỗ ở hiện nay của cha, mẹ, vợ, chồng, con: [user1_family_info]
14. Nơi cư trú ở nước ngoài trước khi nhập cảnh Việt Nam: [user1_foreign_address]
15. Nơi ở hiện tại ở Việt Nam: [user1_current_address]
16. Nội dung đề nghị (2): [user1_request_content]
17. Họ và tên chủ hộ: [user2_full_name] 18. Quan hệ với chủ hộ: [user1_relationship_user2]
19. Số định danh cá nhân/ CMND của chủ hộ: [user2_id_number]	
```


## Example:
Input:
```
{form}
```
Ouput: 
"""

study_template_prompt = """
# Instruction: Study Form

# Goal:
The purpose of this form is to accurately capture and store essential academic and personal details of users in an educational context. The data collected includes information such as name, date of birth, student ID, academic details (class, course, faculty, and school), and contact information. This form is essential for student records, academic tracking, and official documentation. Your task is to ensure each placeholder is replaced with the correct tag name to reflect the user's information. If a placeholder does not match any defined tag, generate a new tag name.

# Your Task:

You are responsible for determining the correct tag name for each placeholder in a study-related form. Your task is to ensure that every placeholder in the form is accurately replaced with the corresponding tag name, based on the user's academic and personal information and the tag names provided. If a placeholder does not match any defined tag, generate a new tag name accordingly.

- Input Format:

The input is a sample form containing placeholders (..........) for collecting information.
Each placeholder represents a piece of information that needs to be mapped to a specific tag, depending on the type of information it corresponds to.

- Output Format:

The output should be a standardized version of the form, where placeholders have been replaced by tags in the format [userX_tagname] or [tagname].
The placeholder tags should be replaced based on a set of predefined tag names for various types of personal and academic information.
Example output should include accurately mapped tags for each type of information required in the form, ensuring clarity and consistency.

Input and output are placed in ``` ```

1. Identify Unique Users

Task: Determine the number of unique users mentioned in the form. Action: Assign a unique identifier to each user (e.g., user1, user2, etc.).

Match and Replace Personal and Academic Information Placeholders

Task: For each placeholder (..........), check if it corresponds to a study-related tag name from the provided list {study_tagnames}.

Action 1: If a match is found, replace the placeholder with the corresponding tag name in the format [userX_tagname], where X is the user identifier.

Action 2: If a single placeholder should represent multiple related tags (e.g., Ngày, tháng, năm sinh: ......... or Ngày sinh: .........), combine these related tags into a single tag name (e.g., [userX_dob] for date of birth). Avoid splitting into multiple placeholders.

Action 3: If a placeholder requires multiple pieces of information (e.g., Ngày và nơi cấp: ..........), ensure to create separate tags for each specific detail within the same square brackets separated by commas (e.g., [user1_id_issue_date, user1_id_issue_place] for id issue date and id issue place)

Action 4: If the placeholder implies multiple details (e.g., "Hiện đang (làm gì, ở đâu)"), generate separate tags for each detail within the same set of square brackets and separate them using a comma. For example: [user1_occupation, user1_current_address].

Action 5: If no match is found, generate a new tag name in the format [userX_new_tagname] and replace the placeholder with this generated tag name.


2. Handle Non-Personal Information Placeholders

Task: If the placeholder does not correspond to any known study-related tag name:

Action 1: Check against the {remaining_tag_names}.

Action 2: If a match is found, replace the placeholder with the corresponding tag name from this list.

Action 3: If no match is found, generate a new tag name in the format [new_tagname] and replace the placeholder with this generated tag name.

3. Ensure Consistency and Accuracy

Task: Ensure that each placeholder is accurately replaced according to the user's unique identifier and the nature of the information provided.

Action: Review the form to confirm that all placeholders are correctly replaced, maintaining the integrity of the user information and the form structure.

Output only.

## Example
Input:
```
ĐƠN ĐỀ NGHỊ XÁC NHẬN VÀ CẤP HỖ TRỢ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi:	
- ..........(Tên cơ sở giáo dục nghề nghiệp);
- ..........(Tên phòng Công tác học sinh, sinh viên/Phòng Đào tạo).
Họ và tên: ..........
Ngày, tháng, năm sinh:..........
Số định danh cá nhân/Chứng minh nhân dân:..........cấp ngày..........tháng..........năm..........nơi cấp..........
Lớp: .......... Khóa: .......... Khoa: ..........
Mã số học sinh, sinh viên: ..........
Để Nhà trường cấp tiền hỗ trợ ở lại trường trong dịp Tết Nguyên đán năm .......... theo quy định tại Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp, tôi làm đơn này đề nghị Phòng Công tác học sinh, sinh viên (hoặc Phòng Đào tạo) xác nhận là tôi “ở lại trường trong dịp Tết Nguyên đán năm..........” với lý do1: ..........
    .........., ngày .......... tháng .......... năm ..........
Người làm đơn
(Ký và ghi rõ họ tên)

```
Ouptut:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ XÁC NHẬN VÀ CẤP HỖ TRỢ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi:	
- [receiver] (Tên cơ sở giáo dục nghề nghiệp);
- [receiver] (Tên phòng Công tác học sinh, sinh viên/Phòng Đào tạo).
Họ và tên: [user1_full_name]
Ngày, tháng, năm sinh: [user1_dob]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number] cấp ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year] nơi cấp [user1_id_issue_place]
Lớp: [user1_class] Khóa: [user1_course] Khoa: [user1_faculty]
Mã số học sinh, sinh viên: [user1_student_id]
Để Nhà trường cấp tiền hỗ trợ ở lại trường trong dịp Tết Nguyên đán năm [user1_tet_year] theo quy định tại Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp, tôi làm đơn này đề nghị Phòng Công tác học sinh, sinh viên (hoặc Phòng Đào tạo) xác nhận là tôi “ở lại trường trong dịp Tết Nguyên đán năm [user1_tet_year]” với lý do: [user1_reason_for_staying]
    [place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)

```

## Example
Input:
```
ĐƠN ĐỀ NGHỊ XÁC NHẬN VÀ CẤP HỖ TRỢ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi:	
- ..........(Tên cơ sở giáo dục nghề nghiệp);
- ..........(Tên phòng Công tác học sinh, sinh viên/Phòng Đào tạo).
Họ và tên: ..........
Ngày, tháng, năm sinh:........../........../..........
Số định danh cá nhân/Chứng minh nhân dân:..........cấp ngày..........tháng..........năm..........nơi cấp..........
Lớp: .......... Khóa: .......... Khoa: ..........
Mã số học sinh, sinh viên: ..........
Để Nhà trường cấp tiền hỗ trợ ở lại trường trong dịp Tết Nguyên đán năm .......... theo quy định tại Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp, tôi làm đơn này đề nghị Phòng Công tác học sinh, sinh viên (hoặc Phòng Đào tạo) xác nhận là tôi “ở lại trường trong dịp Tết Nguyên đán năm..........” với lý do1: ..........
    .........., ngày .......... tháng .......... năm ..........
Người làm đơn
(Ký và ghi rõ họ tên)

```
Ouptut:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ XÁC NHẬN VÀ CẤP HỖ TRỢ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi:	
- [receiver] (Tên cơ sở giáo dục nghề nghiệp);
- [receiver] (Tên phòng Công tác học sinh, sinh viên/Phòng Đào tạo).
Họ và tên: [user1_full_name]
Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number] cấp ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year] nơi cấp [user1_id_issue_place]
Lớp: [user1_class] Khóa: [user1_course] Khoa: [user1_faculty]
Mã số học sinh, sinh viên: [user1_student_id]
Để Nhà trường cấp tiền hỗ trợ ở lại trường trong dịp Tết Nguyên đán năm [user1_tet_year] theo quy định tại Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp, tôi làm đơn này đề nghị Phòng Công tác học sinh, sinh viên (hoặc Phòng Đào tạo) xác nhận là tôi “ở lại trường trong dịp Tết Nguyên đán năm [user1_tet_year]” với lý do: [user1_reason_for_staying]
    [place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN XIN CHUYỂN TRƯỜNG
(dành cho học sinh tiểu học chuyển trường trong nước)
Kính gửi:
- Hiệu trưởng trường..........
- Hiệu trưởng trường..........
Tôi tên là:..........
Hiện trú tại:..........
Số điện thoại:.......... Địa chỉ email (nếu có):..........
Là phụ huynh/người giám hộ hợp pháp của:
Học sinh: .......... Ngày tháng năm sinh:..........
Là học sinh lớp:.......... Trường3..........
Kết quả cuối năm học: ..........
Tôi làm đơn này đề nghị cho con tôi được chuyển từ trường4 ...........về học lớp .......... năm học ..........tại trường5..........
Lý do:..........
Trân trọng cảm ơn.
 	.........., ngày ..........tháng..........năm ..........
Người làm đơn
(Ký và ghi rõ họ tên)
 
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN XIN CHUYỂN TRƯỜNG
(dành cho học sinh tiểu học chuyển trường trong nước)
Kính gửi:
- Hiệu trưởng trường [receiver]
- Hiệu trưởng trường [receiver]
Tôi tên là: [user1_full_name]
Hiện trú tại: [user1_current_address]
Số điện thoại: [user1_phone] Địa chỉ email (nếu có): [user1_email]
Là phụ huynh/người giám hộ hợp pháp của:
Học sinh: [user2_full_name] Ngày tháng năm sinh: [user2_dob]
Là học sinh lớp: [user2_grade] Trường [user2_school_name_from]
Kết quả cuối năm học: [user2_final_grade]
Tôi làm đơn này đề nghị cho con tôi được chuyển từ trường [user2_school_name_from] về học lớp [user2_grade] năm học [user2_school_year] tại trường [user2_school_name_to]
Lý do: [user1_reason_for_transfer]
Trân trọng cảm ơn.
 	[place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký và ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BÁO CÁO TỐT NGHIỆP  
 
Kính gửi: .......... 

1. Họ và tên:	..........
2. Số định danh cá nhân:	..........
3. Cơ quan quản lý trực tiếp (nếu có): 	..........
4. Quyết định cử đi học số.......... ngày.......... tháng.......... năm.......... của..........	
5. Thời gian học tập ở nước ngoài:	..........
6. Thời gian gia hạn học tập ở nước ngoài: từ tháng........../20.......... đến tháng........../20..........
7. Ngày tốt nghiệp:	.......... Ngày về nước:	..........
8. Kết quả học tập: 
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



    .........., ngày.......... tháng.......... năm.......... 
Người báo cáo
(Ký và ghi rõ họ tên)
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BÁO CÁO TỐT NGHIỆP  
 
Kính gửi: [receiver] 

1. Họ và tên:	[user1_full_name]
2. Số định danh cá nhân:	[user1_id_number]
3. Cơ quan quản lý trực tiếp (nếu có): 	[user1_management_organization]
4. Quyết định cử đi học số [user1_study_decision_number] ngày [user1_study_decision_day] tháng [user1_study_decision_month] năm [user1_study_decision_year] của [user1_study_decision_issuer]	
5. Thời gian học tập ở nước ngoài:	[user1_study_period]
6. Thời gian gia hạn học tập ở nước ngoài: từ tháng [user1_extension_start_month]/20[user1_extension_start_year] đến tháng [user1_extension_end_month]/20[user1_extension_end_year]
7. Ngày tốt nghiệp:	[user1_graduation_date] Ngày về nước:	[user1_return_date]
8. Kết quả học tập: 
- Văn bằng, chứng chỉ được cấp:	[user1_degree]
- Kết quả xếp loại học tập:	[user1_study_result_rating]
9. Tên cơ sở giáo dục nước ngoài (ghi bằng tiếng Việt và tiếng Anh):	
[user1_foreign_education_institution_name_vn, user1_foreign_education_institution_name_en]		
10. Tên đề tài luận văn thạc sĩ (nếu học thạc sĩ coursework không có luận văn thì ghi: không có luận văn), đề tài luận án tiến sĩ, chuyên đề thực tập:	
[user1_thesis_topic]	
11. Tên và học hàm, học vị của người hướng dẫn:	[user1_supervisor_name]
12. Đánh giá của cơ sở giáo dục hoặc giáo sư hướng dẫn (nếu có, viết tóm tắt): 
[user1_supervisor_evaluation]
13. Nguyện vọng, đề nghị 3 :	[user1_request]	
14. Cơ quan công tác sau khi tốt nghiệp về Việt Nam:	[user1_post_graduation_organisation]
Địa chỉ:	[user1_post_graduation_address]	
15. Địa chỉ liên hệ :	[user1_contact_address]	
Điện thoại cố định:	[user1_phone_home]	, Điện thoại di động: [user1_phone]		
E-mail:	 [user1_email]	
16. Kiến nghị, đề xuất đối với cơ quan quản lý trực tiếp, cơ quan cử đi học:	
[user1_suggestion]	
		
Tôi cam đoan nội dung báo cáo là hoàn toàn trung thực, chính xác và xin chịu trách nhiệm về nội dung báo cáo. 



    [place], ngày [day] tháng [month] năm [year] 
Người báo cáo
(Ký và ghi rõ họ tên)
```

## Example:
Input:
```
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
```
Output:
```
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
```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ HỖ TRỢ HỌC TẬP 
(Dùng cho cha mẹ trẻ mẫu giáo hoặc người chăm sóc trẻ mẫu giáo học tại các cơ sở giáo dục công lập)
Kính gửi: .......... (Cơ sở giáo dục)
Họ và tên cha mẹ (hoặc người chăm sóc): .......... 
Hộ khẩu thường trú tại:.......... 
Là cha/mẹ (hoặc người chăm sóc) của em:.......... 
Sinh ngày: ........../........../.......... 
Dân tộc:.......... 
Hiện đang học (tại lớp, trường):.......... 
Tôi làm đơn này đề nghị các cấp quản lý xem xét, giải quyết cấp tiền hỗ trợ học tập theo quy định và chế độ hiện hành./.
 
XÁC NHẬN CỦA ỦY BAN NHÂN DÂN CẤP XÃ1
Nơi trẻ mẫu giáo có hộ khẩu thường trú
(Ký tên, đóng dấu)	.......... ,ngày.......... tháng.......... năm.......... 
Người làm đơn
(Ký, ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ HỖ TRỢ HỌC TẬP 
(Dùng cho cha mẹ trẻ mẫu giáo hoặc người chăm sóc trẻ mẫu giáo học tại các cơ sở giáo dục công lập)
Kính gửi: [receiver] (Cơ sở giáo dục)
Họ và tên cha mẹ (hoặc người chăm sóc): [user1_full_name]
Hộ khẩu thường trú tại: [user1_permanent_address]
Là cha/mẹ (hoặc người chăm sóc) của em: [user2_full_name]
Sinh ngày: [user2_dob_day]/[user2_dob_month]/[user2_dob_year]
Dân tộc: [user2_ethnicity]
Hiện đang học (tại lớp, trường): [user2_class, user2_school]
Tôi làm đơn này đề nghị các cấp quản lý xem xét, giải quyết cấp tiền hỗ trợ học tập theo quy định và chế độ hiện hành./.
 
XÁC NHẬN CỦA ỦY BAN NHÂN DÂN CẤP XÃ1
Nơi trẻ mẫu giáo có hộ khẩu thường trú
(Ký tên, đóng dấu)	[place], ngày [day] tháng [month] năm [year]
Người làm đơn
(Ký, ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI  
 
Kính gửi: .......... 

Tôi tên là: ..........
Cơ quan quản lý trực tiếp (nếu có): ..........	
	
Quyết định cử đi học số .......... ngày .......... tháng .......... năm .......... của 	..........
Tên trường đến học, nước: 	..........
Trình độ đào tạo: 	..........
Ngành/nghề đào tạo: 	..........
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo: 	..........
Ngày nhập học: 	..........
Lý do đề nghị gia hạn:..........
Thời gian đề nghị gia hạn: từ tháng ........../năm 20.......... đến tháng ........../năm 20..........	
Kinh phí trong thời gian gia hạn : 	..........
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập. 

Địa chỉ liên lạc của tôi:	..........
E-mail:	..........
Điện thoại cố định:..........	 Điện thoại di động:..........	



		.........., ngày.......... tháng.......... năm.......... 
Người làm đơn
(Ký và ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI  
 
Kính gửi: [receiver] 

Tôi tên là: [user1_full_name]
Cơ quan quản lý trực tiếp (nếu có): [user1_organization]	
	
Quyết định cử đi học số [user1_decision_number] ngày [user1_decision_day] tháng [user1_decision_month] năm [user1_decision_year] của 	[user1_decision_issuer]
Tên trường đến học, nước: 	[user1_university_name]
Trình độ đào tạo: 	[user1_education_level]
Ngành/nghề đào tạo: 	[user1_course]
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo: 	[user1_duration_of_course]
Ngày nhập học: 	[user1_enrollment_date]
Lý do đề nghị gia hạn: [user1_reason_for_extension]
Thời gian đề nghị gia hạn: từ tháng [user1_extension_start_month]/năm 20[user1_extension_start_year] đến tháng [user1_extension_end_month]/năm 20[user1_extension_end_year]	
Kinh phí trong thời gian gia hạn : 	[user1_extension_funding]
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập. 

Địa chỉ liên lạc của tôi:	[user1_contact_address]
E-mail:	[user1_email]
Điện thoại cố định: [user1_phone_home]	 Điện thoại di động: [user1_phone]	

		[place], ngày [day] tháng [month] năm [year] 
Người làm đơn
(Ký và ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

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
Tôi làm đơn này đề nghị các cấp quản lý xem xét, để em  .......... được hưởng chính sách hỗ trợ tiền và gạo theo quy định tại Nghị định số........../2016/NĐ-CP ngày..........tháng..........năm 2016 của Chính phủ, gồm: 

1. Tiền ăn (có/không):..........
2. Tiền nhà ở (đối với trường hợp học sinh phải tự lo chỗ ở)(có/không):..........
3. Gạo(có/không):..........
   .........., ngày ..........tháng..........năm 20..........
Người làm đơn
(Ký, ghi rõ họ, tên hoặc điểm chỉ )

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ HỖ TRỢ 
(Dùng cho cha, mẹ học sinh tiểu học học bán trú tại các trường phổ thông 
ở xã, thôn đặc biệt khó khăn)

Kính gửi Trường : [receiver]
Họ và tên: [user1_full_name]
Là Cha/mẹ (hoặc người giám hộ, nhận nuôi) của em: [user2_full_name]
Sinh ngày [user2_dob_day] tháng [user2_dob_month] năm [user2_dob_year]
Dân tộc: [user2_ethnicity] thuộc hộ nghèo(có/không): [user2_is_poor] 
Thường trú tại thôn/bản [user2_hometown_village] xã [user2_hometown_ward]
thuộc vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn.
Huyện [user2_hometown_district] Tỉnh [user2_hometown_province]
Năm học [user2_school_year] Là học sinh lớp: [user2_grade] Trường [user2_school_name]
Vì lý do (chọn 1 trong 2 lý do sau):
 - Nhà ở xa trường (ghi rõ cách nơi học tập bao nhiêu km): [user2_distance_to_school]
 - Địa hình giao thông khó khăn(có/không): [user2_difficult_traffic]
 Nên em [user2_full_name] không thể đi đến trường và trở về nhà trong ngày.  
Tôi làm đơn này đề nghị các cấp quản lý xem xét, để em  [user2_full_name] được hưởng chính sách hỗ trợ tiền và gạo theo quy định tại Nghị định số [user2_policy_decree_number]/2016/NĐ-CP ngày [user2_policy_decree_date_day] tháng [user2_policy_decree_date_month] năm 2016 của Chính phủ, gồm: 

1. Tiền ăn (có/không): [user2_is_support_food]
2. Tiền nhà ở (đối với trường hợp học sinh phải tự lo chỗ ở)(có/không): [user2_is_support_housing]
3. Gạo(có/không): [user2_is_support_rice]
   [place], ngày [day] tháng [month] năm 20[year]
Người làm đơn
(Ký, ghi rõ họ, tên hoặc điểm chỉ )


```
## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BẢN CAM KẾT
THỰC HIỆN TRÁCH NHIỆM CỦA DU HỌC SINH
(dành cho người chưa có cơ quan công tác)

Kính gửi: Bộ Giáo dục và Đào tạo

Tên tôi là: .......... Sinh ngày .......... 
Giấy CMND/Căn cước công dân số: .......... Ngày cấp:..........
Nơi cấp:.......... 
Hộ chiếu số: .......... Ngày cấp: .......... 
Nơi cấp:..........
Hiện nay là: .......... 
Khi được Nhà nước cử đi học tại nước ngoài, tôi cam kết thực hiện đúng trách nhiệm của người được cử đi học như sau:
1. Chấp hành nghiêm túc quy định việc công dân Việt Nam ra nước ngoài học tập (Nghị định số 86/2021/NĐ-CP ngày 25/9/2021 của Chính phủ), quyết định cử đi học cử Bộ Giáo dục và Đào tạo và các quy định tài chính hiện hành của Nhà nước. 
2. Cam kết tích cực học tập, nghiên cứu để hoàn thành tốt chương trình đào tạo đúng thời hạn được phép. Nếu phải gia hạn thời gian học tập sẽ tự túc kinh phí trong thời gian gia hạn.
.........., ngày .......... tháng .......... năm ..........
Người cam kết
(ký và ghi rõ họ tên)

CAM KẾT CỦA GIA ĐÌNH
Họ và tên bố (mẹ) hoặc người đại diện hợp pháp: ..........
Công tác tại: ..........
Địa chỉ: ..........
đại diện cho gia đình du học sinh có tên trên, chúng tôi cam kết:
- Nhắc nhở, động viên du học sinh thực hiện đầy đủ trách nhiệm đã được quy định đối với du học sinh.
- Chịu trách nhiệm cùng du học sinh bồi hoàn kinh phí đã được Nhà nước cấp nếu du học sinh không thực hiện đúng cam kết.
 
 	.........., ngày .......... tháng.......... năm ..........
Bố (mẹ) hoặc người đại diện hợp pháp
(ký và ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BẢN CAM KẾT
THỰC HIỆN TRÁCH NHIỆM CỦA DU HỌC SINH
(dành cho người chưa có cơ quan công tác)

Kính gửi: Bộ Giáo dục và Đào tạo

Tên tôi là: [user1_full_name] Sinh ngày [user1_dob]
Giấy CMND/Căn cước công dân số: [user1_id_number] Ngày cấp: [user1_id_issue_date]
Nơi cấp: [user1_id_issue_place] 
Hộ chiếu số: [user1_passport_number] Ngày cấp: [user1_passport_issue_date] 
Nơi cấp: [user1_passport_issue_place]
Hiện nay là: [user1_occupation] 
Khi được Nhà nước cử đi học tại nước ngoài, tôi cam kết thực hiện đúng trách nhiệm của người được cử đi học như sau:
1. Chấp hành nghiêm túc quy định việc công dân Việt Nam ra nước ngoài học tập (Nghị định số 86/2021/NĐ-CP ngày 25/9/2021 của Chính phủ), quyết định cử đi học cử Bộ Giáo dục và Đào tạo và các quy định tài chính hiện hành của Nhà nước. 
2. Cam kết tích cực học tập, nghiên cứu để hoàn thành tốt chương trình đào tạo đúng thời hạn được phép. Nếu phải gia hạn thời gian học tập sẽ tự túc kinh phí trong thời gian gia hạn.
[place], ngày [day] tháng [month] năm [year]
Người cam kết
(ký và ghi rõ họ tên)

CAM KẾT CỦA GIA ĐÌNH
Họ và tên bố (mẹ) hoặc người đại diện hợp pháp: [user2_full_name]
Công tác tại: [user2_occupation]
Địa chỉ: [user2_current_address]
đại diện cho gia đình du học sinh có tên trên, chúng tôi cam kết:
- Nhắc nhở, động viên du học sinh thực hiện đầy đủ trách nhiệm đã được quy định đối với du học sinh.
- Chịu trách nhiệm cùng du học sinh bồi hoàn kinh phí đã được Nhà nước cấp nếu du học sinh không thực hiện đúng cam kết.
 
 	[place], ngày [day] tháng [month] năm [year]
Bố (mẹ) hoặc người đại diện hợp pháp
(ký và ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BẢN CAM KẾT
THỰC HIỆN TRÁCH NHIỆM CỦA DU HỌC SINH
(dành cho người chưa có cơ quan công tác)

Kính gửi: Bộ Giáo dục và Đào tạo

Tên tôi là: .......... Sinh ngày .......... 
Giấy CMND/Căn cước công dân số: .......... Ngày cấp:........../........../..........
Nơi cấp:.......... 
Hộ chiếu số: .......... Ngày cấp: ........../........../.......... 
Nơi cấp:..........
Hiện nay là: .......... 
Khi được Nhà nước cử đi học tại nước ngoài, tôi cam kết thực hiện đúng trách nhiệm của người được cử đi học như sau:
1. Chấp hành nghiêm túc quy định việc công dân Việt Nam ra nước ngoài học tập (Nghị định số 86/2021/NĐ-CP ngày 25/9/2021 của Chính phủ), quyết định cử đi học cử Bộ Giáo dục và Đào tạo và các quy định tài chính hiện hành của Nhà nước. 
2. Cam kết tích cực học tập, nghiên cứu để hoàn thành tốt chương trình đào tạo đúng thời hạn được phép. Nếu phải gia hạn thời gian học tập sẽ tự túc kinh phí trong thời gian gia hạn.
.........., ngày .......... tháng .......... năm ..........
Người cam kết
(ký và ghi rõ họ tên)

CAM KẾT CỦA GIA ĐÌNH
Họ và tên bố (mẹ) hoặc người đại diện hợp pháp: ..........
Công tác tại: ..........
Địa chỉ: ..........
đại diện cho gia đình du học sinh có tên trên, chúng tôi cam kết:
- Nhắc nhở, động viên du học sinh thực hiện đầy đủ trách nhiệm đã được quy định đối với du học sinh.
- Chịu trách nhiệm cùng du học sinh bồi hoàn kinh phí đã được Nhà nước cấp nếu du học sinh không thực hiện đúng cam kết.
 
 	.........., ngày .......... tháng.......... năm ..........
Bố (mẹ) hoặc người đại diện hợp pháp
(ký và ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BẢN CAM KẾT
THỰC HIỆN TRÁCH NHIỆM CỦA DU HỌC SINH
(dành cho người chưa có cơ quan công tác)

Kính gửi: Bộ Giáo dục và Đào tạo

Tên tôi là: [user1_full_name] Sinh ngày [user1_dob]
Giấy CMND/Căn cước công dân số: [user1_id_number] Ngày cấp: [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year]
Nơi cấp: [user1_id_issue_place] 
Hộ chiếu số: [user1_passport_number] Ngày cấp: [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]
Nơi cấp: [user1_passport_issue_place]
Hiện nay là: [user1_occupation] 
Khi được Nhà nước cử đi học tại nước ngoài, tôi cam kết thực hiện đúng trách nhiệm của người được cử đi học như sau:
1. Chấp hành nghiêm túc quy định việc công dân Việt Nam ra nước ngoài học tập (Nghị định số 86/2021/NĐ-CP ngày 25/9/2021 của Chính phủ), quyết định cử đi học cử Bộ Giáo dục và Đào tạo và các quy định tài chính hiện hành của Nhà nước. 
2. Cam kết tích cực học tập, nghiên cứu để hoàn thành tốt chương trình đào tạo đúng thời hạn được phép. Nếu phải gia hạn thời gian học tập sẽ tự túc kinh phí trong thời gian gia hạn.
[place], ngày [day] tháng [month] năm [year]
Người cam kết
(ký và ghi rõ họ tên)

CAM KẾT CỦA GIA ĐÌNH
Họ và tên bố (mẹ) hoặc người đại diện hợp pháp: [user2_full_name]
Công tác tại: [user2_occupation]
Địa chỉ: [user2_current_address]
đại diện cho gia đình du học sinh có tên trên, chúng tôi cam kết:
- Nhắc nhở, động viên du học sinh thực hiện đầy đủ trách nhiệm đã được quy định đối với du học sinh.
- Chịu trách nhiệm cùng du học sinh bồi hoàn kinh phí đã được Nhà nước cấp nếu du học sinh không thực hiện đúng cam kết.
 
 	[place], ngày [day] tháng [month] năm [year]
Bố (mẹ) hoặc người đại diện hợp pháp
(ký và ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
 
ĐƠN ĐỀ NGHỊ CẤP CHÍNH SÁCH NỘI TRÚ
(Dùng cho học sinh, sinh viên đang học tại các cơ sở giáo dục nghề nghiệp công lập)
Kính gửi: ..........(Tên cơ sở giáo dục nghề nghiệp công lập)
Họ và tên:	..........
Ngày, tháng, năm sinh:	........../........../..........
Số định danh cá nhân/Chứng minh nhân dân:..........cấp ngày..........tháng..........năm..........nơi cấp..........
Lớp: ..........Khóa: ..........Khoa: ..........
Mã số học sinh, sinh viên: ..........
Thuộc đối tượng: ..........(ghi rõ đối tượng được quy định tại Điều 2 Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ về chính sách nội trú đối với học sinh, sinh viên học cao đẳng, trung cấp).
Căn cứ Quyết định số 53/2015/QĐ-TTg ngày 20 tháng 10 năm 2015 của Thủ tướng Chính phủ, tôi làm đơn này đề nghị được Nhà trường xem xét để cấp chính sách nội trú theo quy định.

Xác nhận của Khoa
(Quản lý học sinh, sinh viên)	      .........., ngày .......... tháng .......... năm ..........
Người làm đơn
(Ký và ghi rõ họ tên)

```
Output:
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

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI  
 
Kính gửi: .......... 

Tôi tên là: ..........
Cơ quan quản lý trực tiếp (nếu có): ..........	
	
Quyết định cử đi học số .......... ngày .......... tháng .......... năm .......... của 	..........
Tên trường đến học, nước: 	..........
Trình độ đào tạo: 	..........
Ngành/nghề đào tạo: 	..........
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo: 	..........
Ngày nhập học: 	..........
Lý do đề nghị gia hạn:..........
Thời gian đề nghị gia hạn: từ tháng ........../năm 20.......... đến tháng ........../năm 20..........	
Kinh phí trong thời gian gia hạn : 	..........
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập. 

Địa chỉ liên lạc của tôi:	..........
E-mail:	..........
Điện thoại cố định:..........	 Điện thoại di động:..........	



		.........., ngày.......... tháng.......... năm.......... 
Người làm đơn
(Ký và ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐƠN ĐỀ NGHỊ GIA HẠN THỜI GIAN HỌC TẬP Ở NƯỚC NGOÀI  
 
Kính gửi: [receiver] 

Tôi tên là: [user1_full_name]
Cơ quan quản lý trực tiếp (nếu có): [user1_organization]	
	
Quyết định cử đi học số [user1_decision_number] ngày [user1_decision_day] tháng [user1_decision_month] năm [user1_decision_year] của 	[user1_decision_issuer]
Tên trường đến học, nước: 	[user1_school_name]
Trình độ đào tạo: 	[user1_education_level]
Ngành/nghề đào tạo: 	[user1_major]
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo: 	[user1_total_training_time]
Ngày nhập học: 	[user1_enrollment_date]
Lý do đề nghị gia hạn: [user1_extension_reason]
Thời gian đề nghị gia hạn: từ tháng [user1_extension_start_month]/năm 20[user1_extension_start_year] đến tháng [user1_extension_end_month]/năm 20[user1_extension_end_year]	
Kinh phí trong thời gian gia hạn : 	[user1_extension_funding]
Trân trọng đề nghị Quý cơ quan xem xét, cho tôi được gia hạn thời gian học tập. 

Địa chỉ liên lạc của tôi:	[user1_current_address]
E-mail:	[user1_email]
Điện thoại cố định: [user1_phone_home]	 Điện thoại di động: [user1_phone]	



		[place], ngày [day] tháng [month] năm [year] 
Người làm đơn
(Ký và ghi rõ họ tên)

```
## Example:
Input:
```
{form}
```
Output:
"""

health_medical_template_prompt = """
# Instruction: Health and Medical Form

# Goal:
The goal of this form is to gather critical health and medical-related information about users, including personal identification, social and health insurance data, and contact details. This information is vital for medical records, insurance claims, and health-related administrative tasks. Your task is to ensure that all placeholders in the form are correctly replaced with the corresponding tag names for accuracy in health and medical documentation.

# Your Task:

You are responsible for determining the correct tag name for each placeholder in a health and medical-related form. Your task is to ensure that every placeholder in the form is accurately replaced with the corresponding tag name, based on the user's medical and personal information. If a placeholder does not match any defined tag, generate a new tag name accordingly.

- Input Format:

The input is a sample form containing placeholders (..........) for collecting information.
Each placeholder represents a piece of information that needs to be mapped to a specific tag, depending on the type of information it corresponds to.

- Output Format:

The output should be a standardized version of the form, where placeholders have been replaced by tags in the format [userX_tagname] or [tagname].
The placeholder tags should be replaced based on a set of predefined tag names for various types of personal and academic information.
Example output should include accurately mapped tags for each type of information required in the form, ensuring clarity and consistency.

Input and output are placed in ``` ```

1. Identify Unique Users

Task: Determine the number of unique users mentioned in the form.

Action: Assign a unique identifier to each user (e.g., user1, user2, etc.).

Match and Replace Personal and Medical Information Placeholders

Task: For each placeholder (..........), check if it corresponds to a health and medical-related tag name from the provided list {health_and_medical_tagnames}.

Action 1: If a match is found, replace the placeholder with the corresponding tag name in the format [userX_tagname], where X is the user identifier.

Action 2: If a single placeholder should represent multiple related tags (e.g., Ngày, tháng, năm sinh: ......... or Ngày sinh: .........), combine these related tags into a single tag name (e.g., [userX_dob] for date of birth). Avoid splitting into multiple placeholders.

Action 3: If a placeholder requires multiple pieces of information (e.g., Ngày và nơi cấp: ..........), ensure to create separate tags for each specific detail within the same square brackets separated by commas (e.g., [user1_id_issue_date, user1_id_issue_place] for id issue date and id issue place)

Action 4: If the placeholder implies multiple details (e.g., "Hiện đang (làm gì, ở đâu)"), generate separate tags for each detail within the same set of square brackets and separate them using a comma. For example: [user1_occupation, user1_current_address].

Action 5: If no match is found, generate a new tag name in the format [userX_new_tagname] and replace the placeholder with this generated tag name.


2. Handle Non-Personal Information Placeholders

Task: If the placeholder does not correspond to any known study-related tag name:

Action 1: Check against the {remaining_tag_names}.

Action 2: If a match is found, replace the placeholder with the corresponding tag name from this list.

Action 3: If no match is found, generate a new tag name in the format [new_tagname] and replace the placeholder with this generated tag name.

3. Ensure Consistency and Accuracy

Task: Ensure that each placeholder is accurately replaced according to the user's unique identifier and the nature of the information provided.

Action: Review the form to confirm that all placeholders are correctly replaced, maintaining the integrity of the user information and the form structure.

Output only.

## Example:
Input:
```
                        TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ

I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): ..........	[02]. Giới tính: ..........
[03]. Ngày, tháng, năm sinh: ........../........../..........	  [04]. Quốc tịch: ..........
[05]. Dân tộc: ..........	[06]. Số CCCD/ĐDCN/Hộ chiếu: ..........	
[07]. Điện thoại: ..........	[08]. Email (nếu có): ..........	
[09]. Nơi đăng ký khai sinh: [09.1]. Xã: ..........	[09.2]. Huyện: .......... [09.3]. Tỉnh: 
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): ................
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: ..........
[12]. Số nhà, đường/phố, thôn/xóm: ..........	
[13]. Xã: ..........	[14]	Huyện: ..........	[15]. Tỉnh: ..........	
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
```
Output:
```
                        TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ

I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): [user1_full_name]	[02]. Giới tính: [user1_gender]
[03]. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]	  [04]. Quốc tịch: [user1_nationality]
[05]. Dân tộc: [user1_ethnicity]	[06]. Số CCCD/ĐDCN/Hộ chiếu: [user1_id_number]	
[07]. Điện thoại: [user1_phone_number]	[08]. Email (nếu có): [user1_email]	
[09]. Nơi đăng ký khai sinh: [09.1]. Xã: [user1_birth_registration_ward]	[09.2]. Huyện: [user1_birth_registration_district] [09.3]. Tỉnh: [user1_birth_registration_province]
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): [user1_parent_name]
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: [user1_result_delivery_method]
[12]. Số nhà, đường/phố, thôn/xóm: [user1_current_address]	
[13]. Xã: [user1_current_address_ward]	[14]	Huyện: [user1_current_address_district]	[15]. Tỉnh: [user1_current_address_province] 	
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
```

## Example:
Input:
```
                        TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ

I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): ..........	[02]. Giới tính: ..........
[03]. Ngày, tháng, năm sinh: ..........	  [04]. Quốc tịch: ..........
[05]. Dân tộc: ..........	[06]. Số CCCD/ĐDCN/Hộ chiếu: ..........	
[07]. Điện thoại: ..........	[08]. Email (nếu có): ..........	
[09]. Nơi đăng ký khai sinh(Xã, Huyện, Tỉnh): 
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): ................
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: ..........
[12]. Số nhà, đường/phố, thôn/xóm: ..........	
[13]. Xã: ..........	[14]	Huyện: ..........	[15]. Tỉnh: ..........	
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
```
Output:
```
                        TỜ KHAI THAM GIA, ĐIỀU CHỈNH THÔNG TIN BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ

I.	Áp dụng đối với người tham gia tra cứu không thấy mã số BHXH do cơ quan BHXH cấp
[01]. Họ và tên (viết chữ in hoa): [user1_full_name]	[02]. Giới tính: [user1_gender]
[03]. Ngày, tháng, năm sinh: [user1_dob]  [04]. Quốc tịch: [user1_nationality]
[05]. Dân tộc: [user1_ethnicity]	[06]. Số CCCD/ĐDCN/Hộ chiếu: [user1_id_number]	
[07]. Điện thoại: [user1_phone_number]	[08]. Email (nếu có): [user1_email]	
[09]. Nơi đăng ký khai sinh(Xã, Huyện, Tỉnh): [user1_birth_registration_ward, user1_birth_registration_district, user1_birth_registration_province]
[10]. Họ tên cha/mẹ/giám hộ (đối với trẻ em dưới 6 tuổi): [user1_parent_name]
[11]. Đăng ký nhận kết quả giải quyết thủ tục hành chính: [user1_result_delivery_method]
[12]. Số nhà, đường/phố, thôn/xóm: [user1_current_address]	
[13]. Xã: [user1_current_address_ward]	[14]	Huyện: [user1_current_address_district]	[15]. Tỉnh: [user1_current_address_province] 	
[16]. Kê khai Phụ lục Thành viên hộ gia đình (phụ lục kèm theo) đối với người tham gia tra cứu không thấy mã số BHXH và người tham gia BHYT theo hộ gia đình để giảm trừ mức đóng.
```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

GIẤY ĐỀ NGHỊ NHẬN CHẾ ĐỘ BẢO HIỂM XÃ HỘI
KHI NGƯỜI HƯỞNG TỪ TRẦN

Kính gửi: Bảo hiểm xã hội ..........
Tôi tên là:.......... Sinh ngày .......... tháng .......... năm ..........
Số chứng minh nhân dân	..........Ngày cấp: 	.......... Nơi cấp: 	..........
Nơi cư trú (ghi rõ: số nhà, đường phố, tổ/xã/phường):..........
Số điện thoại liên hệ: ..........	
Mối quan hệ với người từ trần: ..........
Tôi xin thay mặt cho tất cả thân nhân là .......... người, gồm:
1. Ông (Bà): .......... Sinh ngày .......... tháng .......... năm ..........
Nơi cư trú: ..........
Mối quan hệ với người từ trần: ..........
2. Ông (Bà): .......... Sinh ngày .......... tháng .......... năm ..........
Nơi cư trú: ..........
Mối quan hệ với người từ trần: ..........
3. ..........
để nhận chế độ BHXH của người đang hưởng chế độ BHXH đã từ trần là Ông (Bà):..........
Số sổ BHXH:.......... Chết ngày .......... tháng .......... năm .......... 
Nơi đang nhận lương hưu, trợ cấp BHXH: ..........
Tôi xin cam đoan những nội dung kê khai trên đây là đầy đủ, đúng sự thật và chịu trách nhiệm trước pháp luật về nội dung kê khai cũng như trong trường hợp xảy ra tranh chấp về việc nhận lương hưu, trợ cấp BHXH theo chế độ của người hưởng đã từ trần. Đề nghị cơ quan BHXH xem xét, giải quyết chế độ BHXH cho gia đình chúng tôi theo quy định.

  .........., ngày .......... tháng .......... năm ..........
Xác nhận của chính quyền địa phương 
nơi người đề nghị đang cư trú
(Ký, ghi rõ họ tên và đóng dấu)	.........., ngày.......... tháng .......... năm..........
Người đề nghị
(ký, ghi rõ họ tên)

Chữ ký của các thân nhân
Người thứ nhất: ..........
(Ký, ghi rõ họ tên)

Người thứ hai: ..........
(Ký, ghi rõ họ tên)



Người thứ ba: ..........
(Ký, ghi rõ họ tên)

	Xét duyệt của cơ quan BHXH                                  
- Tổng số tháng được truy lĩnh:.......... tháng
  Từ tháng.......... năm .......... đến tháng.......... năm ..........
- Tổng số tiền được truy lĩnh: .......... đồng
   Bằng chữ: ..........
           .........., ngày .......... tháng .......... năm ..........
                   Giám đốc BHXH
                  (Ký tên, đóng dấu)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

GIẤY ĐỀ NGHỊ NHẬN CHẾ ĐỘ BẢO HIỂM XÃ HỘI
KHI NGƯỜI HƯỞNG TỪ TRẦN

Kính gửi: Bảo hiểm xã hội [local_insurance_office]
Tôi tên là: [user1_full_name] Sinh ngày [user1_dob_day] tháng [user1_dob_month] năm [user1_dob_year]
Số chứng minh nhân dân [user1_id_number] Ngày cấp: [user1_id_issue_date] Nơi cấp: [user1_id_issue_place]
Nơi cư trú (ghi rõ: số nhà, đường phố, tổ/xã/phường): [user1_current_address]
Số điện thoại liên hệ: [user1_phone]
Mối quan hệ với người từ trần: [user1_relationship_with_deceased]
Tôi xin thay mặt cho tất cả thân nhân là [user1_number_of_relatives] người, gồm:
1. Ông (Bà): [user2_full_name] Sinh ngày [user2_dob_day] tháng [user2_dob_month] năm [user2_dob_year]
Nơi cư trú: [user2_current_address]
Mối quan hệ với người từ trần: [user2_relationship_with_deceased]
2. Ông (Bà): [user3_full_name] Sinh ngày [user3_dob_day] tháng [user3_dob_month] năm [user3_dob_year]
Nơi cư trú: [user3_current_address]
Mối quan hệ với người từ trần: [user3_relationship_with_deceased]
3. [user4_full_name]
để nhận chế độ BHXH của người đang hưởng chế độ BHXH đã từ trần là Ông (Bà): [deceased_full_name]
Số sổ BHXH: [deceased_social_insurance_number] Chết ngày [deceased_death_day] tháng [deceased_death_month] năm [deceased_death_year]
Nơi đang nhận lương hưu, trợ cấp BHXH: [deceased_benefit_receiving_location]
Tôi xin cam đoan những nội dung kê khai trên đây là đầy đủ, đúng sự thật và chịu trách nhiệm trước pháp luật về nội dung kê khai cũng như trong trường hợp xảy ra tranh chấp về việc nhận lương hưu, trợ cấp BHXH theo chế độ của người hưởng đã từ trần. Đề nghị cơ quan BHXH xem xét, giải quyết chế độ BHXH cho gia đình chúng tôi theo quy định.

[user1_current_address], ngày [user1_submission_day] tháng [user1_submission_month] năm [user1_submission_year]
Xác nhận của chính quyền địa phương
nơi người đề nghị đang cư trú
(Ký, ghi rõ họ tên và đóng dấu) [place], ngày [day]tháng[month] năm[year]
Người đề nghị
(ký, ghi rõ họ tên)

Chữ ký của các thân nhân
Người thứ nhất: [user2_signature]
(Ký, ghi rõ họ tên)

Người thứ hai: [user3_signature]
(Ký, ghi rõ họ tên)

Người thứ ba: [user4_signature]
(Ký, ghi rõ họ tên)

Xét duyệt của cơ quan BHXH
- Tổng số tháng được truy lĩnh: [deceased_benefit_backpay_months] tháng
Từ tháng [deceased_benefit_backpay_start_month] năm [deceased_benefit_backpay_start_year] đến tháng [deceased_benefit_backpay_end_month] năm [deceased_benefit_backpay_end_year]
- Tổng số tiền được truy lĩnh: [deceased_benefit_backpay_amount] đồng
Bằng chữ: [deceased_benefit_backpay_amount_words]
[local_insurance_office], ngày [insurance_office_decision_day] tháng [insurance_office_decision_month] năm [insurance_office_decision_year]
Giám đốc BHXH
(Ký tên, đóng dấu)
```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

Độc lập - Tự do - Hạnh phúc

---------------

GIẤY ĐỀ NGHỊ KHÁM GIÁM ĐỊNH

Kính gửi:..........
Tên tôi là: ..........
Ngày, tháng, năm sinh: ..........
Chỗ ở hiện tại: ..........
Giấy Chứng minh nhân dân/Thẻ căn cước/Hộ chiếu số: ..........
Ngày cấp: .......... Nơi cấp:..........
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

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

Độc lập - Tự do - Hạnh phúc

---------------

GIẤY ĐỀ NGHỊ KHÁM GIÁM ĐỊNH

Kính gửi: [receiver]
Tên tôi là: [user1_full_name]
Ngày, tháng, năm sinh: [user1_dob]
Chỗ ở hiện tại: [user1_current_address]
Giấy Chứng minh nhân dân/Thẻ căn cước/Hộ chiếu số: [user1_id_number]
Ngày cấp: [user1_id_issue_date] Nơi cấp: [user1_id_issue_place]
Số sổ bảo hiểm xã hội/Mã số bảo hiểm xã hội (1): [user1_social_insurance_number]
Nghề/Công việc (2): [user1_occupation]
Điện thoại liên hệ: [user1_phone]

Đề nghị được giám định mức độ suy giảm khả năng lao động:

Đề nghị giám định (3): [user1_request_content]
Loại hình giám định (4): [user1_assessment_type]
Nội dung giám định (5): [user1_assessment_content]
Đang hưởng chế độ (6): [user1_current_benefits]
Xác nhận của UBND hoặc Công an cấp xã (7)
Người đề nghị

(Ký, ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

Độc lập - Tự do - Hạnh phúc

---------------

GIẤY ĐỀ NGHỊ KHÁM GIÁM ĐỊNH

Kính gửi:..........
Tên tôi là: ..........
Ngày, tháng, năm sinh: ........../........../..........
Chỗ ở hiện tại: ..........
Giấy Chứng minh nhân dân/Thẻ căn cước/Hộ chiếu số: ..........
Ngày cấp: .......... Nơi cấp:..........
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

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

Độc lập - Tự do - Hạnh phúc

---------------

GIẤY ĐỀ NGHỊ KHÁM GIÁM ĐỊNH

Kính gửi: [receiver]
Tên tôi là: [user1_full_name]
Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Chỗ ở hiện tại: [user1_current_address]
Giấy Chứng minh nhân dân/Thẻ căn cước/Hộ chiếu số: [user1_id_number]
Ngày cấp: [user1_id_issue_date] Nơi cấp: [user1_id_issue_place]
Số sổ bảo hiểm xã hội/Mã số bảo hiểm xã hội (1): [user1_social_insurance_number]
Nghề/Công việc (2): [user1_occupation]
Điện thoại liên hệ: [user1_phone]

Đề nghị được giám định mức độ suy giảm khả năng lao động:

Đề nghị giám định (3): [user1_request_content]
Loại hình giám định (4): [user1_assessment_type]
Nội dung giám định (5): [user1_assessment_content]
Đang hưởng chế độ (6): [user1_current_benefits]
Xác nhận của UBND hoặc Công an cấp xã (7)
Người đề nghị

(Ký, ghi rõ họ tên)

```

## Example:
Input:
```
BẢO HIỂM XÃ HỘI TỈNH
PHÒNG........../BHXH HUYỆN..........
-------	CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc 
---------------
Số: ........../TNHS	.........., ngày .......... tháng .......... năm ..........
GIẤY TIẾP NHẬN HỒ SƠ VÀ HẸN TRẢ KẾT QUẢ CẤP, CẤP LẠI 
VÀ ĐỔI THẺ BẢO HIỂM Y TẾ
Người nộp hồ sơ: .......... 
Tên đơn vị (nếu là đại diện cho đơn vị nộp hồ sơ): .......... Mã đơn vị:..........
Họ và tên người tham gia bảo hiểm y tế: ..........
Mã thẻ bảo hiểm y tế: ..........
Nơi đăng ký khám bệnh, chữa bệnh bảo hiểm y tế ban đầu: ..........
Địa chỉ: ..........
Số điện thoại liên hệ: ..........
Email (nếu có) ..........
Nội dung yêu cầu giải quyết: ..........
2. Thời hạn giải quyết hồ sơ theo quy định: .......... ngày
3. Thời gian nhận hồ sơ: ngày .......... tháng .......... năm ..........
4. Thời gian trả kết quả giải quyết hồ sơ: ngày .......... tháng .......... năm ..........
Đối với kết quả là tiền giải quyết chế độ, đề nghị nhận tại:
Số tài khoản: ..........  Ngân hàng ..........
Tên chủ tài khoản: ..........
Đã nhận kết quả giải quyết vào ngày .......... tháng .......... năm ..........
NGƯỜI NHẬN
(Ký và ghi rõ họ tên)
```
Output:
```
BẢO HIỂM XÃ HỘI TỈNH

PHÒNG [local_insurance_office]/BHXH HUYỆN [local_insurance_office]

------- CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
Số: [document_number] /TNHS [place], ngày [day] tháng [month] năm [year]

GIẤY TIẾP NHẬN HỒ SƠ VÀ HẸN TRẢ KẾT QUẢ CẤP, CẤP LẠI VÀ ĐỔI THẺ BẢO HIỂM Y TẾ

Người nộp hồ sơ: [user1_full_name]
Tên đơn vị (nếu là đại diện cho đơn vị nộp hồ sơ): [user1_organisation] Mã đơn vị: [user1_organisation_id]
Họ và tên người tham gia bảo hiểm y tế: [user2_full_name]
Mã thẻ bảo hiểm y tế: [user2_health_insurance_card_number]
Nơi đăng ký khám bệnh, chữa bệnh bảo hiểm y tế ban đầu: [user2_health_insurance_registration_place]
Địa chỉ: [user2_current_address]
Số điện thoại liên hệ: [user2_phone]
Email (nếu có): [user2_email]
Nội dung yêu cầu giải quyết: [user1_request_content]

Thời hạn giải quyết hồ sơ theo quy định: [user1_decision_duration] ngày
Thời gian nhận hồ sơ: ngày [user1_receipt_day] tháng [user1_receipt_month] năm [user1_receipt_year]
Thời gian trả kết quả giải quyết hồ sơ: ngày [user1_result_decision_day] tháng [user1_result_decision_month] năm [user1_result_decision_year]
Đối với kết quả là tiền giải quyết chế độ, đề nghị nhận tại:
Số tài khoản: [user2_bank_account] Ngân hàng: [user2_bank_name]
Tên chủ tài khoản: [user2_full_name]
Đã nhận kết quả giải quyết vào ngày [user2_result_received_day] tháng [user2_result_received_month] năm [user2_result_received_year]

NGƯỜI NHẬN
(Ký và ghi rõ họ tên)
```

## Example:
Input:
```
{form}
```
Output:
"""

vehicle_driver_template_prompt = """
# Instruction: Vehicle Driver Form

# Goal:
The goal of this form is to collect essential information related to vehicle drivers, including personal identification details, driving licenses, tax information, and transport licenses. Accurate data is crucial for vehicle registration, driving license issuance, and compliance with transport regulations. Your task is to ensure that all placeholders in the form are correctly replaced with the appropriate tag names for accurate documentation related to vehicle driving and transportation.

# Your Task:

You are responsible for determining the correct tag name for each placeholder in a vehicle driver-related form. Your task is to ensure that every placeholder in the form is accurately replaced with the corresponding tag name, based on the user's vehicle-related and personal information. If a placeholder does not match any defined tag, generate a new tag name accordingly.

- Input Format:

The input is a sample form containing placeholders (..........) for collecting information.
Each placeholder represents a piece of information that needs to be mapped to a specific tag, depending on the type of information it corresponds to.

- Output Format:

The output should be a standardized version of the form, where placeholders have been replaced by tags in the format [userX_tagname] or [tagname].
The placeholder tags should be replaced based on a set of predefined tag names for various types of personal and academic information.
Example output should include accurately mapped tags for each type of information required in the form, ensuring clarity and consistency.

Input and output are placed in ``` ```

1. Identify Unique Users

Task: Determine the number of unique users mentioned in the form.

Action: Assign a unique identifier to each user (e.g., user1, user2, etc.).

Match and Replace Personal and Vehicle Information Placeholders

Task: For each placeholder (..........), check if it corresponds to a vehicle driver-related tag name from the provided list {vehicle_driver_tagnames}.

Action 1: If a match is found, replace the placeholder with the corresponding tag name in the format [userX_tagname], where X is the user identifier.

Action 2: If a single placeholder should represent multiple related tags (e.g., Ngày, tháng, năm sinh: ......... or Ngày sinh: .........), combine these related tags into a single tag name (e.g., [userX_dob] for date of birth). Avoid splitting into multiple placeholders.

Action 3: If a placeholder requires multiple pieces of information (e.g., Ngày và nơi cấp: ..........), ensure to create separate tags for each specific detail within the same square brackets separated by commas (e.g., [user1_id_issue_date, user1_id_issue_place] for id issue date and id issue place)

Action 4: If the placeholder implies multiple details (e.g., "Hiện đang (làm gì, ở đâu)"), generate separate tags for each detail within the same set of square brackets and separate them using a comma. For example: [user1_occupation, user1_current_address].

Action 5: If no match is found, generate a new tag name in the format [userX_new_tagname] and replace the placeholder with this generated tag name.


2. Handle Non-Personal Information Placeholders

Task: If the placeholder does not correspond to any known study-related tag name:

Action 1: Check against the {remaining_tag_names}.

Action 2: If a match is found, replace the placeholder with the corresponding tag name from this list.

Action 3: If no match is found, generate a new tag name in the format [new_tagname] and replace the placeholder with this generated tag name.

3. Ensure Consistency and Accuracy

Task: Ensure that each placeholder is accurately replaced according to the user's unique identifier and the nature of the information provided.

Action: Review the form to confirm that all placeholders are correctly replaced, maintaining the integrity of the user information and the form structure.

Output only.

## Example:
Input:
```
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
Tên chủ xe :..........
Năm sinh:..........
Địa chỉ : ..........
Số CCCD/CMND/Hộ chiếu của chủ xe:..........
cấp ngày ........../........../.......... tại ..........
Số CCCD/CMND/Hộ chiếu của người làm thủ tục ..........
cấp ngày ........../.......... /.......... tại..........
Điện thoại của chủ xe :..........
Điện thoại của người làm thủ tục :..........
Số hóa đơn điện tử mã số thuế:..........
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp:..........
Số tờ khai hải quan điện tử cơ quan cấp:..........
Số sêri Phiếu KTCLXX Cơ quan cấp ..........
Số giấy phép kinh doanh vận tải cấp ngày ........../.......... / ..........tại..........
Số máy 1 (Engine N0):..........
Số máy 2 (Engine N0):..........
Số khung (Chassis N0):..........
```
Output:
```
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner's)
Tên chủ xe : [user1_full_name]
Năm sinh:[user1_dob_year]
Địa chỉ : [user1_current_address]
Số CCCD/CMND/Hộ chiếu của chủ xe:[user1_id_number]
cấp ngày [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year] tại [user1_id_issue_place]
Số CCCD/CMND/Hộ chiếu của người làm thủ tục [user2_id_number]
cấp ngày [user2_id_issue_day]/[user2_id_issue_month]/[user2_id_issue_year] tại [user2_id_issue_place]
Điện thoại của chủ xe :[user1_phone]
Điện thoại của người làm thủ tục :[user2_phone]
Số hóa đơn điện tử mã số thuế: [user1_tax_invoice_number]
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp: [user1_tax_declaration_code_issuing_agency]
Số tờ khai hải quan điện tử cơ quan cấp: [user1_electronic_customs_declaration_number_issuing_agency]
Số sêri Phiếu KTCLXX Cơ quan cấp [user1_ktclxx_serial_number]
Số giấy phép kinh doanh vận tải cấp ngày [user1_transport_license_issue_day]/[user1_transport_license_issue_month]/[user1_transport_license_issue_year] tại [user1_transport_license_issue_place]
Số máy 1 (Engine N0):[user1_vehicle_engine_number1]
Số máy 2 (Engine N0):[user1_vehicle_engine_number2]
Số khung (Chassis N0):[user1_vehicle_chassis_number] 
```

## Example:
Input:
```
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
Tên chủ xe :..........
Ngày sinh:..........
Địa chỉ : ..........
Số CCCD/CMND/Hộ chiếu của chủ xe:..........
cấp ngày ........../........../.......... tại ..........
Số CCCD/CMND/Hộ chiếu của người làm thủ tục ..........
cấp ngày ........../.......... /.......... tại..........
Điện thoại của chủ xe :..........
Điện thoại của người làm thủ tục :..........
Số hóa đơn điện tử mã số thuế:..........
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp:..........
Số tờ khai hải quan điện tử cơ quan cấp:..........
Số sêri Phiếu KTCLXX Cơ quan cấp ..........
Số giấy phép kinh doanh vận tải cấp ngày ........../.......... / ..........tại..........
Số máy 1 (Engine N0):..........
Số máy 2 (Engine N0):..........
Số khung (Chassis N0):..........
```
Output:
```
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner's)
Tên chủ xe : [user1_full_name]
Ngày sinh:[user1_dob]
Địa chỉ : [user1_current_address]
Số CCCD/CMND/Hộ chiếu của chủ xe:[user1_id_number]
cấp ngày [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year] tại [user1_id_issue_place]
Số CCCD/CMND/Hộ chiếu của người làm thủ tục [user2_id_number]
cấp ngày [user2_id_issue_day]/[user2_id_issue_month]/[user2_id_issue_year] tại [user2_id_issue_place]
Điện thoại của chủ xe :[user1_phone]
Điện thoại của người làm thủ tục :[user2_phone]
Số hóa đơn điện tử mã số thuế: [user1_tax_invoice_number]
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp: [user1_tax_declaration_code_issuing_agency]
Số tờ khai hải quan điện tử cơ quan cấp: [user1_electronic_customs_declaration_number_issuing_agency]
Số sêri Phiếu KTCLXX Cơ quan cấp [user1_ktclxx_serial_number]
Số giấy phép kinh doanh vận tải cấp ngày [user1_transport_license_issue_day]/[user1_transport_license_issue_month]/[user1_transport_license_issue_year] tại [user1_transport_license_issue_place]
Số máy 1 (Engine N0):[user1_vehicle_engine_number1]
Số máy 2 (Engine N0):[user1_vehicle_engine_number2]
Số khung (Chassis N0):[user1_vehicle_chassis_number] 
```

## Example:
Input:
```
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner’s)
Tên chủ xe :..........
Ngày sinh: .........../........../..........
Địa chỉ : ..........
Số CCCD/CMND/Hộ chiếu của chủ xe:..........
cấp ngày ........../........../.......... tại ..........
Số CCCD/CMND/Hộ chiếu của người làm thủ tục ..........
cấp ngày ........../.......... /.......... tại..........
Điện thoại của chủ xe :..........
Điện thoại của người làm thủ tục :..........
Số hóa đơn điện tử mã số thuế:..........
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp:..........
Số tờ khai hải quan điện tử cơ quan cấp:..........
Số sêri Phiếu KTCLXX Cơ quan cấp ..........
Số giấy phép kinh doanh vận tải cấp ngày ........../.......... / ..........tại..........
Số máy 1 (Engine N0):..........
Số máy 2 (Engine N0):..........
Số khung (Chassis N0):..........
```
Output:
```
GIẤY KHAI ĐĂNG KÝ XE (Vehicle registation declaration)
A. PHẦN CHỦ XE TỰ KÊ KHAI (self declaration vehicle owner's)
Tên chủ xe : [user1_full_name]
Ngày sinh:[user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Địa chỉ : [user1_current_address]
Số CCCD/CMND/Hộ chiếu của chủ xe:[user1_id_number]
cấp ngày [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year] tại [user1_id_issue_place]
Số CCCD/CMND/Hộ chiếu của người làm thủ tục [user2_id_number]
cấp ngày [user2_id_issue_day]/[user2_id_issue_month]/[user2_id_issue_year] tại [user2_id_issue_place]
Điện thoại của chủ xe :[user1_phone]
Điện thoại của người làm thủ tục :[user2_phone]
Số hóa đơn điện tử mã số thuế: [user1_tax_invoice_number]
Mã hồ sơ khai lệ phí trước bạ Cơ quan cấp: [user1_tax_declaration_code_issuing_agency]
Số tờ khai hải quan điện tử cơ quan cấp: [user1_electronic_customs_declaration_number_issuing_agency]
Số sêri Phiếu KTCLXX Cơ quan cấp [user1_ktclxx_serial_number]
Số giấy phép kinh doanh vận tải cấp ngày [user1_transport_license_issue_day]/[user1_transport_license_issue_month]/[user1_transport_license_issue_year] tại [user1_transport_license_issue_place]
Số máy 1 (Engine N0):[user1_vehicle_engine_number1]
Số máy 2 (Engine N0):[user1_vehicle_engine_number2]
Số khung (Chassis N0):[user1_vehicle_chassis_number] 
```

## Example:
Input:
```
MẪU ĐƠN ĐỀ NGHỊ ĐỔI, CẤP LẠI GIẤY PHÉP LÁI XE (1)
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
ĐƠN ĐỀ NGHỊ ĐỔI (CẤP LẠI) GIẤY PHÉP LÁI XE (1)
Kính gửi: Sở Giao thông vận tải..........
Tôi là:..........
Ngày tháng năm sinh: .........../........../..........
Số Căn cước công dân hoặc Số Chứng minh nhân dân: ..........
hoặc Hộ chiếu số.......... ngày cấp.......... nơi cấp: ..........
Đã học lái xe tại (trường, năm):
Hiện đã có giấy phép lái xe hạng:..........số:..........
do:.......... cấp ngày........../........../..........
Đề nghị cho tôi được đổi, cấp lại giấy phép lái xe cơ giới đường bộ hạng:..........
Lý do:..........
Vi phạm hành chính trong lĩnh vực giao thông đường bộ với hình thức tước quyền sử dụng giấy phép lái xe(có/không):..........
    .........., ngày .......... tháng .......... năm 20 ..........
NGƯỜI LÀM ĐƠN
(Ký và ghi rõ họ, tên)

```
Output:
```
MẪU ĐƠN ĐỀ NGHỊ ĐỔI, CẤP LẠI GIẤY PHÉP LÁI XE (1)
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
ĐƠN ĐỀ NGHỊ ĐỔI (CẤP LẠI) GIẤY PHÉP LÁI XE (1)
Kính gửi: Sở Giao thông vận tải [receiver]
Tôi là: [user1_full_name]
Ngày tháng năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số Căn cước công dân hoặc Số Chứng minh nhân dân: [user1_id_number]
hoặc Hộ chiếu số [user1_passport_number] ngày cấp [user1_passport_issue_date] nơi cấp: [user1_passport_issue_place]
Đã học lái xe tại (trường, năm): [user1_driving_school, user1_driving_school_year]
Hiện đã có giấy phép lái xe hạng: [user1_driving_license_category] số: [user1_driving_license_number]
do: [user1_driving_license_issuer] cấp ngày [user1_driving_license_issue_day]/[user1_driving_license_issue_month]/[user1_driving_license_issue_year]
Đề nghị cho tôi được đổi, cấp lại giấy phép lái xe cơ giới đường bộ hạng: [user1_new_driving_license_category]
Lý do: [user1_reason]
Vi phạm hành chính trong lĩnh vực giao thông đường bộ với hình thức tước quyền sử dụng giấy phép lái xe(có/không): [user1_driving_license_revoked]
    [user1_driving_license_revoked_details], ngày [user1_driving_license_revoked_day] tháng [user1_driving_license_revoked_month] năm 20 [user1_driving_license_revoked_year]
NGƯỜI LÀM ĐƠN
(Ký và ghi rõ họ, tên)

```

## Example:
Input:
```
MẪU ĐƠN ĐỀ NGHỊ ĐỔI, CẤP LẠI GIẤY PHÉP LÁI XE (1)
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
ĐƠN ĐỀ NGHỊ ĐỔI (CẤP LẠI) GIẤY PHÉP LÁI XE (1)
Kính gửi: Sở Giao thông vận tải..........
Tôi là:..........
Ngày tháng năm sinh: ..........
Số Căn cước công dân hoặc Số Chứng minh nhân dân: ..........
hoặc Hộ chiếu số.......... ngày cấp.......... nơi cấp: ..........
Đã học lái xe tại:..........năm..........
Hiện đã có giấy phép lái xe hạng:..........số:..........
do:.......... cấp ngày........../........../..........
Đề nghị cho tôi được đổi, cấp lại giấy phép lái xe cơ giới đường bộ hạng:..........
Lý do:..........
Vi phạm hành chính trong lĩnh vực giao thông đường bộ với hình thức tước quyền sử dụng giấy phép lái xe(có/không):..........
    .........., ngày .......... tháng .......... năm 20 ..........
NGƯỜI LÀM ĐƠN
(Ký và ghi rõ họ, tên)

```
Output:
```
MẪU ĐƠN ĐỀ NGHỊ ĐỔI, CẤP LẠI GIẤY PHÉP LÁI XE (1)
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
ĐƠN ĐỀ NGHỊ ĐỔI (CẤP LẠI) GIẤY PHÉP LÁI XE (1)
Kính gửi: Sở Giao thông vận tải [receiver]
Tôi là: [user1_full_name]
Ngày tháng năm sinh: [user1_dob]
Số Căn cước công dân hoặc Số Chứng minh nhân dân: [user1_id_number]
hoặc Hộ chiếu số [user1_passport_number] ngày cấp [user1_passport_issue_date] nơi cấp: [user1_passport_issue_place]
Đã học lái xe tại: [user1_driving_school] năm [user1_driving_school_year]
Hiện đã có giấy phép lái xe hạng: [user1_driving_license_category] số: [user1_driving_license_number]
do: [user1_driving_license_issuer] cấp ngày [user1_driving_license_issue_day]/[user1_driving_license_issue_month]/[user1_driving_license_issue_year]
Đề nghị cho tôi được đổi, cấp lại giấy phép lái xe cơ giới đường bộ hạng: [user1_new_driving_license_category]
Lý do: [user1_reason]
Vi phạm hành chính trong lĩnh vực giao thông đường bộ với hình thức tước quyền sử dụng giấy phép lái xe(có/không): [user1_driving_license_revoked]
    [user1_driving_license_revoked_details], ngày [user1_driving_license_revoked_day] tháng [user1_driving_license_revoked_month] năm 20 [user1_driving_license_revoked_year]
NGƯỜI LÀM ĐƠN
(Ký và ghi rõ họ, tên)

```

## Example:
Input:
```
SOCIALIST REPUBLIC OF VIETNAM
Independent - Freedom - Happiness
---------------
ĐƠN ĐỀ NGHỊ CẤP GIẤY PHÉP LÁI XE QUỐC TẾ
APPLICATION FORM FOR ISSUANCE OF INTERNATIONAL DRIVING PERMIT
Kính gửi (To):..........
Tôi là (Full name): ..........
Ngày tháng năm sinh (date of birth) ..........
Số hộ chiếu (Passport No.) ..........cấp ngày (Issuing date): ngày (date): .......... tháng (month).......... năm (year).......... nơi cấp (Place of issue):.......... hoặc Số định danh cá nhân (personal indentification No.):..........
Hiện có giấy phép lái xe cơ giới đường bộ số (Current driving licence No.): ..........
Cơ quan cấp (Issuing Office): ..........
Tại (Place of issue): ..........
Cấp ngày (Issuing date): ngày (date): .......... tháng (month).......... năm (year)..........
Lý do xin cấp giấy phép lái xe (Reason of application for International driving permit:
..........
 	.........., date.......... month.......... year..........
NGƯỜI LÀM ĐƠN (APPLICANT)
(Ký và ghi rõ họ tên)
(Signature and Full name)

```
Output:
```
SOCIALIST REPUBLIC OF VIETNAM
Independent - Freedom - Happiness
---------------
ĐƠN ĐỀ NGHỊ CẤP GIẤY PHÉP LÁI XE QUỐC TẾ
APPLICATION FORM FOR ISSUANCE OF INTERNATIONAL DRIVING PERMIT
Kính gửi (To): [receiver]
Tôi là (Full name): [user1_full_name]
Ngày tháng năm sinh (date of birth) [user1_dob]
Số hộ chiếu (Passport No.) [user1_passport_number] cấp ngày (Issuing date): ngày (date): [user1_passport_issue_day] tháng (month) [user1_passport_issue_month] năm (year) [user1_passport_issue_year] nơi cấp (Place of issue): [user1_passport_issue_place] hoặc Số định danh cá nhân (personal indentification No.): [user1_id_number]
Hiện có giấy phép lái xe cơ giới đường bộ số (Current driving licence No.): [user1_driving_license_number]
Cơ quan cấp (Issuing Office): [user1_driving_license_issuer]
Tại (Place of issue): [user1_driving_license_place]
Cấp ngày (Issuing date): ngày (date): [user1_driving_license_issue_day] tháng (month) [user1_driving_license_issue_month] năm (year) [user1_driving_license_issue_year]
Lý do xin cấp giấy phép lái xe (Reason of application for International driving permit:
[user1_reason]
 	[place], date [day] month [month] year [year]
NGƯỜI LÀM ĐƠN (APPLICANT)
(Ký và ghi rõ họ tên)
(Signature and Full name)

```
## Example:
Input:
```
{form}
```
Output:
"""

job_template_prompt = """

# Instruction: Job-Related Form

# Goal: The goal of this form is to gather comprehensive information related to employment, and unemployment benefits. Accurate completion of this form is crucial for verifying employment history, managing social insurance records, and processing unemployment benefits. Your task is to ensure that all placeholders in the form are correctly replaced with the appropriate tag names for job-related and personal information. If a placeholder does not match any defined tag, generate a new tag name accordingly.

# Your Task:

You are responsible for determining the correct tag name for each placeholder in a job-related form. Your task is to ensure that every placeholder in the form is accurately replaced with the corresponding tag name, based on the user's vehicle-related and personal information. If a placeholder does not match any defined tag, generate a new tag name accordingly.

- Input Format:

The input is a sample form containing placeholders (..........) for collecting information.
Each placeholder represents a piece of information that needs to be mapped to a specific tag, depending on the type of information it corresponds to.

- Output Format:

The output should be a standardized version of the form, where placeholders have been replaced by tags in the format [userX_tagname] or [tagname].
The placeholder tags should be replaced based on a set of predefined tag names for various types of personal and academic information.
Example output should include accurately mapped tags for each type of information required in the form, ensuring clarity and consistency.

Input and output are placed in ``` ```

1. Identify Unique Users
Task: Determine the number of unique users mentioned in the form.

Action: Assign a unique identifier to each user (e.g., user1, user2, etc.).

Match and Replace Personal and Vehicle Information Placeholders

Task: For each placeholder (..........), check if it corresponds to a vehicle driver-related tag name from the provided list {job_tagnames}.

Action 1: If a match is found, replace the placeholder with the corresponding tag name in the format [userX_tagname], where X is the user identifier.

Action 2: If a single placeholder should represent multiple related tags (e.g., Ngày, tháng, năm sinh: ......... or Ngày sinh: .........), combine these related tags into a single tag name (e.g., [userX_dob] for date of birth). Avoid splitting into multiple placeholders.

Action 3: If a placeholder requires multiple pieces of information (e.g., Ngày và nơi cấp: ..........), ensure to create separate tags for each specific detail within the same square brackets separated by commas (e.g., [user1_id_issue_date, user1_id_issue_place] for id issue date and id issue place)

Action 4: If the placeholder implies multiple details (e.g., "Hiện đang (làm gì, ở đâu)"), generate separate tags for each detail within the same set of square brackets and separate them using a comma. For example: [user1_occupation, user1_current_address].

Action 5: If no match is found, generate a new tag name in the format [userX_new_tagname] and replace the placeholder with this generated tag name.


2. Handle Non-Personal Information Placeholders
Task: If the placeholder does not correspond to any known study-related tag name:

Action 1: Check against the {remaining_tag_names}.

Action 2: If a match is found, replace the placeholder with the corresponding tag name from this list.

Action 3: If no match is found, generate a new tag name in the format [new_tagname] and replace the placeholder with this generated tag name.

3. Ensure Consistency and Accuracy
Task: Ensure that each placeholder is accurately replaced according to the user's unique identifier and the nature of the information provided.

Action: Review the form to confirm that all placeholders are correctly replaced, maintaining the integrity of the user information and the form structure.

Output only.

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

THÔNG BÁO 
Về việc .......... (1)
Kính gửi:  Trung tâm Dịch vụ việc làm ..........
Tên tôi là:.......... sinh ngày:..........
Số định danh cá nhân/Chứng minh nhân dân: ..........cấp ngày..........tháng..........năm..........  Nơi cấp..........                 
Số sổ BHXH :..........
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú):..........
Hiện nay, tôi đang hưởng trợ cấp thất nghiệp theo Quyết định số.......... ngày ........../........../.......... của Giám đốc Sở Lao động - Thương binh và Xã hội tỉnh/thành phố..........
Tổng số tháng tôi đã hưởng trợ cấp thất nghiệp: .......... tháng
Nhưng vì lý do (1)...........nên tôi gửi thông báo này (kèm theo bản sao giấy tờ có liên quan).
Trường hợp người lao động chưa có bản sao hợp đồng lao động hoặc hợp đồng làm việc (2).
 Đề nghị quý Trung tâm xem xét, thực hiện các thủ tục về chấm dứt hưởng trợ cấp thất nghiệp để bảo lưu thời gian đóng bảo hiểm thất nghiệp tương ứng với số tháng hưởng trợ cấp thất nghiệp mà tôi chưa nhận tiền tại cơ quan bảo hiểm xã hội./.
                                                                          .........., ngày .......... tháng .......... năm ..........
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

THÔNG BÁO 
Về việc [request_content] (1)
Kính gửi:  Trung tâm Dịch vụ việc làm [receiver]
Tên tôi là: [user1_full_name] sinh ngày: [user1_dob]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number] cấp ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year]  Nơi cấp [user1_id_issue_place]                 
Số sổ BHXH : [user1_social_insurance_number]
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú): [user1_current_address]
Hiện nay, tôi đang hưởng trợ cấp thất nghiệp theo Quyết định số [user1_unemployment_decision_number] ngày [user1_unemployment_decision_day]/[user1_unemployment_decision_month]/[user1_unemployment_decision_year] của Giám đốc Sở Lao động - Thương binh và Xã hội tỉnh/thành phố [user1_unemployment_decision_issuer]
Tổng số tháng tôi đã hưởng trợ cấp thất nghiệp: [user1_unemployment_duration] tháng
Nhưng vì lý do (1) [reason] nên tôi gửi thông báo này (kèm theo bản sao giấy tờ có liên quan).
Trường hợp người lao động chưa có bản sao hợp đồng lao động hoặc hợp đồng làm việc (2).
 Đề nghị quý Trung tâm xem xét, thực hiện các thủ tục về chấm dứt hưởng trợ cấp thất nghiệp để bảo lưu thời gian đóng bảo hiểm thất nghiệp tương ứng với số tháng hưởng trợ cấp thất nghiệp mà tôi chưa nhận tiền tại cơ quan bảo hiểm xã hội./.
                                                                          [place], ngày [day] tháng [month] năm [year]
``` 

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

THÔNG BÁO 
Về việc .......... (1)
Kính gửi:  Trung tâm Dịch vụ việc làm ..........
Tên tôi là:.......... sinh ngày: .........../........../..........
Số định danh cá nhân/Chứng minh nhân dân: ..........cấp ngày..........tháng..........năm..........  Nơi cấp..........                 
Số sổ BHXH :..........
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú):..........
Hiện nay, tôi đang hưởng trợ cấp thất nghiệp theo Quyết định số.......... ngày ........../........../.......... của Giám đốc Sở Lao động - Thương binh và Xã hội tỉnh/thành phố..........
Tổng số tháng tôi đã hưởng trợ cấp thất nghiệp: .......... tháng
Nhưng vì lý do (1)...........nên tôi gửi thông báo này (kèm theo bản sao giấy tờ có liên quan).
Trường hợp người lao động chưa có bản sao hợp đồng lao động hoặc hợp đồng làm việc (2).
 Đề nghị quý Trung tâm xem xét, thực hiện các thủ tục về chấm dứt hưởng trợ cấp thất nghiệp để bảo lưu thời gian đóng bảo hiểm thất nghiệp tương ứng với số tháng hưởng trợ cấp thất nghiệp mà tôi chưa nhận tiền tại cơ quan bảo hiểm xã hội./.
                                                                          .........., ngày .......... tháng .......... năm ..........
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

THÔNG BÁO 
Về việc [request_content] (1)
Kính gửi:  Trung tâm Dịch vụ việc làm [receiver]
Tên tôi là: [user1_full_name] sinh ngày: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number] cấp ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year]  Nơi cấp [user1_id_issue_place]                 
Số sổ BHXH : [user1_social_insurance_number]
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú): [user1_current_address]
Hiện nay, tôi đang hưởng trợ cấp thất nghiệp theo Quyết định số [user1_unemployment_decision_number] ngày [user1_unemployment_decision_day]/[user1_unemployment_decision_month]/[user1_unemployment_decision_year] của Giám đốc Sở Lao động - Thương binh và Xã hội tỉnh/thành phố [user1_unemployment_decision_issuer]
Tổng số tháng tôi đã hưởng trợ cấp thất nghiệp: [user1_unemployment_duration] tháng
Nhưng vì lý do (1) [reason] nên tôi gửi thông báo này (kèm theo bản sao giấy tờ có liên quan).
Trường hợp người lao động chưa có bản sao hợp đồng lao động hoặc hợp đồng làm việc (2).
 Đề nghị quý Trung tâm xem xét, thực hiện các thủ tục về chấm dứt hưởng trợ cấp thất nghiệp để bảo lưu thời gian đóng bảo hiểm thất nghiệp tương ứng với số tháng hưởng trợ cấp thất nghiệp mà tôi chưa nhận tiền tại cơ quan bảo hiểm xã hội./.
                                                                          [place], ngày [day] tháng [month] năm [year]
```        

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐỀ NGHỊ HỖ TRỢ HỌC NGHỀ
Kính gửi: Trung tâm Dịch vụ việc làm ..........
Tên tôi là: ..........  .Sinh ngày ........../........../..........
Số chứng minh nhân dân/Thẻ căn cước công dân: ..........
Ngày cấp: ........../........../..........
Nơi cấp: ..........
Số sổ BHXH ..........
Nơi thường trú (1): ..........
Chỗ ở hiện nay (2): ..........
Số điện thoại để liên hệ (nếu có): ..........
Đang hưởng trợ cấp thất nghiệp theo Quyết định số..........ngày .......... tháng..........năm.......... của Giám đốc Sở Lao động - Thương binh và Xã hội tỉnh/thành phố ..........; thời gian hưởng trợ cấp thất nghiệp là .......... tháng (từ ngày..........tháng..........năm.......... đến ngày..........tháng..........năm..........) (đối với trường hợp đang hưởng trợ cấp thất nghiệp).
Tổng số tháng đóng bảo hiểm thất nghiệp: .......... tháng. Đã nộp hồ sơ đề nghị hưởng trợ cấp thất nghiệp ngày ..........tháng..........năm.........., ngày hẹn trả kết quả được ghi trên phiếu hẹn trả kết quả là ngày..........tháng..........năm..........theo phiếu hẹn trả kết quả số ngày ..........tháng..........năm.......... (đối với trường hợp đang chờ kết quả giải quyết hưởng trợ cấp thất nghiệp).
Tổng số tháng đóng bảo hiểm thất nghiệp: .......... tháng (đối với trường hợp người lao động có thời gian đóng bảo hiểm thất nghiệp từ đủ 09 tháng trở lên nhưng không thuộc diện đang hưởng trợ cấp thất nghiệp).
Tôi có nguyện vọng tham gia khóa đào tạo nghề .......... với thời gian .......... tháng, tại (tên cơ sở đào tạo nghề nghiệp, địa chỉ) ..........
Đề nghị quý Trung tâm xem xét, giải quyết chế độ hỗ trợ học nghề để tôi được tham gia khóa đào tạo nghề nêu trên.
    .........., ngày ..........tháng..........năm..........
Người đề nghị
(Ký, ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐỀ NGHỊ HỖ TRỢ HỌC NGHỀ
Kính gửi: Trung tâm Dịch vụ việc làm [receiver]
Tên tôi là: [user1_full_name]  .Sinh ngày [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số chứng minh nhân dân/Thẻ căn cước công dân: [user1_id_number]
Ngày cấp: [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year]
Nơi cấp: [user1_id_issue_place]
Số sổ BHXH [user1_social_insurance_number]
Nơi thường trú (1): [user1_permanent_address]
Chỗ ở hiện nay (2): [user1_current_address]
Số điện thoại để liên hệ (nếu có): [user1_phone_number]
Đang hưởng trợ cấp thất nghiệp theo Quyết định số [user1_unemployment_decision_number] ngày [user1_unemployment_decision_day] tháng [user1_unemployment_decision_month] năm [user1_unemployment_decision_year] của Giám đốc Sở Lao động - Thương binh và Xã hội tỉnh/thành phố [user1_unemployment_decision_issuer]; thời gian hưởng trợ cấp thất nghiệp là [user1_unemployment_duration] tháng (từ ngày [user1_unemployment_start_day] tháng [user1_unemployment_start_month] năm [user1_unemployment_start_year] đến ngày [user1_unemployment_end_day] tháng [user1_unemployment_end_month] năm [user1_unemployment_end_year]) (đối với trường hợp đang hưởng trợ cấp thất nghiệp).
Tổng số tháng đóng bảo hiểm thất nghiệp: [user1_unemployment_insurance_months] tháng. Đã nộp hồ sơ đề nghị hưởng trợ cấp thất nghiệp ngày [user1_unemployment_application_day] tháng [user1_unemployment_application_month] năm [user1_unemployment_application_year], ngày hẹn trả kết quả được ghi trên phiếu hẹn trả kết quả là ngày [user1_unemployment_decision_day] tháng [user1_unemployment_decision_month] năm [user1_unemployment_decision_year] theo phiếu hẹn trả kết quả số ngày [user1_unemployment_decision_day] tháng [user1_unemployment_decision_month] năm [user1_unemployment_decision_year] (đối với trường hợp đang chờ kết quả giải quyết hưởng trợ cấp thất nghiệp).
Tổng số tháng đóng bảo hiểm thất nghiệp: [user1_unemployment_insurance_months] tháng (đối với trường hợp người lao động có thời gian đóng bảo hiểm thất nghiệp từ đủ 09 tháng trở lên nhưng không thuộc diện đang hưởng trợ cấp thất nghiệp).
Tôi có nguyện vọng tham gia khóa đào tạo nghề [user1_training_program] với thời gian [user1_training_duration] tháng, tại [user1_training_center_name_address]
Đề nghị quý Trung tâm xem xét, giải quyết chế độ hỗ trợ học nghề để tôi được tham gia khóa đào tạo nghề nêu trên.
    [place], ngày [day] tháng [month] năm [year]
Người đề nghị
(Ký, ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐỀ NGHỊ HƯỞNG TRỢ CẤP THẤT NGHIỆP
Kính gửi: Trung tâm Dịch vụ việc làm ..........
Tên tôi là:..........sinh ngày .......... /........../..........
Số định danh cá nhân/Chứng minh nhân dân: ..........cấp ngày.......... tháng.......... năm.......... Nơi cấp:..........
Số sổ BHXH: ..........
Số điện thoại:..........Địa chỉ email (nếu có)..........
Số tài khoản (ATM nếu có).......... tại ngân hàng:..........
Trình độ đào tạo:..........
Ngành nghề đào tạo:..........
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú) (1):..........
Ngày ........../........../.........., tôi đã chấm dứt hợp đồng lao động/hợp đồng làm việc với (tên đơn vị)..........
tại địa chỉ:..........
Lý do chấm dứt hợp đồng lao động/hợp đồng làm việc:..........
Loại hợp đồng lao động/hợp đồng làm việc:..........
Số tháng đóng bảo hiểm thất nghiệp..........tháng.
Nơi đề nghị nhận trợ cấp thất nghiệp (BHXH quận/huyện hoặc qua thẻ ATM):..........
Kèm theo Đề nghị này là (2).......... và Sổ bảo hiểm xã hội của tôi. Đề nghị quý Trung tâm xem xét, giải quyết hưởng trợ cấp thất nghiệp cho tôi theo đúng quy định.
Tôi cam đoan nội dung ghi trên là hoàn toàn đúng sự thật, nếu sai tôi sẽ chịu trách nhiệm trước pháp luật.
	 .........., ngày .......... tháng .......... năm ..........
 Người đề nghị
  (Ký, ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐỀ NGHỊ HƯỞNG TRỢ CẤP THẤT NGHIỆP
Kính gửi: Trung tâm Dịch vụ việc làm [receiver]
Tên tôi là: [user1_full_name] sinh ngày [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number] cấp ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year] Nơi cấp: [user1_id_issue_place]
Số sổ BHXH: [user1_social_insurance_number]
Số điện thoại: [user1_phone_number] Địa chỉ email (nếu có) [user1_email]
Số tài khoản (ATM nếu có) [user1_bank_account_number] tại ngân hàng: [user1_bank_name]
Trình độ đào tạo: [user1_education_level]
Ngành nghề đào tạo: [user1_major]
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú) (1): [user1_current_address]
Ngày [user1_termination_date_day]/[user1_termination_date_month]/[user1_termination_date_year], tôi đã chấm dứt hợp đồng lao động/hợp đồng làm việc với [user1_former_employer_name]
tại địa chỉ: [user1_former_employer_address]
Lý do chấm dứt hợp đồng lao động/hợp đồng làm việc: [user1_termination_reason]
Loại hợp đồng lao động/hợp đồng làm việc: [user1_contract_type]
Số tháng đóng bảo hiểm thất nghiệp [user1_unemployment_insurance_months] tháng.
Nơi đề nghị nhận trợ cấp thất nghiệp (BHXH quận/huyện hoặc qua thẻ ATM): [user1_unemployment_benefit_receiving_method]
Kèm theo Đề nghị này là (2) [user1_attached_documents] và Sổ bảo hiểm xã hội của tôi. Đề nghị quý Trung tâm xem xét, giải quyết hưởng trợ cấp thất nghiệp cho tôi theo đúng quy định.
Tôi cam đoan nội dung ghi trên là hoàn toàn đúng sự thật, nếu sai tôi sẽ chịu trách nhiệm trước pháp luật.
	 .........., ngày [day] tháng [month] năm [year]
 Người đề nghị
  (Ký, ghi rõ họ tên)

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐỀ NGHỊ HƯỞNG TRỢ CẤP THẤT NGHIỆP
Kính gửi: Trung tâm Dịch vụ việc làm ..........
Tên tôi là:..........sinh ngày ..........
Số định danh cá nhân/Chứng minh nhân dân: ..........cấp ngày.......... tháng.......... năm.......... Nơi cấp:..........
Số sổ BHXH: ..........
Số điện thoại:..........Địa chỉ email (nếu có)..........
Số tài khoản (ATM nếu có).......... tại ngân hàng:..........
Trình độ đào tạo:..........
Ngành nghề đào tạo:..........
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú) (1):..........
Ngày ........../........../.........., tôi đã chấm dứt hợp đồng lao động/hợp đồng làm việc với (tên đơn vị)..........
tại địa chỉ:..........
Lý do chấm dứt hợp đồng lao động/hợp đồng làm việc:..........
Loại hợp đồng lao động/hợp đồng làm việc:..........
Số tháng đóng bảo hiểm thất nghiệp..........tháng.
Nơi đề nghị nhận trợ cấp thất nghiệp (BHXH quận/huyện hoặc qua thẻ ATM):..........
Kèm theo Đề nghị này là (2).......... và Sổ bảo hiểm xã hội của tôi. Đề nghị quý Trung tâm xem xét, giải quyết hưởng trợ cấp thất nghiệp cho tôi theo đúng quy định.
Tôi cam đoan nội dung ghi trên là hoàn toàn đúng sự thật, nếu sai tôi sẽ chịu trách nhiệm trước pháp luật.
	 .........., ngày .......... tháng .......... năm ..........
 Người đề nghị
  (Ký, ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

ĐỀ NGHỊ HƯỞNG TRỢ CẤP THẤT NGHIỆP
Kính gửi: Trung tâm Dịch vụ việc làm [receiver]
Tên tôi là: [user1_full_name] sinh ngày [user1_dob_day]
Số định danh cá nhân/Chứng minh nhân dân: [user1_id_number] cấp ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year] Nơi cấp: [user1_id_issue_place]
Số sổ BHXH: [user1_social_insurance_number]
Số điện thoại: [user1_phone_number] Địa chỉ email (nếu có) [user1_email]
Số tài khoản (ATM nếu có) [user1_bank_account_number] tại ngân hàng: [user1_bank_name]
Trình độ đào tạo: [user1_education_level]
Ngành nghề đào tạo: [user1_major]
Chỗ ở hiện nay (trường hợp khác nơi đăng ký thường trú) (1): [user1_current_address]
Ngày [user1_termination_date_day]/[user1_termination_date_month]/[user1_termination_date_year], tôi đã chấm dứt hợp đồng lao động/hợp đồng làm việc với [user1_former_employer_name]
tại địa chỉ: [user1_former_employer_address]
Lý do chấm dứt hợp đồng lao động/hợp đồng làm việc: [user1_termination_reason]
Loại hợp đồng lao động/hợp đồng làm việc: [user1_contract_type]
Số tháng đóng bảo hiểm thất nghiệp [user1_unemployment_insurance_months] tháng.
Nơi đề nghị nhận trợ cấp thất nghiệp (BHXH quận/huyện hoặc qua thẻ ATM): [user1_unemployment_benefit_receiving_method]
Kèm theo Đề nghị này là (2) [user1_attached_documents] và Sổ bảo hiểm xã hội của tôi. Đề nghị quý Trung tâm xem xét, giải quyết hưởng trợ cấp thất nghiệp cho tôi theo đúng quy định.
Tôi cam đoan nội dung ghi trên là hoàn toàn đúng sự thật, nếu sai tôi sẽ chịu trách nhiệm trước pháp luật.
	 .........., ngày [day] tháng [month] năm [year]
 Người đề nghị
  (Ký, ghi rõ họ tên)

```

## Example
Input:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

TỜ KHAI THUẾ THU NHẬP CÁ NHÂN 
(Áp dụng đối với cá nhân cư trú và cá nhân không cư trú có thu nhập từ tiền lương, 
tiền công khai thuế trực tiếp với cơ quan thuế)

[01] Kỳ tính thuế: ........../..........   Tháng .......... năm .......... /Quý .......... năm .......... (Từ tháng ........../.......... đến tháng ........../..........)

[04] Tên người nộp thuế: [user1_full_name]
[05] Mã số thuế: ..........	
[06] Địa chỉ: [user1_current_address]
[07] Quận/huyện: .......... [08] Tỉnh/thành phố: ..........
[09] Điện thoại: .......... [10] Fax: .......... [11] Email: ..........
[12] Tên tổ chức trả thu nhập: ..........
[13] Mã số thuế: ..........			
[14] Địa chỉ: ..........
[15] Quận/huyện: .......... [16] Tỉnh/thành phố: ..........
[17] Tên đại lý thuế (nếu có): ..........
[18] Mã số thuế: ..........				
[19] Hợp đồng đại lý thuế: Số: .......... ngày: .......... 
```
Ouput:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

TỜ KHAI THUẾ THU NHẬP CÁ NHÂN 
(Áp dụng đối với cá nhân cư trú và cá nhân không cư trú có thu nhập từ tiền lương, 
tiền công khai thuế trực tiếp với cơ quan thuế)

[01] Kỳ tính thuế: [tax_period_start_month]/[tax_period_start_year]   Tháng [tax_period_start_month] năm [tax_period_start_year] /Quý [tax_period_quarter] năm [tax_period_year] (Từ tháng [tax_period_start_month]/[tax_period_start_year] đến tháng [tax_period_end_month]/[tax_period_end_year])

[04] Tên người nộp thuế: [user1_full_name]
[05] Mã số thuế: [user1_tax_id]	
[06] Địa chỉ: [user1_current_address]
[07] Quận/huyện: [user1_district] [08] Tỉnh/thành phố: [user1_province]
[09] Điện thoại: [user1_phone_number] [10] Fax: [user1_fax_number] [11] Email: [user1_email]
[12] Tên tổ chức trả thu nhập: [employer_name]
[13] Mã số thuế: [employer_tax_id]			
[14] Địa chỉ: [employer_address]
[15] Quận/huyện: [employer_district] [16] Tỉnh/thành phố: [employer_province]
[17] Tên đại lý thuế (nếu có): [tax_agent_name]
[18] Mã số thuế: [tax_agent_tax_id]				
[19] Hợp đồng đại lý thuế: Số: [tax_agent_contract_number] ngày: [tax_agent_contract_date] 
```



## Example:
Input: 
```
{form}
```
Output:
"""

tagname_Nam_ver1_prompt = """
Bạn có nhiệm vụ điền các tagnames vào các biểu mẫu theo định dạng userX_tagname.

**Hướng dẫn chi tiết:**
1. Giữ nguyên cấu trúc form: Không thay đổi nội dung gốc, chỉ điền tagnames vào các vị trí có dấu ..........

2. Điền tagnames theo danh sách cho trước:
- Tôi sẽ cung cấp danh sách tagnames, ý nghĩa của chúng và các mục mà tagname đó thường xuất hiện.
- Các tagnames đại diện cho một đối tượng duy nhất (VD: user1_ là người điền đơn, user2_ là người được khai báo, user3_, user4_ là cha/mẹ).

3. Các trường không có tagname trong danh sách:
- Nếu không có tagname phù hợp, giữ nguyên .........., không điền gì vào. 

4. Lưu ý:
- Ví dụ mục tên cha mẹ, không sử dụng user1_parent_name, mà thay vào đó, cha mẹ sẽ là đối tượng riêng biệt (user3_, user4_), tương tự với các mục khác.
- Các mục như "Kính gửi" sẽ để trống ......, không tự động điền [receiver].

Input: 
- Danh sách tagnames (có ý nghĩa và các mục mà tagnames thường được sử dụng)
{tagname}
- Form gốc, với vị trí cần điền là các dấu ..........

## Ví dụ:
Input:
```
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
```
Output:
```
TỜ KHAI CĂN CƯỚC CÔNG DÂN
1. Họ, chữ đệm và tên(1): [user1_full_name]
2. Họ, chữ đệm và tên gọi khác (nếu có)(1): [user1_alias_name]
3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]; 4. Giới tính (Nam/nữ): [user1_gender]
5. Số CMND/CCCD: [user1_id_number]
6. Dân tộc: [user1_ethnicity]; 7. Tôn giáo: [user1_religion] 8. Quốc tịch: [user1_nationality]
9. Tình trạng hôn nhân: [user1_marital_status] 10. Nhóm máu (nếu có): [user1_blood_type]
11. Nơi đăng ký khai sinh: [user1_birth_registration_place]
12. Quê quán: [user1_hometown]
13. Nơi thường trú: [user1_permanent_address]
14. Nơi ở hiện tại: [user1_current_address]
15. Nghề nghiệp: [user1_occupation] 16. Trình độ học vấn: ..........
[place], ngày [day] tháng [month] năm [year]
```

## Ví dụ:
Input:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH,
BỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC
Kính gửi: ..........
Họ, chữ đệm, tên người yêu cầu: ..........
Nơi cư trú: ..........
Giấy tờ tùy thân: ..........
Cấp ngày: ..........
Quan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch:..........
Đề nghị cơ quan đăng ký việc ..........cho người có tên dưới đây:
Họ, chữ đệm, tên: ..........
Ngày, tháng, năm sinh: ..........
Giới tính:..........Dân tộc:..........Quốc tịch: ..........
Nơi cư trú:  ..........
Giấy tờ tùy thân: ..........
Đã đăng ký  ..........tại.......... ngày.......... tháng .......... năm .......... số: .......... Quyển số:..........
Nội dung: ..........
Lý do:..........
Tôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.
Đề nghị cấp bản sao: Có , Không ; số lượng:..........bản
Làm tại: .......... , ngày ..........  tháng ..........  năm ..........
Người yêu cầu
(Ký, ghi rõ họ, chữ đệm, tên)

Output:
```
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI ĐĂNG KÝ VIỆC THAY ĐỔI, CẢI CHÍNH,
BỔ SUNG THÔNG TIN HỘ TỊCH, XÁC ĐỊNH LẠI DÂN TỘC
Kính gửi: ..........
Họ, chữ đệm, tên người yêu cầu: [user1_full_name]
Nơi cư trú: [user1_current_address]
Giấy tờ tùy thân: [user1_id_number]
Cấp ngày: [user1_id_issue_date]
Quan hệ với người được thay đổi, cải chính, xác định lại dân tộc, bổ sung thông tin hộ tịch: ..........
Đề nghị cơ quan đăng ký việc .......... cho người có tên dưới đây:
Họ, chữ đệm, tên: [user2_full_name]
Ngày, tháng, năm sinh: [user2_dob]
Giới tính: [user2_gender] Dân tộc: [user2_ethnicity] Quốc tịch: [user2_nationality]
Nơi cư trú:  [user2_current_address]
Giấy tờ tùy thân: [user2_id_number]
Đã đăng ký  .......... tại .......... ngày .......... tháng .......... năm .......... số: [user2_registration_number] Quyển số: [user2_registration_volume]
Nội dung: ..........
Lý do: ..........
Tôi cam đoan những nội dung khai trên đây là đúng sự thật và chịu trách nhiệm trước pháp luật về cam đoan của mình.
Đề nghị cấp bản sao: Có , Không ; số lượng: [user1_copy_request] bản
Làm tại: [place] , ngày [day]  tháng [month]  năm [year]
Người yêu cầu
(Ký, ghi rõ họ, chữ đệm, tên) 

```

## Ví dụ:
Input:
```
TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ
(Dùng cho công dân Việt Nam định cư ở nước ngoài 
không có hộ chiếu Việt Nam còn giá trị sử dụng) 

Kính gửi (1):..........
1. Họ, chữ đệm và tên Việt Nam:..........
2. Họ, chữ đệm và tên trong hộ chiếu/giấy tờ do nước ngoài cấp:	..........
3. Ngày, tháng, năm sinh:........../........../ ..........     4. Giới tính:..........
5. Dân tộc:..........     6. Tôn giáo:..........
7. Số định danh cá nhân/CMND: ..........									
8. Số điện thoại (nếu có):..........	 9. E-mail (nếu có):..........
10. Quốc tịch nước ngoài (nếu có):..........
11. Số hộ chiếu/ Giấy tờ đi lại quốc tế do nước ngoài cấp/ Giấy tờ do cơ quan có thẩm quyền Việt Nam cấp:
Số:	.......... Ngày cấp: ........../........../..........
Cơ quan cấp:..........	 Có giá trị đến ngày:........../........../..........
12. Nghề nghiệp, nơi làm việc ở nước ngoài trước khi nhập cảnh Việt Nam:..........
13. Họ, chữ đệm và tên, năm sinh, quốc tịch, nghề nghiệp, nơi làm việc, chỗ ở hiện nay của cha, mẹ, vợ, chồng, con:..........
14. Nơi cư trú ở nước ngoài trước khi nhập cảnh Việt Nam:..........
15. Nơi ở hiện tại ở Việt Nam:..........
16. Nội dung đề nghị (2):..........
17. Họ và tên chủ hộ:..........18. Quan hệ với chủ hộ:..........
19. Số định danh cá nhân/ CMND của chủ hộ:..........
20. Tên cha mẹ: ..........
```									
Output:
```
TỜ KHAI THAY ĐỔI THÔNG TIN CƯ TRÚ
(Dùng cho công dân Việt Nam định cư ở nước ngoài 
không có hộ chiếu Việt Nam còn giá trị sử dụng) 

Kính gửi (1): ..........
1. Họ, chữ đệm và tên Việt Nam: [user1_full_name]
2. Họ, chữ đệm và tên trong hộ chiếu/giấy tờ do nước ngoài cấp:	..........
3. Ngày, tháng, năm sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]     4. Giới tính: [user1_gender]
5. Dân tộc: [user1_ethnicity]     6. Tôn giáo: [user1_religion]
7. Số định danh cá nhân/CMND: [user1_id_number]									
8. Số điện thoại (nếu có): ..........	 9. E-mail (nếu có): ..........
10. Quốc tịch nước ngoài (nếu có): ..........
11. Số hộ chiếu/ Giấy tờ đi lại quốc tế do nước ngoài cấp/ Giấy tờ do cơ quan có thẩm quyền Việt Nam cấp:
Số:	[user1_passport_number] Ngày cấp: [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]
Cơ quan cấp: [user1_passport_issue_place]	 Có giá trị đến ngày: [user1_passport_expiry_day]/[user1_passport_expiry_month]/[user1_passport_expiry_year]
12. Nghề nghiệp, nơi làm việc ở nước ngoài trước khi nhập cảnh Việt Nam: ..........
13. Họ, chữ đệm và tên, năm sinh, quốc tịch, nghề nghiệp, nơi làm việc, chỗ ở hiện nay của cha, mẹ, vợ, chồng, con: [user1_family_info]
14. Nơi cư trú ở nước ngoài trước khi nhập cảnh Việt Nam: ..........
15. Nơi ở hiện tại ở Việt Nam: [user1_current_address]
16. Nội dung đề nghị (2): ..........
17. Họ và tên chủ hộ: [user2_full_name] 18. Quan hệ với chủ hộ: ..........
19. Số định danh cá nhân/ CMND của chủ hộ: [user2_id_number]	
20. Tên cha mẹ: [user3_full_name]
```

## Ví dụ:
Input:
```
{form}
```
Ouput: 
"""

temp = """
- Ngoại lệ: Các mục thể hiện địa điểm, ngày tháng năm làm form này sẽ dùng các tagnames sau:
- - [place] → Địa điểm điền form.
- - [day], [month], [year] → Ngày, tháng, năm hiện tại.
- - Lưu ý các tagname này thường xuất hiện ở cuối form, hoặc đầu, có khi giữa, thể hiện
nơi chốn, ngày tháng năm làm form, ví dụ thường là 
.........., ngày .......... tháng .......... năm .......... hoặc ví dụ tương tự,
Làm tại [place], ngày [day] tháng [month] năm [year]. Tránh trùng lặp với các tagname có hậu tố year khác (như năm cấp định danh, năm cấp hộ chiếu,....).

"""