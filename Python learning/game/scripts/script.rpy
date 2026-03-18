
define s1 = Character("AI程序員")
define s2 = Character("AI助手")

image images:
    "images/images.png"
    zoom 5.0
    xanchor 0.5# 錨點位置
    yanchor 0.75
    xpos 960
    ypos 1080
image images1:
    "images/images1.png"
    zoom 5.0
    xanchor 0.5 #錨點位置
    yanchor 0.75
    xpos 960
    ypos 1080
image Logo:
    "images/Logo.png"
    zoom 4.0

default flag = 0

label splashscreen:
    play music "audio/music.ogg" fadein 1.0 #fadein 是淡入的時間，單位是秒
    scene Logo
    with dissolve
    hide Logo
    with dissolve

label start:

    # $ flag = 1
    # "flag : [flag][使用者名稱]"


    # 覆蓋圖像 scene 
    show images
    with fade
    s1 "你好，我是AI程序員，{b}歡迎{/b}來到我的世界！"
    s1 "在這裡，我將帶領你進入一個充滿創造力和想像力的旅程。"
    # show img1 as img1_left:        as 是一個複製圖像的語法
    #  xpos 500

    
        # 音樂會在這裡開始播放
    scene images1
    with dissolve
    s2 "你好，我是ai助手，我會幫助你解決問題，提供建議，並陪伴你度過每一天！"
    s2 "無論你遇到什麼困難，我都會在這裡支持你，讓我們一起創造美好的未來！"
    show images:
        xpos 500
    show images1:
        xpos 1920-500

    
    # voice "audio/voice.mp3" #不需要加play
   
    menu:
        "你想和誰聊天？"
        "AI程序員":
            $ flag =1 
        "AI助手":
            jump end  #可以利用jump來跳轉到另一個標籤，這裡是end標籤
    stop music
    "結束"

    if flag == 1:
        "你選擇了與AI程序員同行，開啟了程式設計的旅程"
        stop music
    return

label end:
    "然而...過度依賴的結果，是你被AI助手所支配了"
    stop music
    return 

