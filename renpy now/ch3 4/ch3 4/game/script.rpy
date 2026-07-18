#序章:(這裡主要描述為何需要去修復機器，以及你所扮演的角色)
#角色定義
define p = Character("你", color="#00FFCC")           # 玩家（工程師）
define aria = Character("ARIA", color="#FF9FE5")       # AI 助手（鷹架式引導）
define sys = Character("NEXUS-9", color="#FF4444")     # 系統警報音
define boss = Character("老闆", color="#FFD700")     # 遠端連線的上司

#初始值設定
default aria_trust = 0
default score =0
label start:
    #scene server_room with fade

    "昏暗的企業伺服器機房。冷白燈光打在密密麻麻的機架上，警示燈不停閃爍紅光。"
    scene red server room
    show boss talk:
        xalign 0.5
        ease 0.5 zoom 1.4

    boss "喂，你聽得到嗎？NEXUS-9 的核心系統在三小時前開始異常，我們部署的Python專案陸續發生邏輯錯誤，導致崩潰。"
    boss "那些AI自動生成的程式碼產生了未知的錯誤，把系統鎖死成了好幾個獨立的數據密室。"
    hide boss talk
    show prelude1 with dissolve:
        xalign 0.5
        yalign 0.3
        zoom 1.5
    boss "你是我們最後一張牌。進去把他修好。"
    hide prelude1
    show boss awkward:
        xalign 0.5
        zoom 1.4

    p "我一個人？"

    boss "不是。系統裡有一個AI協作模組，代號ARIA。它會在旁邊提供測試回饋和除錯線索，但最終動手的還是你。"
    boss "時限六小時。開始吧。"

    hide boss awkward

    # sfx:sfx_boot（傳送音效） 
    #scene nexus_core with dissolve  #傳送進空間的畫面

    "意識被拉進虛擬空間。眼前是無盡延伸的數據走廊，地板是半透明的程式碼流。"
    scene virtual space
    
    show prelude2closeeyes with dissolve:
        xalign 0.5
        yalign 0.3
        zoom 1.5

    pause(1.0)
    
    show prelude2openeyes with dissolve:
        xalign 0.5
        yalign 0.3
        zoom 1.5
    
    pause(2.0)

    #show aria  at center #AI助手
    hide prelude2closeeyes
    hide prelude2openeyes
    show aria talk:
        zoom 1.2
        right
    aria "連線確認。你好，工程師。我是ARIA，你的協作模組。"


    aria "NEXUS-9 有多個Python專案的執行環境遭到封鎖。每一個異常的專案，都形成了一個無法通行的密室，我會陪你逐一排除。"
    aria "準備好了嗎？"

    menu:
        "準備好了。":
            $ aria_trust += 1
            show aria talk:
                zoom 1.2
                right
            aria "很好。第一間密室是基礎環境與語法測試，跟我來。"
            hide aria talk
            show aria leave:
                xalign 0.6
                zoom 1.2
            show aria leave:
                xalign 0.6
                yalign 5.0
            with move
                
        "等一下，這裡是哪？":

            show aria talk:
                zoom 1.2
                right
            aria "虛擬伺服器核心空間。你的意識已經數位化。別太緊張，你不會真的死在這裡的。"
            aria "大概不會。"
            hide aria talk

    jump chapter1_1

#1-1 Python 基礎 (100%AI幫助)(選擇題)主要教導int、print這些基礎語法。
label chapter1_1:

    pause(1.0)
    show aria default:
        zoom 1.2
        right
        yalign 5.0
    show aria default:
        right
        yalign 1.0
    with move
    aria "再進行修復程式碼前，您需要了解關於python的一些基本語法。"
    "可以宣告一個變數給予一個數值，像是 a=1，在python中不用像是其他語言一樣先宣告int or char"
    "利用print語法可以將其輸出在螢幕上。例如print(a)"

    show aria talk:
        zoom 1.2
        right

    aria "接下來就是你表現的時候了。"
    aria "首先，我們需要向核心提交合法的Python語法來解鎖。系統提供了三段啟動程式碼，但只有一個是正確的。"

    "畫面出現三個程式碼選項，像全息投影懸浮在空中。"

    show aria default:
        zoom 1.2
        right

    aria "線索提示：Python 用 # 做單行注釋，變數不需要宣告型別，print要加括號。"
    menu:
        "選項 A：\nx = 10\ny = 20\nprint(x + y)":
            $ score += 10
            $ aria_trust += 1

            show aria talk:
                zoom 1.2
                right
            aria "正確！這是標準的Python變數宣告與輸出。"
            hide aria talk
            "系統提示：PyBryt基礎測試通過，獲得碎片鑰匙。密室門發出金屬聲，緩緩開啟。"
            show aria default with Dissolve(0.5)
            aria "我們趕緊移動吧。"
            hide aria default
            jump chapter1_2

            
        "選項 B：\nint x = 10;\nint y = 20;\nprintf(\"%%d\", x+y);":
            aria "PyBryt測試失敗：SyntaxError。這比較像 C 語言，Python 不需要宣告型別，也不用分號結尾。"
            $ score = score - 15
            jump chapter1_1
          
            
        "選項 C：\nDIM x AS INTEGER = 10\nPRINT x + 20":
            $  score = score - 15
            aria "PyBryt測試失敗：SyntaxError。這是BASIC的語法。我們需要的是Python喔。"
            aria "記住：Python 直接寫 x = 10 就好，非常簡潔。"
            jump chapter1_1
#1-2 基本語法
    label chapter1_2:
        "走廊深處出現一個巨大的資料處理模組，像是一個透明的旋轉鼓輪，裡面的數字全是亂碼。通往下一區的閘門緊閉。"
        
        sys "【警報】資料處理模組邏輯異常。運算結果偏差300%%。"

        show aria default:
                zoom 1.2
                right
        aria "糟糕，這個模組負責病患排隊的資料計算。AI 生成了一段錯誤的折扣邏輯。"
        aria "我已經幫你定位出錯誤的程式碼片段，你來選出正確的修正方式，我們才能拿到下一把鑰匙。"

        "投影出現有Bug的程式碼："
        "total= 100\n discount = 20%%\n final=total-discount\n print(final)"

        show aria default:
            zoom 1.2
            right
        aria "線索提示：Python的%%是取餘數運算子，不是百分比。如果要計算20%%的折扣，你會怎麼寫？"

        menu:
            "修正為：discount = total * 0.20":
                $ score += 10
                $ aria_trust += 1
                show aria talk:
                    zoom 1.2
                    right
                aria  "完全正確！discount = total * 0.20 才是正確的百分比計算方式。"
                "系統提示：PyBryt邏輯測試通過。鼓輪停止轉動，數字重新排列整齊，閘門開啟。"
                hide aria talk
                jump chapter1_3

            "修正為：discount = 20":
                $  score = score -  15
                aria  "測試失敗：數值硬編碼 (Hardcoded)。這樣寫是固定折扣20元，不是20%%。如果 total變了，這個數字就不對了。"
                jump chapter1_2

            "修正為：discount = \"20%%\"":
                $  score = score -  15
                aria  "測試失敗：TypeError。這樣 discount 變成字串了，字串不能拿來跟整數做相減運算。"
                jump chapter1_2
#1-3 迴圈與資料結構
    label chapter1_3:
        "空間突然開始扭曲。走廊在眼前無限複製，像鏡中鏡一樣延伸，形成一個無法逃脫的迷宮。"

        sys "【警報】庫存管理密室陷入無限迴圈。CPU使用率99.9%%。"

        show aria talk:
            zoom 1.2
            right
        aria "這就是為什麼密室開始抖動……庫存系統陷入無限迴圈，它一直在重複執行卻沒有停止條件。"
        aria "你來判斷哪裡會造成無限迴圈，並選出最適合管理這個庫存資料的結構。"
        show aria default:
            zoom 1.2
            right

        "投影出現有問題的程式碼："
        "  i = 0\n  while i < 10:\n      print(i)\n  # 少了 i += 1"

        menu:
            "問題在：缺少 i += 1 讓計數器遞增":
                $ score += 5
                hide aria default
                show aria talk:
                    zoom 1.2
                    right
                aria  "對！沒有 i += 1，i 永遠是 0，條件永遠是 True，迴圈永遠不停。"
                hide aria talk
                jump ch1_3b
            "問題在：while應該改成for":
                $  score = score - 10
                aria  "這是一個解法，但不是引發無限迴圈的根本原因。看看i這個變數，它有在迴圈裡面被改變嗎？"
                jump chapter1_3
            "問題在：print(i) 應該移到迴圈外":
                $  score = score - 10
                aria  "這樣的話 i 根本不會被印出來。想想：迴圈什麼時候才會停下來？"
                jump chapter1_3

    label ch1_3b:
        show aria talk:
            zoom 1.2
            right
        aria "很好！現在，這個庫存系統需要頻繁地『新增』和『取出』資料。"
        aria "你會選哪種資料結構作為修復的基底？"
        show aria default:
            zoom 1.2
            right

        menu:
            "佇列（Queue）— 先進先出（FIFO）":
                $ score += 10
                $ aria_trust += 1

                hide aria default
                show aria talk:
                    zoom 1.2
                    right

                aria  "完美！佇列就是為了這種先進先出的場景設計的，非常適合庫存管理。"
                hide aria talk
                jump chapter1_clear

            "堆疊（Stack）— 後進先出（LIFO）":
                $  score = score -  15
                aria  "堆疊是後進先出。想像你在排隊買票，先排的人先買到——這是哪種結構？"
                jump ch1_3b

            "字典（Dict）— 鍵值對應":
                $  score = score -  15
                aria  "字典適合用『名稱』查找對應資料，但不擅長管理順序和進出。"
                jump ch1_3b

    label chapter1_clear:

        "走廊的扭曲消失，密室解鎖。一扇通往下層的電梯門緩緩開啟，發出藍色光暈。"

        show aria talk:
            zoom 1.2
            right
        aria  "累計總得分:[score] 分。\nLayer 1密室修復完成！你做得很好。"
        aria "接下來是 Layer 2，那裡的 AI 輔助會少一點，你需要由自己負責主要部份了。"

        show aria default:
            zoom 1.2
            right

        p "等一下——你說『少一點』？"

        show aria talk:
            zoom 1.2
            right
        aria  "我不能一直把答案塞到你手裡，否則你永遠無法對抗那些失控的AI程式碼。"
        aria  "準備迎接真正的Debug吧，加油。"
        hide aria talk
    
        jump chapter2_intro

#CHAPTER 2：Layer 2 — 應用區（80% 鷹架，有 Bug 需修正）
label chapter2_intro:
    "進入一個像辦公室的空間，但所有門都被紅色雷射網封鎖。電話不停響，卻沒人接聽。"

    sys "【警報】Layer 2 三個子系統異常。通信模組 Lag、日誌系統崩潰、情報爬蟲被封鎖。"
    
    show aria talk:
        zoom 1.2
        right
    aria  "這層的密室比較麻煩。我會給你有 Bug 的程式碼，你需要找出問題並修正。"
    aria "我還是會在旁邊提供錯誤訊息線索，但我不會直接把正確語法列出來了。"
    hide aria talk
    show aria default:
        zoom 1.2
        right

    # 2-1：函式與模組
    label chapter2_1:
        "一面巨大的白板上貼滿了重複的便利貼，每張都寫著幾乎一樣的程式碼。通訊室的門緊閉。"

        aria  "通信模組的程式碼，同樣的計算邏輯被 AI 複製貼上了七次。而且執行時會拋出 UnboundLocalError。"

        "投影出現有Bug的程式碼："
        "  total = 0\n\n  def add_score(points):\n      total += points\n      return total\n\n  add_score(10)"

        aria "這段程式試圖修改全域變數，但失敗了。你知道為什麼嗎？"

        menu:
            "global total 沒有宣告，函式內無法修改外部變數":
                $ score += 10
                $ aria_trust += 1

                hide aria default
                show aria talk:
                    zoom 1.2
                    right
                aria  "完全正確！Python 函式內若要修改外部變數，需要加上 global 宣告。"
                "白板上的便利貼一張張脫落，匯聚成一個整齊的函式模組。通訊室雷射網解除。"
                hide aria talk
                jump chapter2_2

            "函式名稱add_score需要改成addScore":
                $  score = score -  15
                aria  "命名不影響執行。問題在於變數的『作用域』(Scope)。"
                jump chapter2_1

            "return total 應該改成print(total)":
                $  score = score -  15
                aria  "return 是將值傳遞出去的正確做法。這不是造成錯誤的原因。"
                jump chapter2_1


    # 2-2：檔案與例外處理
    label chapter2_2:
        "資料中心的走廊，地板上散落著破碎的日誌檔碎片，像玻璃一樣發光。"

        sys "【警報】日誌系統崩潰。關鍵修復紀錄遺失 47 筆。"

        show aria talk:
            zoom 1.2
            right
        aria  "日誌系統在寫檔時，遇到權限不足就直接崩潰，完全沒有例外處理機制。"
        aria "我已經寫好了架構，但缺少容錯的機制。剩下交由你來補完。"

        "投影出現需要補完的程式碼："
        "  def write_log(filename, data):\n      f = open(filename, 'w')\n      f.write(data)\n      f.close()\n      print('寫入成功')"

        aria "如果 open 失敗，整個密室就會崩潰。你會怎麼改？"
        hide aria talk
        show aria default:
            zoom 1.2
            right

        menu:
            "用 try-except 包住 open 和 write，except 捕捉 Exception":
                $ score += 10
                $ aria_trust += 1

                hide aria default
                show aria talk:
                    zoom 1.2
                    right
                aria  "很好！try-except 可以讓程式在出錯時優雅地捕捉例外，而不是直接終止程式。"
                "地板上的碎片重新拼合，日誌檔一筆筆恢復完整。下一扇門開啟。"
                hide aria talk
                jump chapter2_2_1

            "在 open 前加上 if os.path.exists(filename)":
                $  score = score -  15
                aria  "這只能確認檔案存在，無法處理『權限不足』或『磁碟空間已滿』等無法預期的錯誤。"
                jump chapter2_2

            "加上 print('寫入失敗') 在最後":
                $  score = score -  15
                aria  "print 不能阻止程式崩潰，只是在崩潰前多說一句話而已。你需要控制流的結構。"
                jump chapter2_2

    # 2-2-1：額外章節
    label chapter2_2_1:
        "恭喜你，已經完成了檔案處理的問題了。"
        show aria talk:
            zoom 1.2
            right
        aria  "你想要額外的加分嗎?"
        

        hide aria talk
        show aria default:
            zoom 1.2
            right

        menu:
            "是":
                aria  "那就進行額外的關卡了唷。"
                aria  "不要害怕很簡單的。"
                hide aria talk
                jump chapter2_2_2

            "否":
                aria  "那就繼續進行下一關了唷。"

                jump chapter2_3

            
    # 2-2-2：額外章節的題目
label chapter2_2_2:
        show aria talk:
            zoom 1.2
            right
        aria  "恭喜你進入了額外的題目。"
        aria  "try: \n      a = input('輸入數字：') \n   print(a + 1) \n    except:  \n     print('發生錯誤') \n    print('hello')，這裡會出現什麼結果，請打出來。"
        hide aria talk
        show aria default:
            zoom 1.2
            right
        jump ch2_2_2_input

label ch2_2_2_input:
    python:
        ans_2_2_2 = renpy.input("請輸入正確的 Python 正確的輸入結果：（輸入半形符號即可）", default="").strip()

    if not ans_2_2_2:
        "系統" "編輯器未偵測到任何輸入，請輸入測試代碼！"
        jump ch2_2_2_input

    # 💡 嚴格驗證改良：利用 and 檢查三個關鍵字是否「都在」玩家輸入的內容中
    # 這樣不管學生用空格分開、逗號分開、還是打在一起，只要答案對了就給過！
    if ("輸入數字:1" in ans_2_2_2) and ("發生錯誤" in ans_2_2_2) and ("hello" in ans_2_2_2):
        $ score += 10
        $ aria_trust += 1
        show aria talk at right
        aria "恭喜答對了！"
        "【系統提示：日誌完整性驗證成功，順利導出正確異常紀錄。】" 
        jump chapter2_3

    else:
        show aria talk at right
        aria "不對喔，輸出的日誌內容或格式似乎有誤，請再想想！"
        jump ch2_2_2_input



    # ---- 2-3：網路爬蟲 ----
label chapter2_3:
        "牆壁上出現一個巨大的網路節點圖，其中 ETtoday 的入口閃爍著大大的 403 Forbidden 封鎖標誌。"

        show aria talk:
            zoom 1.2
            right
        aria  "為了獲取外部情報，系統需要爬取新聞。但 AI 寫的爬蟲一直被拒絕。"

        "【投影出現有問題的程式碼：】"
        "  import requests\n\n  response = requests.get('https://www.ettoday.net')\n  print(response.status_code)"

        aria "這段程式執行後會收到 403 Forbidden。你猜伺服器是怎麼識破我們是機器人的？"
        hide aria talk
        show aria default:
            zoom 1.2
            right

        menu:
            "缺少 User-Agent headers，伺服器拒絕非瀏覽器請求":
                $ score += 10
                $ aria_trust += 1

                hide aria default
                show aria talk:
                    zoom 1.2
                    right
                aria  "正確！沒有偽裝 User-Agent，伺服器一看就知道是 Python-requests 發出的請求。"
                "【403 封鎖標誌轉為綠色 200 OK，大量新聞標題開始流入系統。】"
                hide aria talk
                jump chapter2_clear

            "需要加上 time.sleep(1) 避免太頻繁":
                $  score = score -  15
                aria  "睡眠時間可以降低被封鎖的機率，但 403 是當下就被拒絕，不是因為太頻繁造成的 429 Too Many Requests。"
                jump chapter2_3

            "URL 需要加上 https://www. 才正確":
                $  score = score -  15
                aria  "URL 本身沒問題。問題在 HTTP Request Headers 裡面缺少了關鍵的身份證明。"
                jump chapter2_3

label chapter2_clear:
        "【CG：辦公室空間的紅色雷射網全數消失，螢幕一個個恢復正常顯示。】"

        show aria talk:
            zoom 1.2
            right
        aria  "累計總得分:[score] 分。\nLayer 2 密室修復完成。你的除錯直覺越來越敏銳了。"
        p "下一層呢？"

        aria  "Layer 3……我的輔助會降到 50%%。我只會幫你生出程式碼架構，但我不保證邏輯是對的。"
        aria "你必須運用『測試驅動』 的思維，自己找出漏洞。"
        hide aria talk
        show aria default:
            zoom 1.2
            right
        p "明白了。來吧。"
        hide aria default
        show aria leave:
            xalign 0.6
            zoom 1.2
        show aria leave:
            xalign 0.6
            yalign 5.0
        with move

        
        #jump chapter3_intro

label chapter3_intro:
    pause(1.0)
    show aria default:
        zoom 1.2
        right
        yalign 5.0
    show aria default:
        right
        yalign 1.0
    with move
    "進入公司12樓的投資分析辦公室,這裡留了一封內部郵件和權限受限制的AI助理,這時警報突然大響,主控台上出現了AI助理的聲音。"
    sys "【警報】警告!警告!投資數據和資料被駭客入侵了,趕快去分析辦公室處理。"
    aria "這裡會很麻煩。我會給你有Bug的程式碼,你需要找出問題並修正。"
        
    aria "從現在開始,我的AI 參與度降到 50%%。我只能幫你盲目產出 Code 構架,但我完全無法檢查邏輯對錯"
    hide aria talk
    show aria default:
        zoom 1.2
        right
    p "也就是說,你寫出來的東西可能是垃圾,我得自己寫測試去抓你的 Bug？"

    hide aria default
    show aria talk:
        zoom 1.2
        right
    aria "是的。你必須扮演『最嚴格的驗收官』,用測試驅動的思維來糾正我。我們第一個要救的是財務部!"
    hide aria talk
    jump chapter3_1
        
    # ==========================================
    # 3-1：Matplotlib 座標軸測試驗證
    # ==========================================
    label chapter3_1:
        "財務部辦公室。財務長(CFO)正對著筆電瘋狂敲擊鍵盤,臉色慘白。"
        boss "完蛋了!下半年的『全球投資分析儀表板』數據全亂了!Y 軸和 X 軸數據嚴重拉曲、甚至倒轉，高層差點做出賠上數百萬的錯誤決策!"
        aria "我試圖調用 Matplotlib 自動重新繪製圖表了……程式碼已經吐在全息螢幕上。"
        "全息投影浮現出 ARIA 自動生成的 Matplotlib 程式碼,但圖表的座標範圍(xlim)極度詭異。"
        aria "請你撰寫一段 Python 的『斷言測試 (Assertion)』來驗證圖表的 get_xlim() 是否回傳正確的區間 \[0, 100\]，以防錯誤圖表被導出。"
        
        # 全息投影顯示程式碼提示
        "【全息投影提示：請補完驗證測試碼】\ncurrent_xl = ax.get_xlim()\n_____(current_xl == [0, 100])"

        label ch3_1_input:
            python:
                # 讓玩家手動輸入測試關鍵字
                ans_3_1 = renpy.input("請輸入正確的 Python 測試斷言關鍵字（注意大小寫）：", default="").strip()

            if not ans_3_1:
                "系統" "編輯器未偵測到任何輸入，請輸入測試代碼！"
                jump ch3_1_input

            # 嚴格驗證：只接受 python 內建的 assert 關鍵字
            if ans_3_1 == "assert":
                $ score += 10
                $ aria_trust += 1
                show aria talk at right
                aria "測試通過！成功使用 assert 進行自動化邊界驗證！圖表的座標軸自動縮放回正常範圍，數據曲線變美觀了！"
                "【系統提示: 圖表正確性與美觀度評測達標。財務長的血壓降下來了。】" 
                jump chapter3_2
            else:
                $  score = score -  5
                show aria talk at right
                aria "驗收失敗！輸入錯誤或使用了無法自動化驗證的語法。財務長看不懂亂掉的趨勢！"
                "【系統提示：扣除 5 分！目前分數：[score]，繼續加油，你可以的！】"
                
                jump ch3_1_input

# ==========================================
    # 3-2：人資部影音完整性檢查
    # ==========================================
    label chapter3_2:
        "人資部(HR)辦公區。走廊上堆滿了新進員工的教育訓練資料。"
        boss "新進員工線上培訓一小時後就要開始!但影音伺服器中了病毒,影片庫的下載功能失效,有些檔案甚至變成了毀損的空白檔案!"
        aria "我已經用 Python 寫好了一套自動化下載與重組影音流的邏輯。Code 就在這裡。"
        p "你確定這套邏輯能載到完整的影片？"    
        aria "我不確定……我現在只管吐 Code,不管邏輯驗收。你需要撰寫測試案例來驗收我的程式碼。"
        aria "線索提示: 功能完整性的驗收,關鍵在於檢查下載後檔案的格式與檔案大小是否大於 0。我們會用到 os 模組下的路徑與大小檢查工具。"
        
        "【全息投影提示：請輸入正確的 os 函式來獲取檔案大小 (Bytes)】\nif os.path.______(video_path) > 0:\n    print('下載成功')"

        label ch3_2_input:
            python:
                # 測試學生是否知道獲取檔案大小的函式是 getsize
                ans_3_2 = renpy.input("請輸入正確的 os.path 內建子函式名稱：", default="").strip()

            if not ans_3_2:
                "系統" "編輯器未偵測到任何輸入，請輸入測試代碼！"
                jump ch3_2_input

            if ans_3_2 == "getsize" or ans_3_2 == "getsize()":
                # 防呆：如果學生加了括號，幫他過濾掉
                $ score += 10
                $ aria_trust += 1
                show aria talk at right
                aria "精準的測試!我的下載邏輯裡確實少判斷了未傳輸完成的情況。使用 getsize 成功攔截了 0 KB 的壞檔！影片庫功能完全恢復了!"
                "【系統提示: 功能完整性評測通過。新員工影音系統上線成功。】"
                jump chapter3_3
            else:
                $  score = score -  15
                show aria talk at right
                aria "測試漏洞！這個方法無法正確讀取檔案大小，畫面上流過了好多 0 KB 的毀損影片，人資部要暴走了！"
                "【系統提示：扣除 15 分！目前分數：[score]】"
                if score < 60:
                    "系統" "分數過低，系統邏輯鏈全面崩潰！"
                    
                jump ch3_2_input

    # ==========================================
    # 3-3：IoT 環控系統空值清洗
    # ==========================================
    label chapter3_3:
        "突然間,辦公室的冷氣發出劇烈運轉聲,溫度瞬間掉到 16 度,會議室的智慧燈光開始瘋狂閃爍。"
        sys "【警告】總務部智慧辦公室 IoT 環控系統暴走。數據讀取到大量空值。"
        aria "駭客切斷了感測器 API 的部分數據,導致系統一直讀到 None。我的程式碼沒有處理空值,直接把空值帶入計算,系統卡死了!"
        p "快把你的 API 接收 Code 丟出來,我來寫資料清洗測試!"
        
        "【全息投影提示：請輸入防呆判斷，當 data 為什麼時給予預設值 26 度？】\nif data is ____:\n    data = 26"

        label ch3_3_input:
            python:
                # 測試學生是否知道 Python 的空值型態是大寫的 None
                ans_3_3 = renpy.input("請填入 Python 的空值關鍵字（注意大小寫）：", default="").strip()

            if ans_3_3 == "None":
                $ score += 10
                $ aria_trust += 1
                show aria talk at right
                aria "完美清洗！環控系統成功跳過了駭客製造的空值陷阱，冷氣和燈光恢復正常了！"
                "【系統提示: API 接收正確性評測通過。Layer 3 數據密室全面解鎖!】"
                jump chapter3_clear

            elif ans_3_3.lower() == "null" or ans_3_3.lower() == "none":
                show aria talk at right
                aria "注意！Python 的空值宣告與 JavaScript 或 SQL 不同，且大小寫極為嚴格！請重新檢查。"
                jump ch3_3_input
            else:
                $  score = score -  15
                show aria talk at right
                aria "不行啊！錯誤的判斷式導致程式拋出 NameError 或 TypeError，系統陷入無限重啟！"
                "【系統提示：扣除 15 分！目前分數：[score]】"
                ##3if score < 60:
                ###    "系統" "分數過低，系統邏輯鏈全面崩潰！"
                ###    return
                jump ch3_3_input



label chapter3_clear:
        "成功修復辦公室的Debug了，資料數據慢慢恢復了。"

        aria "累計總得分:[score] 分。\nLayer 3密室修復完成！你越來越厲害了。"
        aria "接下來是 Layer 4，那裡的 AI 輔助會降至20%%~0%%，你需要由自己負責主要部份了。"

        p "等一下——你說『變少甚至沒有』？"

        aria "我的核心算力正被 Null-Void 強制剝離...這是我最後能維持的連線了。"
        aria "接下來的路...請相信你這幾層樓累積的直覺，加油。"
        "ARIA 的身影閃爍了一下，逐漸變得透明，虛擬空間的雜訊聲越來越大。"        
        jump chapter4_intro

label chapter4_intro:
        "整棟辦公大樓的燈光突然熄滅。幾秒後,紅色的應援燈緩緩亮起,四周的虛擬數據走廊開始崩解。"
        sys "【終極警報】Null-Void 發現防線被破,正在切斷 AI 助理的雲端算力!"
        aria "啊……我的核心連線……要被切斷了……"
        "ARIA 的身體開始變得半透明,全息投影斷斷續續,發出沙沙的雜訊聲。"
        aria "接下來的 Layer 4……多媒體應用……我的參與度將降到 20%% 甚至 0%%……我只能提供極少提示,甚至……甚至無法幫你寫任何一行 Code……"
        p "ARIA!撐住啊!"
        aria "相信……你自己的……應用能力……行銷部……OpenCV……"
        "【系統提示:AI 助理 ARIA 已斷線,進入離線託管狀態。接下來的關卡將由學生完全主導。】"
        jump chapter4_1




# ==========================================
    # 4-1：OpenCV 批次去雜訊
    # ==========================================
label chapter4_1:
        "行銷部辦公區。桌上散落著週一盛大發表會的企劃書,螢幕上的產品宣傳圖全部被駭客加上了厚重的條紋雜訊與惡意色偏。"
        boss "完蛋了,幾百張 KOL 合作素材和產品圖全毀了!AI 現在只在螢幕上吐出三個字:『OpenCV』,然後就完全死機了!"
        p "沒時間指望 AI 了。只能我自己寫自動化批次修復腳本了。"
        "畫面上是一片空白的編輯器，你必須在代碼開頭引入正確的 OpenCV 函式庫名稱。"
        
        "【編輯器提示】\nimport ________\nfor file in glob.glob('*.png'):\n    img = cv2.imread(file)..."

        label ch4_1_input:
            python:
                ans_4_1 = renpy.input("請輸入要 import 的 OpenCV 核心函式庫模組名稱：", default="").strip()

            if ans_4_1 == "cv2":
                $ score += 10
                "aria" "(系統自動日誌) 成功載入 cv2 模組！幾百張圖片在 5 秒內完成批次去雜訊與色彩通道修復，影像完美恢復！"
                "【系統提示: 處理效率與品質評測優良。成功拯救行銷部的發表會素材!】"
                jump chapter4_2
            elif ans_4_1.lower() == "opencv":
                "aria" "(系統自動日誌) ModuleNotFoundError: No module named 'opencv'。注意：雖然外包裝叫 OpenCV，但 Python 導入時必須使用其核心縮寫！"
                jump ch4_1_input
            else:
                $  score = score -  15
                "aria" "(系統自動日誌) 無法辨識的模組。發表會迫在眉睫，行銷部亂成一團！"
                "【系統提示：扣除 15 分！目前分數：[score]】"
              
                jump ch4_1_input


    # ==========================================
    # 4-2：音訊阻塞與多執行緒審查
    # ==========================================
label chapter4_2:
        "員工休息區。廣播喇叭正傳出駭客留下的刺耳高頻雜訊(Noise),福委會的點歌介面整個死當卡死。"
        "隔壁桌那位平時自稱『程式大神』的豬隊友同事一臉自信地走過來。"
        "同事" "嘿!我剛才幫辦公室音樂系統寫了一段修正 Code。我打包票沒問題，你直接部署上線吧!"
        p "等一下……音訊解碼與播放的巨量運算全被他塞在了 GUI 的主執行緒裡，難怪介面會卡死。我必須用多執行緒重構它！"
        
        "【重構提示】\nimport ________\nt = threading.Thread(target=play_audio)\nt.start()"

        label ch4_2_input:
            python:
                ans_4_2 = renpy.input("請輸入要導入的多執行緒標準函式庫名稱（全部小寫）：", default="").strip()

            if ans_4_2 == "threading":
                $ score += 10
                "aria" "(系統自動日誌) 審查與重構精準！成功導入 threading。音訊解碼移至背景執行，刺耳雜訊消失，介面流暢無比！"
                "【系統提示: 程式判斷能力評測達標。成功防範豬隊友的二次災難。】"
                jump chapter4_3
            else:
                $  score = score -  15
                "aria" "(系統自動日誌) 災難部署！未處理主執行緒卡頓問題。喇叭爆發出更大的噪音，整個福利系統伺服器當死燒毀！"
                "【系統提示：扣除 15 分！目前分數：[score]】"
                ### if score < 60:
                ###     "系統" "分數過低，最終修復宣告失敗……"
                ###     return
                jump ch4_2_input

# ==========================================
    # 4-3：總機房 TTS 語音合成解鎖
    # ==========================================
label chapter4_3:
        "終於來到了最深處的總機房大門前。然而大門被厚重的電子鎖鎖死,畫面上顯示出駭客最後的嘲諷字條。"
        "字條 『想要重啟系統？密碼隱藏在底層的加密文字檔中。但本大門只接受語音聲學頻率解鎖,你們的語音模組已經被我報廢了,慢慢猜吧!』"
        boss "客服部的無障礙語音導覽與自動回覆系統完全故障了!如果沒辦法用語音把密碼『讀出來』,我們就一輩子被關在辦公室裡了!"
        p "這是最後一關了……AI 參與度 0%%。我必須完全主導,當場寫出一個 TTS (Text-to-Speech) 語音合成模組!"
        "畫面上是一片黑暗的終端機，你需要引用 Python 最經典的文字轉語音函式庫。"
        
        "【終端機提示】\nfrom ______ import gTTS\ntts = gTTS(text=password, lang='en')\ntts.save('lock.mp3')"

        label ch4_3_input:
            python:
                # 測試學生是否知道 gTTS 函式庫導入時的模組名稱（全小寫）
                ans_4_3 = renpy.input("請輸入正確的 TTS 來源函式庫名稱（全部小寫）：", default="").strip()

            if ans_4_3 == "gtts":
                $ score += 10
                "【系統提示: 密碼文字成功轉換為清晰的語音輸出:'NEXUS_RESET_2026'】"
                "機房大門偵測到正確的語音頻率,發出機械解鎖聲,轟然開啟!"
                jump chapter4_clear
            elif ans_4_3 == "pyttsx3":
                # 如果學生打另一個知名的離線 TTS 函式庫，也算他對！但給予對應的劇情台詞
                $ score += 10
                "【系統提示: 成功調用 pyttsx3 離線語音引擎，成功初始化 TTS 語音！】"
                "清晰的電子合成音在大廳響起：'NEXUS_RESET_2026'。大門轟然開啟！"
                jump chapter4_clear
            else:
                $  score = score -  15
                "aria" "(系統自動日誌) ModuleNotFoundError: 找不到該名稱的語音合成函式庫。大門毫無反應。"
                "【系統提示：扣除 15 分！目前分數：[score]】"
                             


label chapter4_clear:
    "一陣強大的綠色光芒由機房中心擴散至整棟大樓。所有的螢幕瞬間亮起,恢復成熟悉的辦公室介面。"
    sys "【系統通告】Null-Void 病毒已被全數清除。所有業務部門系統重啟完畢,運作良好。"
    "全息投影閃爍,ARIA 的身影重新凝聚,露出了欣慰的笑容。"
    show aria default with Dissolve(0.5)
    aria "連線全面恢復!工程師,你成功了!在沒有我提供語音與程式碼邏輯的情況下,你竟然獨自完成了多媒體與自動化測試的重建!"
        
    # 計算最終成績    
    if score >= 60:
        show aria talk:
            right
        with move   
        aria "最終結算得分:[score] 分!你展現了極高水準的『測試驅動思維』與『獨立應用能力』,你是真正的核心架構師!"
        boss "太感謝你了!明天的週一例會,我會正式宣布晉升你為我們的首席資訊長(CIO)!現在,給自己開一罐慶祝的啤酒吧!"
        "【辦公室數據密室逃脫——成功!THE END】"

    else:
        show aria talk:
            right
        with move   
        aria "最終結算得分:[score] 分。分數未達到標準，最終修復宣告失敗……"
        "【辦公室數據密室逃脫——失敗!THE END】"
    return
