"""Build the current portal. The original Universal 2 builder is preserved."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/'build_horizon_portal.py'),run_name='__main__')
