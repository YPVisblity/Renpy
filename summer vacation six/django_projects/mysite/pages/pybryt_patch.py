import pybryt.student as _student
from pybryt.preprocessors import NotebookPreprocessor
from pybryt.utils import make_secret
import nbformat as _nbformat
import os as _os
import dill as _dill
from copy import deepcopy as _deepcopy
from tempfile import mkstemp as _mkstemp
from textwrap import dedent as _dedent
from nbconvert.preprocessors import ExecutePreprocessor as _EP
import time as _time


PYBRYT_EXECUTION_TIMEOUT_SECONDS = 120

PYBRYT_PATCHED = False

def patch_pybryt_execute_notebook():
    global PYBRYT_PATCHED
    if PYBRYT_PATCHED:
        return
    def _patched_execute_notebook(nb, nb_path, addl_filenames=[], timeout=PYBRYT_EXECUTION_TIMEOUT_SECONDS):
        nb = _deepcopy(nb)
        preprocessor = NotebookPreprocessor()

        preprocessor.preprocessors = [
            p for p in preprocessor.preprocessors
            if type(p).__name__ != "IntermediateVariablePreprocessor"
        ]

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
   
        try:
            with open(footprint_fp,"rb") as f:
                footprint=_dill.load(f)

        except Exception as e:
            raise RuntimeError(
                f"PyBryt footprint 建立失敗: {e}"
            )
        finally:
            if _os.path.exists(footprint_fp):
                _os.remove(footprint_fp)

        footprint.add_imports(*preprocessor.get_imports())
        footprint.set_executed_notebook(nb)
        return footprint

    _student.execute_notebook = _patched_execute_notebook
    PYBRYT_PATCHED = True
