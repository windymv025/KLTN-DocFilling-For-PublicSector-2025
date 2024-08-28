define_tagnames_prompt = """
Instruction: Creating and Defining a New Tag Name
Objective:
Guide the LLM to create and define new tag names for specific types of information in a form, without using [another] to represent missing information.

Steps:
Identify the Specific Information:

Review the form and determine the exact type of data that needs a tag name. Focus on data that is clearly defined by the form’s context.
Generate a Descriptive Tag Name:

Create a new tag name that accurately reflects the required information. Use square brackets to enclose the tag name.
Examples:
For a field related to a specific date, create [start_date].
For a financial field, use [budget].
Define the New Tag Name:

Provide a clear and concise definition of the new tag name, describing the type of information it represents.
Example Definitions:
[start_date]: The exact date when the study abroad program begins.
[budget]: The total amount of money allocated for the extension period.

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
Tổng thời gian đào tạo theo Quyết định cử đi học/Văn bản tiếp nhận đào tạo: [another]
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
[training_duration]: Total duration of study according to the Decision or Acceptance Document.
[start_date]: The date when the study program begins.
[extension_start_month]: The month when the extension period starts.
[extension_start_year]: The year when the extension period starts.
[extension_end_month]: The month when the extension period ends.
[extension_end_year]: The year when the extension period ends.
[budget]: The financial amount allocated for the extension period.

Form:
ĐƠN ĐỀ NGHỊ CẤP GIẤY PHÉP LÁI XE QUỐC TẾ
APPLICATION FORM FOR ISSUANCE OF INTERNATIONAL DRIVING PERMIT
Kính gửi (To): [receiver]
Tôi là (Full name): [user1_full_name]
Ngày tháng năm sinh (date of birth) [user1_dob_day]/[user1_dob_month]/[user1_dob_year]
Số hộ chiếu (Passport No.) [user1_id] cấp ngày (Issuing date): ngày [another] tháng [another] năm [another] nơi cấp (Place of issue): [another] hoặc Số định danh cá nhân (personal indentification No.): [user1_id_number]
Hiện có giấy phép lái xe cơ giới đường bộ số (Current driving licence No.): [user1_driving_license_number]
Cơ quan cấp (Issuing Office): [another]
Tại (Place of issue): [another]
Cấp ngày (Issuing date): ngày [another] tháng [another] năm [another]
Lý do xin cấp giấy phép lái xe (Reason of application for International driving permit:
[reason]

        [place], ngày [day] tháng [month] năm [year]
NGƯỜI LÀM ĐƠN (APPLICANT)
(Ký và ghi rõ họ tên)
(Signature and Full name)
Answer:
[passport_issue_day]: The day when the passport was issued.
[passport_issue_month]: The month when the passport was issued.
[passport_issue_year]: The year when the passport was issued.
[passport_issue_place]: The place where the passport was issued.
[driving_license_issuing_office]: The office that issued the current driving license.
[driving_license_issue_place]: The place where the current driving license was issued.
[driving_license_issue_day]: The day when the driving license was issued.
[driving_license_issue_month]: The month when the driving license was issued.
[driving_license_issue_year]: The year when the driving license was issued.

Form:
{form}
Answer:
"""