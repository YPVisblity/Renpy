# Code Quest

一個以 Django 打造的程式教學平台，前端利用Renpy建立敘事故事，內建瀏覽器端 Jupyter Notebook 風格編輯器（透過 [Pyodide](https://pyodide.org/) 在瀏覽器裡直接執行 Python），搭配 [PyBryt](https://github.com/microsoft/pybryt) 自動評測學生程式碼，並整合 Google Gemini 提供 AI 問答輔助。

## 功能特色

- **關卡式學習地圖**：章節、關卡、題目三層結構，支援點數解鎖、額外挑戰題解鎖、前一章全破自動解鎖等多種解鎖規則
- **瀏覽器內建 Notebook**：Pyodide 驅動的 Cell 編輯器，不需安裝本地 Python 環境即可寫程式、執行、看輸出
- **自動評測**：學生提交後，後端用 PyBryt 比對執行足跡與參考解答，即時回饋通過與否
- **點數 / 商店系統**：通過關卡獲得點數，可用點數解鎖進階關卡或購買商店道具
- **討論區**：每道題目底下的留言、按讚、回覆功能
- **AI 問答**：整合 Gemini API，針對 Python 課程內容提供輔助說明
- **教師後台**：教師/管理員可檢視、重新評測學生繳交的檔案

## 技術架構

| 項目 | 說明 |
|---|---|
| 後端框架 | Django |
| 資料庫 | SQLite（開發環境預設，可換成 MySQL） |
| 前端執行環境 | Pyodide（瀏覽器內 WebAssembly Python） |
| 劇情敘事引擎 | [Ren'Py](https://www.renpy.org/)（匯出成網頁版，以 iframe 嵌入每關的「劇情」分頁；內容原始碼另外維護在 [YPVisblity/chapter_python](https://github.com/YPVisblity/chapter_python)） |
| 自動評測 | PyBryt + nbformat |
| AI 問答 | Google Gemini API（`google-genai`） |
| Email | Resend（透過 SMTP） |

## 安裝與執行

### 0. 取得專案原始碼

```bash
git clone https://github.com/YPVisblity/Renpy.git
cd Renpy
```

本專案支援兩種環境安裝方式：`venv + pip`（跨平台，推薦給非 Windows 使用者），或 `conda`（適合已經在用 Anaconda / Miniconda 的人，尤其是原作者的 Windows 開發環境）。兩種擇一即可，不用都裝。

### 方式一：venv + pip（跨平台）

#### 1. 建立虛擬環境

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 2. 安裝套件

```bash
pip install -r requirements.txt
```

### 方式二：conda（用 `pythonclean.yaml` 還原環境）

專案根目錄下的 `pythonclean.yaml` 是用 `conda env export` 匯出的完整環境快照，包含 Python 版本、conda 套件、以及所有 pip 套件（Django、pybryt、nbformat、google-genai 等）。

#### 1. 安裝 Anaconda 或 Miniconda

先確認電腦上有 `conda` 指令，沒有的話先安裝 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)（比 Anaconda 輕量，只裝 conda 本身，之後再依需求裝套件）。

#### 2. 平台注意事項

`pythonclean.yaml` 是在 **Windows** 上匯出的，裡面像 `ucrt`、`vc14_runtime`、`vs2015_runtime`、`libwinpthread` 這幾個都是 Windows 專屬的系統相依套件。

- **在 Windows 上**：可以直接用這份 yaml 還原環境。
- **在 macOS / Linux 上**：直接 `conda env create -f pythonclean.yaml` 會因為找不到這些 Windows 套件而失敗（`PackagesNotFoundError`）。macOS / Linux 使用者建議改用上面的「方式一：venv + pip」，或參考下方「跨平台版本」自己重新匯出一份。

#### 3. 用 yaml 建立環境（Windows）

```bash
conda env create -f pythonclean.yaml
```
或者利用anaconda Navigator裡的import載入yaml檔

這會依照 yaml 裡 `name: pythonclean` 建立一個叫 `pythonclean` 的 conda 環境，並自動安裝所有 conda 套件跟 pip 套件（`pip:` 區塊底下列出的 Django、pybryt、nbformat 等，會在 conda 套件裝完後自動用 pip 裝進同一個環境）。

#### 4. 啟用環境

```bash
conda activate pythonclean
```

之後終端機前面出現 `(pythonclean)` 字樣，就代表目前在這個環境裡，執行 `python manage.py runserver` 等指令都會使用這個環境裡的套件版本。

#### 5. 驗證安裝是否成功

```bash
python -c "import django, pybryt, nbformat; print(django.get_version())"
```

能正常印出 Django 版本、沒有噴 `ModuleNotFoundError`，就代表環境沒問題。

#### 常用指令備忘

```bash
# 列出目前有哪些 conda 環境
conda env list

# 之後如果 yaml 有更新，同步更新既有環境（不用整個刪掉重建）
conda env update -f pythonclean.yaml --prune

# 離開目前環境
conda deactivate

# 整個刪除這個環境（環境設定壞掉、想重來時用）
conda env remove -n pythonclean

# 匯出「跨平台版本」的 yaml（去掉 build hash，方便分享給 Mac/Linux 同學）
conda env export --no-builds > pythonclean-cross-platform.yaml
```

`--no-builds` 匯出的版本會拿掉每個套件後面那串平台專屬的 build 編號（例如 `h2bbff1b_6`），只保留套件名稱跟版本號，其他平台安裝時比較不會因為 build 對不上而失敗；但要注意這樣沒辦法 100% 保證版本一致，遇到某些套件在別的平台上剛好沒有對應版本時，還是可能要手動調整。

### 共用步驟：設定環境變數、建立資料庫、啟動伺服器

不管用哪種方式安裝套件，接下來的步驟都一樣：

#### 設定環境變數

在專案根目錄（跟 `manage.py` 同一層）建立 `.env` 檔案，內容如下：

```env
GEMINI_API_KEY=你的_Gemini_API_Key
RESEND_API_KEY=你的_Resend_API_Key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```
這裡我會給env檔

> `GEMINI_API_KEY` 是 AI 問答功能需要的金鑰；`RESEND_API_KEY`、`DEFAULT_FROM_EMAIL` 是寄送密碼重設信等系統郵件用的，沒有這些功能可以先留空，但 `.env` 檔本身要存在，程式才讀得到 `load_dotenv()`。

#### 建立資料庫

```bash
python manage.py migrate
```

#### 建立管理員帳號（用來登入 `/admin/`、審核學生繳交的檔案）

```bash
python manage.py createsuperuser
```
gmail中會給帳號密碼，不用額外新增。

#### 啟動開發伺服器

```bash
python manage.py runserver
```

啟動後，瀏覽器打開 [http://127.0.0.1:8000](http://127.0.0.1:8000) 即可看到首頁。

## 課程內容結構

關卡與題目資料放在 `levels/` 資料夾底下，依照以下結構組織：

```
levels/
└── chapter-1-level-1/
    ├── level.json          # 這一關的基本資訊（標題、章節、劇情連結等）
    └── topics/
        └── topic-1/
            ├── info.json        # 題目的 id、標題
            ├── description.md   # 題目說明
            ├── starter.py       # 給學生的預設程式碼（含自我檢查）
            ├── example_code.py  # 示範用的已完成程式碼
            └── test.py          # 提交後自動附加執行、供 PyBryt 比對用
```

新增關卡或題目時，只要照這個資料夾結構放好對應檔案，伺服器重啟後就會自動被載入（詳見 `pages/level_loader.py`）。

## 自動評測（PyBryt）運作方式

1. 學生提交的 notebook 會被附加上對應題目的 `test.py`。
2. 整份 notebook 在後端實際執行一次。
3. PyBryt 會將執行過程中出現過的變數值，拿去跟 `references/` 資料夾內對應的 `.pkl` 參考答案比對，決定每個檢查點是否通過。

`.pkl` 參考答案需要另外用該題的正確解答 notebook 搭配 `pybryt.ReferenceImplementation.compile()` 產生，並放到 `references/<題目id>.pkl`。

## 專案結構（節錄）

```
mysite/          # Django 專案設定（settings.py、urls.py）
pages/           # 主要 app：關卡地圖、提交評測、解鎖邏輯、AI 問答
blog/            # 附屬 app 可以忽略
polls/           # 附屬 app 可以忽略
levels/          # 課程內容（章節 / 關卡 / 題目）
references/      # PyBryt 參考答案（.pkl）
submissions/     # 學生提交紀錄（自動建立）
```
