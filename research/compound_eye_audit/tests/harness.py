import importlib.util, json, sys, traceback, numpy as np
U='/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/mixer51/unz/Compound_Eye_Matrix_Mixer_Canonical_5_1/engines/domain_plugins/'
R='/home/user/operator-first/tools/compound-eye/plugins/installed/'
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
RESULTS=[]
def check(eye,fn,test,expected,got,ok,note=''):
    RESULTS.append({'eye':eye,'function':fn,'test':test,'expected':str(expected)[:160],'got':str(got)[:160],'verdict':'PASS' if ok else 'FAIL','note':note})
    print(('PASS ' if ok else 'FAIL ')+eye+' :: '+test+('' if ok else f'  expected={str(expected)[:80]} got={str(got)[:80]}'))
def run(f,case):
    try: return f({'case':case})
    except Exception as e: return {'_status':'exception','reason':repr(e)}
def blocked(r): return isinstance(r,dict) and r.get('_status') in ('blocked','exception')
def save(name): json.dump(RESULTS,open(f'/tmp/claude-0/-home-user-operator-first/134a87db-34f4-5773-8170-2c301f6ca866/scratchpad/eye_audit/{name}.json','w'),indent=1)
