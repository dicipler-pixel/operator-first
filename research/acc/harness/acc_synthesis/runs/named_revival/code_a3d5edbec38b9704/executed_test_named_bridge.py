import unittest
from helpers.named_bridge_lane_v1 import neighborhood, distances
from helpers.kernel_lane_v1 import replay, prefix_path, suffix_path
import official_checker

class NamedBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core,_,_,_=official_checker.load_kernel()

    def test_predecessors_reconstruct_paid_forward_bridge(self):
        goal=((1,),(2,))
        near,generated=neighborhood(self.core,goal,'predecessor')
        self.assertEqual(generated,210)
        for node,moves in near.items():
            self.assertLessEqual(len(moves),2)
            self.assertEqual(replay(self.core,node,moves)[-1],goal)

    def test_successors_reconstruct_paid_prefix_and_cover_all_strings(self):
        start=((1,2,-1),(2,1))
        near,generated=neighborhood(self.core,start,'successor')
        self.assertEqual(generated,210)
        for node,moves in near.items():
            self.assertEqual(replay(self.core,start,moves)[-1],node)
        for first in range(14):
            for second in range(14):
                self.assertIn(replay(self.core,start,[first,second])[-1],near)

    def test_saved_graph_prefix_suffix_and_disconnected_origin(self):
        goal=((1,),(2,)); start=self.core.apply_move(goal,2)
        graph={start:{(goal,self.core.INVERSE_MOVE[2])},goal:{(start,2)}}
        pref,pp=distances(graph,start,lambda:None)
        suff,sp=distances(graph,goal,lambda:None)
        self.assertEqual(replay(self.core,start,prefix_path(pp,goal))[-1],goal)
        self.assertEqual(replay(self.core,start,suffix_path(self.core,sp,start))[-1],goal)
        missing=((1,1),(2,2))
        dist,_=distances(graph,missing,lambda:None)
        self.assertEqual(dist,{missing:0})

    def test_capacity_failure_is_not_complete_neighborhood(self):
        used=[0]
        def limited():
            used[0]+=1
            if used[0]>3:raise InterruptedError('record_cap')
        with self.assertRaises(InterruptedError):
            neighborhood(self.core,((1,),(2,)),'successor',limited)

if __name__=='__main__':unittest.main()
