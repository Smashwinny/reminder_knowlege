import json,sys,http.server,threading,urllib.request
from pathlib import Path
mode=sys.argv[1]
if mode=='dns':
 records=[{'name':'www','type':'A','proxied':True},{'name':'mail','type':'A','proxied':True},{'name':'@','type':'MX','target':'mail'}]
 errors=[r['name'] for r in records if r['name']=='mail' and r.get('proxied')]
 assert errors==['mail'];print('fixture invalid mail proxy:',errors)
 records[1]['proxied']=False;assert not [r for r in records if r['name']=='mail' and r.get('proxied')];print('corrected fixture: PASS (not live DNS)')
elif mode=='tls':
 def loop(mode,redirect):return mode=='flexible' and redirect
 assert loop('flexible',True) and not loop('strict',True)
 print('redirect model: flexible+origin HTTPS redirect -> loop; strict -> no modeled loop')
elif mode=='web':
 class H(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
   body=b'cloud-lab-local';self.send_response(200);self.end_headers();self.wfile.write(body)
  def log_message(self,*a):pass
 s=http.server.HTTPServer(('127.0.0.1',0),H);t=threading.Thread(target=s.serve_forever,daemon=True);t.start()
 u=f'http://127.0.0.1:{s.server_port}/';v=urllib.request.urlopen(u);b=v.read();assert b==b'cloud-lab-local';print('loopback HTTP:',v.status,b.decode(),'; NOT Cloudflare deployment');s.shutdown();s.server_close()
elif mode=='storage':
 # Local byte store; not an R2 emulation or API benchmark.
 p=Path('exercise/object.bin');p.write_bytes(b'cyan-blue-orange');import hashlib
 a=hashlib.sha256(p.read_bytes()).hexdigest();assert a==hashlib.sha256(b'cyan-blue-orange').hexdigest();print('local object bytes=',p.stat().st_size,'sha256=',a)
