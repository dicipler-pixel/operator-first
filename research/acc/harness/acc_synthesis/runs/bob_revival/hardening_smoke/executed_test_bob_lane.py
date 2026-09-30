import sys
import unittest
from types import SimpleNamespace
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

    def test_paid_transfer_and_absent_seed(self):
        budget=bob.Budget(10,10000,1024)
        donor={'start':[(2,1,-2),(2,)],'moves':[9]}
        result=bob.transfer(self.core,bob.T,donor,((1,),(2,)),{1:(1,),2:(2,)},budget,3)
        self.assertIsNotNone(result)
        line,detail=result
        self.assertEqual(len(line),2)
        self.assertEqual(detail['alignment_moves'],1)
        self.assertEqual(bob.replay(self.core,bob.T,line),bob.T)
        self.assertEqual(bob.shortest_saved(self.core,bob.T,[]),(None,0,0))
        self.assertEqual(bob.own_seeds('ac-does-not-exist',None),[])

    def test_limits_and_reuse_protection(self):
        args=SimpleNamespace(wall_seconds=180,node_cap=600000,memory_mib=1024,target_length=47)
        bob.validate_limits(args)
        for key,value in [('wall_seconds',float('nan')),('wall_seconds',181),('node_cap',600001),
                          ('memory_mib',1025),('target_length',-1)]:
            bad=SimpleNamespace(**vars(args));setattr(bad,key,value)
            with self.assertRaises(ValueError):bob.validate_limits(bad)

if __name__=='__main__':unittest.main()
