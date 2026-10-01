# relator-swap relabelling of move ids: (r0,r1) -> (r1,r0)
SW={0:1,1:0,2:4,3:5,4:2,5:3,6:10,7:11,8:12,9:13,10:6,11:7,12:8,13:9}
def swap(path): return [SW[m] for m in path]
