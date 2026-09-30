from lib import *
import json
print(list(CH['ac-03855'].keys()))
s,t=st('ac-03855'); print('03855 start',S(s[0]),S(s[1]),'target',S(t[0]),S(t[1]))
for x in traj(s,[0,7,3,7,5,1,6,13,13,5,3,3,3,3,3,3,3,3]): print(x)
for cid in ['ac-08441','ac-06010','ac-00724','ac-08692','ac-02255','ac-07069']:
    s,t=st(cid); print(cid,S(s[0]),S(s[1]),'->',S(t[0]),S(t[1]))
