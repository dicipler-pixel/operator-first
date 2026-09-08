"""Compatibility entry point: build the current synchronized portal."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/"build_portal.py"),run_name="__main__")
