import json, requests, io, sys

class StudentNotebook:
    def __init__(self):
        self.cells = []          # [{"source": "...", "outputs": []}]
        self._namespace = {}
        self._exec_count = 0

    def add_cell(self, source=""):
        self.cells.append({"source": source, "outputs": [], "count": None})
        return len(self.cells) - 1

    def run_cell(self, idx):
        cell = self.cells[idx]
        self._exec_count += 1
        cell["count"] = self._exec_count

        old_stdout = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            exec(compile(cell["source"], "<cell>", "exec"), self._namespace)
            out = buf.getvalue()
            cell["outputs"] = [{"output_type": "stream", "text": out}] if out else []
        except Exception as e:
            cell["outputs"] = [{"output_type": "error", "evalue": str(e)}]
        finally:
            sys.stdout = old_stdout
        return cell["outputs"]

    def to_ipynb(self):
        """把目前所有 cell 打包成標準 .ipynb JSON"""
        nb_cells = []
        for c in self.cells:
            nb_cells.append({
                "cell_type": "code",
                "source": [c["source"]],
                "metadata": {},
                "outputs": c["outputs"],
                "execution_count": c["count"]
            })
        return {
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {"kernelspec": {"name": "python3"}},
            "cells": nb_cells
        }

    def submit(self, django_url, student_id, assignment_id):
        """送出到 Django，回傳 PyBryt 批改結果"""
        ipynb_json = json.dumps(self.to_ipynb())
        try:
            r = requests.post(
                django_url + "/api/grade/",
                json={
                    "student_id": student_id,
                    "assignment_id": assignment_id,
                    "notebook": json.loads(ipynb_json)
                },
                timeout=30
            )
            return r.json()   # {"passed": True/False, "messages": [...], "score": 85}
        except Exception as e:
            return {"passed": False, "messages": [str(e)], "score": 0}