import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'helpers'))
sys.path.insert(0,str(ROOT))
import bob_lane_v1 as bob
import official_checker

class BobLaneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core,_,_,cls.challenges=official_checker.load_kernel()
    def test_nielsen_inverse_and_unit_conjugators(self):
        for a,b in bob.autos():
            inverse=bob.inverse_auto(a,b)
            self.assertIsNotNone(inverse)
            self.assertEqual(bob.sub(a,inverse),(1,))
            self.assertEqual(bob.sub(b,inverse),(2,))
            # An atomic conjugation by x after pulling x -> xy costs two moves.
            s=((2,1,-2),(2,))
            for m in (6,8,10,12):
                p=bob.pullback([m],inverse)
                a1=bob.replay(self.core,s,p)
                word=inverse[1 if m in (6,10) else 2]
                k=0 if m<10 else 1
                w=bob.red(word+s[k]+bob.inv(word))
                expected=(w,s[1]) if k==0 else (s[0],w)
                self.assertEqual(a1,expected)
    def test_saved_target_exact_and_bridge(self):
        c=self.challenges['ac-00012'];start=tuple(tuple(w) for w in c['initial_relators'])
        import json
        paths=[r['moves'] for r in json.loads(bob.ROUTES.read_text())['routes'] if r['row_id']=='ac-00012']
        best,valid,n=bob.shortest_saved(self.core,start,paths)
        self.assertEqual(valid,3)
        self.assertEqual(bob.replay(self.core,start,best),bob.T)
        self.assertLessEqual(len(best),52)
        budget=bob.Budget(10,10000,1024)
        p=bob.bridge_word(self.core,(1,2,-1),(2,),0,budget,4)
        self.assertIsNotNone(p)
        self.assertEqual(bob.replay(self.core,((1,2,-1),(2,)),p)[0],(2,))

if __name__=='__main__':unittest.main()
