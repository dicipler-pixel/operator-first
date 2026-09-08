"""Exercise live HTTP computation and actual browser-script handlers together."""
from pathlib import Path
from http.server import HTTPServer
from urllib.request import urlopen
import json,os,subprocess,threading
from serve import Handler
HERE=Path(__file__).parent
server=HTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
base=f'http://127.0.0.1:{server.server_port}'
try:
    health=json.load(urlopen(base+'/api/health'));assert health['status']=='ready'
    for study,value in [('weak',.137),('skew',.513),('peeling',.137)]:
        result=json.load(urlopen(base+f'/api/frame?study={study}&x={value}'))
        assert result['frame']['parameter']==value and result['frame']['status_counts']['error']==0
    subprocess.run(['node',str(HERE/'test_ui.js')],check=True,env={**os.environ,'OBSERVATORY_TEST_URL':base})
    print('Live health, three unrecorded parameter computations, and real UI HTTP handlers PASS')
finally:server.shutdown();server.server_close();thread.join()
