import json
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai import types
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from .models import Submission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

import pybryt
import pybryt.student as _student
from pybryt.preprocessors import NotebookPreprocessor
from pybryt.utils import make_secret
import nbformat as _nbformat
import os as _os, dill as _dill
from copy import deepcopy as _deepcopy
from tempfile import mkstemp as _mkstemp
from textwrap import dedent as _dedent
from nbconvert.preprocessors import ExecutePreprocessor as _EP
from textwrap import indent



client=genai.Client(api_key="")

EDITABLE_STUDENT_FILE_TYPES = {".ipynb", ".py", ".txt", ".json", ".md"}
EVALUATABLE_STUDENT_FILE_TYPES = {".ipynb"}

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
        "topics": [
        {
            "id": "chapter-1-level-1-1",
            "title": "認識變數",
            "description":"蘋果的價格為26元，請問小明購買6個蘋果需要多少錢?\t請用value(x,y)計算蘋果總價為何?",
            "starter_code": "# 在這裡寫程式\n",
            "test_code": "value(26,6)",
        },
        ]
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
        "topics": [
        {
            "id": "chapter-1-level-2-1",
            "title": "BMI計算",
            "description": "請定義一個basic(height, weight) 函數，計算BMI判斷過輕、正常、過重。bmi< 18.5為過輕、18.5<=bmi<=24為正常、bmi > 24為過重",
            "starter_code": "# 在這裡寫程式\n",
            "test_code": "print(basic(1.78, 70))\nprint(basic(1.60, 40))\nprint(basic(1.60, 80))",
        },
        ]
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
        "topics": [
        {
            "id": "chapter-1-level-3-1",
            "title": "矩陣相加",
            "description": "請定義一個matrix_add(A,B)函數，計算函數相加。使用for迴圈",
            "starter_code": "# 在這裡寫程式\n",
            "test_code": "A = [[1,2],[3,4]]\nB = [[5,6],[7,8]]\nmatrix_add(A,B)\nA = [[2,1],[0,3]]\nB = [[1,4],[5,2]]\nmatrix_add(A,B)",
        },
        ]
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
        "topics": [
        {
            "id": "chapter-2-level-1-1",
            "title": "等差數列",
            "description": "請建立一個sequence串列後使用公式term = a + i * d計算等差數列。",
            "starter_code": "# 在這裡寫程式\n",
            "test_code": "val = generate_arithmetic_sequence(2,3,5)\nval",
        },
        ]
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
            "user_name": request.user.username if request.user.is_authenticated else "Guest",
        },
    )
    
@login_required
def my_submissions(request):
    submissions = Submission.objects.filter(user=request.user)
    return render(request, "pages/submissions.html", {
        "submissions": submissions
    })

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST) 
        if form.is_valid():  #判定密碼強弱 自動登入並返回首頁
            user = form.save()
            login(request, user)     
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def _teacher_required(user):
    return (
        user.is_authenticated
        and (
            user.is_staff
            or user.is_superuser
            or user.groups.filter(name="Teachers").exists()
        )
    )

class RoleLoginView(LoginView):
    template_name = "registration/login.html"

    def _is_teacher_login(self):
        return self.request.POST.get("next") == "/teacher/files/" or self.request.GET.get("next") == "/teacher/files/"

    def form_valid(self, form):
        user = form.get_user()
        is_teacher = _teacher_required(user)

        if self._is_teacher_login() and not is_teacher:
            form.add_error(None, "學生帳號不能從老師登入入口登入。")
            return self.form_invalid(form)

        if not self._is_teacher_login() and is_teacher:
            form.add_error(None, "老師帳號請使用老師登入入口。")
            return self.form_invalid(form)

        return super().form_valid(form)

def _student_files_dir():
    submissions_dir = Path(settings.BASE_DIR) / "submissions"
    submissions_dir.mkdir(exist_ok=True)
    return submissions_dir

def _safe_student_file(filename):
    submissions_dir = _student_files_dir().resolve()
    file_path = (submissions_dir / filename).resolve()
    if submissions_dir not in file_path.parents or file_path.suffix not in EDITABLE_STUDENT_FILE_TYPES:
        raise PermissionDenied
    return file_path

def _infer_level_from_filename(filename):
    parts = filename.split("_", 2)
    if len(parts) >= 2:
        return parts[1]
    return "unknown-level"

def _find_reference_file(level):
    references_dir = Path(settings.BASE_DIR) / "references"
    candidate_levels = [level]
    if not level.endswith("-1"):
        candidate_levels.append(f"{level}-1")

    for candidate_level in candidate_levels:
        ref_path = references_dir / f"{candidate_level}.pkl"
        if ref_path.exists():
            return ref_path, candidate_level
    return None, candidate_levels[-1]

def _patch_pybryt_execute_notebook():
    def _patched_execute_notebook(nb, nb_path, addl_filenames=[], timeout=1200):
        nb = _deepcopy(nb)
        preprocessor = NotebookPreprocessor()
        nb = preprocessor.preprocess(nb)

        fd, footprint_fp = _mkstemp()
        _os.close(fd)
        safe_fp = footprint_fp.replace("\\", "/")

        nb_dir = _os.path.abspath(_os.path.split(nb_path)[0])
        secret = make_secret()
        ftv = f"frame_tracer_{secret}"

        first_cell = _nbformat.v4.new_code_cell(_dedent(f"""
            import inspect, sys
            from pybryt.execution import FrameTracer
            {ftv} = FrameTracer(inspect.currentframe())
            {ftv}.start_trace(addl_filenames={addl_filenames})
            %cd {nb_dir}
        """))

        last_cell = _nbformat.v4.new_code_cell(_dedent(f"""
            {ftv}.end_trace()
            footprint = {ftv}.get_footprint()
            footprint.filter_out_unpickleable_values()
            import dill
            with open("{safe_fp}", "wb+") as f:
                dill.dump(footprint, f)
        """))

        nb["cells"].insert(0, first_cell)
        nb["cells"].append(last_cell)
        _EP(timeout=timeout, allow_errors=True).preprocess(nb)

        with open(footprint_fp, "rb") as f:
            footprint = _dill.load(f)
        _os.remove(footprint_fp)
        footprint.add_imports(*preprocessor.get_imports())
        footprint.set_executed_notebook(nb)
        return footprint

    _student.execute_notebook = _patched_execute_notebook

def evaluate_student_file(file_path, level=None):
    level = level or _infer_level_from_filename(file_path.name)
    if file_path.suffix not in EVALUATABLE_STUDENT_FILE_TYPES:
        return {
            "filename": file_path.name,
            "level": level,
            "passed": None,
            "steps": None,
            "messages": "此檔案類型不能使用 PyBryt 評測。",
            "feedback": [],
        }

    _patch_pybryt_execute_notebook()
    ref_path, reference_level = _find_reference_file(level)
    if ref_path is None:
        return {
            "filename": file_path.name,
            "level": level,
            "passed": None,
            "steps": None,
            "messages": f"找不到 {level} 或 {reference_level} 的參考答案。",
            "feedback": [],
        }

    reference = pybryt.ReferenceImplementation.load(str(ref_path))
    student_impl = pybryt.StudentImplementation(str(file_path))
    results = student_impl.check(reference)
    result_list = results if isinstance(results, list) else [results]
    first_result = result_list[0]

    feedback = []
    all_passed = True
    for result in result_list:
        if not result.correct:
            all_passed = False
        for ann_res in result.to_dict()["results"]:
            ann = ann_res["annotation"]
            satisfied = ann_res["satisfied"]
            feedback.append({
                "name": ann.get("name", "檢查點"),
                "passed": satisfied,
                "message": ann.get("success_message") if satisfied else ann.get("failure_message"),
            })

    return {
        "filename": file_path.name,
        "level": reference_level,
        "passed": all_passed,
        "steps": student_impl.footprint.num_steps,
        "messages": "\n".join(first_result.messages),
        "feedback": feedback,
    }

@login_required
def teacher_files(request):
    if not _teacher_required(request.user):
        raise PermissionDenied

    submissions_dir = _student_files_dir()
    review_results = []
    if request.method == "POST":
        for path in submissions_dir.iterdir():
            if not path.is_file() or path.suffix not in EVALUATABLE_STUDENT_FILE_TYPES:
                continue
            try:
                review_results.append(evaluate_student_file(path))
            except Exception as e:
                review_results.append({
                    "filename": path.name,
                    "level": _infer_level_from_filename(path.name),
                    "passed": False,
                    "steps": None,
                    "messages": f"評測錯誤：{str(e)}",
                    "feedback": [],
                })

    files = [
        {
            "name": path.name,
            "size": path.stat().st_size,
            "modified_at": datetime.fromtimestamp(path.stat().st_mtime),
            "can_review": path.suffix in EVALUATABLE_STUDENT_FILE_TYPES,
        }
        for path in submissions_dir.iterdir()
        if path.is_file() and path.suffix in EDITABLE_STUDENT_FILE_TYPES
    ]
    files.sort(key=lambda item: item["modified_at"], reverse=True)
    return render(request, "teacher/files.html", {
        "files": files,
        "review_results": review_results,
    })

@login_required
def teacher_file_edit(request, filename):
    if not _teacher_required(request.user):
        raise PermissionDenied

    file_path = _safe_student_file(filename)
    if not file_path.exists() or not file_path.is_file():
        raise PermissionDenied

    message = ""
    review_result = None
    if request.method == "POST":
        try:
            review_result = evaluate_student_file(file_path)
            message = "已完成 PyBryt 評測。"
        except Exception as e:
            review_result = {
                "filename": file_path.name,
                "level": _infer_level_from_filename(file_path.name),
                "passed": False,
                "steps": None,
                "messages": f"評測錯誤：{str(e)}",
                "feedback": [],
            }
            message = "PyBryt 評測失敗。"

    content = file_path.read_text(encoding="utf-8")
    return render(
        request,
        "teacher/file_edit.html",
        {
            "filename": file_path.name,
            "content": content,
            "message": message,
            "review_result": review_result,
        },
    )

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
        只回答python的問題，其他一律回答這不符合我們的關卡內容。
        若是他詢問Lv1-1-1的問題則回答
        def value(x,y):
            if x == 0 or y == 0:
                return "EOFError"
            else:
                return x*y
        並且說明為何要這麼做題目為蘋果價格與數量計算
        若是詢問lv1-2-1的問題則回答
        def basic(h,w):
            bmi= w/(h*h)
            if (bmi < 18.5):
                return "過輕"
            elif (bmi > 24):
                return "過重"
            else:
                return "正常"
        並且說明為何要這麼做題目為bmi測量
        若是詢問lv1-3-1的問題則會回答
        使用一個for迴圈來表示row的值再在裡面套個for迴圈表示col的值，像是這樣:
        def matrix_add(A,B):
        ...
        ...
        for i in range(row):
            row = []
            for i in range(col):
                ...
        若是詢問lv2-1-1的問題則回答
        def sequence(a,d,n):
        ...
        ...
        for i in range(n):
                term = a + i * d
            sequence.append(term)"""),
                ],
            )
            try:
                #1.優先嘗試呼叫最新的3.5模型
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=[user_message],
                    config=generate_content_config,
                )
            except Exception as model_err:
                # 2. 如果遇到503錯誤不論是透過 code 屬性還是字串比對），觸發降級機制
                err_msg = str(model_err)
                err_code = getattr(model_err, 'code', None) 
                if err_code == 503 or "503" in err_msg or "Service Unavailable" in err_msg:
                    # 降級改用容量較大、穩定的2.5模型
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[user_message],
                        config=generate_content_config,
                    )
                else:
                    # 如果不是503，就把原本的錯誤往外丟給外層 catch 處理
                    raise model_err
            
            return JsonResponse({"reply": response.text})
        
        except json.JSONDecodeError:
            return JsonResponse({"error":"無效的 JSON 格式"},status=400)
        
        except Exception as e:
            if "503" in str(e):
               return JsonResponse({"error":"模型忙碌中，請稍後再試。"},status=500)
            else:
                raise
            # return JsonResponse({"error":f"系統錯誤: {str(e)}"},status=500)    
            
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
    try:
        review_result = evaluate_student_file(file_path, level)
        all_passed = review_result["passed"]

        if request.user.is_authenticated:
            Submission.objects.create(
                user=request.user,
                level=level, 
                filename=filename,
                passed=all_passed,
            )

        return JsonResponse({
            "message": "全部通過！" if all_passed else "部分未通過",
            "filename": filename,
            "passed": all_passed,
            "steps": review_result["steps"],
            "messages": review_result["messages"],
            "feedback": review_result["feedback"],
        })

    except Exception as e:
        return JsonResponse({
            "message": f"已儲存 {filename}，鑑定錯誤：{str(e)}",
            "filename": filename,
            "passed": False,
            "feedback": []
        })
