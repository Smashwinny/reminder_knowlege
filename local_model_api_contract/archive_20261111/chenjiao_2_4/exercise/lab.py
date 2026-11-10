import sys,json,http.server,threading,urllib.request,urllib.error
mode=sys.argv[1]
if mode=='shape':
 req={'model':'fixture-not-a-real-model','messages':[{'role':'user','content':'hello'}],'max_tokens':8}
 assert req['messages'][0]['role']=='user';print(json.dumps(req));print('request shape only; no inference')
elif mode in ['http','limit']:
 class H(http.server.BaseHTTPRequestHandler):
  def do_POST(self):
   n=int(self.headers.get('Content-Length',0));body=json.loads(self.rfile.read(n));code=400 if body.get('max_tokens',0)>16 else 200
   self.send_response(code);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps({'object':'chat.completion','model':'MOCK','choices':[{'message':{'role':'assistant','content':'MOCK ONLY'}}]} if code==200 else {'error':'fixture token cap'}).encode())
  def log_message(self,*a):pass
 s=http.server.HTTPServer(('127.0.0.1',0),H);threading.Thread(target=s.serve_forever,daemon=True).start();p={'model':'MOCK','messages':[{'role':'user','content':'hi'}],'max_tokens':8 if mode=='http' else 17}
 q=urllib.request.Request(f'http://127.0.0.1:{s.server_port}/v1/chat/completions',json.dumps(p).encode(),{'Content-Type':'application/json'})
 try:
  res=urllib.request.urlopen(q);d=json.load(res);assert d['model']=='MOCK';print('loopback actual HTTP',res.status,d)
 except urllib.error.HTTPError as e:assert mode=='limit' and e.code==400;print('actual HTTP rejection:',e.code,e.read().decode())
 s.shutdown();s.server_close()
elif mode=='memory':
 weight=8_000_000_000*0.5;kv=2*32*8*128*4096*2
 print('hypothetical 8B INT4 raw weights=',int(weight),'bytes; sample GQA KV=',kv,'bytes; overhead excluded; no model loaded')
