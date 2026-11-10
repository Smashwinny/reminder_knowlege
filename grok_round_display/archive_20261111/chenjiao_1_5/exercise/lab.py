from pathlib import Path
import sys,json,hashlib,platform
P=Path(__file__).parent
step=int(sys.argv[1])
def emit(**v):
 print(json.dumps(v,ensure_ascii=False,sort_keys=True))
 (P/f"result-{step}.json").write_text(json.dumps(v,ensure_ascii=False,indent=2))

# 自写环回HTTP替身，不调用真实Webhook/账户/模型，不是宗主协议实现。
if step==1:emit(python=platform.python_version(),scope='127.0.0.1临时HTTP请求；无凭证，无真实Bot')
if step==2:
 import http.server,threading,urllib.request
 class H(http.server.BaseHTTPRequestHandler):
  def do_POST(self):
   d=json.loads(self.rfile.read(int(self.headers['Content-Length'])));self.send_response(202);self.end_headers();self.wfile.write(json.dumps({'request_id':d['request_id'],'state':'accepted'}).encode())
  def log_message(self,*a):pass
 server=http.server.HTTPServer(('127.0.0.1',0),H);t=threading.Thread(target=server.serve_forever);t.start()
 try:
  req=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/webhook',data=json.dumps({'request_id':'demo-001','command':'仅测试'}).encode(),headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req) as r:status=r.status;d=json.load(r)
  assert status==202 and d['state']=='accepted';emit(http_status=status,response=d,has_answer=False)
 finally:server.shutdown();t.join();server.server_close()
if step==3:
 expected='demo-001';replies=[{'request_id':'other','text':'错配'},{'request_id':expected,'text':'环回测试成功'},{'request_id':expected,'text':'环回测试成功'}];seen=set();accepted=[];rejected=0
 for d in replies:
  if d['request_id']!=expected or d['request_id'] in seen:rejected+=1;continue
  seen.add(d['request_id']);accepted.append(d)
 assert len(accepted)==1 and rejected==2
 (P/'reply.json').write_text(json.dumps(accepted[0],ensure_ascii=False));emit(accepted=accepted,rejected_wrong_or_duplicate=rejected)
if step==4:
 d=json.loads((P/'reply.json').read_text());assert d['request_id']=='demo-001'
 emit(reply_file_valid=True,subtitle=d['text'],audio_generated=False,timeout_seconds_example=300,automatic_resubmissions=0,hardware='待验证',real_bot='未调用')
