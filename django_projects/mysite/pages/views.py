import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


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


@csrf_exempt
def submit_solution(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST requests are accepted."}, status=405)

    level = request.POST.get("level", "unknown-level").replace("/", "-").replace("\\", "-")
    player = request.POST.get("player", "player").replace("/", "-").replace("\\", "-")
    code = request.POST.get("code", "").strip()

    if not code:
        return JsonResponse({"message": "請先輸入要提交的程式碼。"}, status=400)

    submitted_at = datetime.now().strftime("%Y%m%d-%H%M%S")
    submissions_dir = Path(settings.BASE_DIR) / "submissions"
    submissions_dir.mkdir(exist_ok=True)
    filename = f"{submitted_at}_{level}_{player}.py"
    file_path = submissions_dir / filename
    file_path.write_text(code + "\n", encoding="utf-8")

    return JsonResponse(
        {
            "message": f"已儲存到後端 submissions/{filename}",
            "filename": filename,
        }
    )
