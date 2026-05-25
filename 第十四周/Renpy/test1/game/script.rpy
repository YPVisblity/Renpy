# 遊戲腳本位於此檔案。

# 宣告該遊戲使用的角色。 color 參數
# 為角色的名稱著色。

define s = Character("shark",what_size=30,who_size=40,who_color="#ffcce0", who_outlines=[(4,"fff",0,0)],what_prefix="《",what_suffix="》",image="shark") 
image side shark ="images/Shark.jpg"
image side shark b = "images/SharkB.png"
image side shark c = "images/SharkC.jpg"

image shark ="images/Shark.jpg"
image shark b = "images/SharkB.png"
image shark c = "images/SharkC.jpg"



# 遊戲從這裡開始。

label start:
    scene black
    show shark:
        parallel:
            xalign 0.0
            linear 1.3 xalign 1.0
            linear 1.3 xalign 0.0
            repeat
        parallel:
            yalign 0.0
            linear 1.3 yalign 1.0
            linear 1.3 yalign 0.0
            repeat
    s b"我是b表情的鯊魚"
    s c"我是c表情的鯊魚"
    

    return
