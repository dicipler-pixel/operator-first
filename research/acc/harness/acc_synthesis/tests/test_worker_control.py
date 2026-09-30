import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class WorkerControlTests(unittest.TestCase):
    def test_workers_stop_without_opening_sqlite(self):
        for helper, function in [('charlie', 'controller_stopped'), ('bob', 'controller_stopped'), ('kernel', 'stopped')]:
            spec = importlib.util.spec_from_file_location('control_' + helper, ROOT / f'helpers/{helper}_lane_v1.py')
            lane = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lane)
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / 'continuation').mkdir()
                checkpoint = root / 'continuation/checkpoint.json'
                lane.ROOT = root
                with patch('sqlite3.connect', side_effect=AssertionError('worker accessed database')):
                    checkpoint.write_text(json.dumps({'stopped': False}))
                    lane._control_checked_at = float('-inf')
                    self.assertFalse(getattr(lane, function)())
                    checkpoint.write_text(json.dumps({'stopped': True}))
                    lane._control_checked_at = float('-inf')
                    self.assertTrue(getattr(lane, function)())
                    checkpoint.write_text('incomplete')
                    lane._control_checked_at = float('-inf')
                    self.assertTrue(getattr(lane, function)())
                    checkpoint.unlink()
                    lane._control_checked_at = float('-inf')
                    self.assertTrue(getattr(lane, function)())


if __name__ == '__main__':
    unittest.main()
