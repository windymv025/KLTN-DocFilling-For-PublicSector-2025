import google.generativeai as genai
import constant_value as CONST
import re
import os

class LLM_Gemini:
    def __init__(self, api_key):
        # Set up the model  
        genai.configure(api_key=api_key)
        generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 8291,
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        #Model
        self.model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
        
    def print_hello(self):
        print("Hello")

class MultiValueDict:
    def __init__(self):
        self.data = {}

    def add(self, key, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)

    def get_and_pop(self, key):
        if key in self.data and self.data[key]:
            return self.data[key].pop(0)
        raise ValueError(f"Key not in dictionary")    

class Text_Processing:
    def __init__(self):
        pass
    def min_uniform(self,a, b):
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

    def generate_uniform(self,Question):
        # Chuyển tất cả các dạng ......(number).... về dạng ..........(number)
        Question = Question.replace('…','..')
        # print(new_form)
        Question = re.sub(r'\.{2,}\((\d+)\)\.{2,}', r'............(\1)', Question)
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
            Question = Question[:first_index] + "(Blank" + str(placeholder_counter) + ")" + Question[first_index:]
            #Index }
            start_index = first_index+2+(len(str(placeholder_counter)))+5
            end_index = start_index
            # Increment the counter
            placeholder_counter += 1

            #Kiểm tra trên hàng đó còn . tiếp hoặc … đó hay không --> vẫn là chỗ điền này.
            while (end_index < (len(Question))) and (Question[end_index] == "…" or Question[end_index] == "."):
                end_index  += 1

            # if (end_index+1 < (len(Question))) and (Question[end_index] == "\n") and (Question[end_index+1] == "…" or Question[end_index+1] == "."):
            #     end_index  += 1
            #Kiểm tra trường hợp xuống hàng vẫn còn ....
            while (end_index+1 < (len(Question))) and (Question[end_index] == "\n"):
              while (Question[end_index+1] == "…" or Question[end_index+1] == "."):
                end_index  += 1
              if Question[end_index+1] == "\n":
                end_index += 1
                continue
              if (Question[end_index+1] != "…" and Question[end_index+1] != "."):
                break

            #Đã Hàng mới (Đã xuống hàng mà vẫn là chỗ điền thì cả cái hàng là của nó luôn)
            while end_index < len(Question) and Question[end_index] == "\n":
              # Kiểm tra hàng sau
              next_line_start = end_index + 1
              next_line_end = Question.find("\n", next_line_start)
              if next_line_end == -1:  # Nếu không có dấu xuống dòng tiếp theo, chỉ đến cuối văn bản
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
            with open(file_path, 'r',encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
            return None
    
    def Save_txt_file(self, file_path, text):
        #Delete all before create
        if os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        # Write content to the file
        try:
            with open(file_path, 'w',encoding='utf-8') as file:
                file.write(text)
            # print(f"File written successfully to '{file_path}'.")
        except Exception as e:
            print(f"An error occurred while writing the file: {e}")

    ## Summary tagnames (return list of N tagnames to check)
    def Summary_tagnames(self):
        modified_cccd_tagnames = [
            f"user0_{tagname.strip('[]')}" for tagname in CONST.list_cccd_passport_tagnames
        ]
        modified_general_tagnames = [
            f"{tagname.strip('[]')}" for tagname in CONST.list_general_tagnames
        ]
        our_N_tagnames = modified_cccd_tagnames + modified_general_tagnames
        return our_N_tagnames

    ## Some functions to from LLM filled form --> pass tagname to input form
    # Function to process a place, date, month, year format
    def process_declaration_date_and_place(self, form_text):  
        '''
        - Hàm để đưa chỗ điền ....., ngày.... tháng.... năm về đúng format [place], ngày [day] tháng [month] năm [year]
        - Vì chỗ điền này thì đặc trưng, nên có thể xử lý thẳng điểm đặc biệt này.
        '''
        # Define the regex pattern to match the specific date format with optional spaces
        # Cái re này tui chưa rõ nha, tương lai có thể thay thế
        date_pattern = re.compile(r'\s*\[[#a-zA-Z0-9_]+?\]\s*,\s*ngày\s*\[.+?\]\s*tháng\s*\[.+?\]\s*năm\s*\[.+?\]')
        # Define the replacement format
        replacement_format = '[place], ngày [day] tháng [month] năm [year]'
        # Use sub to replace matched dates with the correct format
        fixed_text = date_pattern.sub(replacement_format, form_text)
        
        return fixed_text
    
    def get_contextual_tagnames(self, data_form):
        '''
        Hàm để lấy các nội dung trước các tagnames (ngữ cảnh), nhằm so sánh giữa LLM fillied form và input --> từ đó xác định chỗ điền phù hợp.
        Input: 
        - form: form điền vào (các ... được thay bằng #another)
        Output:
        - Mảng, phần tử là nội dung trước tagnames
        - Ví dụ: ['chỗ', 'ở', 'hiện', 'nay']
        Cách làm:
        Đầu tiên, với form đưa vào, ta bắt các vị trí có [tagname] (chú ý [^\d] vì có một số chỗ [01] là sai (form y tế), 
        từ đó ta lấy được text trước tagnames + tagname.
        Sau đó, với mỗi cặp bắt được, ta chuẩn hóa nội dung trước chỗ điền
        Chuẩn hóa.
        - Lowercase, bỏ hết ký tự đặc biệt (.,:!)... chỉ để lại chữ, số và dấu / (vì chỗ ngày/tháng/năm) có mỗi / làm cách giữa hai tagnames.
        - Chỗ /tháng hay /năm có thể dính vào nhau --> thêm khoảng cách vào để split.
        - Sau khi xong, ta strip() bỏ khoảng cách trống, sau đó split theo space (khoảng trắng).  
        '''
        form = data_form
        # Bắt các vị trí text trước tagname + tagname
        pattern = re.compile(r'(.*?)(\[[^\d].+?\])', re.DOTALL)
        matches = pattern.findall(form)
        # Collecting the sentences
        sentences = []
        labels = []
        for match in matches:
            sentence = match[0].strip()  # Get the text before ".........."
            labels.append(match[1])
            # chuẩn hóa
            sentence = sentence.lower()
            sentence = re.sub(r'[^\w\s\/]', '', sentence)
            sentence = re.sub(r'\/(thang|tháng|nam|năm)', r' / \1', sentence)
            sentence = sentence.strip().split()

            # Thêm vào sentences
            sentences.append(sentence)
        return sentences, labels
    
    def get_hash_name_from_context_at_index(self,context,i):
        if len(context[i])==0:
            return "Empty"
        else:
            # return f"{context[i][0]}_{context[i][-1]}_{len(context[i])}"
            return f"{context[i][-1]}" # chỉ lấy chữ cuối
        
    def get_hash_name_from_context(self,context,i1,i2):
        '''
        Hàm này đơn giản tạo một chuỗi là key của dict, hiện tại, sẽ lấy context[0]_context[-1]_len(context)
        Tức sử dụng chữ đầu - chữ cuối - chuỗi
        Tiền tố 1: sử dụng context[i] context[i+1]
        Tiền tố 2: sử dụng context[i] context[i-1]

        Output: tên (key) cho LLM_contextual_to_tagname
        '''
        name_i1 = self.get_hash_name_from_context_at_index(context,i1)
        name_i2 = self.get_hash_name_from_context_at_index(context,i2)
        if i2>i1:
            name = f"1-{name_i1}-{name_i2}"
        elif i2<i1:
            name = f"2-{name_i1}-{name_i2}"
        return name

    def get_tagnames_from_LLM_filled_form(self,contextual_llm, label_llm, contextual_input, label_input):
        '''
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
        '''
        LLM_contextual_to_tagname = MultiValueDict()
        # Lấy tagname từ LLM filled form
        for i in range(len(contextual_llm)):
            if i ==0:
                hash_name = self.get_hash_name_from_context(contextual_llm,i,i+1)
                LLM_contextual_to_tagname.add(hash_name, label_llm[i])
            elif i == len(contextual_llm)-1:
                hash_name = self.get_hash_name_from_context(contextual_llm,i,i-1)
                LLM_contextual_to_tagname.add(hash_name, label_llm[i])
            else:
                hash_name1 = self.get_hash_name_from_context(contextual_llm,i,i-1)
                hash_name2 = self.get_hash_name_from_context(contextual_llm,i,i+1)
                LLM_contextual_to_tagname.add(hash_name1, label_llm[i])
                LLM_contextual_to_tagname.add(hash_name2, label_llm[i])
        # return LLM_contextual_to_tagname
        # Từ dữ liệu LLM filled, điền vào input form (Lưu các tagname vào list)
        for i in range(len(contextual_input)):
            T = False
            if i ==0:
                hash_name = self.get_hash_name_from_context(contextual_input,i,i+1)
                try:
                    label_input[i] = LLM_contextual_to_tagname.get_and_pop(hash_name)
                    T = True
                except:
                    pass
                
            elif i == len(contextual_input)-1:
                hash_name = self.get_hash_name_from_context(contextual_input,i,i-1)
                try:
                    label_input[i] = LLM_contextual_to_tagname.get_and_pop(hash_name)
                    T = True
                except:
                    pass
            else:
                hash_name1 = self.get_hash_name_from_context(contextual_input,i,i-1)
                hash_name2 = self.get_hash_name_from_context(contextual_input,i,i+1)
                try:
                    label_input[i] = LLM_contextual_to_tagname.get_and_pop(hash_name1)
                    T = True
                except:
                    pass
                try:
                    label_input[i] = LLM_contextual_to_tagname.get_and_pop(hash_name2)
                    T = True
                except:
                    pass
            if not T:
                continue
            # Xử lý với tagname dob, date,..
            # TH1: Là dob
            try:
                pattern_dob = re.compile(r'_dob\]$')
                if pattern_dob.search(label_input[i]) and i<len(contextual_input)-1:
                    # Kiểm tra có tháng, năm phía sau không (nếu có thì biến đổi thành day, month, year), nếu không thì giữ nguyên
                    if "tháng" in contextual_input[i+1] or "/" in contextual_input[i+1]:
                        label_input[i] =f"{label_input[i][:-1]}_day]"
                        label_input[i+1] =f"{label_input[i][:-1]}_month]"
                        label_input[i+2] =f"{label_input[i][:-1]}_year]"  
                        
                # TH2: có _date
                pattern_date = re.compile(r'_date\]$')
                if pattern_date.search(label_input[i]) and i<len(contextual_input)-1:
                    # Kiểm tra có tháng, năm phía sau không (nếu có thì biến đổi thành day, month, year), nếu không thì giữ nguyên
                    if "tháng" in contextual_input[i+1] or "/" in contextual_input[i+1]:
                        prefix_date = label_input[i].split("_date",1)[0]
                        label_input[i] =f"{prefix_date}_day]"
                        label_input[i+1] =f"{prefix_date}_month]"
                        label_input[i+2] =f"{prefix_date}_year]"
                        
                # Th3: có _day
                pattern_day = re.compile(r'_day\]$')
                if pattern_day.search(label_input[i]) and i<len(contextual_input)-1:
                    # Kiểm tra có tháng, năm phía sau không (nếu không thì biến đổi thành date), nếu có thì giữ nguyên
                    if "tháng" not in contextual_input[i+1] and "/" not in contextual_input[i+1]:
                        prefix_day = label_input[i].split("_day",1)[0]
                        label_input[i] =f"{prefix_day}_date]"
            except:
                break

        return label_input

    # Sau đó đơn giản tạo hàm đưa label vào input form
    def fill_tagname_to_form(self,list_tag_name, form):
        '''
        Từ list_tag_name, và form
        Điền list_tag_name này vào form (input với .....)
        Cần check nếu len(list_tag_name) = với số lượng ..... cần điền.
        '''
        # Ensure the length matches the number of placeholders
        num_placeholders = form.count('[#another]')
        # print(num_placeholders)
        if len(list_tag_name) != num_placeholders:
            raise ValueError(f"Mismatch: Found {num_placeholders} placeholders, but {len(list_tag_name)} tagnames were provided.")
        
        # Replace each occurrence of [#another] with the corresponding tagname
        for tag in list_tag_name:
            form = form.replace('[#another]', f'{tag}', 1)
        
        return form    

    # Overall function input form_llm_filled, input_form --> output filled_form
    def fill_input_by_llm_form(self, form_llm_filled, input_form):
        # Fix place, day, month, year format
        form_llm_filled = self.process_declaration_date_and_place(form_llm_filled)
        # Get contextual
        contextual_llm, label_llm = self.get_contextual_tagnames(form_llm_filled)
        contextual_input, label_input = self.get_contextual_tagnames(input_form)
        # List tagname
        tagname_for_input = self.get_tagnames_from_LLM_filled_form(contextual_llm, label_llm, contextual_input, label_input)
        # Fill
        filled_form = self.fill_tagname_to_form(tagname_for_input, input_form)
        filled_form = self.process_declaration_date_and_place(filled_form)
        return filled_form

    # 2. Remove different tagnames
    def remove_invalid_tagnames(self, form_text, valid_tagnames_general, valid_tagnames_cccd_passport):
        
        # Regular expression to match all tagnames (e.g., [user1_full_name], [place], etc.)
        tagname_pattern = re.compile(r'\[[^\d].*?\]')

        # Function to replace invalid tagnames
        def replace_invalid_tagname(match):
            tagname = match.group(0)

            # Check if the tagname is a general tagname (direct match)
            if tagname in valid_tagnames_general:
                return tagname  # Keep general tagnames unchanged

            # Check if the tagname is a valid cccd/passport tagname with userX_ prefix (e.g., [user1_full_name])
            for valid_tagname in valid_tagnames_cccd_passport:
                if re.match(r'\[user\d+_' + re.escape(valid_tagname[1:-1]) + r'\]', tagname):
                    return tagname  # Keep valid userX_ prefixed tagnames

            # If the tagname is not in the valid lists, remove it
            return ".........."

        # Process the form by replacing invalid tagnames
        cleaned_form = re.sub(tagname_pattern, replace_invalid_tagname, form_text)

        return cleaned_form

    def remove_different_tagnames(self, form):
        valid_tagnames_cccd_passport = CONST.list_cccd_passport_tagnames
        valid_tagnames_general = CONST.list_general_tagnames
        cleaned_form = self.remove_invalid_tagnames(form, valid_tagnames_general, valid_tagnames_cccd_passport)
        return cleaned_form
# Class này để sau
# class Form_With_Tagname:
#     def __init__(self):
#         pass



