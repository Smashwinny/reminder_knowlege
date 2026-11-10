#!/usr/bin/env python3
"""Local HTTP acceptance tests, same source provenance as gateway.py. No network credentials."""
import importlib.util,pathlib,json,sys,http.client
spec=importlib.util.spec_from_file_location("study",pathlib.Path(__file__).with_name("ma-laoshi-20261111-gateway.py")); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
case=sys.argv[1]; u,ut=g.start(g.Mock); u.seen=[]
s,st=g.start(g.Gateway); s.upstream=u.server_port; s.meter={"success":0,"upstream_attempts":0,"rejected":0,"input_units":0,"output_units":0}
def base(**extra):
    b={"model":"study/fast","max_tokens":16,"messages":[{"role":"user","content":"hello world"}]}; b.update(extra); return b
def call(b,expect=200):
    status,out=g.post(s.server_port,"/v1/messages",b); print(json.dumps({"request":b,"status":status,"response":out},ensure_ascii=False)); assert status==expect,(status,expect); return out
try:
    if case=="text":
        a=call(base(system=[{"type":"text","text":"be brief"}],messages=[{"role":"user","content":[{"type":"text","text":"hello"},{"type":"text","text":"world"}]}]))
        assert u.seen[-1]=={"model":"mock-fast-v1","messages":[{"role":"system","content":"be brief"},{"role":"user","content":"hello\nworld"}],"max_tokens":16}
        assert a["content"][0]["text"]=="mock answer" and a["stop_reason"]=="end_turn"
        print("PASS system/text-block conversion + max_tokens + response contract")
    elif case=="routes":
        for name,target in g.ROUTES.items():
            a=call(base(model=name)); assert u.seen[-1]["model"]==target and a["model"]==name
            print("PASS actual upstream observed:",target)
        c=http.client.HTTPConnection("127.0.0.1",s.server_port); c.request("POST","/v1/messages",json.dumps(base())); r=c.getresponse(); r.read(); assert r.getheader("X-Study-Upstream-Model")=="mock-fast-v1"; c.close()
        print("PASS upstream header is different from client-visible alias")
    elif case=="usage":
        call(base()); call(base(model="study/deep"))
        c=http.client.HTTPConnection("127.0.0.1",s.server_port); c.request("GET","/usage"); r=c.getresponse(); meter=json.loads(r.read()); c.close()
        print("METER",json.dumps(meter,sort_keys=True)); assert meter=={"success":2,"upstream_attempts":2,"rejected":0,"input_units":4,"output_units":4}
        print("PASS 2 requests, 4 synthetic input + 4 output units; NOT credits or billing")
    elif case=="errors":
        call(base(model="not-real"),404); call(base(stream=True),501); call(base(tools=[]),400)
        call(base(messages=[{"role":"user","content":[{"type":"image","source":{}}]}]),400)
        call(base(max_tokens=0),400); call(base(messages=[]),400)
        assert len(u.seen)==0; print("PASS 6 local rejections, zero upstream attempts")
        call(base(messages=[{"role":"user","content":"__fail503__"}]),502)
        assert s.meter["success"]==0 and s.meter["upstream_attempts"]==1
        c=http.client.HTTPConnection("127.0.0.1",s.server_port); c.request("POST","/v1/messages",json.dumps(base()),{"Authorization":"Bearer DUMMY-DO-NOT-USE"}); r=c.getresponse(); r.read(); assert r.status==400; c.close()
        assert len(u.seen)==1
        print("PASS injected mock 503 maps to 502, no success usage; dummy credential rejected")
    else: raise ValueError("choose text/routes/usage/errors")
    print("SEEN_UPSTREAM",json.dumps(u.seen,ensure_ascii=False)); print("PASS CASE",case)
finally:
    s.shutdown(); u.shutdown(); s.server_close(); u.server_close(); st.join(); ut.join(); print("CLEANUP listeners closed")
