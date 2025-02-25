# ===== Ask LLM generates form =====
import json
import random
# Get random forms
from Config.tagnames import remaining_tag_names
from Config.LLM import gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Tagnames.get_tagnames import get_tagnames, get_all_tagnames
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

data_noise = {
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

merged_data = {**data, **data_noise}

data_tagname = {
    "họ và tên": "user1_full_name",
    "tên gọi khác": "user1_alias_name",
    "ngày sinh bằng chữ": "user1_dob_text",
    "ngày tháng năm sinh": "user1_dob",
    "năm sinh": "user1_dob_year",
    "giới tính": "user1_gender",
    "số định danh": "user1_id_number",
    "ngày cấp CCCD": "user1_id_issue_date",
    "nơi cấp CCCD": "user1_id_issue_place",
    "nghề nghiệp": "user1_occupation",
    "trình độ học vấn": "user1_education_level",
    "dân tộc": "user1_ethnicity",
    "tôn giáo": "user1_religion",
    "quốc tịch": "user1_nationality",
    "tình trạng hôn nhân": "user1_marital_status",
    "nhóm máu": "user1_blood_type",
    "nơi sinh": "user1_birthplace",
    "nơi đăng ký khai sinh": "user1_birth_registration_place",
    "quê quán": "user1_hometown",
    "địa chỉ thường trú": "user1_permanent_address",
    "địa chỉ hiện tại": "user1_current_address",
    "tình trạng hiện tại": "user1_current_status",
    "số hộ chiếu": "user1_passport_number",
    "ngày cấp hộ chiếu": "user1_passport_issue_date",
    "nơi cấp hộ chiếu": "user1_passport_issue_place",
    "ngày hết hạn hộ chiếu": "user1_passport_expiry_date"
}

data_tagname_noise = {
    "Email": "user1_email",
    "Số điện thoại": "user1_phone",
    "Số điện thoại di động": "user1_phone",
    "Trường học": "user1_school",
    "Ngành học": "user1_major",
    "Chuyên ngành": "user1_major",
    "Mã số học sinh/ sinh viên": "user1_MSSV",
    "Lớp học": "user1_class",
    "Khóa học": "user1_grade",
    "Niên khóa": "user1_grade",
    "Khoa": "user1_faculty",
    "Năm học": "user1_school_year",
    "Học kì": "user1_semester",
    "Hệ đào tạo": "user1_training_system",
    "Quyết định cử đi học": "user1_decision_study",
    "Số tài khoản": "user1_bank_account",
    "Ngân hàng": "user1_bank_name",
    "Số": "user1_number",
    "Bệnh nghề nghiệp": "user1_occupational_disease",
    "Nơi đăng ký khám bệnh": "user1_medical_registration_place",
    "Tài liệu kèm theo": "user1_attached_documents",
    "Thuộc đối tượng": "user1_eligible_subject",
    "Đề tài luận văn": "user1_thesis_topic",
    "Thời gian thất nghiệp": "user1_unemployment_duration"
}

merged_data_tagname = {**data_tagname, **data_tagname_noise}

# Gen form 11
prompt = """
Bạn là một AI có nhiệm vụ tạo ra các biểu mẫu hành chính từ thông tin cá nhân được cung cấp. 
Bạn sẽ nhận đầu vào là thông tin của một cá nhân và sinh ra một biểu mẫu phù hợp với ngữ cảnh sử dụng.
Dữ liệu đầu vào có dạng một danh sách cặp khóa-giá trị (key-value), trong đó:
- Key là tên thông tin (ví dụ: "họ và tên", "năm sinh", "giới tính", v.v.).
- Value là giá trị tương ứng (ví dụ: "Nguyễn Đức Anh", "2011", "Nam", v.v.).

**Quy tắc tạo form:**
1. Chỉ sử dụng dữ liệu được cung cấp. 
Nếu một thông tin không có trong dữ liệu đầu vào, điền [Trống] thay vì bỏ trống hoặc sử dụng placeholder chung.
Định dạng dữ liệu:
Dữ liệu điền vào phải giữ nguyên định dạng [Giá trị], ví dụ [Nguyễn Đức Anh], [2011], [Nam], v.v.
2. Chọn một loại form phù hợp với các trường dữ liệu có sẵn. Ví dụ:
- Đơn đăng ký tạm trú
- Đơn xin cấp hộ chiếu
- Tờ khai căn cước công dân
- Đơn xin việc
- Đơn đăng ký kết hôn
- Giấy khai sinh
- ...
3. Bảo đảm form đúng chuẩn hành chính với đầy đủ tiêu đề, định dạng, bố cục.
4. Giữ nguyên thông tin mà không sửa đổi hoặc diễn giải lại.
5. Đảm bảo văn phong hành chính rõ ràng, trang trọng.
6. Một số quy tắc tạo dữ liệu:
- Nếu chỉ có "Ngày sinh" hay "Sinh ngày",... thì điền giá trị ngày tháng năm đầy đủ (dd/mm/yyyy). (VD Ngày sinh: [11/11/2011]),
tránh nhầm lẫn với các thông tin khác như "Ngày sinh bằng chữ", "Năm sinh", "Tên gọi", "Tên gọi khác",..
- Nếu "Ngày sinh bằng chữ", thì giữ nguyên giá trị chữ. (VD Ngày sinh bằng chữ: [Mười một tháng Mười một năm 2011])
- Nếu chỉ có "Năm sinh", thì điền chỉ năm (yyyy). (VD Năm sinh: [2011])
- Ví dụ tên gọi khác, dùng mục Tên gọi khác : [Anh Nguyễn]
- Với các mục A/B, ví dụ  Số CCCD/Hộ chiếu, thì mặc định điền theo nội dung là CCCD, tức id_number, hay số định danh.
Ví dụ: 
Có giá trị:
"số định danh": "11111111", và "số hộ chiếu": "C12345678", thì mục
Số CCCD/Hộ chiếu: .......... ta cần điền: Số CCCD/Hộ chiếu: [11111111]

- Ngày sinh: Nếu có "Ngày sinh" hoặc "Sinh ngày" → dùng định dạng đầy đủ dd/mm/yyyy (VD: Ngày sinh : [11/11/2011] hay sinh ngày : [11/11/2011]).
- Ngày sinh bằng chữ: Nếu có "Ngày sinh bằng chữ", điền ngày sinh bằng chữ (VD: Ngày sinh bằng chữ: [Mười một tháng Mười một năm 2011]).
Năm sinh: Nếu chỉ có "Năm sinh", điền năm sinh: [2011].
Tên gọi khác: Nếu có "Tên gọi khác", ghi vào "Tên gọi khác:" [Anh Nguyễn].
Số CCCD/Hộ chiếu: Mặc định điền giá trị "Số CCCD", tức số định danh. 
VD: 
Số CCCD/Hộ chiếu: [11111111]
Ngày cấp: [11/11/2021]
Nơi cấp: [Công an TP.HCM 11]

- Tất cả các thông tin cung cấp đều mang nghĩa giá trị hiện tại, nếu mục để nội dung liên quan quá khứ,
như số căn cước cũ, số hộ chiếu cũ, thì sẽ không điền giá trị vào các mục này.
Tức chỉ điền nếu là mục số căn cước, hộ chiếu, không điền với mục là số hộ chiếu cũ, số căn cước cũ.
- Với giá trị liên quan tình trạng hiện tại (tiêu biểu như đang làm việc, học tập tại đâu), chỉ điền giá trị đó
nếu mục là tình trạng hiện tại, trạng thái hiện tại.
Ví dụ: 
- Tình trạng hiện tại: [Đang làm việc tại công ty FPT]
- Trạng thái hiện tại: [Học tại trường HCMUS] 
Còn các mục như lý do tạm trú, nơi làm việc, thì không điền vào mục tình trạng hiện tại, cũng như trạng thái hiện tại, và tương tự.
- Kinh nghiệm làm việc được hiểu là giá trị [Trống] (Không phải tình trạng hiện tại, cũng không phải nghề nghiệp)
Ví dụ:
Input:
```
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
họ và tên: Nguyễn Đức Anh
ngày tháng năm sinh: 11/11/2011
dân tộc: Kinh
tên gọi khác: Anh Nguyễn
ngày hết hạn hộ chiếu: 20/07/2030
tình trạng hiện tại: Đang làm việc tại công ty FPT
nơi cấp hộ chiếu: Cục Quản lý Xuất nhập cảnh Hà Nội
quốc tịch: Việt Nam
nơi cấp CCCD: Công an TP.HCM 11
tôn giáo: Không
nhóm máu: O
trình độ học vấn: Đại học
nơi sinh: Bệnh viện Từ Dũ, TP.HCM
địa chỉ thường trú: 5 Lê Lợi, Hà Nội/nEmail: nguyenvantoi@gmail.com
Số điện thoại: 0123456789
Khoa: Công nghệ Thông tin
Số tài khoản: 0123123123
Tài liệu kèm theo: Bản sao CMND, giấy khai sinh
Đề tài luận văn: Ứng dụng LLM trong Doc Filling
Quyết định cử đi học: Số 123/QĐ-ĐHKHTN
Năm học: 2024-2025
Ngành học: Trí tuệ nhân tạo
Bệnh nghề nghiệp: Không có
```

Output:
```
GIẤY XÁC NHẬN CÔNG TÁC

Kính gửi: Cơ quan [Trống]

Tôi, người ký tên dưới đây, xin xác nhận thông tin công tác của cá nhân như sau:

Họ và tên: [Nguyễn Đức Anh]

Ngày tháng năm sinh: [11/11/2011]

Dân tộc: [Kinh]

Quốc tịch: [Việt Nam]

Tôn giáo: [Không]

Nhóm máu: [O]

Trình độ học vấn: [Đại học]

Nghề nghiệp: [Đang làm việc tại công ty FPT]

Địa chỉ thường trú: [5 Lê Lợi, Hà Nội]

Số điện thoại: [0123456789]

Email: [nguyenvantoi@gmail.com]

THÔNG TIN GIẤY TỜ TÙY THÂN

Số CCCD/Hộ chiếu: [Trống]

Ngày hết hạn hộ chiếu: [20/07/2030]

Nơi cấp hộ chiếu: [Cục Quản lý Xuất nhập cảnh Hà Nội]

Nơi cấp CCCD: [Công an TP.HCM 11]

THÔNG TIN HỌC TẬP

Khoa: [Công nghệ Thông tin]

Ngành học: [Trí tuệ nhân tạo]

Năm học: [2024-2025]

Đề tài luận văn: [Ứng dụng LLM trong Doc Filling]

Quyết định cử đi học: [Số 123/QĐ-ĐHKHTN]

THÔNG TIN KHÁC

Số tài khoản ngân hàng: [0123123123]

Tài liệu kèm theo: [Bản sao CMND, giấy khai sinh]

Bệnh nghề nghiệp: [Không có]

Tôi xin cam kết rằng những thông tin trên là chính xác và chịu trách nhiệm hoàn toàn trước pháp luật về nội dung khai báo.

Ngày [Trống] tháng [Trống] năm [Trống]

Người xác nhận(Ký và ghi rõ họ tên)

[Nguyễn Đức Anh]
```

Input:
```
{input_form}
```
Output:

"""

prompt_backup = """
Bạn là một AI có nhiệm vụ tạo ra các biểu mẫu hành chính từ thông tin cá nhân được cung cấp. 
Bạn sẽ nhận đầu vào là thông tin của một cá nhân và sinh ra một biểu mẫu phù hợp với ngữ cảnh sử dụng.
Dữ liệu đầu vào có dạng một danh sách cặp khóa-giá trị (key-value), trong đó:
- Key là tên thông tin (ví dụ: "họ và tên", "năm sinh", "giới tính", v.v.).
- Value là giá trị tương ứng (ví dụ: "Nguyễn Đức Anh", "2011", "Nam", v.v.).

**Quy tắc tạo form:**
1. Chỉ sử dụng dữ liệu được cung cấp. 
Nếu một thông tin không có trong dữ liệu đầu vào, điền [Trống] thay vì bỏ trống hoặc sử dụng placeholder chung.
Định dạng dữ liệu:
Dữ liệu điền vào phải giữ nguyên định dạng [Giá trị], ví dụ [Nguyễn Đức Anh], [2011], [Nam], v.v.
2. Chọn một loại form phù hợp với các trường dữ liệu có sẵn. Ví dụ:
- Đơn đăng ký tạm trú
- Đơn xin cấp hộ chiếu
- Tờ khai căn cước công dân
- Đơn xin việc
- Đơn đăng ký kết hôn
- Giấy khai sinh
- ...
3. Bảo đảm form đúng chuẩn hành chính với đầy đủ tiêu đề, định dạng, bố cục.
4. Giữ nguyên thông tin mà không sửa đổi hoặc diễn giải lại.
5. Đảm bảo văn phong hành chính rõ ràng, trang trọng.
6. Một số quy tắc tạo dữ liệu:
- Nếu chỉ có "Ngày sinh" hay "Sinh ngày",... thì điền giá trị ngày tháng năm đầy đủ (dd/mm/yyyy). (VD Ngày sinh: [11/11/2011]),
tránh nhầm lẫn với các thông tin khác như "Ngày sinh bằng chữ", "Năm sinh", "Tên gọi", "Tên gọi khác",..
- Nếu "Ngày sinh bằng chữ", thì giữ nguyên giá trị chữ. (VD Ngày sinh bằng chữ: [Mười một tháng Mười một năm 2011])
- Nếu chỉ có "Năm sinh", thì điền chỉ năm (yyyy). (VD Năm sinh: [2011])
- Ví dụ tên gọi khác, dùng mục Tên gọi khác : [Anh Nguyễn]
- Với các mục A/B, ví dụ  Số CCCD/Hộ chiếu, thì mặc định điền theo nội dung là CCCD, tức id_number, hay số định danh.
Ví dụ: 
Có giá trị:
"số định danh": "11111111", và "số hộ chiếu": "C12345678", thì mục
Số CCCD/Hộ chiếu: .......... ta cần điền: Số CCCD/Hộ chiếu: [11111111]

- Ngày sinh: Nếu có "Ngày sinh" hoặc "Sinh ngày" → dùng định dạng đầy đủ dd/mm/yyyy (VD: Ngày sinh : [11/11/2011] hay sinh ngày : [11/11/2011]).
- Ngày sinh bằng chữ: Nếu có "Ngày sinh bằng chữ", điền ngày sinh bằng chữ (VD: Ngày sinh bằng chữ: [Mười một tháng Mười một năm 2011]).
Năm sinh: Nếu chỉ có "Năm sinh", điền năm sinh: [2011].
Tên gọi khác: Nếu có "Tên gọi khác", ghi vào "Tên gọi khác:" [Anh Nguyễn].
Số CCCD/Hộ chiếu: Mặc định điền giá trị "Số CCCD", tức số định danh. 
VD: 
Số CCCD/Hộ chiếu: [11111111]
Ngày cấp: [11/11/2021]
Nơi cấp: [Công an TP.HCM 11]

- Tất cả các thông tin cung cấp đều mang nghĩa giá trị hiện tại, nếu mục để nội dung liên quan quá khứ,
như số căn cước cũ, số hộ chiếu cũ, thì sẽ không điền giá trị vào các mục này.
Tức chỉ điền nếu là mục số căn cước, hộ chiếu, không điền với mục là số hộ chiếu cũ, số căn cước cũ.
- Với giá trị liên quan tình trạng hiện tại (tiêu biểu như đang làm việc, học tập tại đâu), chỉ điền giá trị đó
nếu mục là tình trạng hiện tại, trạng thái hiện tại.
Ví dụ: 
- Tình trạng hiện tại: [Đang làm việc tại công ty FPT]
- Trạng thái hiện tại: [Học tại trường HCMUS] 
Còn các mục như lý do tạm trú, nơi làm việc, thì không điền vào mục tình trạng hiện tại, cũng như trạng thái hiện tại, và tương tự.

Ví dụ:
Input:
```
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
{input_form}
```
Output:

"""

def extract_random_data(data):
    keys = list(data.keys())
    selected_data = {keys[0]: data[keys[0]]}  # Always keep the first key (full_name)
    selected_data[keys[1]] = data[keys[1]]  # Always keep the second key (dob)
    
    remaining_keys = keys[2:]
    sample_size = int(random.uniform(0.4, 0.7) * len(remaining_keys))
    selected_keys = random.sample(remaining_keys, sample_size)
    
    for key in selected_keys:
        selected_data[key] = data[key]
    
    return '\n'.join(f"{key}: {value}" for key, value in selected_data.items())

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
    - "Trống" is replaced with [Empty].
    - Other bracketed values are replaced with ..........

    Parameters:
        form (str): The generated form as a string.
        data (dict): The dictionary containing personal data.

    Returns:
        tuple[bool, str]: 
            - True if all bracketed values are valid, otherwise False.
            - The modified form with replacements.
    """
    # Create a set of allowed values from data (strip spaces) and include "Trống" as a valid placeholder.
    allowed_values = {v.strip() for v in data.values()}
    allowed_values.add("Trống")
    
    # Find all occurrences of text within square brackets.
    # bracket_values = re.findall(r'\[([^\]]+)\]', form)
    
    # Initialize valid flag
    is_valid = True
    
    # Replace values in form
    def replace_value(match):
        value = match.group(1).strip()
        nonlocal is_valid  # Allow modification of the outer variable
        if value not in allowed_values:
            is_valid = False  # Mark as invalid
        # return "[Empty]" if value == "Trống" else ".........."
        return ".........." if value == "Trống" else ".........."

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
    def replace_match(match):
        value = match.group(1).strip()
        if value == "Trống":
            return "[#another]"
        for key, val in data.items():
            if val == value and key in data_tagname:
                # Process here
                # tagname = f"[{data_tagname[key]}]"

                return f"[{data_tagname[key]}]"
        return match.group(0)  # Return unchanged if no match is found

    return re.sub(r'\[([^\]]+)\]', replace_match, form)

Num_forms = 50
for i in range(Num_forms):
    if i%1==0:
        print(f"Process until {i}") 
    file_name = f"input_{i}.txt"
    file_save_path_label = f"{label_folder}/{file_name}"
    file_save_path_info = f"{info_folder}/{file_name}"
    # Check if not file_save_path exist file already
    if not os.path.exists(file_save_path_info):    
        # data_form = extract_random_data(data)
        data_form = extract_random_data(merged_data)
        
        response = generate_form(prompt, data_form)
        # is_valid, input_form = check_generated_form(response, data)
        is_valid, input_form = check_generated_form(response, merged_data)
    else:
        with open(file_save_path_info, "r", encoding="utf-8") as f:
            response = f.read()
        is_valid, input_form = check_generated_form(response, merged_data)
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
            data_form = extract_random_data(merged_data)
            response = generate_form(prompt, data_form)
            # is_valid, input_form = check_generated_form(response, data)
            is_valid, input_form = check_generated_form(response, merged_data)
