# 範例：字串與數字相加會出錯，需要先轉型（已完成，供參考）
def show_age(age):
    # return "年齡："+ age     #利用str 才能使age相加字串
    return "年齡："+ str(age)    

print(show_age(15))