import json,sys,threading,urllib.request,urllib.error
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
P=Path(__file__).parent;s=sys.argv[1]
if s=='prepare':
 cfg={'bind':'127.0.0.1','upstreams':['local-429','local-ok'],'real_keys':False};(P/'mock-config.json').write_text(json.dumps(cfg));print(cfg)
elif s in ['failover','auth']:
 counts={'bad':0,'good':0}
 class H(BaseHTTPRequestHandler):
  def log_message(self,*a):pass
  def do_POST(self):
   counts['bad' if self.path=='/bad' else 'good']+=1
   code=(401 if s=='auth' else 429) if self.path=='/bad' else 200
   self.send_response(code);self.end_headers();self.wfile.write(json.dumps({'mock':True,'code':code}).encode())
 server=ThreadingHTTPServer(('127.0.0.1',0),H);t=threading.Thread(target=server.serve_forever,daemon=True);t.start();attempts=[]
 try:
  for path in ['/bad','/good']:
   req=urllib.request.Request(f'http://127.0.0.1:{server.server_port}'+path,data=b'{}',headers={'Content-Type':'application/json'})
   try:
    with urllib.request.urlopen(req,timeout=2) as q:code=q.status
   except urllib.error.HTTPError as e:code=e.code
   attempts.append(code)
   if code==200 or code not in [429,503]:break
  print('attempts=',attempts,'counts=',counts)
  assert attempts==([401] if s=='auth' else [429,200])
 finally:server.shutdown();server.server_close();t.join()
elif s=='budget':
 total=0;admitted=[]
 for n in [40,50,30]:
  if total+n<=100:total+=n;admitted.append(True)
  else:admitted.append(False)
 assert admitted==[True,True,False];print('synthetic reservations=',admitted,'reserved_tokens=',total,'external_requests=0; NOT Magpie execution')
