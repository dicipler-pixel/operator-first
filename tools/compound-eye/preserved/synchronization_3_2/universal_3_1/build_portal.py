"""Build the current Universal 3.1 portal, including the interactive Eye Mixer."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/'build_mixer_portal.py'),run_name='__main__')
