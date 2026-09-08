"""Local live recomputation. Run this complete script, then open its printed URL."""
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlsplit,parse_qs
from pathlib import Path
import argparse,json,time
import sweeps
HERE=Path(__file__).parent
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url=urlsplit(self.path);q=parse_qs(url.query)
        try:
            if url.path in ['/','/index.html']:
                data=(HERE/'All_Eyes_Observatory.html').read_bytes();mime='text/html; charset=utf-8'
            elif url.path=='/api/health':data=json.dumps({'status':'ready','engine':sweeps.machine.VERSION,'mode':'live_registered_python'}).encode();mime='application/json'
            elif url.path=='/api/frame':
                study=q.get('study',[''])[0];x=float(q.get('x',['nan'])[0]);start=time.perf_counter();frame=sweeps.compute(study,x)
                data=json.dumps({'study':study,'frame':frame,'seconds':time.perf_counter()-start},allow_nan=False).encode();mime='application/json'
            else:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
        except Exception as e:
            data=json.dumps({'error':str(e)}).encode();self.send_response(400);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=8765);a=p.parse_args()
    server=HTTPServer(('127.0.0.1',a.port),Handler)
    print(f'Compound Eye live: http://127.0.0.1:{server.server_port} — Ctrl+C stops the server.',flush=True)
    server.serve_forever()
