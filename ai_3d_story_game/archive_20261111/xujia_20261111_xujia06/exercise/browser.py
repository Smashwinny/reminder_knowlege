from pathlib import Path
import http.server,threading,subprocess,socketserver,json,re,html
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=socketserver.TCPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_address[1]}/scene.html'
cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--no-pdf-header-footer','--window-size=900,1100','--virtual-time-budget=3000','--screenshot=scene.png','--dump-dom',url];print('COMMAND',cmd);r=subprocess.run(cmd,capture_output=True,text=True,timeout=30);Path('browser-dom.html').write_text(r.stdout);Path('browser-stderr.txt').write_text(r.stderr);server.shutdown();print('chrome_exit',r.returncode);assert r.returncode==0;assert 'data-test="pass"' in r.stdout,r.stdout[-5000:];text=html.unescape(re.search(r'<pre id="result">(.*?)</pre>',r.stdout,re.S).group(1));obj=json.loads(text);print(json.dumps(obj,indent=2));Path('browser-result.json').write_text(json.dumps(obj,indent=2))
