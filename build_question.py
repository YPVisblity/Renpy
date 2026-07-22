import json
import copy
from pathlib import Path

# 修復語法錯誤後的 LEVELS 陣列
LEVELS = [
    {
        "id": "chapter-1-level-1",
        "chapter": "第 1 章第一關",
        "level": "1-1",
        "title": "變數港口",
        "difficulty": "20％",
        "story_url": "https://ypvisblity.github.io/chapter_python/ch_1/index.html",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-1-level-1.ipynb",
        "summary": "1-1描述",
        "warn": "返回題目點選按鈕，進入關卡",
        "topics": [
            {
                "id": "chapter-1-level-1-1",
                "title": "認識變數",
                "description": "蘋果的價格為26元，請問小明購買6個蘋果需要多少錢?\t請用value(x,y)計算蘋果總價為何?",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "value(26,6)",
            },
            {
                "id": "chapter-1-level-1-2",
                "title": "解釋變數",
                "description": "設定a為一頭牛，b為吃了一顆草?\t請輸出a+b的結果",
                "starter_code": "#請在這裡寫程式\n",
                "test_code": "value(a,b)",
            },
        ],
    },
    {
        "id": "chapter-1-level-2",
        "chapter": "第 1 章第二關",
        "level": "1-2",
        "title": "if else判斷",
        "difficulty": "20％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-1-level-2/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-1-level-2.ipynb",
        "summary": "1-2描述",
        "warn": "返回題目點選按鈕，進入關卡",
        "topics": [
            {
                "id": "chapter-1-level-2-1",
                "title": "BMI計算",
                "description": "請定義一個basic(height, weight) 函數，計算BMI判斷過輕、正常、過重。bmi< 18.5為過輕、18.5<=bmi<=24為正常、bmi > 24為過重",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "print(basic(1.78, 70))\nprint(basic(1.60, 40))\nprint(basic(1.60, 80))",
            },
        ],
    },
    {
        "id": "chapter-1-level-3",
        "chapter": "第 1 章第三關",
        "level": "1-3",
        "title": "矩陣相加",
        "difficulty": "20％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-1-level-3/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-1-level-3.ipynb",
        "summary": "1-3描述",
        "warn": "返回題目點選按鈕，進入關卡",
        "topics": [
            {
                "id": "chapter-1-level-3-1",
                "title": "矩陣相加",
                "description": "請定義一個matrix_add(A,B)函數，計算函數相加。使用for迴圈",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "A = [[1,2],[3,4]]\nB = [[5,6],[7,8]]\nmatrix_add(A,B)\nA = [[2,1],[0,3]]\nB = [[1,4],[5,2]]\nmatrix_add(A,B)",
            },
        ],
    },
    {
        "id": "chapter-2-level-1",
        "chapter": "第 2 章第一關",
        "level": "2-1",
        "title": "等差數列",
        "difficulty": "40％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-2-level-1/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-2-level-1.ipynb",
        "summary": "2-1描述",
        "warn": "返回題目點選按鈕，進入關卡",
        "topics": [
            {
                "id": "chapter-2-level-1-1",
                "title": "等差數列",
                "description": "請建立一個sequence串列後使用公式term = a + i * d計算等差數列。",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "val = generate_arithmetic_sequence(2,3,5)\nval",
            },
        ],
    },
    {
        "id": "chapter-2-level-2",
        "chapter": "第 2 章第二關",
        "level": "2-2",
        "title": "檔案與例外處理",
        "difficulty": "40％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-2-level-2/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-2-level-2.ipynb",
        "summary": "2-2描述",
        "warn": "返回題目點選按鈕，進入關卡",
        "topics": [
            {
                "id": "chapter-2-level-2-1",
                "title": "try-catch兩數相除",
                "description": "請使用try/except處理除以零的錯誤\n，請定義safe_divide(a,b)，當b=0時回傳Error:除以零，否則ab相除回傳結果",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "print(safe_divide(10,0))\nprint(safe_divide(10,2))\n",
            },
        ],
    },
    {
        "id": "chapter-2-level-3",
        "chapter": "第 2 章第三關",
        "level": "2-3",
        "title": "守衛問答",
        "difficulty": "40％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-2-level-3/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-2-level-3.ipynb",
        "summary": "2-3描述",
        "warn": "返回題目點選按鈕，進入關卡",
    },
    {
        "id": "chapter-3-level-1",
        "chapter": "第 3 章第一關",
        "level": "3-1",
        "title": "迴圈礦坑",
        "difficulty": "60％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-3-level-1/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-3-level-1.ipynb",
        "summary": "3-1描述",
        "warn": "返回題目點選按鈕，進入關卡",
    },
    {
        "id": "chapter-3-level-2",
        "chapter": "第 3 章第二關",
        "level": "3-2",
        "title": "函式工坊",
        "difficulty": "60％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-3-level-2/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-3-level-2.ipynb",
        "summary": "3-2描述",
    },
    {
        "id": "chapter-3-level-3",
        "chapter": "第 3 章第三關",
        "level": "3-3",
        "title": "資料結構",
        "difficulty": "80％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-3-level-3/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-3-level-3.ipynb",
        "summary": "3-3描述",
        "warn": "返回題目點選按鈕，進入關卡",
        "topics": [
            {
                "id": "chapter-3-level-3-1",
                "title": "陣列與串列",
                "description": """請完成下方 `SinglyLinkedList` 類別中標記 `# TODO` 的方法：

1. `append(data)`：在串列「尾端」新增一個節點
2. `insert_at(index, data)`：在指定索引位置插入一個節點（index 從 0 開始）
3. `delete_by_value(data)`：刪除第一個資料值等於 data 的節點，若找不到則不做任何事
4. `to_list()`：回傳一個 Python list，內容為串列中所有節點的資料，方便測試與除錯

完成後執行下方的自我檢查（assert），全部通過即代表本關卡練習任務完成。""",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": """sll = SinglyLinkedList()
sll.append(10)
sll.append(20)
sll.append(30)
assert sll.to_list() == [10, 20, 30], "append 或 to_list 尚未正確完成"

sll.insert_at(1, 15)
assert sll.to_list() == [10, 15, 20, 30], "insert_at 尚未正確完成"

sll.delete_by_value(15)
assert sll.to_list() == [10, 20, 30], "delete_by_value 尚未正確完成"

print("恭喜！基礎任務全部通過，可以繼續挑戰進階任務。")""",
            },
            {
                "id": "chapter-3-level-3-2",
                "title": "認識變數",
                "description": "蘋果的價格為26元，請問小明購買6個蘋果需要多少錢?\t請用value(x,y)計算蘋果總價為何?",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "value(26,6)",
            },
            {
                "id": "chapter-3-level-3-3",
                "title": "認識變數",
                "description": "蘋果的價格為26元，請問小明購買6個蘋果需要多少錢?\t請用value(x,y)計算蘋果總價為何?",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "value(26,6)",
            },
            {
                "id": "chapter-3-level-3-4",
                "title": "認識變數",
                "description": "蘋果的價格為26元，請問小明購買6個蘋果需要多少錢?\t請用value(x,y)計算蘋果總價為何?",
                "starter_code": "# 在這裡寫程式\n",
                "test_code": "value(26,6)",
            },
        ],
    },
]

def auto_convert_levels_to_files(levels_data):
    base_dir = Path("levels")
    base_dir.mkdir(exist_ok=True)

    levels = copy.deepcopy(levels_data)

    for lvl_idx, lvl in enumerate(levels, 1):
        # 1. 建立關卡資料夾，例如：chapter-1-level-1
        lvl_folder_name = f"{lvl['id']}"
        lvl_path = base_dir / lvl_folder_name
        lvl_path.mkdir(exist_ok=True)

        topics = lvl.pop("topics", [])

        with open(lvl_path / "level.json", "w", encoding="utf-8") as f:
            json.dump(lvl, f, ensure_ascii=False, indent=2)

        if topics:
            topics_path = lvl_path / "topics"
            topics_path.mkdir(exist_ok=True)

            for t_idx, topic in enumerate(topics, 1):
                # 建立題目資料夾，例如：chapter-1-level-1-1
                t_folder_name = f"{topic['id']}"
                t_path = topics_path / t_folder_name
                t_path.mkdir(exist_ok=True)

                (t_path / "description.md").write_text(topic.get("description", ""), encoding="utf-8")
                (t_path / "starter.py").write_text(topic.get("starter_code", ""), encoding="utf-8")
                (t_path / "test.py").write_text(topic.get("test_code", ""), encoding="utf-8")

                info = {
                    "id": topic["id"],
                    "title": topic["title"]
                }
                with open(t_path / "info.json", "w", encoding="utf-8") as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)

    print("所有關卡資料夾與 .md/.py 檔案已自動生成至 levels/ 目錄下。")

if __name__ == "__main__":
    auto_convert_levels_to_files(LEVELS)