import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Prompts.create_forms import create_forms_template_prompt
from Config.tagnames import residence_identification_tagnames
from Config.LLM import gemini


def create_forms(
    llm, create_forms_template_prompt, residence_identification_tagnames, form_features
):
    prompt = PromptTemplate.from_template(create_forms_template_prompt)
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(
        {"tag_names": residence_identification_tagnames, "form_features": form_features}
    )
    return response


form_features = """
**Mẫu đơn thường gặp:**  
- Tờ khai căn cước công dân, hộ chiếu, chứng minh nhân dân.  
- Đơn đề nghị khôi phục, điều chỉnh thông tin liên quan đến cư trú hoặc giấy tờ tùy thân.

**Từ khóa đặc trưng:**
- "TỜ KHAI CĂN CƯỚC CÔNG DÂN"
- "TỜ KHAI"
- "GIẤY XÁC NHẬN"
- "ĐƠN ĐỀ NGHỊ"
- "CMND", "CCCD", "Chứng minh nhân dân", "Căn cước công dân"
- "Hộ chiếu", "passport", "số hộ chiếu"
- "Nơi cấp", "Ngày cấp", "Tháng cấp", "Năm cấp"
- "Quốc tịch", "Quê quán", "Địa chỉ thường trú", "Địa chỉ hiện tại"
- "Nghề nghiệp", "Nơi đăng ký khai sinh"
- "Phường", "Xã", "Quận", "Huyện", "Tỉnh"
- "Số thị thực (visa)", "Ngày hết hạn thị thực"
- "Lý do thay đổi", "Điều chỉnh thông tin cư trú", "Khôi phục hộ chiếu"

**Thông tin bổ sung đặc trưng:**
- Thông tin cá nhân như: tên, họ, chữ đệm, ngày/tháng/năm sinh.
- Số chứng minh nhân dân hoặc căn cước công dân.
- Các thông tin liên quan đến địa chỉ và nơi cư trú của người dùng.
"""

form = create_forms(
    gemini,
    create_forms_template_prompt,
    residence_identification_tagnames,
    form_features,
)
print(form)
