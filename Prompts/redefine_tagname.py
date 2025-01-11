redefine_tag_names_template_prompt = """
Here is a form template with certain fields represented as placeholder tags. The tag names should match a predefined list, but some tags in this form don't align with the list and need to be corrected. Your task is to generate the output using only the predefined tag names.

Predefined Tags List:

{pre_define_tag_names}

Commonly Mistaken Tags: Errors frequently occur when similar but incorrect tags are used.

# Instructions:

1. Identify incorrect tags: Review each placeholder tag in the form. If a tag does not match any tag in the predefined list, treat it as an error.

2. Replace incorrect tags: For each incorrect tag, choose the closest match from the predefined tag list based on the intended meaning.

3. Update related tags consistently:

- If a corrected tag relates to other tags (e.g., family member names, contact information, roles), update all related tags to maintain consistency.
- Special Rule: For tags involving a person's name, always use the format [userX_full_name] regardless of their role or function. For example:
    Incorrect: "Chủ nhiệm, chủ trì thiết kế: [user1_design_leader]"
    Corrected: "Chủ nhiệm, chủ trì thiết kế: [user1_full_name]"

4. Maintain structure: Do not alter the form's layout, spacing, or non-placeholder content. Only change the placeholder tags as needed.

5. Output only the corrected form: Return only the corrected form with placeholder tags now matching the predefined tags list.

## Example:
Input:
```
CÔNG TY [company_name]
Số: [document_number]/CV-[document_number]
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM

Độc lập - Tự do - Hạnh phúc

                                [place], ngày [day] tháng [month] năm [year]
Kính gửi: [receiver]
(V/v: [request_content])

Tên doanh nghiệp:  CÔNG TY [company_name]
- Số điện thoại liên hệ: [company_phone_number] Fax: [company_fax_number]
- Email: [company_email]
- Mã số thuế: [company_tax_id]
- Ngành nghề kinh doanh: [company_business_field]
- Địa chỉ trụ sở chính: [company_address]
Người đại diện theo pháp luật: [company_legal_representative_name]
- Chức vụ: [company_legal_representative_position]
- CMND/CCCD/Hộ chiếu số: [company_legal_representative_id_number]  Nơi cấp: [company_legal_representative_id_issue_place] Ngày cấp: [company_legal_representative_id_issue_day]/[company_legal_representative_id_issue_month]/[company_legal_representative_id_issue_year]
- Nội dung: [company_request_content] (Trình bày tình hình doanh nghiệp, những vấn đề, thắc mắc mà doanh nghiệp đang vướng phải)

Công ty chúng tôi xin cam kết nội dung trên là đúng và xin hoàn toàn chịu trách nhiệm trước pháp luật.


Nơi nhận:

- Như trên;

- Lưu.

Đại diện Doanh nghiệp

Giám Đốc

(Ký tên và đóng dấu)
```
Output:
```
CÔNG TY [company_name]
Số: [document_number]/CV-[document_number]
CỘNG HOÀ XÃ HỘI CHỦ NGHĨA VIỆT NAM

Độc lập - Tự do - Hạnh phúc

                                [place], ngày [day] tháng [month] năm [year]
Kính gửi: [receiver]
(V/v: [request_content])

Tên doanh nghiệp:  CÔNG TY [company_name]
- Số điện thoại liên hệ: [company_phone_number] Fax: [company_fax_number]
- Email: [company_email]
- Mã số thuế: [company_tax_id]
- Ngành nghề kinh doanh: [company_business_field]
- Địa chỉ trụ sở chính: [company_address]
Người đại diện theo pháp luật: [user1_full_name]
- Chức vụ: [user1_position]
- CMND/CCCD/Hộ chiếu số: [user1_id_number]  Nơi cấp: [user1_id_issue_place] Ngày cấp: [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year]
- Nội dung: [company_request_content] (Trình bày tình hình doanh nghiệp, những vấn đề, thắc mắc mà doanh nghiệp đang vướng phải)

Công ty chúng tôi xin cam kết nội dung trên là đúng và xin hoàn toàn chịu trách nhiệm trước pháp luật.


Nơi nhận:

- Như trên;

- Lưu.

Đại diện Doanh nghiệp

Giám Đốc

(Ký tên và đóng dấu)
```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
                                                                            
GIẤY ĐỀ NGHỊ MUA ĐIỆN 
SỬ DỤNG MỤC ĐÍCH NGOÀI SINH HOẠT
Kính gửi: [receiver]
1.Tên cơ quan hoặc cá nhân đăng ký mua điện: [user1_organization_name] (1).
2.Đại diện là ông (bà): [user1_representative] (2).
3.Số CMND/Hộ chiếu/CMCAND/CMQĐND: [user1_id_number] Cơ quan cấp [user1_id_issue_place] ngày [user1_id_issue_date]
4.Theo giấy uỷ quyền [user1_authorization_document_number] ngày làm việc [user1_authorization_date] của [user1_authorization_issuer]      (3)
5.Số điện thoại liên hệ và nhận nhắn tin (SMS): [user1_phone];
6. Fax [user1_fax] ; 7.Email [user1_email] (4)
8.Tài khoản số: [user1_account_number] Tại ngân hàng: [user1_bank_name] (5)
9.Hình thức thanh toán: [user1_payment_method]
10.Địa chỉ giao dịch: [user1_address]; 
11.Mã số thuế: [user1_tax_code]
12,Mục đích sử dụng điện: [user1_electricity_purpose]
13.Địa điểm đăng ký sử dụng điện: [user1_electricity_location]
14.Công suất đăng ký sử dụng: [user1_electricity_capacity] kW
15.Tình trạng sử dụng điện hiện tại: (Chưa có điện / Đang dùng công tơ chung): [user1_electricity_status]
16.Tên chủ hộ dùng chung/số HĐMBĐ/mã số KH/địa chỉ [user2_shared_household_info] (6).

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
                                                                            
GIẤY ĐỀ NGHỊ MUA ĐIỆN 
SỬ DỤNG MỤC ĐÍCH NGOÀI SINH HOẠT
Kính gửi: [receiver]
1.Tên cơ quan hoặc cá nhân đăng ký mua điện: [user1_organization_name] (1).
2.Đại diện là ông (bà): [user1_full_name] (2).
3.Số CMND/Hộ chiếu/CMCAND/CMQĐND: [user1_id_number] Cơ quan cấp [user1_id_issue_place] ngày [user1_id_issue_date]
4.Theo giấy uỷ quyền [user1_authorization_document_number] ngày làm việc [user1_authorization_date] của [user1_authorization_issuer]      (3)
5.Số điện thoại liên hệ và nhận nhắn tin (SMS): [user1_phone];
6. Fax [user1_fax] ; 7.Email [user1_email] (4)
8.Tài khoản số: [user1_account_number] Tại ngân hàng: [user1_bank_name] (5)
9.Hình thức thanh toán: [user1_payment_method]
10.Địa chỉ giao dịch: [user1_address]; 
11.Mã số thuế: [user1_tax_code]
12,Mục đích sử dụng điện: [user1_electricity_purpose]
13.Địa điểm đăng ký sử dụng điện: [user1_electricity_location]
14.Công suất đăng ký sử dụng: [user1_electricity_capacity] kW
15.Tình trạng sử dụng điện hiện tại: (Chưa có điện / Đang dùng công tơ chung): [user1_electricity_status]
16.Tên chủ hộ dùng chung/số HĐMBĐ/mã số KH/địa chỉ [user2_shared_household_info] (6).

```

## Example:
Input:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

THÔNG BÁO THAY ĐỔI THÔNG TIN NGƯỜI HƯỞNG
Kính gửi: Bảo hiểm xã hội quận/huyện/thị xã [local_insurance_office]
Tên tôi là: [user1_full_name] Ngày, tháng, năm sinh: [user1_dob]
Số sổ BHXH/Số định danh: [user1_social_insurance_number]
Số chứng minh nhân dân: [user1_id_number] ngày cấp: [user1_id_issue_date], nơi cấp: [user1_id_issue_place]
Từ tháng [user1_change_request_month] năm [user1_change_request_year], đề nghị cơ quan BHXH thay đổi, bổ sung thông tin của tôi như sau:
Giới tính: [user1_gender]
Số điện thoại: [user1_phone]
Số điện thoại người thân khi cần liên lạc: [user1_emergency_contact_phone]
Địa chỉ cư trú (ghi đầy đủ theo thứ tự số nhà, ngõ, ngách/hẻm, đường phố, tổ/thôn/xóm/ấp, xã/phường/thị trấn, huyện/quận/thị xã/thành phố, tỉnh/thành phố): 
[user1_current_address]
Hình thức nhận lương hưu, trợ cấp BHXH hàng tháng:
Nhận bằng tiền mặt:
Địa chỉ nhận (ghi đầy đủ:xã/phường, tổ dân phố/tổ chi trả, quận/huyện/thị xã, tỉnh/ thành phố): [user1_benefit_receiving_address]
Nhận qua Tài khoản:
Số tài khoản cá nhân: [user1_bank_account]
Ngân hàng nơi mở TK: [user1_bank_name]
Tôi xin cam đoan các thông tin sửa đổi, bổ sung của tôi là đúng, nếu sai tôi xin chịu trách nhiệm trước pháp luật.
	[user1_current_address] , ngày [user1_submission_day] tháng [user1_submission_month] năm [user1_submission_year]
Người đề nghị
(Ký, ghi rõ họ tên)

```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

THÔNG BÁO THAY ĐỔI THÔNG TIN NGƯỜI HƯỞNG
Kính gửi: Bảo hiểm xã hội quận/huyện/thị xã [receiver]
Tên tôi là: [user1_full_name] Ngày, tháng, năm sinh: [user1_dob]
Số sổ BHXH/Số định danh: [user1_social_insurance_number]
Số chứng minh nhân dân: [user1_id_number] ngày cấp: [user1_id_issue_date], nơi cấp: [user1_id_issue_place]
Từ tháng [user1_change_request_month] năm [user1_change_request_year], đề nghị cơ quan BHXH thay đổi, bổ sung thông tin của tôi như sau:
Giới tính: [user1_gender]
Số điện thoại: [user1_phone]
Số điện thoại người thân khi cần liên lạc: [user1_emergency_contact_phone]
Địa chỉ cư trú (ghi đầy đủ theo thứ tự số nhà, ngõ, ngách/hẻm, đường phố, tổ/thôn/xóm/ấp, xã/phường/thị trấn, huyện/quận/thị xã/thành phố, tỉnh/thành phố): 
[user1_current_address]
Hình thức nhận lương hưu, trợ cấp BHXH hàng tháng:
Nhận bằng tiền mặt:
Địa chỉ nhận (ghi đầy đủ:xã/phường, tổ dân phố/tổ chi trả, quận/huyện/thị xã, tỉnh/ thành phố): [user1_benefit_receiving_address]
Nhận qua Tài khoản:
Số tài khoản cá nhân: [user1_bank_account]
Ngân hàng nơi mở TK: [user1_bank_name]
Tôi xin cam đoan các thông tin sửa đổi, bổ sung của tôi là đúng, nếu sai tôi xin chịu trách nhiệm trước pháp luật.
	[place] , ngày [day] tháng [month] năm [year]
Người đề nghị
(Ký, ghi rõ họ tên)

```

## Example:
Input:
```
{form}
```

"""
