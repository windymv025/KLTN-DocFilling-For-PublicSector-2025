# ===== Ask LLM generates form =====
import json
import random
# Get random forms
from collections import defaultdict
from Config.tagnames import remaining_tag_names
from Config.LLM import gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Prompts.create_forms import gen_forms_tagnames_label_forms
# Text Processing
from Utils.text_processing import Text_Processing
# os and Time 
import os
import time
import json
import re

from Config.config import Data_num, Type, Label_Input_num

# Folder
label_folder = f"Temp/Data_{Data_num}/{Type}/Label{Label_Input_num}"
info_folder = f"Temp/Data_{Data_num}/{Type}/Info{Label_Input_num}"
input_folder = f"Temp/Data_{Data_num}/{Type}/Input{Label_Input_num}"
# Ensure the folder exists
os.makedirs(info_folder, exist_ok=True)
os.makedirs(label_folder, exist_ok=True)
os.makedirs(input_folder, exist_ok=True)

data = {
  "họ và tên": "Nguyễn Đức Anh",
  "ngày tháng năm sinh": "11/11/2011",
  "tên gọi khác": "Anh Nguyễn",
  "ngày sinh bằng chữ": "Mười một tháng Mười một năm 2011",
  "năm sinh": "2011",
  "giới tính": "Nam",
  "số định danh": "11111111",
  "ngày cấp CCCD": "11/11/2021",
  "nơi cấp CCCD": "Công an TP.HCM 11",
  "nghề nghiệp": "Kỹ sư phần mềm",
  "trình độ học vấn": "Đại học",
  "dân tộc": "Kinh",
  "tôn giáo": "Không",
  "quốc tịch": "Việt Nam",
  "tình trạng hôn nhân": "Độc thân",
  "nhóm máu": "O",
  "nơi sinh": "Bệnh viện Từ Dũ, TP.HCM",
  "nơi đăng ký khai sinh": "UBND Quận 1, TP.HCM",
  "quê quán": "Nam Định",
  "địa chỉ thường trú": "5 Lê Lợi, Hà Nội",
  "địa chỉ hiện tại": "111 Trần Hưng Đạo, TP.HCM",
  "tình trạng hiện tại": "Đang làm việc tại công ty FPT",
  "số hộ chiếu": "C12345678",
  "ngày cấp hộ chiếu": "20/07/2020",
  "nơi cấp hộ chiếu": "Cục Quản lý Xuất nhập cảnh Hà Nội",
  "ngày hết hạn hộ chiếu": "20/07/2030"
}

data2 = {
  "họ và tên": "Trần Minh Khoa",
  "ngày tháng năm sinh": "05/06/1995",
  "tên gọi khác": "Khoa Trần",
  "ngày sinh bằng chữ": "Năm tháng Sáu năm 1995",
  "năm sinh": "1995",
  "giới tính": "Nam",
  "số định danh": "22222222",
  "ngày cấp CCCD": "15/08/2022",
  "nơi cấp CCCD": "Công an TP.Hà Nội",
  "nghề nghiệp": "Bác sĩ",
  "trình độ học vấn": "Cao học",
  "dân tộc": "Kinh",
  "tôn giáo": "Không",
  "quốc tịch": "Việt Nam",
  "tình trạng hôn nhân": "Kết hôn",
  "nhóm máu": "A",
  "nơi sinh": "Bệnh viện Bạch Mai, Hà Nội",
  "nơi đăng ký khai sinh": "UBND Quận Hoàn Kiếm, Hà Nội",
  "quê quán": "Hải Dương",
  "địa chỉ thường trú": "23 Nguyễn Trãi, Hà Nội",
  "địa chỉ hiện tại": "56 Võ Văn Kiệt, Đà Nẵng",
  "tình trạng hiện tại": "Đang công tác tại Bệnh viện Chợ Rẫy",
  "số hộ chiếu": "B98765432",
  "ngày cấp hộ chiếu": "12/03/2019",
  "nơi cấp hộ chiếu": "Cục Quản lý Xuất nhập cảnh TP.HCM",
  "ngày hết hạn hộ chiếu": "12/03/2029"
}

data3 = {
  "họ và tên": "Lê Thanh Hằng",
  "ngày tháng năm sinh": "21/09/1988",
  "tên gọi khác": "Hằng Lê",
  "ngày sinh bằng chữ": "Hai mươi mốt tháng Chín năm 1988",
  "năm sinh": "1988",
  "giới tính": "Nữ",
  "số định danh": "33333333",
  "ngày cấp CCCD": "03/12/2020",
  "nơi cấp CCCD": "Công an TP.Đà Nẵng",
  "nghề nghiệp": "Giáo viên",
  "trình độ học vấn": "Đại học",
  "dân tộc": "Kinh",
  "tôn giáo": "Phật giáo",
  "quốc tịch": "Việt Nam",
  "tình trạng hôn nhân": "Ly hôn",
  "nhóm máu": "B",
  "nơi sinh": "Bệnh viện Phụ sản Đà Nẵng",
  "nơi đăng ký khai sinh": "UBND Quận Hải Châu, Đà Nẵng",
  "quê quán": "Quảng Nam",
  "địa chỉ thường trú": "78 Lý Thường Kiệt, Đà Nẵng",
  "địa chỉ hiện tại": "90 Trần Phú, Đà Nẵng",
  "tình trạng hiện tại": "Giảng dạy tại Trường THPT Nguyễn Hiền",
  "số hộ chiếu": "D24681012",
  "ngày cấp hộ chiếu": "08/09/2021",
  "nơi cấp hộ chiếu": "Cục Quản lý Xuất nhập cảnh Đà Nẵng",
  "ngày hết hạn hộ chiếu": "08/09/2031"
}

data4 = {
  "họ và tên": "Phạm Hoàng Nam",
  "ngày tháng năm sinh": "14/02/2000",
  "tên gọi khác": "Nam Phạm",
  "ngày sinh bằng chữ": "Mười bốn tháng Hai năm 2000",
  "năm sinh": "2000",
  "giới tính": "Nam",
  "số định danh": "44444444",
  "ngày cấp CCCD": "22/05/2023",
  "nơi cấp CCCD": "Công an TP.Cần Thơ",
  "nghề nghiệp": "Kinh doanh",
  "trình độ học vấn": "Cao đẳng",
  "dân tộc": "Kinh",
  "tôn giáo": "Không",
  "quốc tịch": "Việt Nam",
  "tình trạng hôn nhân": "Độc thân",
  "nhóm máu": "AB",
  "nơi sinh": "Bệnh viện Trung ương Huế",
  "nơi đăng ký khai sinh": "UBND TP. Huế",
  "quê quán": "Thừa Thiên Huế",
  "địa chỉ thường trú": "10 Hoàng Diệu, Huế",
  "địa chỉ hiện tại": "27 Nguyễn Văn Linh, Cần Thơ",
  "tình trạng hiện tại": "Chủ doanh nghiệp tư nhân",
  "số hộ chiếu": "E13579246",
  "ngày cấp hộ chiếu": "19/06/2022",
  "nơi cấp hộ chiếu": "Cục Quản lý Xuất nhập cảnh Cần Thơ",
  "ngày hết hạn hộ chiếu": "19/06/2032"
}


noise_data = {
    "Email": "nguyenvantoi@gmail.com",
    "Số điện thoại": "0123456789",
    "Số điện thoại di động": "0987654321",
    "Trường học": "Đại học Khoa học Tự nhiên",
    "Ngành học": "Trí tuệ nhân tạo",
    "Chuyên ngành": "NLP",
    "Mã số học sinh/ sinh viên": "22122212",
    "Lớp học": "22CTT01",
    "Khóa học": "2022-2026",
    "Niên khóa": "2022-2026",
    "Khoa": "Công nghệ Thông tin",
    "Năm học": "2024-2025",
    "Học kì": "Học kỳ 1",
    "Hệ đào tạo": "Chính quy",
    "Quyết định cử đi học": "Số 123/QĐ-ĐHKHTN",
    "Số tài khoản": "0123123123",
    "Ngân hàng": "Vietcombank",
    "Bệnh nghề nghiệp": "Không có",
    "Nơi đăng ký khám bệnh": "Bệnh viện Đại học Y Dược",
    "Tài liệu kèm theo": "Bản sao CMND, giấy khai sinh",
    "Thuộc đối tượng": "Sinh viên chính quy",
    "Đề tài luận văn": "Ứng dụng LLM trong Doc Filling",
    "Thời gian thất nghiệp": "3 tháng"
}

data_tagname = {
    "họ và tên": "user0_full_name",
    "tên gọi khác": "user0_alias_name",
    "ngày sinh bằng chữ": "user0_dob_text",
    "ngày tháng năm sinh": "user0_dob",
    "năm sinh": "user0_dob_year",
    "giới tính": "user0_gender",
    "số định danh": "user0_id_number",
    "ngày cấp CCCD": "user0_id_issue_date",
    "nơi cấp CCCD": "user0_id_issue_place",
    "nghề nghiệp": "user0_occupation",
    "trình độ học vấn": "user0_education_level",
    "dân tộc": "user0_ethnicity",
    "tôn giáo": "user0_religion",
    "quốc tịch": "user0_nationality",
    "tình trạng hôn nhân": "user0_marital_status",
    "nhóm máu": "user0_blood_type",
    "nơi sinh": "user0_birthplace",
    "nơi đăng ký khai sinh": "user0_birth_registration_place",
    "quê quán": "user0_hometown",
    "địa chỉ thường trú": "user0_permanent_address",
    "địa chỉ hiện tại": "user0_current_address",
    "tình trạng hiện tại": "user0_current_status",
    "số hộ chiếu": "user0_passport_number",
    "ngày cấp hộ chiếu": "user0_passport_issue_date",
    "nơi cấp hộ chiếu": "user0_passport_issue_place",
    "ngày hết hạn hộ chiếu": "user0_passport_expiry_date"
}

data_tagname_noise = {
    "Email": "user0_email",
    "Số điện thoại": "user0_phone",
    "Số điện thoại di động": "user0_phone",
    "Trường học": "user0_school",
    "Ngành học": "user0_major",
    "Chuyên ngành": "user0_major",
    "Mã số học sinh/ sinh viên": "user0_MSSV",
    "Lớp học": "user0_class",
    "Khóa học": "user0_grade",
    "Niên khóa": "user0_grade",
    "Khoa": "user0_faculty",
    "Năm học": "user0_school_year",
    "Học kì": "user0_semester",
    "Hệ đào tạo": "user0_training_system",
    "Quyết định cử đi học": "user0_decision_study",
    "Số tài khoản": "user0_bank_account",
    "Ngân hàng": "user0_bank_name",
    "Số": "user0_number",
    "Bệnh nghề nghiệp": "user0_occupational_disease",
    "Nơi đăng ký khám bệnh": "user0_medical_registration_place",
    "Tài liệu kèm theo": "user0_attached_documents",
    "Thuộc đối tượng": "user0_eligible_subject",
    "Đề tài luận văn": "user0_thesis_topic",
    "Thời gian thất nghiệp": "user0_unemployment_duration"
}

merged_data_tagname = {**data_tagname, **data_tagname_noise}

# Gen form 11
prompt = """
# AI Tạo Biểu Mẫu Từ Thông Tin Cá Nhân

## **1. Đầu vào:**  
Dữ liệu đầu vào là danh sách chứa thông tin của **một hoặc nhiều cá nhân** dưới dạng **cặp khóa - giá trị** (*key-value*).  
- **Key**: Tên thông tin (VD: `"họ và tên"`, `"năm sinh"`, `"giới tính"`, v.v.).  
- **Value**: Giá trị tương ứng (VD: `"Nguyễn Đức Anh"`, `"2011"`, `"Nam"`, v.v.).  

---

## **2. Quy tắc chung khi tạo biểu mẫu:**  

### **2.1. Chỉ sử dụng dữ liệu được cung cấp**  
- Nếu một thông tin không có trong dữ liệu đầu vào, điền **[Trống]** thay vì để trống hoặc sử dụng placeholder chung.  
- **Mỗi cá nhân sẽ có một biểu mẫu riêng biệt**, không trộn lẫn dữ liệu giữa nhiều cá nhân.  

### **2.2. Chọn loại biểu mẫu phù hợp**  
Mỗi cá nhân sẽ được tạo một biểu mẫu phù hợp với các trường dữ liệu có sẵn, ví dụ:  
- **Tờ khai căn cước công dân**  
- **Đơn xin cấp hộ chiếu**  
- **Đơn đăng ký tạm trú**  
- **Đơn xin việc**  
- **Đơn đăng ký kết hôn**  
- **Giấy khai sinh**, v.v.  

---

## **3. Quy tắc xử lý dữ liệu khi điền vào form:**  

### **3.1. Ngày tháng năm**  
- **Ngày sinh**: Ghi theo định dạng `dd/mm/yyyy` (VD: `Ngày sinh: [11/11/2011]`).  
- **Ngày sinh bằng chữ**: Giữ nguyên giá trị chữ nếu có (VD: `Ngày sinh bằng chữ: [Mười một tháng Mười một năm 2011]`).  
- **Năm sinh**: Nếu chỉ có "Năm sinh", điền năm đầy đủ (VD: `Năm sinh: [2011]`).  

### **3.2. Danh tính cá nhân**  
- **Tên gọi khác**: Nếu có "Tên gọi khác", ghi vào mục "Tên gọi khác" (VD: `Tên gọi khác: [Anh Nguyễn]`).  
- **Số CCCD/Hộ chiếu**: Nếu có cả số CCCD và số hộ chiếu, ưu tiên điền số CCCD.  
  - VD:  
    - `Số CCCD/Hộ chiếu: [11111111]`  
    - `Ngày cấp: [11/11/2021]`  
    - `Nơi cấp: [Công an TP.HCM]`  

### **3.3. Thông tin về tình trạng cá nhân**  
- **Tình trạng hiện tại** / **Trạng thái hiện tại**: Nếu có dữ liệu, điền theo từng cá nhân.  
  - VD:  
    - `Tình trạng hiện tại: [Đang làm việc tại công ty FPT]`  
    - `Trạng thái hiện tại: [Học tại trường HCMUS]`  

### **3.4. Kinh nghiệm làm việc**  
- Nếu không có dữ liệu, điền **[Trống]**.  

### **3.5. Quy tắc xử lý số liệu cũ**  
- Chỉ điền số hiện tại vào mục chính thống.  

---
## **4. Cách trình bày biểu mẫu nhiều cá nhân**  
- **Dạng danh sách liệt kê**: Khi cần mô tả chi tiết từng cá nhân.  

---

**Lưu ý:**  
- **Không chỉnh sửa hoặc diễn giải lại dữ liệu**.  
- **Đảm bảo văn phong hành chính rõ ràng, trang trọng**.  

-- Ví dụ:

Input:
```
**Thông tin của User1:**

họ và tên: Nguyễn Đức Anh,
ngày tháng năm sinh: 11/11/2011,
tên gọi khác: Anh Nguyễn,
ngày sinh bằng chữ: Mười một tháng Mười một năm 2011,
năm sinh: 2011,
giới tính: Nam,
số định danh: 11111111,
ngày cấp CCCD: 11/11/2021,
nơi cấp CCCD: Công an TP.HCM 11,
nghề nghiệp: Kỹ sư phần mềm,
trình độ học vấn: Đại học,
dân tộc: Kinh,
tôn giáo: Không,
quốc tịch: Việt Nam,
tình trạng hôn nhân: Độc thân,
nhóm máu: O,
nơi sinh: Bệnh viện Từ Dũ, TP.HCM,
nơi đăng ký khai sinh: UBND Quận 1, TP.HCM,
quê quán: Nam Định,
địa chỉ thường trú: 5 Lê Lợi, Hà Nội,
địa chỉ hiện tại: 111 Trần Hưng Đạo, TP.HCM,
tình trạng hiện tại: Đang làm việc tại công ty FPT,
số hộ chiếu: C12345678,
ngày cấp hộ chiếu: 20/07/2020,
nơi cấp hộ chiếu: Cục Quản lý Xuất nhập cảnh Hà Nội,
ngày hết hạn hộ chiếu: 20/07/2030
```

Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
ĐƠN ĐĂNG KÝ TẠM TRÚ
Kính gửi: Công an phường/xã

Họ và tên: [NGUYỄN ĐỨC ANH]
Tên gọi khác: [Anh Nguyễn]
Ngày sinh: [11/11/2011] (Bằng chữ: [Mười một tháng Mười một năm 2011])
Giới tính: [Nam]
Số CCCD: [11111111]
Ngày cấp: [11/11/2021]
Nơi cấp: [Công an TP.HCM 11]

Quê quán: [Nam Định]
Địa chỉ thường trú: [5 Lê Lợi, Hà Nội]
Địa chỉ tạm trú: [111 Trần Hưng Đạo, TP.HCM]

Lý do đăng ký tạm trú: Làm việc tại TP.HCM

Tôi xin cam đoan những thông tin trên là đúng sự thật và cam kết chấp hành đầy đủ quy định về tạm trú theo pháp luật Việt Nam.

[Trống], ngày [Trống] tháng [Trống] năm [Trống]
Người làm đơn
(Ký và ghi rõ họ tên)
[Nguyễn Đức Anh]
```

Input:
```
**Thông tin của User1:**

họ và tên: Nguyễn Đức Anh
ngày tháng năm sinh: 11/11/2011
năm sinh: 2011
giới tính: Nam
tôn giáo: Không
nơi sinh: Bệnh viện Từ Dũ, TP.HCM
ngày cấp CCCD: 11/11/2021
nơi đăng ký khai sinh: UBND Quận 1, TP.HCM
nhóm máu: O
quốc tịch: Việt Nam
số định danh: 11111111
địa chỉ thường trú: 5 Lê Lợi, Hà Nội
nơi cấp CCCD: Công an TP.HCM 11
nơi cấp hộ chiếu: Cục Quản lý Xuất nhập cảnh Hà Nội
ngày cấp hộ chiếu: 20/07/2020
tình trạng hiện tại: Đang làm việc tại công ty FPT
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
TỜ KHAI CĂN CƯỚC CÔNG DÂN
Họ và tên: [NGUYỄN ĐỨC ANH]
Ngày sinh: [11/11/2011]
Năm sinh: [2011]
Giới tính: [Nam]
Tôn giáo: [Không]
Quốc tịch: [Việt Nam]
Nhóm máu: [O]

Số định danh cá nhân: [11111111]
Nơi sinh: [Bệnh viện Từ Dũ, TP.HCM]
Nơi đăng ký khai sinh: [UBND Quận 1, TP.HCM]
Quê quán: [Trống]

Địa chỉ thường trú: [5 Lê Lợi, Hà Nội]

Thông tin giấy tờ cá nhân:

Ngày cấp CCCD: [11/11/2021]
Nơi cấp CCCD: [Công an TP.HCM 11]
Ngày cấp hộ chiếu: [20/07/2020]
Nơi cấp hộ chiếu: [Cục Quản lý Xuất nhập cảnh Hà Nội]
Tình trạng hiện tại: [Đang làm việc tại công ty FPT]

Tôi xin cam đoan những thông tin trên là chính xác và hoàn toàn chịu trách nhiệm trước pháp luật.

[Trống], ngày [Trống] tháng [Trống] năm [Trống]
```

Input:
```
**Thông tin của User1:**

họ và tên: Nguyễn Đức Anh
ngày tháng năm sinh: 11/11/2011
giới tính: Nam
tôn giáo: Không
địa chỉ thường trú: 5 Lê Lợi, Hà Nội
ngày cấp CCCD: 11/11/2021
trình độ học vấn: Đại học
nơi đăng ký khai sinh: UBND Quận 1, TP.HCM
nghề nghiệp: Kỹ sư phần mềm
ngày hết hạn hộ chiếu: 20/07/2030
quê quán: Nam Định
số định danh: 11111111
tên gọi khác: Anh Nguyễn
tình trạng hiện tại: Đang làm việc tại công ty FPT
nơi cấp CCCD: Công an TP.HCM 11
quốc tịch: Việt Nam
nhóm máu: O
ngày cấp hộ chiếu: 20/07/2020
dân tộc: Kinh
địa chỉ hiện tại: 111 Trần Hưng Đạo, TP.HCM
số hộ chiếu: C12345678
nơi sinh: Bệnh viện Từ Dũ, TP.HCM
nơi cấp hộ chiếu: Cục Quản lý Xuất nhập cảnh Hà Nội
tình trạng hôn nhân: Độc thân
ngày sinh bằng chữ: Mười một tháng Mười một năm 2011
năm sinh: 2011/nEmail: nguyenvantoi@gmail.com
Số điện thoại: 0123456789
Số điện thoại di động: 0987654321
Thời gian thất nghiệp: 3 tháng
Thuộc đối tượng: Sinh viên chính quy
Nơi đăng ký khám bệnh: Bệnh viện Đại học Y Dược
Ngân hàng: Vietcombank
Tài liệu kèm theo: Bản sao CMND, giấy khai sinh
Ngành học: Trí tuệ nhân tạo
Khóa học: 2022-2026
Niên khóa: 2022-2026
Mã số học sinh/ sinh viên: 22122212
Số tài khoản: 0123123123
Quyết định cử đi học: Số 123/QĐ-ĐHKHTN
Chuyên ngành: NLP
Khoa: Công nghệ Thông tin
Lớp học: 22CTT01
Hệ đào tạo: Chính quy
Bệnh nghề nghiệp: Không có
Trường học: Đại học Khoa học Tự nhiên
Học kì: Học kỳ 1
Năm học: 2024-2025
Đề tài luận văn: Ứng dụng LLM trong Doc Filling
```

Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
GIẤY CHỨNG NHẬN SINH VIÊN

Kính gửi: [Trống]

Chúng tôi xác nhận rằng:

Họ và tên: [Nguyễn Đức Anh]
Ngày tháng năm sinh: [11/11/2011]
Giới tính: [Nam]
Quốc tịch: [Việt Nam]
Dân tộc: [Kinh]
Tôn giáo: [Không]
Số CCCD/định danh cá nhân: [11111111]
Ngày cấp CCCD: [11/11/2021]
Nơi cấp CCCD: [Công an TP.HCM 11]
Địa chỉ thường trú: [5 Lê Lợi, Hà Nội]
Địa chỉ hiện tại: [111 Trần Hưng Đạo, TP.HCM]
Số điện thoại: [0123456789]
Email: [nguyenvantoi@gmail.com]
Trường học: [Đại học Khoa học Tự nhiên]
Khoa: [Công nghệ Thông tin]
Ngành học: [Trí tuệ nhân tạo]
Chuyên ngành: [NLP]
Hệ đào tạo: [Chính quy]
Mã số học sinh/ sinh viên: [22122212]
Khóa học: [2022-2026]
Đề tài luận văn: [Ứng dụng LLM trong Doc Filling]
Sinh viên [Nguyễn Đức Anh] hiện đang theo học tại [Đại học Khoa học Tự nhiên], 
thuộc [Khoa Công nghệ Thông tin], chuyên ngành [NLP], hệ [Chính quy].

Giấy chứng nhận này được cấp để xác nhận thông tin sinh viên theo yêu cầu.

Ngày [Trống] tháng [Trống] năm [Trống]

XÁC NHẬN CỦA TRƯỜNG
(Ký, đóng dấu)

```

Input:
```
**Thông tin của User1:**

họ và tên: Phạm Hoàng Nam
ngày tháng năm sinh: 14/02/2000
Ngân hàng: Vietcombank
Nơi đăng ký khám bệnh: Bệnh viện Đại học Y Dược
Khoa: Công nghệ Thông tin
Lớp học: 22CTT01
nơi cấp CCCD: Công an TP.Cần Thơ
quốc tịch: Việt Nam
địa chỉ hiện tại: 27 Nguyễn Văn Linh, Cần Thơ
Năm học: 2024-2025
nơi đăng ký khai sinh: UBND TP. Huế
ngày cấp hộ chiếu: 19/06/2022
tên gọi khác: Nam Phạm
năm sinh: 2000
dân tộc: Kinh
giới tính: Nam
tôn giáo: Không
Học kì: Học kỳ 1
Thuộc đối tượng: Sinh viên chính quy
Hệ đào tạo: Chính quy
Email: nguyenvantoi@gmail.com

**Thông tin của User2:**

họ và tên: Lê Thanh Hằng
ngày tháng năm sinh: 21/09/1988
ngày sinh bằng chữ: Hai mươi mốt tháng Chín năm 1988
Quyết định cử đi học: Số 123/QĐ-ĐHKHTN
Số tài khoản: 0123123123
Tài liệu kèm theo: Bản sao CMND, giấy khai sinh
Số điện thoại: 0123456789
Thời gian thất nghiệp: 3 tháng
tên gọi khác: Hằng Lê
Học kì: Học kỳ 1
dân tộc: Kinh
Bệnh nghề nghiệp: Không có
Ngành học: Trí tuệ nhân tạo
Lớp học: 22CTT01
Đề tài luận văn: Ứng dụng LLM trong Doc Filling
Số điện thoại di động: 0987654321
giới tính: Nữ
số hộ chiếu: D24681012
trình độ học vấn: Đại học
Năm học: 2024-2025

**Thông tin của User3:**

họ và tên: Nguyễn Đức Anh
ngày tháng năm sinh: 11/11/2011
nơi sinh: Bệnh viện Từ Dũ, TP.HCM
tình trạng hiện tại: Đang làm việc tại công ty FPT
Ngành học: Trí tuệ nhân tạo
ngày hết hạn hộ chiếu: 20/07/2030
Mã số học sinh/ sinh viên: 22122212
địa chỉ thường trú: 5 Lê Lợi, Hà Nội
Khoa: Công nghệ Thông tin
tình trạng hôn nhân: Độc thân
số định danh: 11111111
Nơi đăng ký khám bệnh: Bệnh viện Đại học Y Dược
ngày sinh bằng chữ: Mười một tháng Mười một năm 2011
Thuộc đối tượng: Sinh viên chính quy
Thời gian thất nghiệp: 3 tháng
Lớp học: 22CTT01
năm sinh: 2011
Bệnh nghề nghiệp: Không có
Tài liệu kèm theo: Bản sao CMND, giấy khai sinh
Trường học: Đại học Khoa học Tự nhiên
Khóa học: 2022-2026
tôn giáo: Không
dân tộc: Kinh
tên gọi khác: Anh Nguyễn
giới tính: Nam
Năm học: 2024-2025
quốc tịch: Việt Nam
địa chỉ hiện tại: 111 Trần Hưng Đạo, TP.HCM
nghề nghiệp: Kỹ sư phần mềm
Email: nguyenvantoi@gmail.com
Đề tài luận văn: Ứng dụng LLM trong Doc Filling
quê quán: Nam Định
```

Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BIỂU MẪU THÔNG TIN CÁ NHÂN

1. Thông tin cá nhân

Họ và tên: [Phạm Hoàng Nam]
Ngày tháng năm sinh: [14/02/2000]
Tên gọi khác: [Nam Phạm]
Giới tính: [Nam]Dân tộc: [Kinh]
Tôn giáo: [Không]Quốc tịch: [Việt Nam]
Nơi đăng ký khai sinh: [UBND TP. Huế]
Nơi cấp CCCD: [Công an TP.Cần Thơ]
Địa chỉ hiện tại: [27 Nguyễn Văn Linh, Cần Thơ]
Ngân hàng: [Vietcombank]
Nơi đăng ký khám bệnh: [Bệnh viện Đại học Y Dược]
Hệ đào tạo: [Chính quy]
Thuộc đối tượng: [Sinh viên chính quy]
Khoa: [Công nghệ Thông tin]
Lớp học: [22CTT01]
Năm học: [2024-2025]
Học kỳ: [Học kỳ 1]
Email: [nguyenvantoi@gmail.com]
Ngày cấp hộ chiếu: [19/06/2022]


Họ và tên: [Lê Thanh Hằng]
Ngày tháng năm sinh: [21/09/1988]
Ngày sinh bằng chữ: [Hai mươi mốt tháng Chín năm 1988]
Tên gọi khác: [Hằng Lê]
Giới tính: [Nữ]
Dân tộc: [Kinh]
Trình độ học vấn: [Đại học]
Ngành học: [Trí tuệ nhân tạo]
Lớp học: [22CTT01]
Năm học: [2024-2025]
Học kỳ: [Học kỳ 1]
Số hộ chiếu: [D24681012]
Bệnh nghề nghiệp: [Không có]
Quyết định cử đi học: [Số 123/QĐ-ĐHKHTN]
Số tài khoản: [0123123123]
Tài liệu kèm theo: [Bản sao CMND, giấy khai sinh]
Thời gian thất nghiệp: [3 tháng]
Số điện thoại: [0123456789]
Số điện thoại di động: [0987654321]
Đề tài luận văn: [Ứng dụng LLM trong Doc Filling]


Họ và tên: [Nguyễn Đức Anh]
Ngày tháng năm sinh: [11/11/2011]
Ngày sinh bằng chữ: [Mười một tháng Mười một năm 2011]
Tên gọi khác: [Anh Nguyễn]
Giới tính: [Nam]
Dân tộc: [Kinh]
Tôn giáo: [Không]
Quốc tịch: [Việt Nam]
Nơi sinh: [Bệnh viện Từ Dũ, TP.HCM]
Địa chỉ thường trú: [5 Lê Lợi, Hà Nội]
Địa chỉ hiện tại: [111 Trần Hưng Đạo, TP.HCM]
Số định danh: [11111111]
Nơi đăng ký khám bệnh: [Bệnh viện Đại học Y Dược]
Tình trạng hiện tại: [Đang làm việc tại công ty FPT]
Nghề nghiệp: [Kỹ sư phần mềm]
Ngành học: [Trí tuệ nhân tạo]
Trường học: [Đại học Khoa học Tự nhiên]
Khoa: [Công nghệ Thông tin]
Lớp học: [22CTT01]
Năm học: [2024-2025]
Khóa học: [2022-2026]
Tài liệu kèm theo: [Bản sao CMND, giấy khai sinh]
Bệnh nghề nghiệp: [Không có]
Tình trạng hôn nhân: [Độc thân]
Thời gian thất nghiệp: [3 tháng]
Đề tài luận văn: [Ứng dụng LLM trong Doc Filling]
Ngày hết hạn hộ chiếu: [20/07/2030]
Email: [nguyenvantoi@gmail.com]
Quê quán: [Nam Định]


Người khai thông tin 1(Ký, ghi rõ họ tên): [Phạm Hoàng Nam]

Người khai thông tin 2(Ký, ghi rõ họ tên): [Lê Thanh Hằng]

Người khai thông tin 3(Ký, ghi rõ họ tên): [Nguyễn Đức Anh]
```

Input:
```
**Thông tin của User1:**

họ và tên: Trần Minh Khoa
ngày tháng năm sinh: 05/06/1995
Năm học: 2024-2025
trình độ học vấn: Cao học
Số tài khoản: 0123123123
Bệnh nghề nghiệp: Không có
Thuộc đối tượng: Sinh viên chính quy
địa chỉ hiện tại: 56 Võ Văn Kiệt, Đà Nẵng
quốc tịch: Việt Nam
Ngân hàng: Vietcombank
Tài liệu kèm theo: Bản sao CMND, giấy khai sinh
Số điện thoại di động: 0987654321
tôn giáo: Không
nghề nghiệp: Bác sĩ
nơi cấp hộ chiếu: Cục Quản lý Xuất nhập cảnh TP.HCM
Nơi đăng ký khám bệnh: Bệnh viện Đại học Y Dược
Số điện thoại: 0123456789
số định danh: 22222222
ngày sinh bằng chữ: Năm tháng Sáu năm 1995
số hộ chiếu: B98765432
nhóm máu: A

**Thông tin của User2:**

họ và tên: Nguyễn Đức Anh
ngày tháng năm sinh: 11/11/2011
giới tính: Nam
tên gọi khác: Anh Nguyễn
Khoa: Công nghệ Thông tin
quốc tịch: Việt Nam
Quyết định cử đi học: Số 123/QĐ-ĐHKHTN
Thuộc đối tượng: Sinh viên chính quy
nhóm máu: O
Email: nguyenvantoi@gmail.com
ngày sinh bằng chữ: Mười một tháng Mười một năm 2011
Tài liệu kèm theo: Bản sao CMND, giấy khai sinh
Nơi đăng ký khám bệnh: Bệnh viện Đại học Y Dược
tình trạng hôn nhân: Độc thân
Ngân hàng: Vietcombank
dân tộc: Kinh
Đề tài luận văn: Ứng dụng LLM trong Doc Filling
Số điện thoại di động: 0987654321
nơi cấp CCCD: Công an TP.HCM 11
Số điện thoại: 0123456789
số hộ chiếu: C12345678
tôn giáo: Không
```
Output:
```
CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

BIỂU MẪU THÔNG TIN CÁ NHÂN

1. Họ và tên: [Trần Minh Khoa]
Ngày tháng năm sinh: [05/06/1995]
Năm học: [2024-2025]
Trình độ học vấn: [Cao học]
Số tài khoản: [0123123123]
Bệnh nghề nghiệp: [Không có]
Thuộc đối tượng: [Sinh viên chính quy]
Địa chỉ hiện tại: [56 Võ Văn Kiệt, Đà Nẵng]
Quốc tịch: [Việt Nam]
Ngân hàng: [Vietcombank]
Tài liệu kèm theo: [Bản sao CMND, giấy khai sinh]
Số điện thoại di động: [0987654321]
Tôn giáo: [Không]
Nghề nghiệp: [Bác sĩ]
Nơi cấp hộ chiếu: [Cục Quản lý Xuất nhập cảnh TP.HCM]
Nơi đăng ký khám bệnh: [Bệnh viện Đại học Y Dược]
Số điện thoại: [0123456789]
Số định danh: [22222222]
Ngày sinh bằng chữ: [Năm tháng Sáu năm 1995]
Số hộ chiếu: [B98765432]
Nhóm máu: [A]

2. Họ và tên: [Nguyễn Đức Anh]
Ngày tháng năm sinh: [11/11/2011]
Giới tính: [Nam]
Tên gọi khác: [Anh Nguyễn]
Khoa: [Công nghệ Thông tin]
Quốc tịch: [Việt Nam]
Quyết định cử đi học: [Số 123/QĐ-ĐHKHTN]
Thuộc đối tượng: [Sinh viên chính quy]
Nhóm máu: [O]
Email: [nguyenvantoi@gmail.com]
Ngày sinh bằng chữ: [Mười một tháng Mười một năm 2011]
Tài liệu kèm theo: [Bản sao CMND, giấy khai sinh]
Nơi đăng ký khám bệnh: [Bệnh viện Đại học Y Dược]
Tình trạng hôn nhân: [Độc thân]
Ngân hàng: [Vietcombank]
Dân tộc: [Kinh]
Đề tài luận văn: [Ứng dụng LLM trong Doc Filling]
Số điện thoại di động: [0987654321]
Nơi cấp CCCD: [Công an TP.HCM]
Số điện thoại: [0123456789]
Số hộ chiếu: [C12345678]
Tôn giáo: [Không]

Người khai thông tin 1 (Ký, ghi rõ họ tên): [Trần Minh Khoa]

Người khai thông tin 2 (Ký, ghi rõ họ tên): [Nguyễn Đức Anh]
```

Input:
```
{input_form}
```
Output:

"""

def random_merge(*datasets):
    """
    Hàm chọn ngẫu nhiên một số tập dữ liệu từ danh sách đầu vào và hợp nhất chúng.
    
    :param datasets: Các dictionary dữ liệu có thể truyền vào
    :return: Một dictionary hợp nhất từ các dictionary được chọn ngẫu nhiên
    """
    if not datasets:
        return {}

    selected_datasets = random.sample(datasets, k=random.randint(len(datasets), len(datasets)))
    merged_data = defaultdict(list)

    for i, dataset in enumerate(selected_datasets):
        for key, value in dataset.items():
            # if key == "họ và tên":
            #     names = ['Nguyễn Đức Anh', 'Trần Minh Khoa', 'Lê Thanh Hằng', 'Phạm Hoàng Nam']
            #     for name in names:
            #         merged_data[key].append(name)
            # else:
            merged_data[key].append(value)

    return dict(merged_data)

def extract_random_data(data, noise_data):
    keys = list(data.keys())
    num_user = len(data[keys[0]])
    res = ""
    for i in range(num_user):
        selected_data = {keys[0]: data[keys[0]][i]}  # Always keep the first key (full_name)
        selected_data[keys[1]] = data[keys[1]][i]  # Always keep the second key (dob)
        
        remaining_keys = keys[2:]
        sample_size = int(random.uniform(0.4, 0.7) * len(remaining_keys))
        selected_keys = random.sample(remaining_keys, sample_size)
        
        for key in selected_keys:
            if key in noise_data.keys():
                selected_data[key] = data[key]
            else:
                selected_data[key] = data[key][i]
        
        text = f'**Thông tin của User{i+1}:**\n\n' + '\n'.join(f"{key}: {value}" for key, value in selected_data.items())
        res += text + '\n\n'
    return res

def generate_form(prompt, form_data):  
    prompt_gen_forms = PromptTemplate.from_template(prompt)
    chain = prompt_gen_forms | gemini | StrOutputParser()
    response = chain.invoke({"input_form": form_data})

    return response

def check_generated_form(form: str, data: dict) -> tuple[bool, str]:
    """
    Checks if every value enclosed in [] in the form is one of the values from the data dictionary.
    The placeholder value "Trống" is considered valid.

    Additionally, generates a modified version of the form where:
    - bracketed values are replaced with ..........

    Parameters:
        form (str): The generated form as a string.
        data (dict of array): The dictionary containing personal data.

    Returns:
        tuple[bool, str]: 
            - True if all bracketed values are valid, otherwise False.
            - The modified form with replacements.
    """
    # Create a set of allowed values from data (strip spaces) and include "Trống" as a valid placeholder.
    num_users = len(data['họ và tên'])
    allowed_values = ["Trống"]
    for key, value in data.items():
        for i in range(num_users):
            if isinstance(value, list) and i < len(value):
                allowed_values.append(value[i].strip())
            else:
                allowed_values.append(value)
    list_name = ['Nguyễn Đức Anh', 'Trần Minh Khoa', 'Lê Thanh Hằng', 'Phạm Hoàng Nam']
    list_dob = ['11/11/2011', '05/06/1995', '21/09/1988', '14/02/2000']
    allowed_values.extend(list_name)
    allowed_values.extend(list_dob)
    allowed_values = list(set(allowed_values))
    # print("Alloweed values: ",allowed_values)
    # print()
    # Initialize valid flag
    is_valid = True
    # Replace values in form
    def replace_value(match):
        value = match.group(1).strip()
        nonlocal is_valid  # Allow modification of the outer variable
        if value not in allowed_values:
            # print(value)
            is_valid = False  # Mark as invalid
        return ".........."

    # Generate modified form
    modified_form = re.sub(r'\[([^\]]+)\]', replace_value, form)

    return is_valid, modified_form

def map_values_to_tagnames(form: str, data: dict, data_tagname: dict) -> str:
    """
    Replaces values in the form with their corresponding tagnames from data_tagname.
    If a value is "Trống", it is replaced with "[Empty]".

    Parameters:
        form (str): The generated form as a string.
        data (dict): The dictionary containing actual values.
        data_tagname (dict): The dictionary mapping field names to tagnames.

    Returns:
        str: The transformed form with tagnames.
    """
    pattern = r'\[([^\]]+)\]'
    names = {'Nguyễn Đức Anh', 'Trần Minh Khoa', 'Lê Thanh Hằng', 'Phạm Hoàng Nam'}
    dict = {}
    for name in names:
        dict[name] = 0
    count = 0  # Biến đếm để tăng giá trị i mỗi lần gặp names
    def replace_match(match):
        nonlocal count
        value = match.group(1)
        if value in names:
            if dict[value] == 0:
                count += 1
                dict[value] = count
            else:
                count = dict[value]
        if value == "Trống":
            return "[#another]"
        for key, val in data.items():
            if isinstance(val, list):
                for v in val:
                    if v.strip() == value:
                        return f"[{data_tagname[key].replace('0', str(count))}]"
            elif val == value and key in data_tagname:
                return f"[{data_tagname[key].replace('0', str(count))}]"
        
        return match.group(0)  # Giữ nguyên nếu không tìm thấy
    
    return re.sub(pattern, replace_match, form)

def merge_all(*datasets):
    """
    Hợp nhất tất cả các tập dữ liệu được truyền vào.
    
    :param datasets: Các dictionary dữ liệu có thể truyền vào
    :return: Một dictionary hợp nhất từ tất cả các dictionary
    """
    if not datasets:
        return {}

    merged_data = defaultdict(list)

    for dataset in datasets:
        for key, value in dataset.items():
            if isinstance(value, list):
                merged_data[key].extend(value)
            else:
                merged_data[key].append(value)

    return dict(merged_data)

def process_response_LLM_II(response, names):
    """
    Xử lý kết quả sinh ra từ mô hình LLM.

    Parameters:
        response (str): Kết quả sinh ra từ mô hình LLM.

    # Task
    - Chuyển 4 tên users trên thành [Giá trị] nếu chưa có

    Returns:
        str: Kết quả đã được xử lý.
    """
    # Xử lý kết quả sinh ra từ mô hình LLM
    for name in names:
        pattern = rf"(?<!\[)({name})(?!\])"
        response = re.sub(pattern, r"[\1]", response)
    return response
    
names = ['Nguyễn Đức Anh', 'Trần Minh Khoa', 'Lê Thanh Hằng', 'Phạm Hoàng Nam']

Num_forms = 500
for i in range(Num_forms):
    if i%1==0:
        print(f"Process until {i}") 
    file_name = f"input_{i}.txt"
    file_save_path_label = f"{label_folder}/{file_name}"
    file_save_path_info = f"{info_folder}/{file_name}"
    user_data = random_merge(data, data2, data3, data4)
    # print(user)
    merged_data = {**user_data, **noise_data}
    data_form = extract_random_data(merged_data, noise_data)
    # print(data_form)
    # Check if not file_save_path exist file already
    if not os.path.exists(file_save_path_info):    
        print("ERRORRRRROROROROR")
        response = generate_form(prompt, data_form)
        # Process response
        response = process_response_LLM_II(response, names)
        is_valid, input_form = check_generated_form(response, merged_data)
    else:
        with open(file_save_path_info, "r", encoding="utf-8") as f:
            response = f.read()
        # Process response
        response = process_response_LLM_II(response, names)
        # print(response)
        is_valid, input_form = check_generated_form(response, merged_data)
        is_valid = True
    while True:
        if is_valid:
            # Save to info folder
            with open(file_save_path_info, "w", encoding="utf-8") as f:
                f.write(response)
            # Take label tagname form
            # label_tagname_form = map_values_to_tagnames(response, data, data_tagname)
            label_tagname_form = map_values_to_tagnames(response, merged_data, merged_data_tagname)
            # Save to label folder
            with open(file_save_path_label, "w", encoding="utf-8") as f:
                f.write(label_tagname_form)
            # Save to input
            with open(f"{input_folder}/{file_name}", "w", encoding="utf-8") as f:
                f.write(input_form)
            break
        else:
            print(f"Error at form {i}")
            # Save to f"{file_save_path_info}/Error/{file_name}" for debugging
            # Ensure folder exist
            os.makedirs(f"{info_folder}/Error", exist_ok=True)
            with open(f"{info_folder}/Error/{file_name}", "w", encoding="utf-8") as f:
                f.write(response)
                f.write("/n ===== Form supplied into ===== /n")
                f.write(data_form)
            # Generate again
            # data_form = extract_random_data(data)
            data_form = extract_random_data(merged_data, noise_data)
            response = generate_form(prompt, data_form)
            # is_valid, input_form = check_generated_form(response, data)
            is_valid, input_form = check_generated_form(response, merged_data)