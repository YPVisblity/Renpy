screen notebook_ui():
    default nb = StudentNotebook()
    default result = None
    default submitting = False

    vbox:
        spacing 8
        xfill True

        # ── Cell 列表 ──
        for i, cell in enumerate(nb.cells):
            frame:
                background "#1e1e2e"
                padding (12, 8)
                xfill True
                vbox:
                    hbox:
                        text f"In [{cell['count'] or ' '}]:" color "#888" size 13
                        textbutton "▶ Run":
                            action Function(nb.run_cell, i)
                    # 模擬 code editor (實際可換成 renpy input)
                    input:
                        value ScreenVariableInputValue("nb.cells[i]['source']")
                        color "#cdd6f4"
                        size 14

                    # Output 區域
                    if cell["outputs"]:
                        for out in cell["outputs"]:
                            if out["output_type"] == "stream":
                                text out["text"] color "#a6e3a1" size 13
                            else:
                                text out.get("evalue","error") color "#f38ba8" size 13

        # ── 新增 Cell ──
        textbutton "+ Add cell":
            action Function(nb.add_cell)

        null height 16

        # ── 送出按鈕 ──
        if not submitting:
            textbutton "Submit for grading":
                action [
                    SetScreenVariable("submitting", True),
                    Function(do_submit, nb)
                ]
        else:
            text "Submitting..." color "#fab387"

        # ── 批改結果 ──
        if result is not None:
            frame:
                background "#313244"
                padding (16, 12)
                xfill True
                vbox:
                    spacing 6
                    if result["passed"]:
                        text "PASSED" color "#a6e3a1" size 16
                    else:
                        text "NEEDS WORK" color "#f38ba8" size 16
                    text f"Score: {result['score']}" size 14
                    for msg in result["messages"]:
                        text f"• {msg}" size 13 color "#cdd6f4"