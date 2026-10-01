"""Isolated lease/audit regression; never reads or mutates production tasks."""
import hashlib,json,shutil,sqlite3,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from runtime import Store,HarnessError
from helpers.audit_artifacts import audit_all
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'state').mkdir();(p/'continuation').mkdir()
 s=Store(p/'state/ledger.sqlite3');task=s.enqueue('code_search',{'key':'fixture'},'fixture');lease=s.claim(task_id=task)
 result={'kind':'bounded_miss','evidence':[]};(p/'result.json').write_text(json.dumps(result))
 cp={'attempts':[{'key':'fixture','kind':'bounded_miss','result_path':'result.json','result_sha256':hashlib.sha256((p/'result.json').read_bytes()).hexdigest()}]}
 (p/'continuation/checkpoint.json').write_text(json.dumps(cp))
 try:audit_all(p,sync=True)
 except ValueError as e:assert 'conflicts with local task' in str(e)
 else:raise AssertionError('Live lease incorrectly accepted as terminal')
 try:s.finish(task,'foreign-token',result)
 except HarnessError as e:assert e.code=='stale_lease'
 else:raise AssertionError('Foreign token accepted')
 s.finish(task,lease['token'],result);audit_all(p,sync=True)
 # Cold copy deliberately excludes WAL: the explicit barrier must have put
 # completion in the main database, not just an open connection's view.
 cold=p/'cold.sqlite3';shutil.copy2(p/'state/ledger.sqlite3',cold)
 with sqlite3.connect('file:'+str(cold)+'?immutable=1',uri=True) as db:
  assert db.execute('select status,token,lease_until from tasks where id=?',(task,)).fetchone()==('completed',None,None)
 print(json.dumps({'active_terminal_mismatch_rejected':True,'foreign_token_rejected':True,'cold_main_database_completion_verified':True,'production_tasks_mutated':0}))
