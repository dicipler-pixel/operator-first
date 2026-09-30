import gzip,json,tempfile,unittest
from pathlib import Path
from acc_synthesis.helpers.kernel_lane_v1 import write_graph_archive


class AtomicGraphTests(unittest.TestCase):
    def test_success_publishes_complete_gzip(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'graph.json.gz';value={'states':[[[1],[2]]],'edges':[]}
            write_graph_archive(p,value)
            self.assertEqual(json.loads(gzip.decompress(p.read_bytes())),value)
            self.assertFalse(p.with_name(p.name+'.partial').exists())

    def test_failed_stream_keeps_previous_final_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'graph.json.gz';p.write_bytes(b'previous-final')
            with self.assertRaises(TypeError):write_graph_archive(p,{'bad':object()})
            self.assertEqual(p.read_bytes(),b'previous-final')
            self.assertTrue(p.with_name(p.name+'.partial').exists())
