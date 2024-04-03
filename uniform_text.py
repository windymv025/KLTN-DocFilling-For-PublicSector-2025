import re

#Write min function
def min(a, b):
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

def generate_uniform(Question):
    # Initialize a counter for numbering the placeholders
    placeholder_counter = 1

    type1 = ".."
    type2 = "…"
    first_index = min(Question.find(type1), Question.find(type2))
    # Loop through the question and replace the placeholders with the numbered placeholders
    while first_index != -1:
        # Replace the first occurrence of the placeholder with the formatted numbered placeholder
        Question = Question[:first_index] + "(Blank" + str(placeholder_counter) + ")" + Question[first_index:]
        #Index }
        start_index = first_index+2+(len(str(placeholder_counter)))+5
        end_index = start_index
        # Increment the counter
        placeholder_counter += 1

        while (end_index < (len(Question))) and (Question[end_index] == "…" or Question[end_index] == "."):
            end_index  += 1

        if (end_index+1 < (len(Question))) and (Question[end_index] == "\n") and (Question[end_index+1] == "…" or Question[end_index+1] == "."):
            end_index  += 1

        while (end_index < (len(Question))) and (Question[end_index] == "…" or Question[end_index] == "."):
            end_index  += 1
        if end_index == 212:
            a = 2+3
        try:
            Question = Question[:start_index] + Question[end_index:]
        except:
            Question = Question[:start_index]

        # Find the indices of the next placeholders
        first_index = min(Question.find(type1), Question.find(type2))

    return Question


def fill_form(data, form):
    data_dict = dict(re.findall(r'\(Blank(\d+)\): (.+)', data))
    def replace(match):
        blank_number = match.group(1)
        return data_dict.get(blank_number, '')

    form = re.sub(r'\(Blank(\d+)\)', replace, form)
    return form
