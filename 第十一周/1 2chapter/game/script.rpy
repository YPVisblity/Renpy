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

    boss "喂，你聽得到嗎？NEXUS-9 的核心系統在三小時前開始異常，我們部署的Python專案陸續發生邏輯錯誤，導致崩潰。"
    boss "那些AI自動生成的程式碼產生了未知的錯誤，把系統鎖死成了好幾個獨立的數據密室。"
    boss "你是我們最後一張牌。進去把它們修好。"

    p "我一個人？"

    boss "不是。系統裡有一個AI協作模組，代號ARIA。它會在旁邊提供測試回饋和除錯線索，但最終動手的還是你。"
    boss "時限六小時。開始吧。"

    # sfx:sfx_boot（傳送音效） 
    #scene nexus_core with dissolve  #傳送進空間的畫面

    "意識被拉進虛擬空間。眼前是無盡延伸的數據走廊，地板是半透明的程式碼流。"

    #show aria  at center #AI助手

    aria "連線確認。你好，工程師。我是ARIA，你的協作模組。"
    aria "NEXUS-9 有多個Python專案的執行環境遭到封鎖。每一個異常的專案，都形成了一個無法通行的密室，我會陪你逐一排除。"
    aria "準備好了嗎？"

    menu:
        "準備好了。":
            $ aria_trust += 1
            aria "很好。第一間密室是基礎環境與語法測試，跟我來。"
        "等一下，這裡是哪？":
            aria "虛擬伺服器核心空間。你的意識已經數位化。別太緊張，你不會真的死在這裡的。"
            aria "大概不會。"

    jump chapter1_1

#1-1 Python 基礎 (100%AI幫助)(選擇題)主要教導int、print這些基礎語法。

label chapter1_1:
    aria "再進行修復程式碼前，您需要了解關於python的一些基本語法。"
    "可以宣告一個變數給予一個數值，像是 a=1，在python中不用像是其他語言一樣先宣告int or char"
    "利用print語法可以將其輸出在螢幕上。例如print(a)"

    aria "接下來就是你表現的時候了。"
    aria "首先，我們需要向核心提交合法的Python語法來解鎖。系統提供了三段啟動程式碼，但只有一個是正確的。"

    "畫面出現三個程式碼選項，像全息投影懸浮在空中。"

    aria "線索提示：Python 用 # 做單行注釋，變數不需要宣告型別，print要加括號。"
    menu:
        "選項 A：\nx = 10\ny = 20\nprint(x + y)":
            $ score += 10
            $ aria_trust += 1
            aria "正確！這是標準的Python變數宣告與輸出。"
            "系統提示：PyBryt基礎測試通過，獲得碎片鑰匙。密室門發出金屬聲，緩緩開啟。"
            jump chapter1_2

        "選項 B：\nint x = 10;\nint y = 20;\nprintf(\"%%d\", x+y);":
            aria "PyBryt測試失敗：SyntaxError。這比較像 C 語言，Python 不需要宣告型別，也不用分號結尾。"
            jump chapter1_1

        "選項 C：\nDIM x AS INTEGER = 10\nPRINT x + 20":
            aria "PyBryt測試失敗：SyntaxError。這是BASIC的語法。我們需要的是Python喔。"
            aria "記住：Python 直接寫 x = 10 就好，非常簡潔。"
            jump chapter1_1
#1-2 基本語法
    label chapter1_2:
        "走廊深處出現一個巨大的資料處理模組，像是一個透明的旋轉鼓輪，裡面的數字全是亂碼。通往下一區的閘門緊閉。"

        sys "【警報】資料處理模組邏輯異常。運算結果偏差300%%。"

        aria "糟糕，這個模組負責病患排隊的資料計算。AI 生成了一段錯誤的折扣邏輯。"
        aria "我已經幫你定位出錯誤的程式碼片段，你來選出正確的修正方式，我們才能拿到下一把鑰匙。"

        "投影出現有Bug的程式碼："
        "total= 100\n discount = 20%%\n final=total-discount\n print(final)"

        aria "線索提示：Python的%%是取餘數運算子，不是百分比。如果要計算20%%的折扣，你會怎麼寫？"

        menu:
            "修正為：discount = total * 0.20":
                $ score += 10
                $ aria_trust += 1
                aria  "完全正確！discount = total * 0.20 才是正確的百分比計算方式。"
                "系統提示：PyBryt邏輯測試通過。鼓輪停止轉動，數字重新排列整齊，閘門開啟。"
                jump chapter1_3

            "修正為：discount = 20":
                aria  "測試失敗：數值硬編碼 (Hardcoded)。這樣寫是固定折扣20元，不是20%%。如果 total變了，這個數字就不對了。"
                jump chapter1_2

            "修正為：discount = \"20%%\"":
                aria  "測試失敗：TypeError。這樣 discount 變成字串了，字串不能拿來跟整數做相減運算。"
                jump chapter1_2
#1-3 迴圈與資料結構
    label chapter1_3:
        "空間突然開始扭曲。走廊在眼前無限複製，像鏡中鏡一樣延伸，形成一個無法逃脫的迷宮。"

        sys "【警報】庫存管理密室陷入無限迴圈。CPU使用率99.9%%。"

        aria "這就是為什麼密室開始抖動……庫存系統陷入無限迴圈，它一直在重複執行卻沒有停止條件。"
        aria "你來判斷哪裡會造成無限迴圈，並選出最適合管理這個庫存資料的結構。"

        "投影出現有問題的程式碼："
        "  i = 0\n  while i < 10:\n      print(i)\n  # 少了 i += 1"

        menu:
            "問題在：缺少 i += 1 讓計數器遞增":
                $ score += 5
                aria  "對！沒有 i += 1，i 永遠是 0，條件永遠是 True，迴圈永遠不停。"
                jump ch1_3b
            "問題在：while應該改成for":
                aria  "這是一個解法，但不是引發無限迴圈的根本原因。看看i這個變數，它有在迴圈裡面被改變嗎？"
                jump chapter1_3
            "問題在：print(i) 應該移到迴圈外":
                aria  "這樣的話 i 根本不會被印出來。想想：迴圈什麼時候才會停下來？"
                jump chapter1_3

    label ch1_3b:
        aria "很好！現在，這個庫存系統需要頻繁地『新增』和『取出』資料。"
        aria "你會選哪種資料結構作為修復的基底？"

        menu:
            "佇列（Queue）— 先進先出（FIFO）":
                $ score += 10
                $ aria_trust += 1
                aria  "完美！佇列就是為了這種先進先出的場景設計的，非常適合庫存管理。"
                jump chapter1_clear

            "堆疊（Stack）— 後進先出（LIFO）":
                aria  "堆疊是後進先出。想像你在排隊買票，先排的人先買到——這是哪種結構？"
                jump ch1_3b

            "字典（Dict）— 鍵值對應":
                aria  "字典適合用『名稱』查找對應資料，但不擅長管理順序和進出。"
                jump ch1_3b

    label chapter1_clear:
        "走廊的扭曲消失，密室解鎖。一扇通往下層的電梯門緩緩開啟，發出藍色光暈。"

        aria  "Layer 1密室修復完成！你做得很好。"
        aria "接下來是 Layer 2，那裡的 AI 輔助會少一點，你需要由自己負責主要部份了。"

        p "等一下——你說『少一點』？"

        aria  "我不能一直把答案塞到你手裡，否則你永遠無法對抗那些失控的AI程式碼。"
        aria  "準備迎接真正的Debug吧，加油。"

        jump chapter2_intro

#CHAPTER 2：Layer 2 — 應用區（80% 鷹架，有 Bug 需修正）
label chapter2_intro:
    "進入一個像辦公室的空間，但所有門都被紅色雷射網封鎖。電話不停響，卻沒人接聽。"

    sys "【警報】Layer 2 三個子系統異常。通信模組 Lag、日誌系統崩潰、情報爬蟲被封鎖。"

    aria  "這層的密室比較麻煩。我會給你有 Bug 的程式碼，你需要找出問題並修正。"
    aria "我還是會在旁邊提供錯誤訊息線索，但我不會直接把正確語法列出來了。"

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
                aria  "完全正確！Python 函式內若要修改外部變數，需要加上 global 宣告。"
                "白板上的便利貼一張張脫落，匯聚成一個整齊的函式模組。通訊室雷射網解除。"
                jump chapter2_2

            "函式名稱add_score需要改成addScore":
                aria  "命名不影響執行。問題在於變數的『作用域』(Scope)。"
                jump chapter2_1

            "return total 應該改成print(total)":
                aria  "return 是將值傳遞出去的正確做法。這不是造成錯誤的原因。"
                jump chapter2_1

    # 2-2：檔案與例外處理
    label chapter2_2:
        "資料中心的走廊，地板上散落著破碎的日誌檔碎片，像玻璃一樣發光。"

        sys "【警報】日誌系統崩潰。關鍵修復紀錄遺失 47 筆。"

        aria  "日誌系統在寫檔時，遇到權限不足就直接崩潰，完全沒有例外處理機制。"
        aria "我已經寫好了架構，但缺少容錯的機制。剩下交由你來補完。"

        "投影出現需要補完的程式碼："
        "  def write_log(filename, data):\n      f = open(filename, 'w')\n      f.write(data)\n      f.close()\n      print('寫入成功')"

        aria "如果 open 失敗，整個密室就會崩潰。你會怎麼改？"

        menu:
            "用 try-except 包住 open 和 write，except 捕捉 Exception":
                $ score += 10
                $ aria_trust += 1
                aria  "很好！try-except 可以讓程式在出錯時優雅地捕捉例外，而不是直接終止程式。"
                "地板上的碎片重新拼合，日誌檔一筆筆恢復完整。下一扇門開啟。"
                jump chapter2_3

            "在 open 前加上 if os.path.exists(filename)":
                aria  "這只能確認檔案存在，無法處理『權限不足』或『磁碟空間已滿』等無法預期的錯誤。"
                jump chapter2_2

            "加上 print('寫入失敗') 在最後":
                aria  "print 不能阻止程式崩潰，只是在崩潰前多說一句話而已。你需要控制流的結構。"
                jump chapter2_2

    # ---- 2-3：網路爬蟲 ----
    label chapter2_3:
        "牆壁上出現一個巨大的網路節點圖，其中 ETtoday 的入口閃爍著大大的 403 Forbidden 封鎖標誌。"

        aria  "為了獲取外部情報，系統需要爬取新聞。但 AI 寫的爬蟲一直被拒絕。"

        "【投影出現有問題的程式碼：】"
        "  import requests\n\n  response = requests.get('https://www.ettoday.net')\n  print(response.status_code)"

        aria "這段程式執行後會收到 403 Forbidden。你猜伺服器是怎麼識破我們是機器人的？"

        menu:
            "缺少 User-Agent headers，伺服器拒絕非瀏覽器請求":
                $ score += 10
                $ aria_trust += 1
                aria  "正確！沒有偽裝 User-Agent，伺服器一看就知道是 Python-requests 發出的請求。"
                "【403 封鎖標誌轉為綠色 200 OK，大量新聞標題開始流入系統。】"
                jump chapter2_clear

            "需要加上 time.sleep(1) 避免太頻繁":
                aria  "睡眠時間可以降低被封鎖的機率，但 403 是當下就被拒絕，不是因為太頻繁造成的 429 Too Many Requests。"
                jump chapter2_3

            "URL 需要加上 https://www. 才正確":
                aria  "URL 本身沒問題。問題在 HTTP Request Headers 裡面缺少了關鍵的身份證明。"
                jump chapter2_3

    label chapter2_clear:
        "【CG：辦公室空間的紅色雷射網全數消失，螢幕一個個恢復正常顯示。】"

        aria  "Layer 2 密室修復完成。你的除錯直覺越來越敏銳了。"
        p "下一層呢？"

        aria  "Layer 3……我的輔助會降到 50%%。我只會幫你生出程式碼架構，但我不保證邏輯是對的。"
        aria "你必須運用『測試驅動』 的思維，自己找出漏洞。"

        p "明白了。來吧。"

        #jump chapter3_intro