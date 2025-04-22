list_cccd_passport_tagnames = [
    "[full_name]",
    "[last_name]",
    "[middle_and_first_name]",
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
    #Nơi sinh
    "[birthplace]",
    "[birthplace_ward]",
    "[birthplace_district]",
    "[birthplace_province]",
    #Nơi đăng ký khai sinh
    "[birth_registration_place]",
    "[birth_registration_place_ward]",
    "[birth_registration_place_district]",
    "[birth_registration_place_province]",
    "[hometown]",
    "[hometown_ward]",
    "[hometown_district]",
    "[hometown_province]",
    "[permanent_address]",
    "[permanent_address_village]",
    "[permanent_address_ward]",
    "[permanent_address_district]",
    "[permanent_address_province]",
    "[current_address]",
    "[current_address_village]",
    "[current_address_ward]",
    "[current_address_district]",
    "[current_address_province]",
    "[passport_number]",
    "[passport_issue_date]",
    "[passport_issue_day]",
    "[passport_issue_month]",
    "[passport_issue_year]",
    "[passport_issue_place]",
    "[email]",
    "[home_phone]",
    "[phone]",
    "[health_insurance_number]",
    "[social_insurance_number]",
    "[education_level]",
    "[passport_expiry_date]",
    "[passport_expiry_day]",
    "[passport_expiry_month]",
    "[passport_expiry_year]",
]

#  Define group
group_id_tagname = ["id_number", "id_issue_date", "id_issue_day", "id_issue_month", "id_issue_year", "id_issue_place"]
group_passport_tagname = ["passport_number", "passport_issue_date", "passport_issue_day", "passport_issue_month", "passport_issue_year", "passport_issue_place"]
group_current_address_tagname = ["current_address","current_address_village","current_address_ward","current_address_district","current_address_province"]
group_permanent_address_tagname = ["permanent_address","permanent_address_village","permanent_address_ward","permanent_address_district","permanent_address_province"]
group_hometown_tagname = ["hometown"]
group_birth_registration_tagname = ["birth_registration_place", "birth_registration_place_ward", "birth_registration_place_district", "birth_registration_place_province"]
group_birthplace_tagname = ["birthplace", "birthplace_ward", "birthplace_district", "birthplace_province"]
group_dob_tagname = ["dob_text", "dob", "dob_date", "dob_day", "dob_month", "dob_year"]
group_name_tagname = ["full_name", "alias_name", "last_name", "middle_and_first_name"]
group_education_tagname = ["education_level"]
group_day_month_year = ["_day", "_month", "_year"]
group_phone_tagname = ["phone", "home_phone"]
group_social_insurance_tagname = ["social_insurance_number", "health_insurance_number"]

group_tagname_have_ward_district_province = ["current_address", "permanent_address", "hometown", "birth_registration_place", "birthplace"]

list_context_current_address = ["địa chỉ", "ở", "nơi", "trú", "sống"]
list_permanent_address = ["thường trú", "thương trú", "thương tru"]
list_current_address = ["hiện tại", "tạm trú", "cư trú", "nơi ở", "hiện nay"]
list_hometown = ["quê quán", "nguyên quán", "quê gốc"]
list_occupation = ["nghề nghiệp", "công việc"] 
list_contextual_id_number = ["cmnd", "chứng minh", "cccd", "căn cước", "định danh", "cmtnd", "giấy tờ tùy thân"]
list_contextual_passport = ["hộ chiếu","passport"]
list_contextual_social_number = ["xã hội", "bhxh", "xh"]
list_contextual_health_number = ["y tế", "bhyt", "yt"]
list_education = ["trình độ", "học vấn", "học lực"]
list_village = ["thôn", "xóm"]
list_ward = ["phường", "xã"]
list_district = ["quận", "huyện"]
list_province = ["tỉnh", "phố"]
list_not_village = ["phường", "xã", "quận", "huyện", "tỉnh", "phố"]
list_not_ward = ["thôn", "xóm", "quận", "huyện", "tỉnh", "phố"]
list_not_district = ["thôn", "xóm", "phường", "xã", "tỉnh", "phố"]
list_not_province = ["thôn", "xóm", "phường", "xã", "quận", "huyện"]





list_general_tagnames = ["[receiver]", "[place]", "[day]", "[month]", "[year]"]
# list_general_tagnames = [] # Now empty

tagname_Nam_ver1 = '''
# Hướng dẫn sử dụng tagnames trong biểu mẫu

## Định nghĩa tagname
Tagname được định nghĩa là một chuỗi ký tự đặc biệt, đại diện cho một giá trị cụ thể liên quan đến người dùng. Mỗi Tagname bao gồm hai phần: phần đầu tiên xác định người dùng,
được biểu diễn dưới dạng userX, trong đó X là số thứ tự của người dùng trong biểu mẫu; phần thứ hai là trường thông tin field name, biểu thị một loại thông tin cụ thể của người
dùng, chẳng hạn như `full_name`, `dob`, `id_number`, v.v.
Ví dụ, tagname [user2_full_name] biểu thị trường “họ, chữ đệm và tên” của người dùng thứ hai.

**Lưu ý:** Trong các ví dụ dưới đây, nếu không có đề cập cụ thể đến thứ tự người dùng, hãy mặc định hiểu đó là người dùng thứ nhất (tức là `user1`).

Phần dưới dưới đây liệt kê các tagnames phổ biến theo từng nhóm thông tin cụ thể. Mỗi tagname đi kèm phần giải thích cách sử dụng, cách điền vào biểu mẫu,
ví dụ minh họa và những lưu ý quan trọng để tránh sai sót khi áp dụng.
## Với mục liên quan họ tên, có các trường hợp sau:

### 1. Họ và tên đầy đủ
Tagname: [userX_full_name]
- Dùng để điền họ và tên đầy đủ của người dùng, bao gồm cả họ, chữ đệm và tên.
- Một số biểu thức thường gặp: "Họ và tên", "Tên đầy đủ", "Tôi tên là"
Ví dụ điền:
```
Họ và tên: [user1_full_name]
Tôi tên là: [user1_full_name]
```
**Lưu ý:**
- Không sử dụng các tagnames khác cho cha mẹ/người đại diện
- Nếu biểu mẫu yêu cầu nhập họ và tên của cha, mẹ, người giám hộ, người đại diện, thì mỗi người sẽ được xem là một user mới với tagname [userX_full_name].
Không dùng các tagnames như [parent_name], [guardian_name], [representative_name].
Ví dụ:
```
Họ và tên cha: [user3_full_name] (nếu người cha là người dùng thứ 3 trong biểu mẫu.)
Họ và tên mẹ: [user4_full_name] (nếu người mẹ là người dùng thứ 4 trong biểu mẫu.)
Họ và tên người đại diện: [user1_full_name] (nếu người đại diện là người dùng thứ 1 trong biểu mẫu.)
```
- Dùng [userX_full_name] khi biểu mẫu yêu cầu nhập cả họ và tên trong một ô duy nhất

### 2. Khi họ, chữ đệm và tên tách riêng
Các tagname:
- Họ: [userX_last_name]
- Chữ đệm + Tên: [user1_middle_and_first_name]
Chọn tagname phù hợp dựa trên cách trình bày trong biểu mẫu:
- Nếu biểu mẫu tách riêng họ và chữ đệm + tên:
Ví dụ điền:
```
Họ: [user1_last_name], Chữ đệm và tên: [user1_middle_and_first_name]
```
```
**Lưu ý:**
- Dùng [user1_middle_and_last_name] khi chữ đệm và tên được gộp chung một ô.

### 3. Tên gọi khác
Tagname: [userX_alias_name]
Biểu thức thường gặp: "Tên gọi khác", "Biệt danh", "Tên thường gọi", "Tên khác (nếu có)"

Ví dụ điền:
```
- Tên gọi khác: [user1_alias_name]
- Tên thường gọi: [user1_alias_name]
```
---

## Với mục ngày sinh, hay ngày tháng năm sinh, có các trường hợp sau:

### 1. Ngày sinh đầy đủ
Tagname: [userX_dob]
- Dùng khi biểu mẫu chỉ có 1 ô để điền ngày/tháng/năm sinh.
- Cụm từ thường gặp: "Ngày sinh", "Ngày tháng năm sinh", "Sinh ngày", "Ngày sinh đầy đủ"
**Lưu ý**
- Nếu biểu mẫu chỉ có một ô trống để điền toàn bộ ngày sinh mà không tách riêng ngày, tháng, năm, dùng [user1_dob].
Ví dụ điền:
```
Ngày sinh: [user1_dob], ngày sinh đầy đủ [user1_dob]
```
### 2. Ngày, tháng, năm sinh tách riêng
- Ngày: [userX_dob_day]
- Tháng: [userX_dob_month]
- Năm: [userX_dob_year]
Chọn tagname phù hợp dựa trên cách trình bày trong biểu mẫu:
- Nếu biểu mẫu yêu cầu nhập ngày, tháng, năm riêng biệt, dùng các tagnames tương ứng:
Ví dụ điền:
```
Ngày sinh ngày [user1_dob_day] tháng [user1_dob_month] năm [user1_dob_year]
```
- Nếu biểu mẫu sử dụng định dạng số (DD/MM/YYYY hoặc DD-MM-YYYY):
Ví dụ điền:
```
Ngày sinh: [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
```

### 3. Ngày sinh viết bằng chữ
Tagname: [userX_dob_text]
Chỉ dùng khi có yêu cầu viết ngày sinh bằng chữ.
Cụm từ thường gặp: "Ngày sinh viết bằng chữ", "Ngày tháng năm sinh viết bằng chữ"
**Lưu ý:**
- Chỉ sử dụng [user1_dob_text] nếu biểu mẫu yêu cầu viết bằng chữ.
Ví dụ điền:
```
Ngày sinh viết bằng chữ: [user1_dob_text]
```

### 4. Chỉ yêu cầu năm sinh
Tagname: [userX_dob_year]
Tagname dành riêng để điền năm sinh khi biểu mẫu không yêu cầu đầy đủ ngày, tháng.
Các mục thường xuất hiện: ["năm sinh"].

Ví dụ:
```
Năm sinh: [user1_dob_year]
```
---

## Với mục liên quan số định danh, CCCD, CMND, có các trường hợp sau:

### 1. Số định danh cá nhân / CCCD / CMND
Tagname: [userX_id_number]
- Dùng để điền số định danh cá nhân, bao gồm:
  - Căn cước công dân (CCCD)
  - Chứng minh nhân dân (CMND)
  - Số định danh cá nhân

Biểu thức thường gặp:
- "Số định danh"
- "Giấy tờ tùy thân"
- "Số CCCD"
- "Số căn cước công dân"
- "Số chứng minh nhân dân"

Ví dụ điền:
```
Số định danh cá nhân: [user1_id_number]
Số CCCD: [user1_id_number]
Số CMND: [user1_id_number]
```
**Lưu ý:**
- Dùng chung `[userX_id_number]` cho cả CCCD và CMND, không phân biệt loại giấy tờ.

### 2. Ngày cấp CCCD/CMND
Các tagnames:
- Ngày cấp đầy đủ: [userX_id_issue_date]
- Ngày riêng: [userX_id_issue_day]
- Tháng riêng: [userX_id_issue_month]
- Năm riêng: [userX_id_issue_year]

Chọn tagname phù hợp dựa trên cách trình bày trong biểu mẫu:

- Nếu chỉ có một ô cho ngày cấp (đầy đủ ngày/tháng/năm):
Ví dụ điền:
```
Ngày cấp: [user1_id_issue_date]
```

- Nếu tách riêng từng phần:
Ví dụ điền:
```
Ngày cấp: ngày [user1_id_issue_day] tháng [user1_id_issue_month] năm [user1_id_issue_year]
```
- Nếu định dạng dạng số (VD: DD/MM/YYYY):
Ví dụ điền:
```
Ngày cấp: [user1_id_issue_day]/[user1_id_issue_month]/[user1_id_issue_year]
```
### 3. Nơi cấp CCCD/CMND
Tagname: [userX_id_issue_place]
- Dùng để điền nơi cấp số định danh cá nhân.

Biểu thức thường gặp:
- "Nơi cấp CCCD"
- "Nơi cấp căn cước"
- "Nơi cấp CMND"
- "Nơi cấp số định danh"

Ví dụ điền:
```
Nơi cấp: [user1_id_issue_place]
```

**Lưu ý:**
Không dùng tagname này cho mục nơi cấp hộ chiếu.


### 4. Cách điền thông tin khi có cả CCCD và CMND
Nguyên tắc: Dùng chung tagname [userX_id_number] cho cả CCCD và CMND.
Ví dụ trong biểu mẫu yêu cầu nhập cả CCCD và CMND:
```
Số CCCD: [user1_id_number], ngày cấp: [user1_id_issue_date], nơi cấp: [user1_id_issue_place]
Số CMND: [user1_id_number], ngày cấp: [user1_id_issue_date], nơi cấp: [user1_id_issue_place]
```

---

## Liên quan đến nơi sinh và nơi đăng ký khai sinh, có các tagnames sau:

### 1. Nơi đăng ký khai sinh (Birth Registration Place)
Tagname: [userX_birth_registration_place]
Nơi mà chính quyền thực hiện đăng ký khai sinh của người dùng. Không nhất thiết phải trùng với nơi sinh thực tế.
Các mục thường xuất hiện: "nơi đăng ký khai sinh", "nơi làm giấy khai sinh", "nơi khai sinh"

Ví dụ điền:
```
Nơi đăng ký khai sinh của người dùng: [user1_birth_registration_place]
hay Nơi làm giấy khai sinh: [user1_birth_registration_place]
```

### 2. Nơi đăng ký khai sinh (Birth Registration Place) - Phân cấp
Tagnames:
- [userX_birth_registration_place_ward]: Phường/xã nơi đăng ký khai sinh.
- [userX_birth_registration_place_district]: Quận/huyện nơi đăng ký khai sinh.
- [userX_birth_registration_place_province]: Tỉnh/thành phố nơi đăng ký khai sinh.
Các mục thường xuất hiện:
- "phường/xã đăng ký khai sinh", "nơi đăng ký khai sinh (phường/xã)"
- "quận/huyện đăng ký khai sinh", "nơi đăng ký khai sinh (quận/huyện)"
- "tỉnh/thành đăng ký khai sinh", "nơi đăng ký khai sinh (tỉnh/thành phố)"

Ví dụ điền:
```
Nơi đăng ký khai sinh: Phường [user1_birth_registration_place_ward], Quận [user1_birth_registration_place_district], Tỉnh [user1_birth_registration_place_province]
```
Hoặc:

```
Phường/Xã đăng ký khai sinh: [user1_birth_registration_place_ward]
Quận/Huyện đăng ký khai sinh: [user1_birth_registration_place_district]
Tỉnh/Thành phố đăng ký khai sinh: [user1_birth_registration_place_province]
```

### 3. Nơi sinh (Birthplace)
Tagname: [userX_birthplace]
 - Địa điểm thực tế mà người dùng sinh ra, có thể là bệnh viện, nhà riêng, hoặc một địa điểm cụ thể.
Các mục thường xuất hiện: "nơi sinh"

Ví dụ điền:
```
Nơi sinh: [user1_birthplace]
```
### 4. Nơi sinh (Birthplace) - Phân cấp
Tagnames:
- [userX_birthplace_ward]: Phường/xã nơi sinh.
- [userX_birthplace_district]: Quận/huyện nơi sinh.
- [userX_birthplace_province]: Tỉnh/thành phố nơi sinh.
Các mục thường xuất hiện:
- "phường/xã nơi sinh", "nơi sinh (phường/xã)"
- "quận/huyện nơi sinh", "nơi sinh (quận/huyện)"
- "tỉnh/thành nơi sinh", "nơi sinh (tỉnh/thành phố)"

Ví dụ điền:
```
Nơi sinh: Phường [user1_birthplace_ward], Quận [user1_birthplace_district], Tỉnh [user1_birthplace_province]
```

hoặc

```
Phường/Xã nơi sinh: [user1_birthplace_ward]
Quận/Huyện nơi sinh: [user1_birthplace_district]
Tỉnh/Thành phố nơi sinh: [user1_birthplace_province]
```

**Lưu ý:**

- Nơi đăng ký khai sinh là nơi cơ quan chính quyền thực hiện đăng ký khai sinh, có thể khác với nơi sinh. Nếu chỉ mục ghi:
- "Nơi đăng ký khai sinh: .........." hoặc "Nơi khai sinh: .........." → Điền [user1_birth_registration_place].
- Nếu có phân cấp (phường/xã, quận/huyện, tỉnh/thành phố), điền tagnames tương ứng như [user1_birth_registration_place_ward], [user1_birth_registration_place_district], [user1_birth_registration_place_province].

---

## Liên quan quê quán, đại chỉ thường trú, địa chỉ tạm trú (cư trú):
### 1. Quê quán
Tagname: [userX_hometown]
- Là quê gốc của người dùng, thường ghi trong giấy khai sinh.
Các mục thường xuất hiện: "quê quán", "nguyên quán".

Ví dụ điền:
```
Quê quán: [user1_hometown], nguyên quán : [user1_hometown]
```

**Lưu ý:**

- Quê quán thường không thay đổi theo thời gian. Là quê của bố/mẹ hoặc nơi sinh ra của người đó.

## 2. Địa chỉ thường trú
Tagname: [userX_permanent_address]
- Địa chỉ hộ khẩu thường trú, tức là nơi ở cố định theo hồ sơ pháp lý.
Các mục thường xuất hiện: "địa chỉ thường trú", "hộ khẩu thường trú".

Ví dụ điền:
```
Địa chỉ thường trú: [user1_permanent_address]
```

**Lưu ý:**

- Địa chỉ thường trú có thể thay đổi nếu người đó chuyển hộ khẩu.
- Nếu có từ khóa như "thường trú", "hộ khẩu" dùng [userX_permanent_address].

### 3. Phân tách địa chỉ thường trú
Tagnames:
- [userX_permanent_address_village]: Thôn/xóm của địa chỉ thường trú.
- [userX_permanent_address_ward]: Phường/xã của địa chỉ thường trú.
- [userX_permanent_address_district]: Quận/huyện của địa chỉ thường trú.
- [userX_permanent_address_province]: Tỉnh/thành phố của địa chỉ thường trú.
Các mục thường xuất hiện:
- "thôn/xóm nơi ở thường trú, "nơi ở (thôn/xóm) thường trú"
- "phường/xã nơi ở thường trú", "nơi ở (phường/xã) thường trú"
- "quận/huyện nơi ở thường trú", "nơi ở (quận/huyện) thường trú"
- "tỉnh/thành nơi ở thường trú", "nơi ở (tỉnh/thành phố) thường trú"

Ví dụ điền:
```
Tỉnh/Thành phố thường trú: [user1_permanent_address_province]
```

### 4. Địa chỉ hiện tại
Tagname: [userX_current_address]
- Địa chỉ nơi người dùng đang sinh sống hiện tại, có thể khác với địa chỉ thường trú.
Các mục thường xuất hiện: "địa chỉ hiện tại", "chỗ ở hiện tại", "nơi cư trú".
Ví dụ điền:
```
Địa chỉ hiện tại: [user1_current_address]
```
**Lưu ý:**
- Hoặc nếu chỉ nói là Địa chỉ mà không nói là thường trú hay tạm trú thì dùng [userX_current_address].
- Nếu có từ khóa như "tạm trú", "nơi ở hiện tại", "nơi cư trú", dùng [user1_current_address]. Không dùng [user1_temporary_address], chỉ dùng [user1_current_address].

### 5. Phân tách địa chỉ hiện tại (village, ward, district, province)
Tagnames:
- [userX_current_address_village]: Thôn/xóm của địa chỉ hiện tại.
- [userX_current_address_ward]: Phường/xã của địa chỉ hiện tại.
- [userX_current_address_district]: Quận/huyện của địa chỉ hiện tại.
- [userX_current_address_province]: Tỉnh/thành phố của địa chỉ hiện tại.
Các mục thường xuất hiện:
- "thôn/xóm nơi ở", "nơi ở (thôn/xóm)"
- "phường/xã nơi ở", "nơi ở (phường/xã)"
- "quận/huyện nơi ở", "nơi ở (quận/huyện)"
- "tỉnh/thành nơi ở", "nơi ở (tỉnh/thành phố)"
Ví dụ điền:
```
Tỉnh/Thành phố nơi ở: [user1_current_address_province]
Nơi cư trú: [user1_current_address]
Nếu thông tin không phải hiện tại thì không điền, ví dụ nơi cư trú trước đây: ..........
```

### 6. Cách phân biệt hometown, permanent_address, current_address
- Hometown (quê quán):
+ Ý nghĩa: Quê gốc của người dùng, thường là nơi sinh ra của bố/mẹ hoặc nơi sinh của chính người đó.
+ Có thể thay đổi không: Không.
+ Từ khóa nhận diện: "quê quán", "nguyên quán".

- Permanent address (địa chỉ thường trú):
+ Ý nghĩa: Địa chỉ hộ khẩu thường trú – nơi ở cố định được ghi trong hồ sơ pháp lý.
+ Có thể thay đổi không: Có (khi chuyển hộ khẩu).
+ Từ khóa nhận diện: "địa chỉ thường trú", "hộ khẩu thường trú".

- Current address (địa chỉ hiện tại):
+ Ý nghĩa: Nơi đang cư trú thực tế, có thể khác với địa chỉ thường trú.
+ Có thể thay đổi không: Có (khi người đó chuyển chỗ ở).
+ Từ khóa nhận diện: "địa chỉ hiện tại", "chỗ ở hiện tại", "nơi cư trú", "Địa chỉ".

---

## Liên quan nghề nghiệp
### 1. Nghề nghiệp
Tagname: [userX_occupation]
- Nghề nghiệp hiện tại của người dùng, mô tả công việc chuyên môn mà họ đang làm.
Các mục thường xuất hiện: "nghề nghiệp", "công việc", "công việc hiện tại".
Ví dụ điền:
```
Nghê nghiệp: [user1_occupation]
```
hoặc
```
Công việc hiện tại: [user1_occupation]
```

**Lưu ý:**

Các trường hợp không sử dụng tagname [user1_occupation]:
- Khi câu chỉ đề cập đến nơi làm việc mà không thể hiện nghề nghiệp cụ thể.
Ví dụ: "Công tác tại: Công ty ABC" → Không điền [user1_occupation].
- Khi thông tin nêu rõ người đó đang thất nghiệp.
Ví dụ: "Thất nghiệp: ..." → Không điền [user1_occupation].
- Khi nội dung liên quan đến bệnh nghề nghiệp, không phải mô tả nghề nghiệp thực tế.
Ví dụ: "Bệnh nghề nghiệp: Viêm phổi mãn tính" → Không điền [user1_occupation].
---

## Với các mục liên quan tới hộ chiếu:
### 1. Sô hộ chiếu
Tagname: [userX_passport_number]
- Dùng để điền số hộ chiếu của người dùng.
Các mục thường xuất hiện: "Số hộ chiếu", "Số passport", "Mã số hộ chiếu", "Mã số passport", "Số hộ chiếu của bạn", "Số hộ chiếu của tôi", "Số hộ chiếu của người dùng".

Ví dụ điền:
```
Số hộ chiếu: [user1_passport_number]
```

### 2. Ngày cấp hộ chiếu:
Tagname: [userX_passport_issue_date]
- Ngày cấp hộ chiếu của người dùng.
- Các mục thường xuất hiện: "Ngày cấp hộ chiếu", "Ngày cấp passport".
Ví dụ điền:
```
Ngày cấp hộ chiếu: [user1_passport_issue_date]
```
**Lưu ý:**
- Nếu input chỉ hiện ngày cấp hộ chiếu: .........., không có tháng, năm phía sau dùng tagname:
thì điền một tagname [user1_passport_issue_date] (vì một tagname này có thể hiện cả 3 mục ngày, tháng, năm)

### 3. Ngày cấp hộ chiếu - Phân tách
Tagnames:
- Ngày cấp hộ chiếu(chỉ tính ngày): [userX_passport_issue_day]
- Tháng cấp hộ chiếu(chỉ tính tháng): [userX_passport_issue_month]
- Năm cấp hộ chiếu(chỉ tính năm): [userX_passport_issue_year]

Lưu ý:
- Nếu input có dạng ngày cấp hộ chiếu: ........../........../.......... (có 3 mục rõ ràng cho ta điền).

Ví dụ điền:
```
Ngày cấp hộ chiếu: [user1_passport_issue_day]/[user1_passport_issue_month]/[user1_passport_issue_year]
```

- Nếu input có dạng ngày cấp hộ chiếu: ngày ..........,tháng .........., năm .......... (có 3 mục rõ ràng cho ta điền) thì điền riêng lẻ từng mục ngày, tháng, năm (vào ..........).

Ví dụ điền:
```
Ngày: [user1_passport_issue_day], tháng: [user1_passport_issue_month], năm: [user1_passport_issue_year]
```

### 4. Nơi cấp hộ chiếu
Tagname: [userX_passport_issue_place]
- Nơi cấp hộ chiếu của người dùng.
Các mục thường xuất hiện: "Nơi cấp hộ chiếu", "Nơi cấp passport", "Nơi cấp số hộ chiếu", "Nơi cấp số passport".
Ví dụ điền:
```
Nơi cấp hộ chiếu: [user1_passport_issue_place]
```

### 5. Với mục ngày hết hạn hộ chiếu
Tagname: [userX_passport_expiry_date]
- Ngày hết hạn hộ chiếu của người dùng.
Các mục thường xuất hiện: "Ngày hết hạn hộ chiếu", "Ngày hết hạn passport", "Ngày hết hạn", "Ngày hết hạn của hộ chiếu", "Ngày hết hạn của passport".

Ví dụ điền:
```
Ngày hết hạn hộ chiếu: [user1_passport_expiry_date]
```

Lưu ý:

- Nếu input chỉ hiện ngày hết hạn hộ chiếu: .........., không có tháng, năm phía sau, hay không có ........../.......... dùng tagname:
thì điền một tagname [user1_passport_expiry_date] (vì một tagname này có thể hiện cả 3 mục ngày, tháng, năm)

### 6. Ngày hết hạn hộ chiếu - Phân tách
Tagnames:
- Ngày hết hạn hộ chiếu(chỉ tính ngày): [userX_passport_expiry_day]
- Tháng hết hạn hộ chiếu(chỉ tính tháng): [userX_passport_expiry_month]
- Năm hết hạn hộ chiếu(chỉ tính năm): [userX_passport_expiry_year]

Lưu ý:
- Nếu input có dạng ngày hết hạn hộ chiếu: ngày ..........,tháng .........., năm .......... (có 3 mục rõ ràng cho ta điền), thì điền riêng lẻ từng mục ngày, tháng, năm (vào ..........).
Ví dụ điền:
```
ngày: [user1_passport_expiry_day], tháng: [user1_passport_expiry_month], năm: [user1_passport_expiry_year]
```

- Nếu input có dạng ngày hết hạn hộ chiếu: ........../........../.......... (có 3 mục rõ ràng cho ta điền),
thì điền riêng lẻ từng mục ngày, tháng, năm (vào ..........).
Ví dụ điền:
```
Ngày hết hạn hộ chiếu:[user1_passport_expiry_day]/[user1_passport_expiry_month]/[user1_passport_expiry_year]
Hoặc nếu chỉ điền 1 tagname
Ngày hết hạn hộ chiếu: .......... --> Ngày hết hạn hộ chiếu: [user1_passport_expiry_date]
```

---

## Các mục khác liên quan đến thông tin cá nhân của người dùng:

### 1. Giới tính
Tagname: [userX_gender]
Biểu thức thường gặp: "Giới tính", "Nam hay nữ"

Ví dụ điền:
```
Giới tính: [user1_gender]
```

### 2. Trình độ học vấn
Tagname: [userX_education_level]
Các mục thường xuất hiện: "trình độ học vấn", "bằng cấp"

Ví dụ điền:
```
Bằng cấp: [user1_education_level]
Trình độ học vấn: [user1_education_level]
```

### 3. Dân tộc
Tagname: [userX_ethnicity]
Các mục thường xuất hiện: "dân tộc", "sắc tộc"

Ví dụ điền:
```
Dân tộc: [user1_ehnicity]
```

### 4. Tôn giáo
Tagname: [user1_religion]
Các mục thường xuất hiện: "tôn giáo"

Ví dụ điền:
```
Tôn giao: [user1_religion]
```


### 5. Quốc tịch
Tagname: [userX_nationality]
Các mục thường xuất hiện: "quốc tịch"

Lưu ý: Không dùng tagname này cho mục "Quốc tịch nước ngoài"

Ví dụ:
```
Quốc tịch: [user1_nationality]

### 6. Tình trạng hôn nhân
Tagname: [userX_marital_status]
Các mục thường xuất hiện: "tình trạng hôn nhân", "trạng thái hôn nhân"

**Lưu ý:** Nếu input là "tình trạng hôn nhân" thì ghi:
  Tình trạng hôn nhân: [user1_marital_status]
  Nếu input là "trạng thái hôn nhân" thì ghi:
  Trạng thái hôn nhân: [user1_marital_status]
  (Giữ nguyên từ ngữ input, không thay đổi)

Ví dụ điền:
```
Trạng thái hôn nhân: [user1_marital_status]
```

### 7. Nhóm máu
Tagname: [userX_blood_type]
Các mục thường xuất hiện: "nhóm máu", "loại máu"

Ví dụ điền:
```
Nhóm máu: [user1_blood_type]
```

---

## Với mục liên quan tới thông tin liên lạc:
### 1. Địa chỉ email của người dùng.
Tagname: [userX_email]
- Dùng để điền địa chỉ email của người dùng.
Các mục thường xuất hiện: "Email", "Địa chỉ email", "Email của bạn".
Ví dụ điền:
```
Email: [user1_email]
```

### 2. Số điện thoại cá nhân.
Tagname: [userX_phone]
- Dùng để điền số điện thoại cá nhân của người dùng.
Các mục thường xuất hiện: "Số điện thoại", "Số điện thoại di động", "SĐT", "Điện thoại cá nhân".

Ví dụ điền:
```
Số điện thoại: [user1_phone], số điện thoại di động [user1_phone]
```
Lưu ý phân biệt với số điền thoại bàn, định nghĩa ngay sau đây.

### 3. Số điện thoại bàn
Tagname: [userX_home_phone]
- Dùng để điền số điện thoại bàn của người dùng.
Các mục thường xuất hiện: "Số điện thoại bàn", "Điện thoại cố định", "Điện thoại nhà riêng".

Ví dụ điền:
```
Số điện thoại bàn: [user1_home_phone], số cố định: [user1_home_phone]
```
## Với các mục liên quan tới số bảo hiểm xã hội:
### 1. Số bảo hiểm xã hội
Tagname: [userX_social_insurance_number]
- Dùng để điền số bảo hiểm xã hội của người dùng.
Các mục thường xuất hiện: "Số bảo hiểm xã hội", "Mã số BHXH", "Số sổ bảo hiểm", "Số bảo hiểm".
Ví dụ điền:
```
Số bảo hiểm xã hội: [user1_social_insurance_number]
```
**Lưu ý:**
- Dùng `[user1_social_insurance_number]` cho mọi biểu mẫu yêu cầu nhập số bảo hiểm xã hội (BHXH).
- Đây là mã số định danh cá nhân trong hệ thống bảo hiểm xã hội.
- Nếu biểu mẫu yêu cầu thông tin về bảo hiểm y tế, sử dụng `[user1_health_insurance_number]`.
'''

temp = None