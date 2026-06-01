import json
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai import types
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

client=genai.Client(api_key="")

LEVELS = [
    {
        "id": "chapter-1-level-1",
        "chapter": "第 1 章第一關",
        "level": "1-1",
        "title": "變數港口",
        "difficulty": "20％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-1-level-1/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-1-level-1.ipynb",
        "summary": "1-1描述",
    },
    {
        "id": "chapter-1-level-2",
        "chapter": "第 1 章第二關",
        "level": "1-2",
        "title": "輸入溪谷",
        "difficulty": "20％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-1-level-2/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-1-level-2.ipynb",
        "summary": "1-2描述",
    },
    {
        "id": "chapter-1-level-3",
        "chapter": "第 1 章第三關",
        "level": "1-3",
        "title": "字串營地",
        "difficulty": "20％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-1-level-3/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-1-level-3.ipynb",
        "summary": "1-3描述",
    },
    {
        "id": "chapter-2-level-1",
        "chapter": "第 2 章第一關",
        "level": "2-1",
        "title": "條件森林",
        "difficulty": "40％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-2-level-1/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-2-level-1.ipynb",
        "summary": "2-1描述",
    },
    {
        "id": "chapter-2-level-2",
        "chapter": "第 2 章第二關",
        "level": "2-2",
        "title": "分支吊橋",
        "difficulty": "40％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-2-level-2/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-2-level-2.ipynb",
        "summary": "2-2描述",
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
        "title": "資料城堡",
        "difficulty": "80％",
        "story_url": "http://127.0.0.1:8080/renpy/chapter-3-level-3/",
        "game_url": "http://127.0.0.1:8888/notebooks/chapter-3-level-3.ipynb",
        "summary": "3-3描述",
    },
]


def home(request):
    levels_by_id = {level["id"]: level for level in LEVELS}
    return render(
        request,
        "pages/home.html",
        {
            "levels": LEVELS,
            "levels_json": json.dumps(levels_by_id, ensure_ascii=False),
        },
    )
    
#@login_required   
def ai_chat(request):
    if request.method =="POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            if not user_message:
                return JsonResponse({"error":"輸入內容不能為空"},status=400)
            #google search tools
            #極度消耗token,所以先暫停
            #tools= [types.Tool(googleSearch=types.GoogleSearch()),]
            # 思考程度與關卡指定 （模型配置）
            generate_content_config = types.GenerateContentConfig(
                #tools=tools 購買額度再去使用 先設定成None
                tools=None,
                system_instruction=[
                    types.Part.from_text(text="""只利用到 python 的技巧以及導入numpy 等等套件 
        https://steam.oxxostudio.tw/category/python/info/start.html
        參考這份steam教育學習網站的python 技巧
        只回答python的問題，其他一律回答這不符合我們的關卡內容。"""),
                ],
            )
            
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=[user_message],
                config=generate_content_config,
            )
            return JsonResponse({"reply":response.text})
        
        except json.JSONDecodeError:
            return JsonResponse({"error":"無效的 JSON 格式"},status=400)
        
        except Exception as e:
            return JsonResponse({"error":f"系統錯誤: {str(e)}"},status=500)     
    return render(request,'ai/ai_chat.html')
    
@csrf_exempt
def submit_solution(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST requests are accepted."}, status=405)

    level = request.POST.get("level", "unknown-level").replace("/", "-").replace("\\", "-")
    player = request.POST.get("player", "player").replace("/", "-").replace("\\", "-")
    notebook_json = request.POST.get("notebook", "").strip()

    if not notebook_json:
        return JsonResponse({"message": "請先輸入要提交的程式碼。"}, status=400)

    try:
        notebook_data = json.loads(notebook_json)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Notebook 格式錯誤。"}, status=400)

    submitted_at = datetime.now().strftime("%Y%m%d-%H%M%S")
    submissions_dir = Path(settings.BASE_DIR) / "submissions"
    submissions_dir.mkdir(exist_ok=True)
    filename = f"{submitted_at}_{level}_{player}.ipynb"
    file_path = submissions_dir / filename
    file_path.write_text(
        json.dumps(notebook_data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    # PyBryt 鑑定
    try:
        ref_path = Path(settings.BASE_DIR) / "references" / f"{level}.pkl"
        if not ref_path.exists():
            return JsonResponse({
                "message": f"已儲存 {filename}（找不到此關卡的參考答案）",
                "filename": filename,
                "passed": None,
                "feedback": []
            })

        reference = pybryt.ReferenceImplementation.load(str(ref_path))
        student_impl = pybryt.StudentImplementation(str(file_path))
        results = student_impl.check(reference)

        feedback = []
        all_passed = True
        for res in (results if isinstance(results, list) else [results]):
            if not res.correct:
                all_passed = False
            for ann_res in res.results:
                feedback.append({
                    "name": ann_res.name or "檢查點",
                    "passed": ann_res.satisfied,
                    "message": ann_res.failure_message if not ann_res.satisfied else "通過",
                })

        return JsonResponse({
            "message": "✅ 全部通過！" if all_passed else "❌ 部分未通過",
            "filename": filename,
            "passed": all_passed,
            "feedback": feedback,
        })

    except Exception as e:
        return JsonResponse({
            "message": f"已儲存 {filename}，鑑定錯誤：{str(e)}",
            "filename": filename,
            "passed": False,
            "feedback": []
        })
