# ===== Take  tagname =====
'''
Mục đích, lấy danh sách tagname theo loại mong muốn dạng dictionary.
Ví dụ: 
"[full_name]": " Họ và tên của người dùng.",
"[alias_name]": " Tên gọi khác của người dùng.",
"[dob_day]": " Ngày sinh của người dùng.",
'''

from Config.tagnames import residence_identification_tagnames, study_tagnames, health_and_medical_tagnames, vehicle_driver_tagnames, job_tagnames

list_tagnames = [residence_identification_tagnames, study_tagnames, health_and_medical_tagnames, vehicle_driver_tagnames, job_tagnames]
type_forms = [
'1. Cư trú và giấy tờ tùy thân',
'2. Giáo dục',
'3. Y tế và sức khỏe',
'4. Phương tiện và lái xe',
'5. Việc làm',
'6. Khác'
]

def get_tagnames(type_index:int):
    '''
    Lấy danh sách theo type_index:
    '1. Cư trú và giấy tờ tùy thân',
    '2. Giáo dục',
    '3. Y tế và sức khỏe',
    '4. Phương tiện và lái xe',
    '5. Việc làm',
    '6. Khác'
    Output:
    Dictnary: {tagname: description}
    '''
    tagnames = {}
    print(list_tagnames[type_index])
    list_tagname =  list_tagnames[type_index]
    split_tagname = list_tagname.split("\n")[1:-1]
    # print(split_tagname)
    # print()
    for tagname in split_tagname:
        key, value = tagname.split(":")[0], tagname.split(":")[1]
        if key not in tagnames:
            tagnames[key] = value
    return tagnames

def get_all_tagnames():
    '''
    Lấy tất cả danh sách tagname (là tổng hợp các loại trên, xóa bỏ trùng lặp)
    Output:
    Dictnary: {tagname: description}
    ''' 
    tagnames = {}
    for list_tagname in list_tagnames:
        split_tagname = list_tagname.split("\n")[1:-1]
        # print()
        # print(split_tagname)
        # print()
        for tagname in split_tagname:
            # print(tagname.split(":")[0])
            key, value = tagname.split(":")[0], tagname.split(":")[1]
            if key not in tagnames:
                tagnames[key] = value
    return tagnames

