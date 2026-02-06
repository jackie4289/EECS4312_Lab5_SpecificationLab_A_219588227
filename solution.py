import importlib.util
import os
import sys

_here = os.path.dirname(__file__)
_target = os.path.join(_here, "project-folder", "solution.py")

_spec = importlib.util.spec_from_file_location("project_folder_solution", _target)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)  # type: ignore[attr-defined]

suggest_slots = _mod.suggest_slots

__all__ = ["suggest_slots"]
