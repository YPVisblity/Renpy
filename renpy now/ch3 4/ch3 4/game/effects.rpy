# ==========================================
# effects.rpy - 專門存放背景與圖片特效的檔案
# ==========================================

# ---- 1. 自訂轉場特效 (Transitions) ----

# 快速淡入淡出（0.5秒）
define flash_cut = Fade(0.1, 0.0, 0.3, color="#fff") # 閃白轉場
define slow_dissolve = Dissolve(2.0)                # 超慢融解

# ---- 2. 自訂動態切換特效 (Transforms) ----

# 背景稍微放大並緩慢往上移動（製造運鏡感）
transform bg_pan_up:
    subpixel True
    anchor (0.5, 0.5) pos (0.5, 0.5) zoom 1.0
    # 費時 5 秒，慢慢放大到 1.15 倍並往上移
    ease 5.0 zoom 1.15 yalign 0.3

# 驚悚場景：背景劇烈震動
transform bg_shake:
    subpixel True
    anchor (0.5, 0.5) pos (0.5, 0.5)
    linear 0.05 xoffset 10 yoffset -5
    linear 0.05 xoffset -10 yoffset 5
    linear 0.05 xoffset 5 yoffset 10
    linear 0.05 xoffset -5 yoffset -10
    linear 0.05 xoffset 0 yoffset 0
    repeat 3 # 重複震動 3 次

# 昏迷特效：背景先模糊再變暗
transform bg_faint:
    anchor (0.5, 0.5) pos (0.5, 0.5)
    linear 1.5 blur 20 matrixcolor BrightnessMatrix(-0.5)