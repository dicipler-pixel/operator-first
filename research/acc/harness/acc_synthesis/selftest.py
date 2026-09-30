#!/usr/bin/env python3
"""Run local fault tests. These do not call a model or validate real ACC routes."""
from pathlib import Path
import sys
import unittest
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent))
suite=unittest.defaultTestLoader.discover(str(root/'tests'))
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
