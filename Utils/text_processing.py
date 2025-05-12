import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Utils.multi_value_dict import MultiValueDict
from Config.tagnames import (
    list_cccd_passport_tagnames, 
    list_general_tagnames,
    group_name_tagname,
    group_birthplace_tagname,
    group_birth_registration_tagname,
    group_id_tagname,
    group_passport_tagname,
    group_current_address_tagname,
    group_hometown_tagname,
    group_permanent_address_tagname,
    group_dob_tagname,
    group_tagname_have_ward_district_province,
    group_phone_tagname,
    group_social_insurance_tagname,
    list_village,list_ward,list_district,list_province,
    list_not_village, list_not_ward, list_not_district, list_not_province,
    group_education_tagname,
    list_contextual_id_number,
    list_contextual_passport,
    list_contextual_health_number,
    list_contextual_social_number,
    list_context_current_address,
    list_current_address,
    list_hometown,
    list_permanent_address,
    list_occupation,
    list_education,
    group_day_month_year
)


class Text_Processing:
    def __init__(self):
        pass
    ## Read TXT file
    def Read_txt_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
            return None

    def Save_txt_file(self, file_path, text):
        # Delete all before create
        if os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Write content to the file
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
            # print(f"File written successfully to '{file_path}'.")
        except Exception as e:
            print(f"An error occurred while writing the file: {e}")

    ## Summary tagnames (return list of N tagnames to check)
    def Summary_tagnames(self):
        modified_cccd_tagnames = [
            f"user0_{tagname.strip('[]')}" for tagname in list_cccd_passport_tagnames
        ]
        modified_general_tagnames = [
            f"{tagname.strip('[]')}" for tagname in list_general_tagnames
        ]
        our_N_tagnames = modified_cccd_tagnames + modified_general_tagnames
        return our_N_tagnames

    ## Some functions to from LLM filled form --> pass tagname to input form
    # Function to process a place, date, month, year format
    def get_contextual_tagnames(self, data_form):
        """
        Hàm để lấy các nội dung trước các tagnames (ngữ cảnh), nhằm so sánh giữa LLM fillied form và input --> từ đó xác định chỗ điền phù hợp.
        Input:
        - form: form điền vào (các ... được thay bằng #another)
        Output:
        - Mảng, phần tử là nội dung trước tagnames
        - Ví dụ: ['chỗ', 'ở', 'hiện', 'nay']
        Cách làm:
        Đầu tiên, với form đưa vào, ta bắt các vị trí có [tagname] (chú ý [^\d] vì có một số chỗ [01] là sai (form y tế),
        từ đó ta lấy được [text trước tagnames : tagname.]
        Sau đó, với mỗi cặp bắt được, ta chuẩn hóa nội dung trước chỗ điền
        Chuẩn hóa.
        - Lowercase, bỏ hết ký tự đặc biệt (.,:!)... chỉ để lại chữ, số và dấu / (vì chỗ ngày/tháng/năm) có mỗi / làm cách giữa hai tagnames.
        - Chỗ /tháng hay /năm có thể dính vào nhau --> thêm khoảng cách vào để split.
        - Sau khi xong, ta strip() bỏ khoảng cách trống, sau đó split theo space (khoảng trắng).
        """
        form = data_form
        # Bắt các vị trí text trước tagname + tagname
        pattern = re.compile(r"(.*?)(\[[^\d\]].+?\])", re.DOTALL)
        matches = pattern.findall(form)
        # Collecting the sentences
        sentences = []
        labels = []
        for match in matches:
            sentence = match[0].strip()  # Get the text before ".........."
            labels.append(match[1])
            # chuẩn hóa
            sentence = sentence.lower()
            sentence = re.sub(r"[^\w\s\/\(\)]", "", sentence)
            sentence = re.sub(r"\/(thang|tháng|nam|năm)", r" / \1", sentence)
            sentence = sentence.strip().split()

            # Thêm vào sentences
            sentences.append(sentence)
        return sentences, labels

    def get_hash_name_from_context_at_index(self, context, i):
        if len(context[i])==0:
            return "Empty"
        else:
            if len(context[i])<=2:
                return f"{context[i][0]}_{context[i][-1]}_{len(context[i])}" #Đầu_Cuối_Length
            elif len(context[i])<=4:
                return f"{context[i][0]}_{context[i][1]}_{context[i][-2]}_{context[i][-1]}_{len(context[i])}" #Đầu_KeD_KeC_Cuối_Length    
            else:
                return f"{context[i][0]}_{context[i][1]}_{context[i][2]}_{context[i][-3]}_{context[i][-2]}_{context[i][-1]}_{len(context[i])}" #Đầu_KeD_KeKeD_KeKeC_KeC_Cuối_Length

    def modified_label_llm(self, label_llm, index_llm, now_fieldname, modified_fieldname):
        #Change now to modifed
        label_llm[index_llm] = re.sub(now_fieldname, modified_fieldname, label_llm[index_llm])
        # Change all tagname after this tagname have same fieldname with now_fieldname
        # Need to check if next index is not out of range
        while (index_llm < len(label_llm)-1) and now_fieldname in label_llm[index_llm+1]:
            # Do something
            label_llm[index_llm+1] = re.sub(now_fieldname, modified_fieldname, label_llm[index_llm+1])
            index_llm += 1

        return label_llm
    
    def standard_tagname(self, tagname):
        # temporary_address --> current_address
        tagname = re.sub(r"temporary_address", "current_address", tagname)
        # personal_id, personal_identification_number, personal_identification --> id_number
        tagname = re.sub(r"personal_id", "id_number", tagname)
        tagname = re.sub(r"personal_identification", "id_number", tagname)
        tagname = re.sub(r"personal_identification_number", "id_number", tagname)
        # id_number_issue, passport_number_issue -->id, passport_issue 
        tagname = re.sub(r"passport_number_issue", "passport_issue", tagname)
        tagname = re.sub(r"id_number_issue", "id_issue", tagname)
        # middle_first_name --> middle_and_first_name
        tagname = re.sub(r"middle_first_name", "middle_and_first_name", tagname)
        # phone_number --> phone
        tagname = re.sub(r"phone_number", "phone", tagname)
        # lastname --> last_name
        tagname = re.sub(r"lastname", "last_name", tagname)
        # Default userX_address = current_address
        tagname = re.sub(r"user(\d+)_address", r"user\1_current_address", tagname)
        # Replace _hamlet to _village
        tagname = re.sub(r"_hamlet", "_village", tagname)
        # Default user_village = current_village
        tagname = re.sub(r"user(\d+)_village", r"user\1_current_address_village", tagname)
        tagname = re.sub(r"user(\d+)_ward", r"user\1_current_address_ward", tagname)
        tagname = re.sub(r"user(\d+)_district", r"user\1_current_address_district", tagname)
        tagname = re.sub(r"user(\d+)_province", r"user\1_current_address_province", tagname)
        # Replace "dob_date", full_dob with "dob" exactly
        tagname = re.sub(r"full_dob", "dob", tagname)
        tagname = re.sub(r"dob_date", "dob", tagname)
        # birthdate, birth_date --> dob
        tagname = re.sub(r"birthdate", "dob", tagname)
        tagname = re.sub(r"birth_date", "dob", tagname)
        # day_of_birth, month_of_birth, year_of_birth, date_of_birth, full_date_of_birth
        tagname = re.sub(r"day_of_birth", "dob_day", tagname)
        tagname = re.sub(r"month_of_birth", "dob_month", tagname)
        tagname = re.sub(r"year_of_birth", "dob_year", tagname)
        tagname = re.sub(r"date_of_birth", "dob", tagname)
        tagname = re.sub(r"full_date_of_birth", "dob", tagname)
        # Replace "cmnd" with "id" exactly
        tagname = re.sub(r"cmnd", "id", tagname)
        # personal_identification_number, personal_papers to id_number
        tagname = re.sub(r"personal_identification_number", "id_number", tagname)
        tagname = re.sub(r"personal_papers", "id_number", tagname)
        # Replace "birth_place" with "birthplace" exactly
        tagname = re.sub(r"birth_place", "birthplace", tagname)
        # Replace "registration" with "birth_registration" exactly
        tagname = re.sub(r"birth_registration_place", "birth_registration", tagname)
        tagname = re.sub(r"birth_registration", "birth_registration_place", tagname)
        return tagname
    
    def extract_user_and_tag(self, var):
        pattern = r"\[user(\d+)_(\w+)\]"
        match = re.search(pattern, var)
        if match:
            user_id = f"user{match.group(1)}"
            tagname = match.group(2)
            return user_id, tagname
        return None, None  # Return None if no match

    def get_modifed_tagname(self, contextual, label_llm, index_llm, list_prev_tag=None):
        tagname = label_llm[index_llm]
        new_tagname = tagname
        userX, value_tagname = self.extract_user_and_tag(tagname)
        sentence_contextual = " ".join(contextual)
        if userX is None or value_tagname is None:
            # Modify receiver
            if any(kw in sentence_contextual for kw in ["Kính gửi", "kính gửi"]):
                return "[receiver]"
            # giấy tờ tùy thân
            try:
                temp_index = len(list_prev_tag)-1
                while temp_index>=0:
                    temp_userX, temp_value_tagname = self.extract_user_and_tag(list_prev_tag[temp_index])
                    if temp_userX is None or temp_value_tagname is None:
                        temp_index -= 1
                    else:
                        break
            except:
                pass
            if "giấy tờ tùy thân" in sentence_contextual:
                return f"[{temp_userX}_id_number]" # Return id_number
            # Cư trú --> dễ bỏ trống --> cho thành current
            elif re.search(r'nơi\s*(.*?)\s*cư trú', sentence_contextual, re.IGNORECASE):
                tagname = f"[{temp_userX}_current_address]"
                userX, value_tagname = self.extract_user_and_tag(tagname)
                new_tagname = tagname
            else:
                return tagname
        # Check if tagname is in list_cccd_passport_tagnames
        if "["+value_tagname+"]" not in list_cccd_passport_tagnames:
            # giấy tờ tùy thân
            if "giấy tờ tùy thân" in sentence_contextual:
                temp_index = len(list_prev_tag)-1
                while temp_index>=0:
                    temp_userX, temp_value_tagname = self.extract_user_and_tag(list_prev_tag[temp_index])
                    if temp_userX is None or temp_value_tagname is None:
                        temp_index -= 1
                    else:
                        break
                return f"[{temp_userX}_id_number]" # Return id_number
            # Modify receiver
            if any(kw in sentence_contextual for kw in ["Kính gửi", "kính gửi"]):
                return "[receiver]"
            return tagname
        # Take full sentence of contextual    
        
        # Now, check each group to modify tagname
        # Nhầm giữa _id_number khi chỉ có số
        '''
        Chỉ cần check bối cảnh phía trước, phải thuộc 1 trong 4 id, passport, social, health
        '''
        # Check fullname group
        '''
        In fullname - alias group:
        - If fullname: Nếu là trường ký tên --> another --> để người dùng ký.
        - Fullname + "Tên gọi khác"/"Tên khác" --> alias_name
        - Alias: Mà có trường "họ và tên" --> Fullname
        Nếu không, tin tưởng LLM
        '''
        # Đưa về đúng trường _number (nhầm lẫn giữa các tagname có các _number)
        if "_number" in value_tagname:
            temp_contextual_lists = [list_contextual_id_number, list_contextual_passport, list_contextual_health_number, list_contextual_social_number]
            if all(temp not in sentence_contextual for temp_list in temp_contextual_lists for temp in temp_list):
                new_tagname = "[#another]"
            elif any(temp in sentence_contextual for temp in list_contextual_id_number):
                new_tagname = f"[{userX}_id_number]"
            elif any(temp in sentence_contextual for temp in list_contextual_passport):
                new_tagname = f"[{userX}_passport_number]"
            elif any(temp in sentence_contextual for temp in list_contextual_health_number):
                new_tagname = f"[{userX}_health_insurance_number]"
            elif any(temp in sentence_contextual for temp in list_contextual_social_number):
                new_tagname = f"[{userX}_social_insurance_number]"
        elif value_tagname in group_name_tagname:
            if "last_name" in value_tagname:
                if "họ" not in sentence_contextual:
                    new_tagname = re.sub("last_name","full_name",tagname)
                elif "họ" in sentence_contextual and "tên" in sentence_contextual:
                    new_tagname = re.sub("last_name","full_name",tagname)
            elif "middle_and_first_name" in value_tagname:
                if "đệm" not in sentence_contextual:
                    new_tagname = re.sub("middle_and_first_name","full_name",tagname)
            elif "full_name" in value_tagname:
                if "ký" in sentence_contextual or "(ký" in sentence_contextual:
                    new_tagname = "[#another]"
                elif "tên gọi khác" in sentence_contextual or "tên khác" in sentence_contextual:
                    new_tagname = re.sub("full_name","alias_name",tagname)
            elif "alias_name" in value_tagname and "họ và tên" in sentence_contextual:
                new_tagname = re.sub("alias_name","full_name",tagname)
            
            # label_llm[index_llm] = new_tagname
            # return new_tagname
        # Check Birthplace - birth_registration group
        elif value_tagname in group_birthplace_tagname or value_tagname in group_birth_registration_tagname:        
            '''
            Check sự nhẫm lẫn giữa nơi sinh và nơi đăng ký (birthplace và birth_registration)
            tùy vào phía trước
            - nơi sinh --> birthplace
            - đăng ký --> birth_registration
            - Còn lại, tin tưởng LLM.
            Nếu thay đổi, thay đổi các tagname phía sau tương ứng:
            - Khác với tagname hiện tại.
            -  Có cùng gốc fieldname (birthplace, birth_registration)
            Chưa xử lý xem, xã, huyện, tỉnh có nhầm nhau không (có thể xử lý sau)
            '''
            if "nơi sinh" in sentence_contextual and "birth_registration_place" in tagname:
                new_tagname = re.sub("birth_registration_place","birthplace",tagname)
                label_llm = self.modified_label_llm(label_llm, index_llm, "birth_registration_place", "birthplace")
            elif ("đăng ký" in sentence_contextual or "làm" in sentence_contextual) and "birthplace" in tagname:
                new_tagname = re.sub("birthplace","birth_registration_place",tagname)
                label_llm = self.modified_label_llm(label_llm, index_llm, "birthplace", "birth_registration_place")
            

            # return new_tagname
        # # Check id - passport group
        elif value_tagname in group_id_tagname or value_tagname in group_passport_tagname:
            '''
            Check sự nhẫm lẫn giữa id_number và passport_number
            - Đầu tiên check để đúng field id, passport
            - Tiếp theo, cần check hậu tố _place, _date
            - Và, check nhầm giữa _place, _date với _number
            '''
            #Check if any list_contextual_id_number, list_contextual_passport in sentence_contextual
            # if not any(temp in sentence_contextual for temp in list_contextual_id_number+list_contextual_passport):
            #     return "[#another]"
            # if context exist both in id, passport --> Trust LLM
            if any(temp in sentence_contextual for temp in list_contextual_id_number) and any(temp in sentence_contextual for temp in list_contextual_passport):
                pass
            elif any(temp in sentence_contextual for temp in list_contextual_id_number):
                if "passport" in tagname:
                    new_tagname = re.sub("passport","id_number",tagname)
                    label_llm = self.modified_label_llm(label_llm, index_llm, "passport", "id_number")
            elif any(temp in sentence_contextual for temp in list_contextual_passport):
                if "id" in tagname:
                    new_tagname = re.sub("id","passport",tagname)
                    label_llm = self.modified_label_llm(label_llm, index_llm, "id", "passport")
                        
            # Second, check suffix _date, _place
            if "_place" in new_tagname:
                if "ngày cấp" in sentence_contextual or "cấp ngày" in sentence_contextual:
                    new_tagname = re.sub("_place","_date",tagname)
            elif "_date" in new_tagname:
                if "nơi cấp" in sentence_contextual or "cấp nơi" in sentence_contextual:
                    new_tagname = re.sub("_date","_place",tagname)

            # Third, _date, _place, _date
            if "_number" in new_tagname:
                if "ngày cấp" in sentence_contextual or "cấp ngày" in sentence_contextual:
                    new_tagname = re.sub("_number","_issue_date",tagname)
                elif "nơi cấp" in sentence_contextual or "cấp nơi" in sentence_contextual:
                    new_tagname = re.sub("_number","_issue_place",tagname)
            elif "_date" in new_tagname:
                if "số" in sentence_contextual and "ngày cấp" not in sentence_contextual and "cấp ngày" not in sentence_contextual:
                    new_tagname = re.sub("_issue_date","_number",tagname)
            elif "_place" in new_tagname:
                if "số" in sentence_contextual and "nơi cấp" not in sentence_contextual and "cấp nơi" not in sentence_contextual:
                    new_tagname = re.sub("_issue_place","_number",tagname)
            
            # return new_tagname
        # Check dob group
        elif value_tagname in group_dob_tagname:
            '''
            Check sự nhẫm lẫn giữa dob, _text, và dob_year
            - Nếu có "bằng chữ" --> dob_text
            - Nếu là dob_year, hoặc dob, check nếu là năm (không có tháng, và ngày) --> thành dob, ngược lại là dob_year.
            '''
            if "chữ" in sentence_contextual and "_dob" in tagname:
                new_tagname = f"[{userX}_dob_text]"
            elif "chữ" not in sentence_contextual and "_dob_text" in tagname:
                new_tagname = re.sub("_dob_text","_dob",tagname)
            elif value_tagname in ["dob_year", "dob"]:
                if "năm" in sentence_contextual and "tháng" not in sentence_contextual and "ngày" not in sentence_contextual:
                    new_tagname = f"[{userX}_dob_year]"
                elif all(temp in sentence_contextual for temp in ["ngày", "tháng", "năm"]):
                    new_tagname = f"[{userX}_dob]"
                elif '/' not in sentence_contextual:
                    new_tagname = f"[{userX}_dob]"
            elif value_tagname in ["dob_month", "dob"]:
                if "tháng" in sentence_contextual and "ngày" not in sentence_contextual and "năm" not in sentence_contextual:
                    new_tagname = f"[{userX}_dob_month]"
                elif all(temp in sentence_contextual for temp in ["ngày", "tháng", "năm"]):
                    new_tagname = f"[{userX}_dob]"
                elif '/' not in sentence_contextual:
                    new_tagname = f"[{userX}_dob]"
            # return new_tagname
    
        # Check address group
        ## With hometown
        elif value_tagname in group_hometown_tagname:
            '''
            Vì hometown thường có 1 mình (không có ward...), nên chỉ cần check thuộc group nào.
            '''
            if any(temp in sentence_contextual for temp in list_hometown):
                return tagname
            # Check if miss with tagname permanent, or current
            if any(temp in sentence_contextual for temp in list_permanent_address):
                new_tagname = re.sub("_hometown","_permanent_address",tagname)
                label_llm = self.modified_label_llm(label_llm, index_llm, "hometown", "permanent_address")
            if any(temp in sentence_contextual for temp in list_current_address):
                new_tagname = re.sub("_hometown","_current_address",tagname)
                label_llm = self.modified_label_llm(label_llm, index_llm, "hometown", "current_address")
            # return new_tagname
        ## With permanent and current (check if these are mixed)
        elif value_tagname in group_permanent_address_tagname or value_tagname in group_current_address_tagname:
            '''
            Đối với permanent,và current:
            - Check nếu là hometown --> return.
            - Check nhầm lần với "Trạng thái HIỆN TẠI", "tình trạng HIỆN TẠI" --> return
            - Tương tự check current, và permanent có đúng hay không như birthplace.
            '''
            # if value_tagname in group_current_address_tagname:
            #     if not any(temp in sentence_contextual for temp in list_context_current_address):
            #         return "[#another]"
            # Check if current address mixed with current status
            if ("tình trạng" in sentence_contextual or "trạng thái" in sentence_contextual) and ("địa chỉ" not in sentence_contextual):
                return "[#another]"
            # check if mixed with hometown
            if any(temp in sentence_contextual for temp in list_hometown):
                if "_permanent_address" in tagname:
                    new_tagname = re.sub("_permanent_address","_hometown",tagname)
                    label_llm = self.modified_label_llm(label_llm, index_llm, "permanent_address", "hometown")
                elif "_current_address" in tagname:
                    new_tagname = re.sub("_current_address","_hometown",tagname)
                    label_llm = self.modified_label_llm(label_llm, index_llm, "current_address", "hometown")
                return new_tagname
            # check right field current, permanent
            elif any(temp in sentence_contextual for temp in list_current_address) and any(temp in sentence_contextual for temp in list_permanent_address):
                pass
            elif any(temp in sentence_contextual for temp in list_current_address):
                if "_permanent_address" in tagname:
                    new_tagname = re.sub("_permanent_address","_current_address",tagname)
                    label_llm = self.modified_label_llm(label_llm, index_llm, "permanent_address", "current_address")
            elif any(temp in sentence_contextual for temp in list_permanent_address):
                if "_current_address" in tagname:
                    new_tagname = re.sub("_current_address","_permanent_address",tagname)
                    label_llm = self.modified_label_llm(label_llm, index_llm, "current_address", "permanent_address")
            # return new_tagname     
        # Check marial_status
        elif "marital_status" in value_tagname:
            if "hôn nhân" not in sentence_contextual:
                new_tagname = "[#another]"
                # return new_tagname
        # Check occupation
        elif "occupation" in value_tagname:
            if any(temp in sentence_contextual for temp in list_occupation):
                new_tagname = tagname
            else:
                new_tagname = "[#another]"
        elif value_tagname in group_education_tagname:
            if all(temp not in sentence_contextual for temp in list_education):
                new_tagname = "[#another]"
        # Check group phone
        # Check phone
        elif value_tagname in group_phone_tagname:
            if 'cố định' in sentence_contextual or 'bàn' in sentence_contextual:
                new_tagname = f"[{userX}_home_phone]"
        # Check social insurance
        elif value_tagname in group_social_insurance_tagname:
            if "social_insurance_number" in value_tagname:
                if any(temp in sentence_contextual for temp in list_contextual_health_number):
                    new_tagname = re.sub("social_insurance_number","health_insurance_number",tagname)
            if "health_insurance_number" in value_tagname:
                if any(temp in sentence_contextual for temp in list_contextual_social_number):
                    new_tagname = re.sub("health_insurance_number","social_insurance_number",tagname)
        
        # Take again userX, value_tagname
        userX, value_tagname = self.extract_user_and_tag(tagname)
        # Now check if tagname missing suffix ward, district, province
        if value_tagname in group_tagname_have_ward_district_province:
            if any(temp in sentence_contextual for temp in list_village) and "village" not in new_tagname and all(temp not in sentence_contextual for temp in list_not_village):
                new_tagname = re.sub("]","_village]",new_tagname)
            elif any(temp in sentence_contextual for temp in list_ward) and "ward" not in new_tagname and all(temp not in sentence_contextual for temp in list_not_ward):
                new_tagname = re.sub("]","_ward]",new_tagname)
            elif any(temp in sentence_contextual for temp in list_district) and "district" not in new_tagname and all(temp not in sentence_contextual for temp in list_not_district):
                new_tagname = re.sub("]","_district]",new_tagname)
            elif any(temp in sentence_contextual for temp in list_province) and "province" not in new_tagname and all(temp not in sentence_contextual for temp in list_not_province):
                new_tagname = re.sub("]","_province]",new_tagname)
        # if new_tagname != tagname:
        #     pass
        label_llm[index_llm] = new_tagname
        return new_tagname
    
    def modify_tagname_dob_date_day_month_year(self, contextual_input, copy_contextual_input, label_input, index_filled_input, contextual_llm, label_llm, index_llm):
        try:
            pattern_dob = re.compile(r'_dob\]$')
            if pattern_dob.search(label_input[index_filled_input]) and index_filled_input<len(contextual_input)-1: # Check tháng năm ở phía sau
                # Kiểm tra có tháng, năm phía sau không (nếu có thì biến đổi thành day, month, year), nếu không thì giữ nguyên
                if ("tháng" in contextual_input[index_filled_input + 1] and "ngày" not in contextual_input[index_filled_input + 1]) or "/" in contextual_input[index_filled_input + 1]:
                    # print(f"debug1.1 at {contextual_input[index_filled_input + 1]}")
                    label_input[index_filled_input+2] =f"{label_input[index_filled_input][:-1]}_year]"
                    label_input[index_filled_input+1] =f"{label_input[index_filled_input][:-1]}_month]"
                    label_input[index_filled_input] =f"{label_input[index_filled_input][:-1]}_day]"
                    copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
                    # Điền thêm 2 nên phải + = 2
                    if index_llm<len(contextual_llm)-1:
                        if ("tháng" in contextual_llm[index_llm + 1] and "ngày" not in contextual_llm[index_llm + 1]) or "/" in contextual_llm[index_llm + 1]:
                            copy_contextual_input[index_filled_input+1] = contextual_llm[index_llm+1] + [":"] +  [label_llm[index_llm+1]]
                            copy_contextual_input[index_filled_input+2] = contextual_llm[index_llm+2] + [":"] +  [label_llm[index_llm+2]]
                            index_llm = index_llm + 2
                    # index_llm = index_llm + 2
                    index_filled_input = index_filled_input + 2
                    
                    
            # TH2: có _date
            pattern_date = re.compile(r'_date\]$')
            if pattern_date.search(label_input[index_filled_input]) and index_filled_input<len(contextual_input) - 1:
                # print(f"debug2 at {contextual_input[index_filled_input + 1]}")
                # Kiểm tra có tháng, năm phía sau không (nếu có thì biến đổi thành day, month, year), nếu không thì giữ nguyên
                # if "tháng" in contextual_input[index_filled_input + 1] or "/" in contextual_input[index_filled_input + 1]:
                if ("tháng" in contextual_input[index_filled_input + 1] and "ngày" not in contextual_input[index_filled_input + 1]) or "/" in contextual_input[index_filled_input + 1]:
                    # print(f"debug2.1 at {contextual_input[index_filled_input + 1]}")
                    prefix_date = label_input[index_filled_input].split("_date",1)[0]
                    label_input[index_filled_input + 2] =f"{prefix_date}_year]"
                    label_input[index_filled_input + 1] =f"{prefix_date}_month]"
                    label_input[index_filled_input] =f"{prefix_date}_day]"
                    copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
                    # Điền thêm 2 nên phải + = 2
                    if index_llm<len(contextual_llm)-1:
                        if ("tháng" in contextual_llm[index_llm + 1] and "ngày" not in contextual_llm[index_llm + 1]) or "/" in contextual_llm[index_llm + 1]:
                            copy_contextual_input[index_filled_input+1] = contextual_llm[index_llm+1] + [":"] +  [label_llm[index_llm+1]]
                            copy_contextual_input[index_filled_input+2] = contextual_llm[index_llm+2] + [":"] +  [label_llm[index_llm+2]]
                            index_llm = index_llm + 2
                    # index_llm = index_llm + 2
                    index_filled_input = index_filled_input + 2
                    
            # Th3: có _day
            pattern_day = re.compile(r'_day\]$')
            if pattern_day.search(label_input[index_filled_input]) and index_filled_input<len(contextual_input):
                # print(f"debug3 at {label_input[index_filled_input]}")
                # Kiểm tra có tháng, năm phía sau không (nếu không thì biến đổi thành date), nếu có thì giữ nguyên
                if (index_filled_input == len(contextual_input) - 1) or ("tháng" not in contextual_input[index_filled_input + 1] and "/" not in contextual_input[index_filled_input + 1]) or ("ngày" in contextual_input[index_filled_input + 1] and "tháng" in contextual_input[index_filled_input + 1]):
                    # print(f"debug3.1 at {label_input[index_filled_input]}")
                    # print(f"debug3.1 at {label_input[index_filled_input]}")
                    prefix_day = label_input[index_filled_input].split("_day", 1)[0]
                    label_input[index_filled_input] =f"{prefix_day}_date]"
                    if index_llm<len(contextual_llm)-1 and f"{prefix_day}_month]" in label_llm[index_llm+1]:
                        index_llm += 2
                elif (index_filled_input < len(contextual_input) - 3): # có thể điền hai chỗ nữa
                    if ("tháng" in contextual_input[index_filled_input + 1] and "ngày" not in contextual_input[index_filled_input + 1]) or "/" in contextual_input[index_filled_input + 1]:
                        prefix_day = label_input[index_filled_input].split("_day", 1)[0]
                        label_input[index_filled_input + 2] =f"{prefix_day}_year]"
                        label_input[index_filled_input + 1] =f"{prefix_day}_month]"
                        copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
                        # Điền thêm 2 nên phải + = 2
                        if index_llm<len(contextual_llm)-1:
                            if ("tháng" in contextual_llm[index_llm + 1] and "ngày" not in contextual_llm[index_llm + 1]) or "/" in contextual_llm[index_llm + 1]:
                                copy_contextual_input[index_filled_input+1] = contextual_llm[index_llm+1] + [":"] +  [label_llm[index_llm+1]]
                                copy_contextual_input[index_filled_input+2] = contextual_llm[index_llm+2] + [":"] +  [label_llm[index_llm+2]]
                                index_llm = index_llm + 2
                        # index_llm = index_llm + 2
                        index_filled_input = index_filled_input + 2
            return contextual_input, copy_contextual_input, label_input, index_filled_input, contextual_llm, label_llm, index_llm
        except Exception as error:
            print(f" === Error at here {error} === .")
            raise Exception("Sorry, error at mofidy dob, date, day, month, year!!")

    def check_prev_now_next_context_similiar(self, contextual_input, label_input, index_input, contextual_llm, label_llm, index_llm):
        '''
        Hàm kiểm tra nếu hiện tại giống nhau + trước/sau giống --> điền llm vào input.
        Riêng nếu now là month, year --> phải check cả hai đầu. (Vì trước/sau 100% có context giống rồi).
        Các trường hợp đặc biệt:
        - Vị trí đầu: không có next_contextual, tương tự vị trí cuối, không có prev
        - Nếu now là tháng, năm,/ (tức tagname _month, _year) --> phải có _day mới được điền.   
        - Nếu now là ngày --> check phía trước, vì khả năng cao phía sau auto giống (tháng)

        Output:
        - True/False: Có nên điền tagname hiện tại của LLM điền vào input hay không.
        '''
        prev_name_contextual_input = None
        next_name_contextual_input = None
        prev_name_contextual_llm = None
        next_name_contextual_llm= None
        # Get prev and next contextual input
        if index_input>0:
            prev_name_contextual_input = self.get_hash_name_from_context_at_index(contextual_input, index_input-1)
        if index_input < len(contextual_input)-1:
            next_name_contextual_input = self.get_hash_name_from_context_at_index(contextual_input, index_input+1)
        # Get prev and next contextual llm
        if index_llm>0:
            prev_name_contextual_llm = self.get_hash_name_from_context_at_index(contextual_llm, index_llm - 1)
        if index_llm < len(contextual_llm)-1:
            next_name_contextual_llm = self.get_hash_name_from_context_at_index(contextual_llm, index_llm + 1)
        # Get context now
        name_contextual_input = self.get_hash_name_from_context_at_index(contextual_input, index_input)
        name_contextual_llm = self.get_hash_name_from_context_at_index(contextual_llm, index_llm)
        # Checking
        if name_contextual_input != name_contextual_llm:
            return False
        # Tagname hiện tại là tháng/năm/\/
        if len(contextual_input[index_input])==1 and any(temp in name_contextual_input for temp in ["tháng", "năm", "/"]):
            if prev_name_contextual_input is not None and prev_name_contextual_llm is not None and prev_name_contextual_input != prev_name_contextual_llm:
                return False
            if next_name_contextual_input is not None and next_name_contextual_llm is not None and next_name_contextual_input!= next_name_contextual_llm:
                return False
            # if "another" in label_input[index_input-1]:
            #     return False
            return True
        # Current tagname is in [_dob, _date, _day]
        current_tagname_llm = label_llm[index_llm]
        if any(temp in current_tagname_llm for temp in["dob", "date", "day"]):
            if prev_name_contextual_input is not None and prev_name_contextual_llm is not None and prev_name_contextual_input == prev_name_contextual_llm:
                return True
            return False
        # Check prev, or next, if equivalent --> assign
        if prev_name_contextual_input is not None and prev_name_contextual_llm is not None and prev_name_contextual_input == prev_name_contextual_llm:
            return True
        if next_name_contextual_input is not None and next_name_contextual_llm is not None and next_name_contextual_input == next_name_contextual_llm:
            return True
        return False         
    
    def get_tagnames_from_LLM_filled_form(
        self, contextual_llm, label_llm, contextual_input, label_input, process_tagname=True
    ):
        """
        Hàm trích xuất tagnames từ LLM filled form, dùng thông tin ngữ cảnh tagname
        Trích xuất, tạo được một list các tagname sẽ điền vào cho input form
        Input
        - contextual_llm: ngữ cảnh của LLM filled form
        - label_llm: list các tagname của LLM filled form
        - contextual_input: ngữ cảnh của input form
        - label_input: tagname input (ban đầu toàn bộ là #another)

        Nhân tiện, khi điền tagname, ta sẽ xử lý lỗi dob, date luôn, có 3 trường hợp.
        Khi xét một tagname điền vào input
        - Nếu là _dob --> check phía sau có tháng, năm --> đổi thành day, month, year
        - Nếu có _date --> check phía sau có tháng, năm --> đổi thành day, month, year
        - Nếu là _day --> check phía sau không có tháng, năm --> đổi thành date (rồi cải tiến sau)

        Output: list tagname để điền vào input
        """
        # Standard all tagname from label_llm
        label_llm = [self.standard_tagname(tagname) for tagname in label_llm]
        
        # DEBUGGING: Get copy of contextual input --> debugging when printout evaluate --> Add '1' to each copy_contextual_input element
        copy_contextual_input = contextual_input.copy()
        copy_contextual_input = [['1'] + sublist for sublist in copy_contextual_input]
        # Từ dữ liệu LLM filled, điền vào input form (Lưu các tagname vào list)
        index_filled_input = 0
        index_llm = 0
        while index_filled_input < len(contextual_input) and index_llm < len(contextual_llm): 
            # print(f"Context input: {contextual_input[index_filled_input]} - llm:  {contextual_llm[index_llm]}")
            if self.check_prev_now_next_context_similiar(contextual_input, label_input, index_filled_input, contextual_llm, label_llm, index_llm): 
                # print(f"True at {index_filled_input} with context {contextual_input[index_filled_input]}  .... ")
                if not process_tagname:
                    label_input[index_filled_input] = label_llm[index_llm]
                else:
                    tagname_fill = self.get_modifed_tagname(contextual_input[index_filled_input], label_llm, index_llm, label_input[:index_filled_input])
                    label_input[index_filled_input] = tagname_fill
                copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
            else: # Thừa hoặc thiếu tagname chỗ này
                # print(f"False from {index_filled_input} .... ")
                temp_count = 1
                T = True
                while ((temp_count < len(contextual_input) - index_filled_input) or (temp_count < len(contextual_llm) - index_llm)) and (temp_count<10):
                    '''
                    Print for debugging
                    Current context input
                    current context llm
                    '''
                    # try:
                    #     print(f"=== Tempcount: {temp_count} ====")
                    #     print(f"Input: Now {index_filled_input} -  {contextual_input[index_filled_input]}")
                    #     print(f"LLM: Now {index_llm} - {contextual_llm[index_llm]}")

                    #     print(f"Input: {contextual_input[index_filled_input + temp_count]}")
                    #     print(f"LLM: {contextual_llm[index_llm + temp_count]}")
                    #     print()
                    # except:
                    #     pass
                    
                    # Check LLM điền thiếu tagname này --> bỏ qua --> ngược lại điền từ tagname sau của input
                    if (temp_count < len(contextual_input) - index_filled_input) and ((index_filled_input+temp_count) < len(contextual_input)):
                        if self.check_prev_now_next_context_similiar(contextual_input, label_input, index_filled_input + temp_count, contextual_llm, label_llm, index_llm): 
                            index_filled_input = index_filled_input + temp_count
                            T = False
                            break
                                
                    # Ngược lại check LLM điền thừa
                    if (temp_count < len(contextual_llm) - index_llm) and ((index_llm+temp_count) < len(contextual_llm)):
                        if self.check_prev_now_next_context_similiar(contextual_input, label_input, index_filled_input, contextual_llm, label_llm, index_llm + temp_count): 
                            index_llm = index_llm + temp_count
                            T = False
                            break
          
                    temp_count = temp_count + 1
                if T:
                    print("Don't have suitable tagname, both input and llm +=1")
                    try:
                        print(f"Index {index_filled_input} with {len(contextual_input)} context {contextual_input[index_filled_input]} t {label_input[index_filled_input]}")
                        print(f"Index {index_llm} with {len(contextual_llm)} context {contextual_llm[index_llm]} t {label_llm[index_llm]}")
                        print() 
                    except Exception as e:
                        print(f"Error at here {e}")
                    index_filled_input += 1
                    index_llm += 1
                    continue
                # else:
                    # print(f"Filling {label_llm[index_llm]} to {contextual_input[index_filled_input]}")
                if not process_tagname:
                    label_input[index_filled_input] = label_llm[index_llm]
                else:
                    tagname_fill = self.get_modifed_tagname(contextual_input[index_filled_input], label_llm, index_llm, label_input[:index_filled_input])
                    label_input[index_filled_input] = tagname_fill
                copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
            # Xử lý với tagname dob, date,..
            contextual_input, copy_contextual_input, label_input, index_filled_input, contextual_llm, label_llm, index_llm = self.modify_tagname_dob_date_day_month_year(contextual_input, copy_contextual_input, label_input, index_filled_input, contextual_llm, label_llm, index_llm)
            # Điền vị trí tiếp
            index_llm = index_llm + 1
            index_filled_input = index_filled_input + 1
        # print(label_input)
        # standard label_input
        label_input = [self.standard_tagname(tagname) for tagname in label_input]
        return label_input, copy_contextual_input
    
    # Sau đó đơn giản tạo hàm đưa label vào input form
    def fill_tagname_to_form(self, list_tag_name, form):
        """
        Từ list_tag_name, và form
        Điền list_tag_name này vào form (input với .....)
        Cần check nếu len(list_tag_name) = với số lượng ..... cần điền.
        """
        # Ensure the length matches the number of placeholders
        num_placeholders = form.count("[#another]")
        # print(num_placeholders)
        if len(list_tag_name) != num_placeholders:
            raise ValueError(
                f"Mismatch: Found {num_placeholders} placeholders, but {len(list_tag_name)} tagnames were provided."
            )

        # Replace each occurrence of [#another] with the corresponding tagname
        # Replace each occurrence of [#another] with the corresponding tagname
        for tag in list_tag_name:
            if tag == "[#another]":
                form = form.replace("[#another]", "[another]", 1)
            else:
                form = form.replace("[#another]", f"{tag}", 1)
        form = form.replace("[another]", "[#another]")
        return form
    
    def renumber_users(self, text):
        # Find all occurrences of userX_
        user_pattern = re.compile(r'user\d+_')
        user_matches = user_pattern.findall(text)
        user_matches = list(dict.fromkeys(user_matches))
        # Here we got list [userY,userX,userZ] --> need to reorder
        num_user = len(user_matches)
        ordered_users = [f"user{index}_" for index in range(1,num_user+1)]
        for i in range(num_user):
            if user_matches[i] == ordered_users[i]:
                continue
            else:
                text = re.sub(rf'{ordered_users[i]}', r'user999_',text)
                backup_num = user_matches[i]
                text = re.sub(rf'{user_matches[i]}', rf'{ordered_users[i]}',text)
                text = re.sub(r'user999_', rf'{backup_num}',text)
                # Update user_matches
                for j in range(num_user):
                    if (user_matches[j]==ordered_users[i]):
                        user_matches[j] = user_matches[i]
                user_matches[i] = ordered_users[i]
                
        return text
    # Filling receiver, place, day, month, year
    def normalize_receiver_expression(self, text):
        """
        - 'Kính gửi: [#another]'
        - 'Kính gửi: text [#another]'
        - 'Kính gửi: Trung tâm [user_tag]'
        - 'Kính gửi : ABC XYZ [user_tag]'
        - 'Kính gửi (1): [#another]'
        - 'Kính gửi: (1) [#another]'

        """
        def replace_tag(match):
            prefix = match.group(1)
            return f"{prefix}[receiver]"

        pattern = r"(Kính\s+gửi\s*(?:\(\d+\))?\s*:\s*(?:\(\d+\))?\s*.*?)(\[[^\]]+\])"
        return re.sub(pattern, replace_tag, text)

    def normalize_filled_date_expression(self, text):
        """
        Các trường hợp được hỗ trợ:

        1. [#another], ngày [#another] tháng [#another] năm [#another]
        2. [#another], ngày [#another], tháng [#another], năm [#another]
        3. Ngày [#another] tháng [#another] năm [#another]
        4. ngày [#another] tháng [#another] năm [#another]
        5. Ngày [#another], tháng [#another], năm [#another]

        Những trường hợp không xử lý:
        1. {text}: ngày [#another] tháng [#another] năm [#another]
        2. ngày [userX_tagname] tháng [userX_tagname] năm [userX_tagname]
        3. {text} ngày [#another] tháng [#another] năm [#another]
        """

        # Mẫu chính cho các kiểu ngày
        date_pattern = re.compile(
            r"(?:\[(?P<place>#another)\],*\s*)?"                          # [place], (tùy chọn)
            r"(?:ngày|Ngày)\s*\[(?P<day>#another)\]\s*,?\s*"              # ngày [day],
            r"(?:tháng|Tháng)\s*\[(?P<month>#another)\]\s*,?\s*"          # tháng [month],
            r"(?:năm|Năm)\s*(?P<number>\d+)?\s*\[(?P<year>#another)\]"             # năm [year], có hoặc không có tiền tố "20"

        )

        # Mẫu loại trừ
        exclude_patterns = [
            r"^[^:]+:\s*ngày\s*\[#another\]\s*tháng\s*\[#another\]\s*năm\s*\[#another\]",
            r"ngày\s*\[user[^\]]+\]\s*tháng\s*\[user[^\]]+\]\s*năm\s*\[user[^\]]+\]",
            r"\w+\s*ngày\s*\[#another\]\s*tháng\s*\[#another\]\s*năm\s*\[#another\]",
            r"\b(?!tại\b)\w+\s*\[#another\],*\s*ngày\s*\[#another\]\s*tháng\s*\[#another\]\s*năm\s*\[#another\]",
            r"\w+\s*\[[^\]]+\]\s*tại\s*,*\s*\[#another\]",
        ]

        exclude_regexes = [re.compile(p) for p in exclude_patterns]

        # Hàm thay thế ngày
        def replace_date(match):
            # Lấy tiền tố từ nhóm năm
            year_prefix = ""
            if match.group("number"):
                year_prefix = match.group("number")
            # Thay thế ngày
            if match.group("place"):
                return f"[place], ngày [day] tháng [month] năm {year_prefix} [year]"
            else:
                return f"ngày [day] tháng [month] năm {year_prefix} [year]"

        # Xử lý từng dòng một
        lines = text.splitlines()
        normalized_lines = []

        for line in lines:
            # Nếu dòng khớp với bất kỳ mẫu loại trừ nào → giữ nguyên
            if any(p.search(line) for p in exclude_regexes):
                normalized_lines.append(line)
            else:
                # Thay thế biểu thức ngày nếu có
                normalized_lines.append(date_pattern.sub(replace_date, line))

        return "\n".join(normalized_lines)

    # def normalize_filled_date_expression_nam(self, input_text):
    #     output = input_text
    #     # Regex pattern:
    #     pattern1 = r'((?:\n+|\t+)|^)ngày\s*\[#another\]\s*tháng\s*\[#another\]\s*năm\s*\[#another\]'
    #     replacement1 = r'\1ngày [day] tháng [month] năm [year]'
        
    #     pattern2 = r'((?:\n+|\t+)|^)\[#another\]\s*(,?)\s*ngày\s*\[#another\]\s*tháng\s*\[#another\]\s*năm\s*\[#another\]'
    #     replacement2 = r'\1[place]\2 ngày [day] tháng [month] năm [year]'

    #     pattern3 = r'((?:\n+|\t+)|^)([^\s]*.*?)tại([^\s]*.*?)\[#another\]\s*(,?)\s*ngày\s*\[#another\]\s*tháng\s*\[#another\]\s*năm\s*\[#another\]'
    #     replacement3 = r'\1\2tại\3[place]\4 ngày [day] tháng [month] năm [year]'

    #     pattern4 = r'((?:\n+|\t+)|^)([^\s]*.*?)tại([^\s]*.*?),\s*(,?)\s*ngày\s*\[#another\]\s*tháng\s*\[#another\]\s*năm\s*\[#another\]'
    #     replacement4 = r'\1\2tại\3,\4 ngày [day] tháng [month] năm [year]'


    #     patterns = [
    #     (pattern1, replacement1),
    #     (pattern2, replacement2),
    #     (pattern3, replacement3),
    #     (pattern4, replacement4)
    #     ]
    #     # Apply
    #     for pattern, replacement in patterns:
    #         output = re.sub(pattern, replacement, output)
    #         # print(output)

    #     return output

    # Overall function input form_llm_filled, input_form --> output filled_form
    def fill_input_by_llm_form(self, form_llm_filled, input_form, process_tagname=True):
        # Reorder userX 
        form_llm_filled = self.renumber_users(form_llm_filled)
        # Get contextual
        contextual_llm, label_llm = self.get_contextual_tagnames(form_llm_filled)
        contextual_input, label_input = self.get_contextual_tagnames(input_form)
        # List tagname
        tagname_for_input,copy_contextual_input = self.get_tagnames_from_LLM_filled_form(
            contextual_llm, label_llm, contextual_input, label_input, process_tagname
        )
        # Fill
        filled_form = self.fill_tagname_to_form(tagname_for_input, input_form)
        # R
        # Modify receiver, place, day, month, year tagname
        filled_form = self.normalize_filled_date_expression(filled_form)
        # filled_form = self.normalize_filled_date_expression_nam(filled_form)
        filled_form = self.normalize_receiver_expression(filled_form)
        return filled_form,copy_contextual_input

    def get_modifed_label_tagname(self, list_contextual, tagname):
        contextual = list_contextual[-1]
        def extract_user_and_tag(var):
            pattern = r"\[user(\d+)_(\w+)\]"
            match = re.search(pattern, var)
            if match:
                user_id = f"user{match.group(1)}"
                tagname = match.group(2)
                return user_id, tagname
            return None, None  # Return None if no match
        
        if "user" not in tagname:
            return tagname

        userX, value_tagname = extract_user_and_tag(tagname)
        if userX is None or value_tagname is None:
            return tagname
            
        userX, value_tagname = extract_user_and_tag(tagname)
        if userX is None or value_tagname is None:
            return tagname
        group_name_tagname = ["full_name"]

        value_bracket_tagname = "["+value_tagname+"]"
        if value_bracket_tagname not in list_cccd_passport_tagnames:
            return tagname
            
        sentence_contextual = " ".join(contextual)
        # Check fullname group
        if value_tagname in group_name_tagname:
            if "full_name" in value_tagname:
                if "ký" in sentence_contextual or "(ký" in sentence_contextual :
                    return "[#another]"
        
        return tagname

    def get_tagnames_from_label_form(
        self, contextual_label, label_label, contextual_input, label_input
    ):
        """
        Copy version to modify label
        """
        # Standard all tagname from label_llm
        label_label = [self.standard_tagname(tagname) for tagname in label_label] 
        # Get copy of contextual input --> debugging when printout evaluate
        copy_contextual_input = contextual_input.copy()
        # Add '1' to each copy_contextual_input element
        copy_contextual_input = [['1'] + sublist for sublist in copy_contextual_input]
        # Từ dữ liệu LLM filled, điền vào input form (Lưu các tagname vào list)
        index_filled_input = 0
        index_llm = 0
        while index_filled_input < len(contextual_input) and index_llm < len(contextual_label): 
            name_contextual_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input)
            name_contextual_llm = self.get_hash_name_from_context_at_index(contextual_label,index_llm)
            if name_contextual_input == name_contextual_llm:
                # label_input[index_filled_input] = label_llm[index_llm]
                tagname_fill = self.get_modifed_label_tagname(contextual_input[:index_filled_input+1], label_label[index_llm])
                label_input[index_filled_input] = tagname_fill

                copy_contextual_input[index_filled_input] = contextual_label[index_llm] + [":"] +  [label_label[index_llm]]
            else:
                print(name_contextual_input)
                print(name_contextual_llm)
                raise ValueError("Contextual input and label are not matched")
            # Điền vị trí tiếp
            index_llm = index_llm + 1
            index_filled_input = index_filled_input + 1
        # print(label_input)
        return label_input, copy_contextual_input

    # Fill by label form
    def fill_input_by_label_form(self, label_form, input_form):
        # Get contextual
        contextual_label, label_label = self.get_contextual_tagnames(label_form)
        contextual_input, label_input = self.get_contextual_tagnames(input_form)

        # List tagname
        tagname_for_input,copy_contextual_input = self.get_tagnames_from_label_form(
            contextual_label, label_label, contextual_input, label_input
        )
        # Fill
        filled_form = self.fill_tagname_to_form(tagname_for_input, input_form)
        return filled_form,copy_contextual_input
    
    # 2. Remove different tagnames
    def remove_invalid_tagnames(
        self, form_text, valid_tagnames_general, valid_tagnames_cccd_passport
    ):
        # Regular expression to match all tagnames (e.g., [user1_full_name], [place], etc.)
        tagname_pattern = re.compile(r"\[[^\d].*?\]")

        # Function to replace invalid tagnames
        def replace_invalid_tagname(match):
            tagname = match.group(0)

            # Check if the tagname is a general tagname (direct match)
            if tagname in valid_tagnames_general:
                return tagname  # Keep general tagnames unchanged

            # Check if the tagname is a valid cccd/passport tagname with userX_ prefix (e.g., [user1_full_name])
            for valid_tagname in valid_tagnames_cccd_passport:
                if re.match(
                    r"\[user\d+_" + re.escape(valid_tagname[1:-1]) + r"\]", tagname
                ) or re.match(
                    r"\[deceased_" + re.escape(valid_tagname[1:-1]) + r"\]", tagname
                ):
                    return tagname  # Keep valid userX_ prefixed tagnames

            # If the tagname is not in the valid lists, remove it
            return ".........."

        # Process the form by replacing invalid tagnames
        cleaned_form = re.sub(tagname_pattern, replace_invalid_tagname, form_text)

        return cleaned_form

    def remove_different_tagnames(self, form):
        valid_tagnames_cccd_passport = list_cccd_passport_tagnames
        valid_tagnames_general = list_general_tagnames
        cleaned_form = self.remove_invalid_tagnames(
            form, valid_tagnames_general, valid_tagnames_cccd_passport
        )
        return cleaned_form

    # 3. Convert label form to input form
    def convert_label_form_to_input_form(self, label_folder, input_folder):
        '''
        Just need to replace all tagnames with placeholders ..........
        '''
        for index,filename in enumerate(os.listdir(label_folder)):
            if filename.endswith(".txt"):
                # print(f"{filename} at index {index}")
                label_path = label_folder + '/' + filename
                input_path = input_folder + '/' + filename
                form_text = self.Read_txt_file(label_path)
                # Replace all [tagname] with .....
                transformed_text = re.sub(r'\[[^\d\]].*?\]', '..........', form_text)
                self.Save_txt_file(input_path, transformed_text)
                print(f"Save successfully file {filename} at index {index} at {input_path}")



Temp = None

