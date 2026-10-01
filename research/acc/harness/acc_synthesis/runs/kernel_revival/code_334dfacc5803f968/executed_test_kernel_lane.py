import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('kernel_lane',ROOT/'helpers/kernel_lane_v1.py')
lane=importlib.util.module_from_spec(spec);spec.loader.exec_module(lane)
core=lane.official_checker.load_kernel()[0]

class KernelLaneTests(unittest.TestCase):
    def test_foreign_road_suffix_minimum_and_direction(self):
        target=((1,),(2,))
        donor=core.apply_move(core.apply_move(target,2),6)
        path=[7,3];trace=lane.replay(core,donor,path)
        graph={target:set()};lane.add_trace(core,graph,trace,path)
        d,p,complete=lane.bfs(graph,target)
        self.assertTrue(complete);self.assertEqual(d[donor],2)
        self.assertEqual(lane.suffix_path(core,p,donor),path)
        for s,edges in graph.items():
            for t,m in edges:self.assertEqual(core.apply_move(s,m),t)

    def test_foreign_route_join_by_paid_bridge(self):
        import time
        target=((1,),(2,));donor=core.apply_move(target,2)
        target_start=core.apply_move(donor,10)
        graph={target:set()};lane.add_trace(core,graph,[donor,target],[3])
        sd,sp,_=lane.bfs(graph,target)
        best,c=lane.bridge_search(core,{target_start:[]},sd,sp,None,
             deadline=time.monotonic()+2,node_cap=1000,max_length=100,depth=1,stop_check=lambda:False)
        self.assertEqual(len(best),2)
        self.assertEqual(lane.replay(core,target_start,best)[-1],target)
        self.assertGreater(c['exact_graph_collisions'],0)

    def test_unpaid_relator_symmetry_never_matches(self):
        target=((1,),(2,));graph={target:set()}
        d,p,_=lane.bfs(graph,target)
        self.assertNotIn(((2,),(1,)),d)
        self.assertNotIn(((-1,),(2,)),d)

    def test_cap_and_stop_are_bounded_misses(self):
        import time
        start=((1,2),(2,))
        _,c=lane.bridge_search(core,{start:[]},{},{},None,deadline=time.monotonic()+2,
          node_cap=1,max_length=100,depth=2,stop_check=lambda:False)
        self.assertEqual(c['termination_reason'],'node_cap');self.assertEqual(c['admitted_records'],1)
        _,c=lane.bridge_search(core,{start:[]},{},{},None,deadline=time.monotonic()+2,
          node_cap=100,max_length=100,depth=2,stop_check=lambda:True)
        self.assertEqual(c['termination_reason'],'controller_stop')

    def test_invalid_saved_move_rejected(self):
        for m in [True,-1,14]:
            with self.assertRaises(ValueError):lane.replay(core,((1,),(2,)),[m])

if __name__=='__main__':unittest.main()
