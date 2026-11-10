from pathlib import Path
import http.server,socketserver,threading,subprocess,json,re,html,sys,functools,os,signal
scenario=sys.argv[1]if len(sys.argv)>1 else 'studio';root=Path('upstream/kestrel-k1').resolve();requests=[];harness=Path('harness.js').read_text()
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(root),**k)
 def log_message(self,fmt,*args):
  requests.append(fmt%args)
  with open(scenario+'-live-requests.txt','a')as f:f.write((fmt%args)+'\n')
 def do_GET(self):
  if self.path.split('?')[0]=='/':
   s=(root/'index.html').read_text().replace('</body>','<script>'+harness+'</script></body>');d=s.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(d)));self.end_headers();self.wfile.write(d)
  else:super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_address[1]}/?quality=low&showcase=0&lab={scenario}';cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--window-size=960,720','--virtual-time-budget=30000',f'--screenshot={scenario}.png','--dump-dom',url];print('COMMAND',cmd,flush=True)
proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
try:
 out,err=proc.communicate(timeout=150)
except subprocess.TimeoutExpired:
 os.killpg(proc.pid,signal.SIGKILL);out,err=proc.communicate();Path(scenario+'-timeout-dom.html').write_text(out);Path(scenario+'-timeout-stderr.txt').write_text(err);Path(scenario+'-requests.txt').write_text('\n'.join(requests));raise
finally:server.shutdown()
r=subprocess.CompletedProcess(cmd,proc.returncode,out,err)
Path(scenario+'-dom.html').write_text(r.stdout);Path(scenario+'-stderr.txt').write_text(r.stderr);Path(scenario+'-requests.txt').write_text('\n'.join(requests));print('chrome_exit',r.returncode);m=re.search(r'<pre id="lab-result"[^>]*>(.*?)</pre>',r.stdout,re.S);assert m,'missing harness result; inspect DOM/stderr';obj=json.loads(html.unescape(m.group(1)));print(json.dumps(obj,indent=2));Path(scenario+'-result.json').write_text(json.dumps(obj,indent=2));assert obj['ok'],obj
