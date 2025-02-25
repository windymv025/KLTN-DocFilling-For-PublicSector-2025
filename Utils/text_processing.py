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

    def get_modifed_tagname(self, contextual, tagname):
        if "user" in tagname:
            v_tagname = tagname[7:-1]
            # Check birthplace
            if "birthplace" in v_tagname:
                if "nơi sinh" in " ".join(contextual):
                    return tagname
                elif "khai sinh" in " ".join(contextual) or "đăng ký" in " ".join(contextual):
                    new_tagname = re.sub("birthplace","birth_registration",tagname)
                    return new_tagname
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
                label_input[index_filled_input] = self.get_modifed_tagname(contextual_llm[index_llm], label_llm[index_llm])
                copy_contextual_input[index_filled_input] = contextual_llm[index_llm] + [":"] +  [label_llm[index_llm]]
            else: # Thừa hoặc thiếu tagname chỗ này
                temp_count = 1
                T = True
                while (temp_count < len(contextual_input) - index_filled_input) or (temp_count < len(contextual_llm) - index_llm):
                    # Check LLM điền thiếu tagname này --> bỏ qua --> ngược lại điền từ tagname sau của input
                    if (temp_count < len(contextual_input) - index_filled_input) and ((index_filled_input+temp_count) < len(contextual_input)):
                        next_name_contextual_input = self.get_hash_name_from_context_at_index(contextual_input,index_filled_input+temp_count)
                        if next_name_contextual_input == name_contextual_llm: # Bắt đầu tại đây
                            # Check previous contextual
                            if (index_filled_input + temp_count)>0 and index_llm>0:
                                if (self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + temp_count - 1) == self.get_hash_name_from_context_at_index(contextual_llm,index_llm-1)):
                                    index_filled_input = index_filled_input + temp_count
                                    T = False
                                    break
                            # Check following contextual
                            if (index_filled_input + temp_count)<len(contextual_input)-1 and index_llm<len(contextual_llm)-1:
                                if (self.get_hash_name_from_context_at_index(contextual_input,index_filled_input + temp_count + 1) == self.get_hash_name_from_context_at_index(contextual_llm,index_llm+1)):
                                    index_filled_input = index_filled_input + temp_count
                                    T = False
                                    break
                    
                    # Ngược lại check LLM điền thừa
                    if (temp_count < len(contextual_llm) - index_llm) and ((index_llm+temp_count) < len(contextual_llm)):
                        next_name_contextual_llm = self.get_hash_name_from_context_at_index(contextual_llm,index_llm+temp_count)
                        if next_name_contextual_llm == name_contextual_input: # Bắt đầu tại đây
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
                label_input[index_filled_input] = self.get_modifed_tagname(contextual_llm[index_llm], label_llm[index_llm])
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
                    if (index_filled_input == len(contextual_input) - 1) or ("tháng" not in contextual_input[index_filled_input + 1] and "/" not in contextual_input[index_filled_input + 1]):
                        # print(f"debug3.1 at {label_input[index_filled_input]}")
                        # print(f"debug3.1 at {label_input[index_filled_input]}")
                        prefix_day = label_input[index_filled_input].split("_day", 1)[0]
                        label_input[index_filled_input] =f"{prefix_day}_date]"
                        if index_llm<len(contextual_llm)-1 and f"{prefix_day}_month]" in label_llm[index_llm+1]:
                            index_llm += 2
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
                form = form.replace("[#another]", f"[another]", 1)
            else:
                form = form.replace("[#another]", f"{tag}", 1)
        form = form.replace("[another]", "[#another]")
        return form

    # Overall function input form_llm_filled, input_form --> output filled_form
    def fill_input_by_llm_form(self, form_llm_filled, input_form):
        # Fix place, day, month, year format
        form_llm_filled = self.process_declaration_date_and_place(form_llm_filled)
        # Get contextual
        contextual_llm, label_llm = self.get_contextual_tagnames(form_llm_filled)
        contextual_input, label_input = self.get_contextual_tagnames(input_form)
        # List tagname
        tagname_for_input,copy_contextual_input = self.get_tagnames_from_LLM_filled_form(
            contextual_llm, label_llm, contextual_input, label_input
        )
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


class Text_Processing12332:
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

    ## Some functions to from LLM filled form --> pass tagname to input form
    # Function to process a place, date, month, year format
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
        pattern = re.compile(r"(.*?)(\[[^\d].+?\])", re.DOTALL)
        matches = pattern.findall(form)
        # Collecting the sentences
        sentences = []
        labels = []
        for match in matches:
            sentence = match[0].strip()  # Get the text before ".........."
            labels.append(match[1])
            # chuẩn hóa
            sentence = sentence.lower()
            sentence = re.sub(r"[^\w\s\/]", "", sentence)
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
            elif len(context[i])>2:
                return f"{context[i][0]}_{context[i][1]}_{context[i][-2]}_{context[i][-1]}_{len(context[i])}" #Đầu_KeD_KeC_Cuối_Length

    def get_hash_name_from_context(self, context, i1, i2):
        """
        Hàm này đơn giản tạo một chuỗi là key của dict, hiện tại, sẽ lấy context[0]_context[-1]_len(context)
        Tức sử dụng chữ đầu - chữ cuối - chuỗi
        Tiền tố 1: sử dụng context[i] context[i+1]
        Tiền tố 2: sử dụng context[i] context[i-1]

        Output: tên (key) cho LLM_contextual_to_tagname
        """
        name_i1 = self.get_hash_name_from_context_at_index(context, i1)
        name_i2 = self.get_hash_name_from_context_at_index(context, i2)
        if i2 > i1:
            name = f"1-{name_i1}-{name_i2}"
        elif i2 < i1:
            name = f"2-{name_i1}-{name_i2}"
        return name
    
    def map_name_to_index_contextual_llm(self,contextual_llm, label_llm):
        '''
        Input: contextual_llm, và label_llm
        Goal: Xây dựng luật từ contextual_llm, duyệt qua, lấy được tên theo từng index tagname
        Trỏ đến index của label_llm, là list tagname tương ứng
        '''
        LLM_contextual_to_index_tagname = MultiValueDict()
        # Lấy tagname từ LLM filled form
        for i in range(len(contextual_llm)):
            if i ==0:
                hash_name = self.get_hash_name_from_context(contextual_llm,i,i+1)
                # LLM_contextual_to_index_tagname.add(hash_name, label_llm[i])
                LLM_contextual_to_index_tagname.add(hash_name, i)
            elif i == len(contextual_llm)-1:
                hash_name = self.get_hash_name_from_context(contextual_llm,i,i-1)
                # LLM_contextual_to_index_tagname.add(hash_name, label_llm[i])
                LLM_contextual_to_index_tagname.add(hash_name, i)
            else:
                hash_name1 = self.get_hash_name_from_context(contextual_llm,i,i-1)
                hash_name2 = self.get_hash_name_from_context(contextual_llm,i,i+1)
                # LLM_contextual_to_index_tagname.add(hash_name1, label_llm[i])
                # LLM_contextual_to_index_tagname.add(hash_name2, label_llm[i])
                LLM_contextual_to_index_tagname.add(hash_name1, i)
                LLM_contextual_to_index_tagname.add(hash_name2, i)
        return LLM_contextual_to_index_tagname

    def fill_label_input_from_hashname(self,label_llm,LLM_contextual_to_tagname,hash_name,index_filled):
        # Process
        tagname = None
        T = False
        try:
            temp_index_tagname = LLM_contextual_to_tagname.get(hash_name)
            if temp_index_tagname >= index_filled:
                index_filled = temp_index_tagname + 1
                tagname = label_llm[temp_index_tagname]
                LLM_contextual_to_tagname.pop(hash_name)
                T = True
            else:
                while temp_index_tagname<index_filled:
                    LLM_contextual_to_tagname.pop(hash_name)
                    temp_index_tagname = LLM_contextual_to_tagname.get(hash_name)
                index_filled = temp_index_tagname + 1
                tagname = label_llm[temp_index_tagname]
                LLM_contextual_to_tagname.pop(hash_name)
                T = True
        except:
            pass
        return LLM_contextual_to_tagname,T,tagname,index_filled

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
        # Get
        LLM_contextual_to_tagname = self.map_name_to_index_contextual_llm(contextual_llm, label_llm)
        # Từ dữ liệu LLM filled, điền vào input form (Lưu các tagname vào list)
        index_filled = 0
        for i in range(len(contextual_input)):
            if label_input[i]!="[#another]":
                # print("herere")
                continue
            # if i == 48:
            #     print("hello")
            if i ==0:
                hash_name = self.get_hash_name_from_context(contextual_input,i,i+1)
                LLM_contextual_to_tagname,T,tagname,index_filled = self.fill_label_input_from_hashname(label_llm,LLM_contextual_to_tagname,hash_name,index_filled)
                if T:
                    label_input[i] = tagname
            elif i == len(contextual_input)-1:
                hash_name = self.get_hash_name_from_context(contextual_input,i,i-1)
                LLM_contextual_to_tagname,T,tagname,index_filled = self.fill_label_input_from_hashname(label_llm,LLM_contextual_to_tagname,hash_name,index_filled)
                if T:
                    label_input[i] = tagname
            else:
                hash_name1 = self.get_hash_name_from_context(contextual_input,i,i-1)
                LLM_contextual_to_tagname,T,tagname,index_filled = self.fill_label_input_from_hashname(label_llm,LLM_contextual_to_tagname,hash_name1,index_filled)
                if T:
                    label_input[i] = tagname
                else:    
                    hash_name2 = self.get_hash_name_from_context(contextual_input,i,i+1)
                    LLM_contextual_to_tagname,T,tagname,index_filled = self.fill_label_input_from_hashname(label_llm,LLM_contextual_to_tagname,hash_name2,index_filled)
                    if T:
                        label_input[i] = tagname
            if not T:
                continue
            # Xử lý với tagname dob, date,..
            # TH1: Là dob
            try:
                pattern_dob = re.compile(r"_dob\]$")
                if pattern_dob.search(label_input[i]) and i < len(contextual_input) - 1:
                    # Kiểm tra có tháng, năm phía sau không (nếu có thì biến đổi thành day, month, year), nếu không thì giữ nguyên
                    if (
                        ("tháng" in contextual_input[i + 1] and "ngày" not in contextual_input[i + 1])
                        or "/" in contextual_input[i + 1]
                    ):
                        # Kiểm tra bên llm điền có tháng, năm --> tăng index filled lên, cũng như loại trong LLM_contextual_to_tagname
                        try:
                            if f"{label_input[i][:-1]}_month]" in label_llm[index_filled]:
                                index_filled += 2
                        except:
                            pass
                        label_input[i + 2] = f"{label_input[i][:-1]}_year]"
                        label_input[i + 1] = f"{label_input[i][:-1]}_month]"
                        label_input[i] = f"{label_input[i][:-1]}_day]"

                # TH2: có _date
                pattern_date = re.compile(r"_date\]$")
                if (
                    pattern_date.search(label_input[i])
                    and i < len(contextual_input) - 1
                ):
                    # Kiểm tra có tháng, năm phía sau không (nếu có thì biến đổi thành day, month, year), nếu không thì giữ nguyên
                    if (
                        ("tháng" in contextual_input[i + 1] and "ngày" not in contextual_input[i + 1])
                        or "/" in contextual_input[i + 1]
                    ):
                        prefix_date = label_input[i].split("_date", 1)[0]
                        try:
                            if f"{prefix_date}_month]" in label_llm[index_filled]:
                                index_filled += 2
                        except:
                            pass
                        label_input[i + 2] = f"{prefix_date}_year]"
                        label_input[i + 1] = f"{prefix_date}_month]"
                        label_input[i] = f"{prefix_date}_day]"

                # Th3: có _day
                pattern_day = re.compile(r"_day\]$")
                if pattern_day.search(label_input[i]) and i < len(contextual_input) - 1:
                    # Kiểm tra có tháng, năm phía sau không (nếu không thì biến đổi thành date), nếu có thì giữ nguyên
                    if (
                        "tháng" not in contextual_input[i + 1]
                        and "/" not in contextual_input[i + 1]
                    ):
                        prefix_day = label_input[i].split("_day", 1)[0]
                        label_input[i] = f"{prefix_day}_date]"
            except:
                break

        return label_input

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

    # Overall function input form_llm_filled, input_form --> output filled_form
    def fill_input_by_llm_form(self, form_llm_filled, input_form):
        # Fix place, day, month, year format
        form_llm_filled = self.process_declaration_date_and_place(form_llm_filled)
        # Get contextual
        contextual_llm, label_llm = self.get_contextual_tagnames(form_llm_filled)
        contextual_input, label_input = self.get_contextual_tagnames(input_form)
        # List tagname
        tagname_for_input = self.get_tagnames_from_LLM_filled_form(
            contextual_llm, label_llm, contextual_input, label_input
        )
        # Fill
        filled_form = self.fill_tagname_to_form(tagname_for_input, input_form)
        filled_form = self.process_declaration_date_and_place(filled_form)
        return filled_form

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
                transformed_text = re.sub(r'\[.*?\]', '..........', form_text)
                self.Save_txt_file(input_path, transformed_text)
                print(f"Save successfully file {filename} at index {index} at {input_path}")


Temp = None

