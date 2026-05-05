# ============================================================
# SYSTEM REBOOT：虛擬空間修復計畫
# Ren'Py Visual Novel Script
# ============================================================
# 世界觀：玩家扮演企業 Debug 工程師「玩家」，
# 被派入公司的核心虛擬伺服器空間 NEXUS-9 執行緊急修復任務。
# AI 夥伴 ARIA 依據鷹架理論，從 100% 引導逐漸退到 0%。
# ============================================================
init python:
    import requests
    import json
    import websocket  # 需要 websocket-client

    JUPYTER_URL = "http://localhost:8888"
    TOKEN = "your_token_here"

    def create_kernel():
        r = requests.post(
            f"{JUPYTER_URL}/api/kernels",
            headers={"Authorization": f"token {TOKEN}"},
            json={"name": "python3"}
        )
        return r.json()["id"]

    def execute_code(kernel_id, code):
        ws_url = f"ws://localhost:8888/api/kernels/{kernel_id}/channels"
        ws = websocket.create_connection(
            ws_url,
            header=[f"Authorization: token {TOKEN}"]
        )
        
        msg = {
            "header": {
                "msg_id": "unique-id-123",
                "msg_type": "execute_request"
            },
            "content": {
                "code": code,
                "silent": False
            },
            "metadata": {},
            "parent_header": {}
        }
        ws.send(json.dumps(msg))
        
        outputs = []
        while True:
            reply = json.loads(ws.recv())
            msg_type = reply["msg_type"]
            if msg_type == "stream":
                outputs.append(reply["content"]["text"])
            elif msg_type == "execute_reply":
                break
        
        ws.close()
        return "\n".join(outputs)
    def do_submit(nb):
    result = nb.submit(
        django_url="http://127.0.0.1:8000",
        student_id=persistent.student_id,
        assignment_id="assignment_01"
    )
    renpy.call_screen("show_feedback", result=result)

# ---------- 角色定義 ----------
define p = Character("你", color="#00FFCC")           # 玩家（工程師）
define aria = Character("ARIA", color="#FF9FE5")       # AI 助手（鷹架式引導）
define sys = Character("NEXUS-9", color="#FF4444")     # 系統警報音
define boss = Character("老闆", color="#FFD700")     # 遠端連線的上司

# ---------- 圖片資源佔位（請替換為實際路徑）----------
image server_room = "images/server_room.png"
# image bg nexus_core  = "images/bg/nexus_core.png"
# image bg corridor    = "images/bg/corridor.png"
# image bg queue_hall  = "images/bg/queue_hall.png"
# image bg loop_void   = "images/bg/loop_void.png"
# image bg office      = "images/bg/office.png"
# image bg datacenter  = "images/bg/datacenter.png"
# image bg chart_room  = "images/bg/chart_room.png"
# image bg broadcast   = "images/bg/broadcast.png"
# image bg final_core  = "images/bg/final_core.png"
#
# image aria normal    = "images/aria/normal.png"
# image aria happy     = "images/aria/happy.png"
# image aria worry     = "images/aria/worry.png"
# image aria serious   = "images/aria/serious.png"
# image aria hint      = "images/aria/hint.png"
# image aria silent    = "images/aria/silent.png"
# image aria error     = "images/aria/error.png"

# ---------- 音樂資源佔位 ----------
# 請依路徑替換
# define audio.bgm_boot    = "audio/bgm_boot.ogg"
# define audio.bgm_normal  = "audio/bgm_normal.ogg"
# define audio.bgm_tense   = "audio/bgm_tense.ogg"
# define audio.bgm_loop    = "audio/bgm_loop.ogg"
# define audio.bgm_calm    = "audio/bgm_calm.ogg"
# define audio.sfx_alarm   = "audio/sfx_alarm.ogg"
# define audio.sfx_correct = "audio/sfx_correct.ogg"
# define audio.sfx_wrong   = "audio/sfx_wrong.ogg"
# define audio.sfx_boot    = "audio/sfx_boot.ogg"

# ---------- 變數 ----------
default score = 0          # 修復進度分數
default aria_trust = 0     # ARIA 信任度（影響結局）

# ============================================================
# 開場：序幕
# ============================================================
label start:

    # BGM: bgm_boot（低沉機械啟動音）
    scene server_room with fade

    "【CG：昏暗的企業伺服器機房。冷白燈光打在密密麻麻的機架上，警示燈不停閃爍紅光。】"

    boss "喂，你聽得到嗎？NEXUS-9 的核心系統在三小時前開始異常，四個子系統陸續失聯。"
    boss "你是我們最後一張牌。進去把它修好。"

    p "……我一個人？"

    boss "不是。系統裡有一個 AI 協作模組，代號 ARIA。它會在旁邊協助你——但最終動手的還是你。"
    boss "時限六小時。開始吧。"

    # sfx: sfx_boot（傳送音效）
    # scene bg nexus_core with dissolve

    "【CG：意識被拉進虛擬空間。眼前是無盡延伸的數據走廊，地板是半透明的程式碼流。】"

    # show aria normal at center
    aria "連線確認。你好，工程師。我是 ARIA，你的協作模組。"
    aria "NEXUS-9 目前有四個區域出現嚴重錯誤。我會陪你逐一排除。"
    aria "……準備好了嗎？"

    menu:
        "準備好了。":
            $ aria_trust += 1
            aria happy "很好。跟我來。"
        "等一下，這裡是哪？":
            aria normal "虛擬伺服器核心空間。你的意識已經數位化。別太緊張，你不會真的死在這裡的。"
            aria hint "……大概不會。"

    jump chapter1_intro

# ============================================================
# CHAPTER 1：Layer 1 — 基礎區（100% 鷹架）
# ============================================================
label chapter1_intro:

    # scene bg corridor with slide
    # bgm: bgm_normal（輕快電子音）

    "【CG：一條發光的資料走廊。左側牆壁投影著大量 Python 程式碼，右側是一扇緊閉的鐵門。】"

    sys "【警報】Layer 1 啟動驗證失敗。環境變數讀取異常。請立即處理。"

    aria serious "這是 NEXUS-9 的入口驗證層。它無法辨識正確的 Python 執行環境，所以整個系統都被鎖住了。"
    aria hint "別擔心，我來一步一步教你。"

    # ---- 1-1：環境與變數 ----
    label chapter1_1:

        # show aria happy
        aria "首先，我們需要確認什麼是合法的 Python 執行環境。"
        aria "系統提供了三段啟動程式碼，但只有一個是正確的 Python 語法。你來選。"

        "【畫面出現三個程式碼選項，像全息投影懸浮在空中。】"

        aria hint "小提示：Python 用 # 做單行注釋，變數不需要宣告型別，print 要加括號。"

        menu ch1_1:
            "選項 A：\nx = 10\ny = 20\nprint(x + y)":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "正確！這是標準的 Python 變數宣告與輸出。"
                "【鐵門發出金屬聲，緩緩開啟。走廊燈光從紅轉綠。】"
                jump chapter1_2

            "選項 B：\nint x = 10;\nint y = 20;\nprintf(\"%d\", x+y);":
                # play sound sfx_wrong
                aria worry "嗯……這比較像 C 語言。Python 不需要宣告型別，也不用分號結尾。"
                aria hint "再試一次？"
                jump chapter1_1

            "選項 C：\nDIM x AS INTEGER = 10\nPRINT x + 20":
                # play sound sfx_wrong
                aria worry "這是 BASIC 的語法。我們需要的是 Python 喔。"
                aria hint "記住：Python 直接寫 x = 10 就好，非常簡潔。"
                jump chapter1_1

    # ---- 1-2：基本語法 ----
    label chapter1_2:

        # scene bg queue_hall with slide
        "【CG：走廊深處出現一個巨大的資料處理模組，像是一個透明的旋轉鼓輪，裡面的數字全是亂碼。】"

        sys "【警報】資料處理模組錯誤。運算結果偏差 300%。"

        # show aria worry
        aria "糟糕，這個模組負責病患排隊的資料計算。如果數字是錯的，整個排程就會亂掉。"
        aria "我找到了錯誤的程式碼片段，你來幫我找出哪一行有問題，然後選出正確的修正方式。"

        "【投影出現有 Bug 的程式碼：】"
        "  total = 100\n  discount = 20%\n  final = total - discount\n  print(final)"

        aria hint "提示：Python 的 % 是取餘數運算子，不是百分比。如果要計算 20% 的折扣，你會怎麼寫？"

        menu ch1_2:
            "修正為：discount = total * 0.20":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "完全正確！discount = total * 0.20 才是正確的百分比計算方式。"
                "【鼓輪停止轉動，數字重新排列整齊，顯示正常數值。】"
                jump chapter1_3

            "修正為：discount = 20":
                aria worry "這樣寫是固定折扣 20 元，不是 20%。如果 total 變了，這個數字就不對了。"
                aria hint "想想百分比的數學：20% = 0.20，所以……？"
                jump chapter1_2

            "修正為：discount = \"20%\"":
                aria worry "哈，這樣 discount 變成字串了，字串不能拿來做數學運算。"
                aria hint "我們需要的是數字，不是文字。"
                jump chapter1_2

    # ---- 1-3：迴圈與資料結構 ----
    label chapter1_3:

        # scene bg loop_void with dissolve
        # bgm: bgm_loop（不斷重複的電子音，帶點詭異感）

        "【CG：空間突然開始扭曲。走廊在眼前無限複製，像鏡中鏡一樣延伸。】"

        sys "【警報】庫存管理子系統進入無限迴圈。CPU 使用率 99.9%。"

        # show aria error
        aria "這就是為什麼整個空間開始抖動……庫存系統陷入無限迴圈，它一直在重複執行卻沒有停止條件。"
        aria "我找到了問題的程式碼，你來判斷哪裡會造成無限迴圈，並選出最適合管理這個庫存資料的結構。"

        "【投影出現有問題的程式碼：】"
        "  i = 0\n  while i < 10:\n      print(i)\n  # 少了 i += 1"

        aria hint "提示：while 迴圈需要一個讓條件變成 False 的方式，否則會永遠跑下去。"

        menu ch1_3a:
            "問題在：缺少 i += 1 讓計數器遞增":
                $ score += 5
                aria happy "對！沒有 i += 1，i 永遠是 0，條件永遠是 True，迴圈永遠不停。"
                jump ch1_3b
            "問題在：while 應該改成 for":
                aria normal "這是一個解法，但不是唯一的問題所在。根本原因是什麼？"
                aria hint "看看 i 這個變數——它有在迴圈裡面被改變嗎？"
                jump chapter1_3
            "問題在：print(i) 應該移到迴圈外":
                aria worry "這樣的話 i 根本不會被印出來。問題在更根本的地方……"
                aria hint "想想：迴圈什麼時候才會停下來？"
                jump chapter1_3

    label ch1_3b:
        aria "很好！現在，這個庫存系統需要頻繁地『新增』和『取出』資料，像排隊一樣先進先出。"
        aria "你會選哪種資料結構？"

        menu ch1_3c:
            "佇列（Queue）— 先進先出（FIFO）":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "完美！佇列就是為了這種先進先出的場景設計的，非常適合庫存管理。"
                jump chapter1_clear

            "堆疊（Stack）— 後進先出（LIFO）":
                aria worry "堆疊是後進先出，適合像『上一步』這種情境。庫存通常是先到先出喔。"
                aria hint "想像你在排隊買票，先排的人先買到——這是哪種結構？"
                jump ch1_3b

            "字典（Dict）— 鍵值對應":
                aria normal "字典適合用『名稱』查找對應資料，但不擅長管理順序和進出。"
                aria hint "我們需要的是有順序感的結構。"
                jump ch1_3b

    label chapter1_clear:

        # bgm: bgm_normal
        # scene bg nexus_core with dissolve

        "【CG：走廊的扭曲消失，空間恢復穩定。一扇通往下層的電梯門緩緩開啟，發出藍色光暈。】"

        # show aria happy
        aria "Layer 1 修復完成！你做得很好。"
        aria "接下來是 Layer 2，那裡的 AI 輔助會少一點……你要靠自己多一點了。"

        p "等一下——你說『少一點』？"

        aria normal "鷹架理論。我不能一直幫你，否則你什麼都學不到。"
        aria hint "……加油。"

        jump chapter2_intro

# ============================================================
# CHAPTER 2：Layer 2 — 應用區（80% 鷹架，有 Bug 需修正）
# ============================================================
label chapter2_intro:

    # scene bg office with slide
    # bgm: bgm_tense（節奏加快）

    "【CG：進入一個像辦公室的空間，但所有螢幕都在閃爍錯誤訊息。電話不停響，卻沒人接聽。】"

    sys "【警報】Layer 2 三個子系統異常。通信模組 Lag、日誌系統崩潰、情報爬蟲被封鎖。"

    # show aria serious
    aria "這層比較麻煩。我會給你有 Bug 的程式碼，你需要找出問題並修正。"
    aria "我還是會在旁邊，但我不會直接告訴你答案了。"

    # ---- 2-1：函式與模組 ----
    label chapter2_1:

        # scene bg office
        "【CG：一面巨大的白板上貼滿了重複的便利貼，每張都寫著幾乎一樣的程式碼。】"

        # show aria worry
        aria "通信模組的程式碼，同樣的計算邏輯被複製貼上了七次。難怪會 Lag。"
        aria "我找到了其中一段有問題的函式，你來修正它。"

        "【投影出現有 Bug 的程式碼：】"
        "  total = 0\n\n  def add_score(points):\n      total += points\n      return total\n\n  add_score(10)"

        aria "這個函式執行時會出錯。你知道為什麼嗎？"

        menu ch2_1:
            "global total 沒有宣告，函式內無法修改外部變數":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "完全正確！Python 函式內若要修改外部變數，需要加上 global total 宣告。"
                aria "修正後的版本：\n  def add_score(points):\n      global total\n      total += points"
                "【白板上的便利貼一張張脫落，匯聚成一個整齊的函式模組。】"
                jump chapter2_2

            "函式名稱 add_score 需要改成 addScore":
                aria normal "命名風格不影響執行。問題在執行時會拋出 UnboundLocalError……"
                aria hint "想想 total 這個變數——它在函式外面定義，函式裡面試圖修改，這在 Python 有什麼限制？"
                jump chapter2_1

            "return total 應該改成 print(total)":
                aria worry "return 和 print 都是合法的，但這不是造成錯誤的原因。"
                aria hint "試著跑一次這段程式，你會看到什麼錯誤訊息？"
                jump chapter2_1

    # ---- 2-2：檔案與例外處理 ----
    label chapter2_2:

        # scene bg datacenter with dissolve
        "【CG：資料中心的走廊，地板上散落著破碎的日誌檔碎片，像玻璃一樣發光。】"

        sys "【警報】日誌系統崩潰。關鍵修復紀錄遺失 47 筆。"

        # show aria serious
        aria "日誌系統在寫檔時，遇到權限不足或檔案不存在就直接崩潰，完全沒有錯誤處理。"
        aria "我已經寫好了架構，但缺少 try-except 區塊。你來加進去。"

        "【投影出現需要補完的程式碼：】"
        "  def write_log(filename, data):\n      f = open(filename, 'w')\n      f.write(data)\n      f.close()\n      print('寫入成功')"

        aria "這段程式如果 open 失敗，整個系統就會崩潰。你會怎麼改？"

        menu ch2_2:
            "用 try-except 包住 open 和 write，except 捕捉 Exception":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "很好！try-except 可以讓程式在出錯時優雅地處理，而不是直接崩潰。"
                aria "參考寫法：\n  try:\n      f = open(filename, 'w')\n      f.write(data)\n  except Exception as e:\n      print(f'錯誤：{e}')\n  finally:\n      f.close()"
                "【地板上的碎片重新拼合，日誌檔一筆筆恢復完整。】"
                jump chapter2_3

            "在 open 前加上 if os.path.exists(filename)":
                aria normal "這只能確認檔案存在，無法處理權限錯誤或磁碟空間不足等其他問題。"
                aria hint "想想：有沒有一種方式可以『嘗試』執行，失敗了再處理？"
                jump chapter2_2

            "加上 print('寫入失敗') 在最後":
                aria worry "print 不能阻止程式崩潰，只是在崩潰前多說一句話而已。"
                aria hint "Python 有專門處理例外狀況的語法結構……"
                jump chapter2_2

    # ---- 2-3：網路爬蟲 ----
    label chapter2_3:

        # scene bg datacenter
        "【CG：牆壁上出現一個巨大的網路節點圖，其中一個節點不斷閃爍紅色——ETtoday 的入口被鎖住了。】"

        # show aria serious
        aria "為了獲取外部情報，系統需要爬取 ETtoday 的新聞。但 AI 的爬蟲請求一直被拒絕。"
        aria "我寫好了基礎的爬蟲，但缺了一個關鍵設定。你知道是什麼嗎？"

        "【投影出現有問題的程式碼：】"
        "  import requests\n\n  response = requests.get('https://www.ettoday.net')\n  print(response.status_code)"

        aria "這段程式執行後會收到 403 Forbidden。你猜是什麼問題？"

        menu ch2_3:
            "缺少 User-Agent headers，伺服器拒絕非瀏覽器請求":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "正確！很多網站會檢查請求來源，若沒有設定 User-Agent 就當成機器人拒絕。"
                aria "修正方式：\n  headers = {'User-Agent': 'Mozilla/5.0 ...'}\n  response = requests.get(url, headers=headers)"
                "【紅色節點轉為綠色，大量新聞標題開始流入系統。】"
                jump chapter2_clear

            "需要加上 time.sleep(1) 避免太頻繁":
                aria normal "睡眠時間可以降低被封鎖的機率，但 403 是當下就被拒絕，不是因為太頻繁。"
                aria hint "想想：伺服器怎麼判斷你是人還是機器人？"
                jump chapter2_3

            "URL 需要加上 https://www. 才正確":
                aria normal "URL 本身沒問題，問題在請求的方式，不是目標地址。"
                aria hint "HTTP 請求有很多參數……其中一個是告訴伺服器你是誰。"
                jump chapter2_3

    label chapter2_clear:

        # scene bg nexus_core with dissolve
        # bgm: bgm_calm

        "【CG：辦公室空間的混亂逐漸平息，螢幕一個個恢復正常顯示。】"

        # show aria normal
        aria "Layer 2 修復完成。你的表現不錯。"
        p "下一層呢？"

        # show aria hint
        aria "Layer 3……我的輔助會更少。我只能在一旁看，你寫的程式，我不保證是對的。"
        aria "你需要自己測試、自己驗證。"

        p "……明白了。"

        jump chapter3_intro

# ============================================================
# CHAPTER 3：Layer 3 — 進階區（50% 鷹架，AI 只幫寫 Code 不查邏輯）
# ============================================================
label chapter3_intro:

    # scene bg datacenter with fade
    # bgm: bgm_tense

    "【CG：進入更深層的空間。這裡的建築結構更複雜，牆壁上的數據流速度極快，難以辨讀。】"

    # show aria silent
    aria "我可以幫你寫程式碼的架構，但邏輯對不對……你得自己負責。"
    aria "如果你的測試通過了，我們就繼續。如果沒有，你自己找問題。"

    # ---- 3-1：Matplotlib ----
    label chapter3_1:

        # scene bg chart_room with slide
        "【CG：投資分析儀表板的房間。巨大的螢幕上顯示著扭曲的折線圖，X 軸和 Y 軸的比例明顯錯誤。】"

        sys "【警報】圖表渲染異常。座標範圍錯誤，數據無法正確呈現。"

        # show aria normal
        aria "我幫你生成了一段 Matplotlib 的程式碼，用來繪製投資數據。但圖表看起來怪怪的……"
        aria "我沒有去檢查邏輯。你需要撰寫測試，找出哪個參數設定錯了。"

        "【投影出現 AI 生成的程式碼：】"
        "  import matplotlib.pyplot as plt\n\n  x = [1, 2, 3, 4, 5]\n  y = [100, 200, 150, 300, 250]\n\n  plt.plot(x, y)\n  plt.xlim(0, 3)  # <-- 可疑的地方\n  plt.ylim(0, 200)  # <-- 可疑的地方\n  plt.show()"

        aria "我已經說完了。接下來要怎麼驗證，你決定。"

        menu ch3_1:
            "xlim 應設為 (0, 5)，ylim 應設為 (0, 350) 才能包含所有數據點":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "你找到了。xlim(0,3) 截掉了第 4、5 筆數據，ylim(0,200) 也讓 300 超出範圍。"
                "【螢幕上的折線圖重新渲染，所有數據點都正確顯示。】"
                jump chapter3_2

            "需要加上 plt.title() 和 plt.xlabel()":
                aria normal "這些是美化圖表的設定，不是造成座標異常的原因。"
                aria "我說了，邏輯你自己找。"
                jump chapter3_1

            "應該換成 plt.bar() 條狀圖":
                aria normal "圖表類型不是問題所在。問題在數據有沒有被正確顯示出來。"
                aria "看看那兩行 lim 的設定……"
                jump chapter3_1

    # ---- 3-2：影音處理 ----
    label chapter3_2:

        # scene bg broadcast with dissolve
        "【CG：一個像電視台機房的空間，架上的影片檔案一個個變成灰色——下載功能完全失效。】"

        sys "【警報】教育訓練影片庫下載功能失效。12 個影片格式驗證失敗。"

        # show aria normal
        aria "我寫了一個影片下載功能，但我沒有驗證下載的檔案格式是否正確。"
        aria "你需要撰寫測試案例，驗證我的邏輯。"

        "【投影出現 AI 生成的程式碼：】"
        "  def download_video(url, save_path):\n      response = requests.get(url)\n      with open(save_path, 'wb') as f:\n          f.write(response.content)\n      return True"

        aria "有沒有問題，你來判斷。"

        menu ch3_2:
            "缺少檔案格式驗證（檢查副檔名或 Content-Type），以及沒有處理下載失敗的情況":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "發現了。response.status_code 沒有被檢查，也沒有驗證檔案格式。"
                aria "應該加上：\n  if response.status_code != 200: return False\n  if not save_path.endswith(('.mp4','.avi')): return False"
                "【灰色的影片檔案重新亮起，下載進度條一個個跑起來。】"
                jump chapter3_3

            "函式應該要有進度條顯示":
                aria normal "使用者體驗是一回事，功能邏輯的正確性才是現在要測試的。"
                aria "想想：這個函式在什麼情況下會靜默失敗？"
                jump chapter3_2

            "with open 應該改成 try-except 包起來":
                aria normal "這可以提升健壯性，但不是唯一的問題。還有別的地方沒有被驗證……"
                aria "下載成功了，但下載的是什麼？"
                jump chapter3_2

    # ---- 3-3：即時資料 ----
    label chapter3_3:

        # scene bg office with slide
        "【CG：辦公室環境監測面板，溫度、濕度、CO2 的數值一半顯示 None，一半顯示正常數值。】"

        sys "【警報】環境監測系統讀取到空值。資料清洗邏輯異常。"

        # show aria serious
        aria "我幫環境監測 API 寫了資料清洗邏輯，但沒有處理 None 值的情況。"
        aria "你需要撰寫測試，驗證在 API 回傳 None 時，我的邏輯是否正確處理。"

        "【投影出現 AI 生成的程式碼：】"
        "  def clean_data(value):\n      return float(value) * 1.0  # 單位轉換"

        aria "剩下的，你自己來。"

        menu ch3_3:
            "當 value 為 None 時，float(None) 會拋出 TypeError，需要加上 None 的判斷":
                $ score += 10
                $ aria_trust += 1
                # play sound sfx_correct
                aria happy "正確！需要在開頭加上：\n  if value is None: return None  # 或 return 0"
                aria "這樣 API 回傳空值時，系統才不會崩潰。"
                "【監測面板的 None 值逐漸被 0 或合理預設值取代，面板恢復正常。】"
                jump chapter3_clear

            "直接把 None 替換成 0 就好":
                aria normal "這是一種做法，但 float(None) 在替換之前就已經拋出例外了。"
                aria "你的測試需要先考慮什麼時機點會出錯……"
                jump chapter3_3

            "加上 try-except TypeError 來捕捉錯誤":
                aria normal "這可以避免崩潰，但返回值是什麼？None 還是 0？這個決策需要你來定義。"
                aria "先把這個邏輯寫清楚，再決定要怎麼處理。"
                jump chapter3_3

    label chapter3_clear:

        # scene bg nexus_core with dissolve
        # bgm: bgm_calm

        "【CG：深層空間的牆壁開始震動，一道巨大的光柱從地板升起，指向最深處。】"

        # show aria normal
        aria "……你做到了。Layer 3 修復完成。"
        aria "最後一層了。"

        p "最後一層……你還在嗎？"

        # show aria silent
        aria "我在。但 Layer 4……我只能給你一個關鍵字。"
        aria "剩下的，全靠你自己。"

        jump chapter4_intro

# ============================================================
# CHAPTER 4：Layer 4 — 核心區（20%→0%，學生主導）
# ============================================================
label chapter4_intro:

    # scene bg final_core with fade
    # bgm: bgm_tense（最強版本）

    "【CG：NEXUS-9 的核心區。這裡沒有走廊，沒有辦公室——只有懸浮在虛空中的巨大程式碼球體，緩慢旋轉著。】"

    # show aria silent
    aria "……這裡是 NEXUS-9 的核心。"
    aria "我能說的，到這裡為止了。"

    # ---- 4-1：圖片處理 ----
    label chapter4_1:

        "【CG：核心球體的一個切面出現了——是被嚴重壓縮的行銷圖片，像素化到幾乎看不出原本的樣子。】"

        sys "【警報】行銷素材圖檔批次損壞。需要自動化修復腳本。"

        # show aria hint
        aria "OpenCV。"

        aria silent "……就這樣。"

        p "就這樣？"

        aria silent "……"

        "【你獨自面對損壞的圖片，思考著如何用 OpenCV 建立自動化批次處理腳本。】"

        menu ch4_1:
            "使用 cv2.imread() 讀取、處理後以 cv2.imwrite() 儲存，搭配 os.listdir() 批次處理":
                $ score += 20
                $ aria_trust += 2
                # play sound sfx_correct
                "【損壞的圖片一張張被修復，像素重新排列，圖像清晰度恢復。】"
                p "……我做到了。"
                # show aria happy
                aria "……嗯。"
                jump chapter4_2

            "使用 PIL/Pillow 的 Image.open() 和 Image.save()":
                aria normal "也是一種方式。但這題的關鍵字是 OpenCV。"
                aria silent "……之後就不說了。"
                jump chapter4_1

    # ---- 4-2：多媒體 ----
    label chapter4_2:

        "【CG：音樂系統的介面浮現——一個充滿設計瑕疵的播放器 UI，按鈕重疊，進度條無法拖動。】"

        sys "【警報】辦公室音樂系統發出雜訊。介面設計存在多處邏輯漏洞。"

        # show aria silent
        aria "這是另一個工程師的程式碼。你來做同儕審查。"

        "【投影出現「AI 隊友」寫的程式碼片段：】"
        "  # 音樂播放器\n  volume = 0\n  def set_volume(v):\n      volume = v  # Bug 1\n\n  def play(file):\n      if file = 'music.mp3':  # Bug 2\n          start()\n\n  # UI：停止按鈕綁定了播放功能  # Bug 3"

        p "讓我仔細看看……"

        menu ch4_2:
            "Bug1: 變數作用域問題（需 global）；Bug2: = 應為 ==；Bug3: 按鈕事件綁定錯誤":
                $ score += 20
                $ aria_trust += 2
                # play sound sfx_correct
                "【音樂系統恢復正常，清晰的背景音樂取代了刺耳的雜訊。】"
                p "三個問題全找到了。"
                # show aria happy
                aria "……你的眼力變好了。"
                jump chapter4_3

            "只找到 Bug2（= 應為 ==）":
                aria normal "這是其中一個，但還有兩個。"
                aria silent "……繼續看。"
                jump chapter4_2

    # ---- 4-3：語音應用 ----
    label chapter4_3:

        "【CG：核心球體的最後一個切面開啟——裡面是一個沉默的語音合成模組，它的嘴形在動，卻發不出任何聲音。】"

        sys "【警報】無障礙資訊服務語音合成模組故障。TTS 輸出失效。"

        # show aria silent
        aria "……"

        p "你不說話了嗎？"

        aria "TTS。"

        aria silent "……"

        "【這是最後的任務。你需要獨立使用 TTS 函式庫，讓語音模組重新開口。】"
        "【沒有選擇，沒有提示，只有你、沉默的模組、和一個關鍵字。】"

        menu ch4_3:
            "使用 pyttsx3 或 gTTS 函式庫，將文字轉換為語音輸出":
                $ score += 20
                $ aria_trust += 2
                # play sound sfx_correct
                "【語音模組緩緩開口，清晰的聲音在虛空中迴盪。】"
                "語音模組：「系統修復完成。感謝您。」"
                jump ending_check

            "使用 subprocess 呼叫系統的 say 指令":
                aria normal "平台相依性太高。我們需要跨平台的解法。"
                aria silent "……"
                jump chapter4_3

    # ============================================================
    # 結局判定
    # ============================================================
    label ending_check:
        if aria_trust >= 8:
            jump ending_good
        elif aria_trust >= 5:
            jump ending_normal
        else:
            jump ending_neutral

# ============================================================
# 結局 A：完全信任（高分結局）
# ============================================================
label ending_good:

    # scene bg final_core with dissolve
    # bgm: bgm_calm（溫柔版本）

    "【CG：核心球體開始發出白色光芒，所有程式碼重新排列，NEXUS-9 的錯誤訊息逐一消失。】"

    # show aria happy
    aria "……修復完成了。"
    aria "Score: [score] / 100。你比我預期的還要厲害。"

    p "ARIA……你從一開始就知道答案對吧？"

    aria "當然。"

    p "那你為什麼不直接告訴我？"

    aria "因為你需要的不是答案。你需要的是找到答案的能力。"
    aria "如果我都幫你做完，你下次遇到問題，還是什麼都不會。"

    p "……謝謝你。"

    aria "下次遇到問題，不要等我說。"

    "【NEXUS-9 全面恢復。你從虛擬空間退出，回到現實的機房。】"
    "【螢幕上顯示：系統修復完成。工程師：玩家。協作模組：ARIA。】"

    boss "幹得好。報告我。"

    "【END A：鷹架撤除】"
    "【你學會了獨立。】"

    return

# ============================================================
# 結局 B：正常通關（標準結局）
# ============================================================
label ending_normal:

    # scene bg final_core with dissolve
    # bgm: bgm_normal

    "【CG：NEXUS-9 的核心恢復運作，但仍有幾個角落閃爍著不穩定的光點。】"

    # show aria normal
    aria "修復完成了。Score: [score] / 100。"
    aria "……有幾個地方你還可以做得更好。"

    p "我知道。"

    aria "下次記得主動思考，不要等提示。"

    "【NEXUS-9 大致恢復正常。少數非關鍵模組仍在離線狀態。】"

    boss "勉強可以。下次要更快。"

    "【END B：任務完成】"
    "【系統修復，但學習之路尚未結束。】"

    return

# ============================================================
# 結局 C：完成但未達信任（中性結局）
# ============================================================
label ending_neutral:

    # scene bg final_core with dissolve
    # bgm: bgm_calm

    "【CG：NEXUS-9 的核心緩慢恢復，像是在深眠後逐漸清醒。】"

    # show aria normal
    aria "修復完成了。Score: [score] / 100。"

    p "……就這樣？"

    aria "就這樣。系統修復了。"
    aria "但你知道嗎，每次你選擇等我給答案而不是自己想的時候……你就少學了一點東西。"

    p "……我明白了。"

    aria "下次，試著在我開口之前，先自己想一想。"

    "【NEXUS-9 完成修復。任務結束。】"

    "【END C：修復者】"
    "【系統重啟，但真正的成長，需要你主動去爭取。】"

    return

# ============================================================
# END OF SCRIPT
# ============================================================
