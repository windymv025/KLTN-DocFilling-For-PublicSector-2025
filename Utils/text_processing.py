import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Utils.multi_value_dict import MultiValueDict
from Config.tagnames import list_cccd_passport_tagnames, list_general_tagnames

class Text_Processing:
    def __init__(self):
        pass

    def min_uniform(self, a, b):
        """
        This function server for function generat_uniform
        """
        if a == -1 and b != -1:
            return b
        if b == -1 and a != -1:
            return a
        if a == -1 and b == -1:
            return -1
        if a < b:
            return a
        else:
            return b

    def generate_uniform(self, Question):
        # Chuyển tất cả các dạng ......(number).... về dạng ..........(number)
        Question = Question.replace("…", "..")
        # print(new_form)
        Question = re.sub(r"\.{2,}\((\d+)\)\.{2,}", r"............(\1)", Question)
        count = 0
        # Initialize a counter for numbering the placeholders
        placeholder_counter = 1

        type1 = ".."
        type2 = "…"
        first_index = self.min_uniform(Question.find(type1), Question.find(type2))
        # Loop through the question and replace the placeholders with the numbered placeholders
        while first_index != -1:
            # Replace the first occurrence of the placeholder with the formatted numbered placeholder
            count += 1
            Question = (
                Question[:first_index]
                + "(Blank"
                + str(placeholder_counter)
                + ")"
                + Question[first_index:]
            )
            # Index }
            start_index = first_index + 2 + (len(str(placeholder_counter))) + 5
            end_index = start_index
            # Increment the counter
            placeholder_counter += 1

            # Kiểm tra trên hàng đó còn . tiếp hoặc … đó hay không --> vẫn là chỗ điền này.
            while (end_index < (len(Question))) and (
                Question[end_index] == "…" or Question[end_index] == "."
            ):
                end_index += 1

            # if (end_index+1 < (len(Question))) and (Question[end_index] == "\n") and (Question[end_index+1] == "…" or Question[end_index+1] == "."):
            #     end_index  += 1
            # Kiểm tra trường hợp xuống hàng vẫn còn ....
            while (end_index + 1 < (len(Question))) and (Question[end_index] == "\n"):
                while Question[end_index + 1] == "…" or Question[end_index + 1] == ".":
                    end_index += 1
                if Question[end_index + 1] == "\n":
                    end_index += 1
                    continue
                if Question[end_index + 1] != "…" and Question[end_index + 1] != ".":
                    break

            # Đã Hàng mới (Đã xuống hàng mà vẫn là chỗ điền thì cả cái hàng là của nó luôn)
            while end_index < len(Question) and Question[end_index] == "\n":
                # Kiểm tra hàng sau
                next_line_start = end_index + 1
                next_line_end = Question.find("\n", next_line_start)
                if (
                    next_line_end == -1
                ):  # Nếu không có dấu xuống dòng tiếp theo, chỉ đến cuối văn bản
                    next_line_end = len(Question)
                next_line = Question[next_line_start:next_line_end]

                # Kiểm tra xem hàng tiếp theo có phải toàn khoảng trắng, dấu chấm hoặc chấm lửng không
                if next_line.strip() == "" or all(c in ".…" for c in next_line.strip()):
                    end_index = next_line_end
                else:
                    break

            # while (end_index < (len(Question))) and (Question[end_index] == "…" or Question[end_index] == "."):
            #     end_index  += 1
            try:
                Question = Question[:start_index] + Question[end_index:]
            except:
                Question = Question[:start_index]
            # Find the indices of the next placeholders
            first_index = self.min_uniform(Question.find(type1), Question.find(type2))
        # Question = re.sub(r'\(Blank\d+\)', '[#another]', Question)
        return Question, count

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
    
    def process_declaration_date_and_place(self, form_text):
        """
        - Hàm để đưa chỗ điền ....., ngày.... tháng.... năm về đúng format [place], ngày [day] tháng [month] năm [year]
        - Vì chỗ điền này thì đặc trưng, nên có thể xử lý thẳng điểm đặc biệt này.
        """
        # Define the regex pattern to match the specific date format with optional spaces
        # Cái re này tui chưa rõ nha, tương lai có thể thay thế
        date_pattern = re.compile(
            r"\s*\[[#a-zA-Z0-9_]+?\]\s*,\s*ngày\s*\[.+?\]\s*tháng\s*\[.+?\]\s*năm\s*\[.+?\]"
        )
        # Define the replacement format
        replacement_format = "[place], ngày [day] tháng [month] năm [year]"
        # Use sub to replace matched dates with the correct format
        fixed_text = date_pattern.sub(replacement_format, form_text)

        return fixed_text

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

    def get_modifed_tagname(self, list_contextual, tagname):
        # print(tagname)
        # print(list_contextual)
        contextual = list_contextual[-1]
        def extract_user_and_tag(var):
            pattern = r"\[user(\d+)_(\w+)\]"
            match = re.search(pattern, var)
            if match:
                user_id = f"user{match.group(1)}"
                tagname = match.group(2)
                return user_id, tagname
            return None, None  # Return None if no match
        if "user" in tagname:
            # Standardize tagname
            tagname = re.sub(r"dob_date", "dob", tagname)
            # Replace "cmnd" with "id" exactly
            tagname = re.sub(r"cmnd", "id", tagname)
            # Replace "birth_place" with "birthplace" exactly
            tagname = re.sub(r"birth_place", "birthplace", tagname)
            # Replace "registration" with "birth_registration" exactly
            tagname = re.sub(r"birth_registration", "birth_registration_place", tagname)
            userX, value_tagname = extract_user_and_tag(tagname)
            value_bracket_tagname = "["+value_tagname+"]"
            #  Define group
            group_id_tagname = ["id_number", "id_issue_date", "id_issue_day", "id_issue_month", "id_issue_year", "id_issue_place"]
            group_passport_tagname = ["passport_number", "passport_issue_date", "passport_issue_day", "passport_issue_month", "passport_issue_year", "passport_issue_place"]
            group_current_address_tagname = ["current_address","current_address_ward","current_address_district","current_address_province"]
            group_permanent_address_tagname = ["permanent_address","permanent_address_ward","permanent_address_district","permanent_address_province"]
            group_hometown = ["hometown"]
            group_birth_registration_tagname = ["birth_registration_place", "birth_registration_place_ward", "birth_registration_place_district", "birth_registration_place_province"]
            group_birthplace_tagname = ["birthplace", "birthplace_ward", "birthplace_district", "birthplace_province"]
            group_dob_tagname = ["dob_text", "dob", "dob_date", "dob_day", "dob_month", "dob_year"]
            group_name_tagname = ["full_name", "alias_name"]
            if value_bracket_tagname in list_cccd_passport_tagnames:
                sentence_contextual = " ".join(contextual)
                # Check fullname group
                if value_tagname in group_name_tagname:
                    if "full_name" in value_tagname:
                        if "ký" in sentence_contextual or "(ký" in sentence_contextual :
                            return "[#another]"
                    if "khác" in sentence_contextual:
                        new_tagname = re.sub("full_name","alias_name",tagname)
                    else:
                        new_tagname = re.sub("alias_name","full_name",tagname)
                    return new_tagname
                    
                # Check Birthplace - birth_registration group
                if value_tagname in group_birthplace_tagname or value_tagname in group_birth_registration_tagname:
                    i_temp = -1
                    while i_temp != 0 and i_temp>=(-len(list_contextual)):
                        contextual_value = " ".join(list_contextual[i_temp])
                        if "nơi sinh" in contextual_value:
                            new_tagname = re.sub("birth_registration","birthplace",tagname)
                            i_temp = 0
                        elif "khai sinh" in contextual_value or "đăng ký" in contextual_value:
                            new_tagname = re.sub("birthplace","birth_registration",tagname)
                            i_temp = 0
                        else:
                            i_temp -= 1
                    if (i_temp < -len(list_contextual)):
                        return "[#another]"
                    return new_tagname
                
                # Check id - passport group
                list_contextual_id_number = ["cmnd", "chứng minh", "cccd", "căn cước", "định danh", "cmtnd"]
                list_contextual_passport = ["hộ chiếu","passport"]
                if value_tagname in group_id_tagname or value_tagname in group_passport_tagname:
                    new_tagname = tagname
                    # First, right id or passport
                    i_temp = -1
                    while i_temp != 0 and i_temp>=(-len(list_contextual)):
                        contextual_value = " ".join(list_contextual[i_temp])
                        if any(context in contextual_value for context in list_contextual_id_number):
                            # Return id_number
                            new_tagname = re.sub("passport","id",tagname)
                            i_temp = 0
                            # return new_tagname
                        elif any(context in contextual_value for context in list_contextual_passport):
                            # return passport
                            new_tagname = re.sub("id","passport",tagname)
                            i_temp = 0
                            # return new_tagname
                        else: # Must check previouse is cccd, or passport --> follow it
                            # Case "giấy tờ tùy thân"
                            if "giấy tờ tùy thân" in contextual_value:
                                new_tagname = re.sub("passport","id",tagname)
                                i_temp = 0
                            else:
                                i_temp -= 1
                        # return new_tagname
                    if (i_temp < -len(list_contextual)):
                        return "[#another]"
                    # Second, check suffix _date, _place
                    if "_place" in new_tagname:
                        # print(new_tagname)
                        # print(contextual_value)
                        if "ngày cấp" in contextual_value:
                            # print(contextual_value)
                            new_tagname = re.sub("_place","_date",tagname)
                    elif "_date" in new_tagname:
                        if "nơi cấp" in contextual_value:
                            new_tagname = re.sub("_date","_place",tagname)

                    # Third, _date with _number
                    if "_number" in new_tagname:
                        if "ngày cấp" in contextual_value or "cấp ngày" in contextual_value:
                            new_tagname = re.sub("_number","_date",tagname)
                        elif "nơi cấp" in contextual_value or "cấp nơi" in contextual_value:
                            new_tagname = re.sub("_number","_place",tagname)
                    elif "_date" in new_tagname:
                        if "số" in contextual_value and "ngày cấp" not in contextual_value and "cấp ngày" not in contextual_value:
                            new_tagname = re.sub("_date","_number",tagname)
                    elif "_place" in new_tagname:
                        if "số" in contextual_value and "nơi cấp" not in contextual_value and "cấp nơi" not in contextual_value:
                            new_tagname = re.sub("_place","_number",tagname)
                    return new_tagname
                
                # Check dob group
                if value_tagname in group_dob_tagname:
                    if "bằng chữ" in sentence_contextual:
                        new_tagname = f"[{userX}_dob_text]"
                        return new_tagname
                    elif value_tagname in ["dob_year", "dob"]:
                        if "năm" in sentence_contextual and "tháng" not in sentence_contextual and "ngày" not in sentence_contextual:
                            new_tagname = f"[{userX}_dob_year]"
                        else:
                            new_tagname = f"[{userX}_dob]"
                            return new_tagname
                    else:
                        return tagname
            
                # Check address group
                list_permanent_address = ["thường trú"]
                list_current_address = ["hiện tại", "tạm trú"]
                list_hometown = ["quê quán", "nguyên quán", "quê gốc"]
                if value_tagname in group_current_address_tagname or value_tagname in group_permanent_address_tagname or value_tagname in group_hometown:
                    new_tagname = tagname
                    if any(temp in sentence_contextual for temp in list_hometown):
                        new_tagname = f"[{userX}_hometown]"
                        # return new_tagname
                    if any(temp in sentence_contextual for temp in list_permanent_address):
                        new_tagname = f"[{userX}_permanent_address]"
                        # return new_tagname
                    if any(temp in sentence_contextual for temp in list_current_address):
                        new_tagname = f"[{userX}_current_address]"
                        # return new_tagname
                    if extract_user_and_tag(new_tagname)[1] == "current_address":
                        if "địa chỉ" not in sentence_contextual and ("tình trạng" in sentence_contextual or "trạng thái" in sentence_contextual):
                            new_tagname = "[#another]"
                    return new_tagname
                
                # Check marial_status
                if "marital_status" in value_tagname:
                    if "hôn nhân" not in sentence_contextual:
                        new_tagname = "[#another]"
                        return new_tagname

                return tagname
            else:
                return tagname
        else:
            return tagname

    def get_tagnames_from_LLM_filled_form(
        self, contextual_llm, label_llm, contextual_input, label_input
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
        # Get copy of contextual input --> debugging when printout evaluate
        copy_contextual_input = contextual_input.copy()
        # Add '1' to each copy_contextual_input element
        copy_contextual_input = [['1'] + sublist for sublist in copy_contextual_input]
        # Từ dữ liệu LLM filled, điền vào input form (Lưu các tagname vào list)
        index_filled_input = 0
        index_llm = 0
        while index_filled_input < len(contextual_input) and index_llm < len(contextual_llm): 
            name_contextual_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input)
            name_contextual_llm = self.get_hash_name_from_context_at_index(contextual_llm,index_llm)
            if name_contextual_input == name_contextual_llm:
                # label_input[index_filled_input] = label_llm[index_llm]
                tagname_fill = self.get_modifed_tagname(contextual_input[:index_filled_input+1], label_llm[index_llm])
                label_input[index_filled_input] = tagname_fill
                copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
            else: # Thừa hoặc thiếu tagname chỗ này
                temp_count = 1
                T = True
                # while (temp_count < len(contextual_input) - index_filled_input) or (temp_count < len(contextual_llm) - index_llm):
                while ((temp_count < len(contextual_input) - index_filled_input) or (temp_count < len(contextual_llm) - index_llm)) and (temp_count<5):
                    # Check LLM điền thiếu tagname này --> bỏ qua --> ngược lại điền từ tagname sau của input
                    if (temp_count < len(contextual_input) - index_filled_input) and ((index_filled_input+temp_count) < len(contextual_input)):
                        next_name_contextual_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input+temp_count)
                        if next_name_contextual_input == name_contextual_llm: # Bắt đầu tại đây
                            if len(contextual_input[index_filled_input+temp_count]) ==1 and contextual_input[index_filled_input+temp_count][0] in ["tháng", "năm","/"]:
                                # Check both sides
                                T1 = False
                                T2 = False
                                if (index_filled_input + temp_count)>0 and index_llm>0:
                                    previous_context_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + temp_count - 1)
                                    previous_context_llm = self.get_hash_name_from_context_at_index(contextual_llm,index_llm-1)
                                    if previous_context_input == previous_context_llm:
                                        # index_filled_input = index_filled_input + temp_count
                                        T1 = True
                                if (index_filled_input + temp_count)<len(contextual_input)-1 and index_llm<len(contextual_llm)-1:
                                    next_context_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + temp_count + 1)
                                    next_context_llm = self.get_hash_name_from_context_at_index(contextual_llm,index_llm+1)
                                    if  next_context_input == next_context_llm:
                                        # index_filled_input = index_filled_input + temp_count
                                        T2 = True
                                if T1 and T2:                                   
                                    T = False
                                    index_filled_input = index_filled_input + temp_count
                                    break
                            else:
                                # Check previous contextual
                                if (index_filled_input + temp_count)>0 and index_llm>0:
                                    previous_context_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + temp_count - 1)
                                    previous_context_llm = self.get_hash_name_from_context_at_index(contextual_llm,index_llm-1)
                                    if previous_context_input == previous_context_llm:
                                        index_filled_input = index_filled_input + temp_count
                                        T = False
                                        break
                                # Check following contextual
                                if (index_filled_input + temp_count)<len(contextual_input)-1 and index_llm<len(contextual_llm)-1:
                                    next_context_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + temp_count + 1)
                                    next_context_llm = self.get_hash_name_from_context_at_index(contextual_llm,index_llm+1)
                                    if next_context_input == next_context_llm:
                                        index_filled_input = index_filled_input + temp_count
                                        T = False
                                        break
                    
                    # Ngược lại check LLM điền thừa
                    if (temp_count < len(contextual_llm) - index_llm) and ((index_llm+temp_count) < len(contextual_llm)):
                        next_name_contextual_llm = self.get_hash_name_from_context_at_index(contextual_llm,index_llm+temp_count)
                        if next_name_contextual_llm == name_contextual_input: # Bắt đầu tại đây
                            if len(contextual_input[index_filled_input]) ==1 and contextual_input[index_filled_input][0] in ["tháng", "năm","/"]:
                                # Check both sides
                                T1 = False
                                T2 = False
                                if index_filled_input>0 and (index_llm + temp_count)>0:
                                    if (self.get_hash_name_from_context_at_index(contextual_input,index_filled_input - 1) == self.get_hash_name_from_context_at_index(contextual_llm,index_llm + temp_count-1)):
                                        # index_llm = index_llm + temp_count
                                        T1 = True
                                # Check following contextual
                                if index_filled_input<len(contextual_input)-1 and (index_llm + temp_count)<len(contextual_llm)-1:
                                    if (self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + 1) == self.get_hash_name_from_context_at_index(contextual_llm,index_llm + temp_count+1)):
                                        # index_llm = index_llm + temp_count
                                        T2 = True
                                if T1 and T2:
                                    T = False
                                    print(contextual_llm[index_llm + temp_count])
                                    index_llm = index_llm + temp_count
                                    break
                            else:
                                # Check previous contextual
                                if index_filled_input>0 and (index_llm + temp_count)>0:
                                    if (self.get_hash_name_from_context_at_index(contextual_input,index_filled_input - 1) == self.get_hash_name_from_context_at_index(contextual_llm,index_llm + temp_count-1)):
                                        index_llm = index_llm + temp_count
                                        T = False
                                        break
                                # Check following contextual
                                if index_filled_input<len(contextual_input)-1 and (index_llm + temp_count)<len(contextual_llm)-1:
                                    if (self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + 1) == self.get_hash_name_from_context_at_index(contextual_llm,index_llm + temp_count+1)):
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
                # label_input[index_filled_input] = label_llm[index_llm]
                tagname_fill = self.get_modifed_tagname(contextual_input[:index_filled_input+1], label_llm[index_llm])
                label_input[index_filled_input] = tagname_fill
                copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
            # print(f"Index {index_filled_input} with {len(contextual_input)} context {contextual_input[index_filled_input]} t {label_input[index_filled_input]}")
            # print(f"Index {index_llm} with {len(contextual_llm)} context {contextual_llm[index_llm]} t {label_llm[index_llm]}")
            # print()   
            # Xử lý với tagname dob, date,..
            # TH1: Là dob
            try:
                pattern_dob = re.compile(r'_dob\]$')
                if pattern_dob.search(label_input[index_filled_input]) and index_filled_input<len(contextual_input)-1: # Check tháng năm ở phía sau
                    # print(f"debug1 at {contextual_input[index_filled_input + 1]}")
                    # Kiểm tra có tháng, năm phía sau không (nếu có thì biến đổi thành day, month, year), nếu không thì giữ nguyên
                    # if "tháng" in contextual_input[index_filled_input + 1] or "/" in contextual_input[index_filled_input + 1]:
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
            except Exception as error:
                print(f" === Error at here {error} === .")
                break
            # Điền vị trí tiếp
            index_llm = index_llm + 1
            index_filled_input = index_filled_input + 1
        # print(label_input)
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
    
    def extract_user_number(self, tagname):
        match = re.search(r'user(\d+)_', tagname)
        if match:
            return int(match.group(1))  # Convert to integer
        raise ValueError('Must have index')

    def renumber_users(self, text):
        count_user = 1
        # Find all occurrences of userX_
        user_pattern = re.compile(r'user\d+_')
        user_matches = user_pattern.findall(text)
        user_matches = list(dict.fromkeys(user_matches))
        i = 0
        num_user = len(user_matches)
        while (i<num_user):
            index_user = self.extract_user_number(user_matches[i])
            if index_user != count_user:
                temp_index = -1
                for j in range(len(user_matches)):
                    if user_matches[j] == f"user{count_user}_":
                        temp_index = j
                        break
                # Swap
                text = re.sub(rf"user{count_user}", "userT",text)
                text = re.sub(rf"user{index_user}", f"user{count_user}",text)
                text = re.sub(r"userT", f"user{index_user}",text)
                if temp_index != -1:
                    user_matches[temp_index] = f"user{index_user}_"
                
            i += 1
            count_user += 1
        return text

    # Overall function input form_llm_filled, input_form --> output filled_form
    def fill_input_by_llm_form(self, form_llm_filled, input_form):
        # Fix place, day, month, year format
        form_llm_filled = self.process_declaration_date_and_place(form_llm_filled)
        # Reorder userX 
        form_llm_filled = self.renumber_users(form_llm_filled)
        print("debug1")
        # Get contextual
        contextual_llm, label_llm = self.get_contextual_tagnames(form_llm_filled)
        print("debug1.2")

        contextual_input, label_input = self.get_contextual_tagnames(input_form)
        print("debug2")

        # List tagname
        tagname_for_input,copy_contextual_input = self.get_tagnames_from_LLM_filled_form(
            contextual_llm, label_llm, contextual_input, label_input
        )
        print("debug3")

        # Fill
        filled_form = self.fill_tagname_to_form(tagname_for_input, input_form)
        filled_form = self.process_declaration_date_and_place(filled_form)
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

