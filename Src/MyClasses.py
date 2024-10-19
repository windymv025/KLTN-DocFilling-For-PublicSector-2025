import google.generativeai as genai
import constant_value as CONST
import re

def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

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
        
    def blank_to_tagnames(self, text_with_blank, tagnames):
        """
        text_with_blank: form with (Blank_x)....
        tagnames: list of tag names
        return: list of tagnames coressponding to the blanks
        """
        #Get response
        prompt_parts = CONST.template_blank_to_tagname.format(tag_names=tagnames, Abstract = text_with_blank)
        response = self.model.generate_content(prompt_parts)
        response = response.text
        #Handle response
        try:
            response = re.search(r'Answer:(.*)', response, re.DOTALL).group(1).strip()
        except:
            pass
        list_tag_names = []
        pattern1 = r'Blank\d+:'
        pattern2 = r':\s*(.*)'

        blank_to_tagnames = {}

        matches1 = re.findall(pattern1, response)
        matches2 = re.findall(pattern2, response)
        for match1,match2 in zip(matches1, matches2):
            temp1 = match1.replace(":","").strip()
            temp2 = match2.replace("]","").strip()
            
            blank_to_tagnames[temp1] = temp2
            
        return blank_to_tagnames  

    def translate_tag_names(self, list_tag_names, translations):
        """
        Convert from list_tag_names into values
        Example: #Full_name --> Họ và tên
        list_tag_names: list of tag names
        translations: dictionary of translations
        """
        list_value_keys = [] #
        pattern = r'#(\w+)'
        for tag_name in list_tag_names:
            match = re.search(pattern, tag_name)
            temp = match.group(0)
            list_value_keys.append(translations[temp])
            temp = temp.replace("#","")
        return list_value_keys
    
    def auto_blank_to_tagname(self, text_with_blank):
        """
        text_with_blank: form with (Blank_x)....
        return: list of tagnames coressponding to the blanks (llm auto generate)
        """
        prompt_parts = CONST.template_llm_auto_blanks_to_tagnames.format(Abstract = text_with_blank)
        response = self.model.generate_content(prompt_parts)
        # print(response)
        return response.text

    def extract_content(self, Abstract, list_value_keys):
        #Convert Question to right format
        Question = """"""
        for item in list_value_keys:
            Question += item + "\n"
        #Get response
        prompt_parts = CONST.template_extract_content.format(Abstract = Abstract, Question = Question)
        response = self.model.generate_content(prompt_parts)
        response = response.text

        #Handle this response
        pattern1 = r'\[(.*?)\s*:'
        pattern2 = r':\s*(.*)'

        value_keys_to_context_value = {}
        try:
            response = re.search(r'Answer:(.*)', response, re.DOTALL).group(1).strip()
        except:
            pass

        matches1 = re.findall(pattern1, response)
        matches2 = re.findall(pattern2, response)
        for match1,match2 in zip(matches1, matches2):
            temp1 = match1.replace(":","").strip()
            temp2 = match2.replace("]","").strip()
            if temp1 not in value_keys_to_context_value:
                value_keys_to_context_value[temp1] = []  # Initialize list for the key if it doesn't exist
            value_keys_to_context_value[temp1].append(temp2)

        return value_keys_to_context_value
    
    def generate_user_tagname_from_blankX_form(self, Abstract):
        prompt_parts = CONST.form_tagging_prompt.format(Abstract = Abstract)
        # print(prompt_parts)
        response = self.model.generate_content(prompt_parts)
        # print(response.text)
        return response.text
    
    def generate_tagname_cccd_passport(self,form,cccd_passport_tagnames=CONST.cccd_passport_tagnames,general_tagnames=CONST.general_tagnames):
        prompt_parts = CONST.template_generate_id_passport.format(cccd_passport_tagnames=cccd_passport_tagnames,general_tagnames=general_tagnames,form = form)
        # print("prompt parts:", prompt_parts)
        response = self.model.generate_content(prompt_parts)
        return response.text
    
    def mapping_tagname(self,input_form,output_form,request):
        prompt_parts = CONST.mapping_prompt.format(input_form = input_form,output_form = output_form,request = request)
        response = self.model.generate_content(prompt_parts)
        return response.text

    
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
    
    def getMissItem(self, value_keys_to_context_value, translations, list_values):
        list_miss_items= []
        list_miss_keys = [] # Dùng cho database
        list_index = [] # Chứa index của miss item tại list_info, dùng để thay thế list_info sau khi query
        for i, value in enumerate(list_values):
            info = value_keys_to_context_value[value]
            if value == 'Trống' or "#Empty" == info[0]: # tag_name không tồn tại
                list_index.append(i)
                list_miss_items.append(value)
                list_miss_keys.append(find_key_by_value(translations, value))
            value_keys_to_context_value[value].pop(0)
        return list_miss_items, list_miss_keys, list_index
    
    
    def getlistInfo(self, value_keys_to_context_value, list_values):
        listInfo = []
        count = 0
        for value in list_values:
            if value != 'Trống':
                listInfo.append(value_keys_to_context_value[value][0])
            else:
                listInfo.append(value_keys_to_context_value[value][count])
                count += 1

        return listInfo

    def create_tag_info_dict(self, id, list_tag_names, list_info):
        data_to_insert = {"ID": id}
        for i, tag in enumerate(list_tag_names):
            tag = tag.replace("#","")
            data_to_insert[tag] = list_info[i]
        return data_to_insert

    def fill_form(self,blanked_text, list_info):
        """
        From values, and blanked form
        Fill value into this blank
        """
        for i in range(1,len(list_info)+1):
            blanked_text = blanked_text.replace(f"(Blank{i})", list_info[i-1])
        return blanked_text




#

