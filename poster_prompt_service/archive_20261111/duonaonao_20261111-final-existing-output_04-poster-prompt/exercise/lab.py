#!/usr/bin/env python3
"""Offline poster asset lab, self-authored teaching code, no model or API calls."""
import argparse, json, hashlib, re, copy, xml.etree.ElementTree as ET
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out'
def save(name,data):
 OUT.mkdir(exist_ok=True); (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def load():return json.loads((OUT/'library.json').read_text())
def validate(x):
 errors=[]
 for key in ['id','subject','brand','tagline','keywords','background','accent','layout','rights','provenance','engine']:
  if key not in x: errors.append('missing:'+key)
 if errors:return errors
 if x['rights']!='self-authored-demo':errors.append('rights:unapproved')
 if x['layout'] not in ['A','B','C']:errors.append('layout:invalid')
 for k in ['background','accent']:
  if not re.fullmatch('#[0-9a-fA-F]{6}',x[k]):errors.append('color:invalid')
 if len(x['brand'])>12:errors.append('brand:too-long')
 if not 6<=len(x['keywords'])<=10:errors.append('keywords:count')
 if any(not re.fullmatch('[a-z]+',w) for w in x['keywords']):errors.append('keywords:latin')
 return errors
def init():
 data=[]
 for id,subject,brand,bg,ac,layout in [('lamp','lamp','NOVA','#123B72','#FF952B','A'),('bottle','bottle','TIDE','#075968','#20DBE6','A'),('disc','disc','ORBIT','#213EC5','#FF9B36','C')]:
  data.append(dict(id=id,subject=subject,brand=brand,tagline='less form more meaning',keywords=['light','quiet','shape','space','line','calm'],background=bg,accent=ac,layout=layout,rights='self-authored-demo',provenance='worker-original-demo-not-author-prompt',engine='deterministic-svg-v1',seed=None))
 save('library.json',data);print(json.dumps({'templates':len(data),'model_calls':0,'private_inputs':0}))
def lint():
 data=load(); good=[validate(x) for x in data]
 negatives=[]
 for name,key,val in [('unknown-rights','rights','unknown'),('bad-layout','layout','Z'),('bad-color','background','red'),('long-brand','brand','X'*13),('bad-keywords','keywords',['中文'])]:
  x=copy.deepcopy(data[0]);x[key]=val;err=validate(x);assert err;negatives.append({'case':name,'errors':err})
 assert all(not e for e in good)
 save('lint.json',{'valid_templates':len(good),'negative_cases_rejected':negatives,'scope':'self-authored structural checks, NOT independent review or legal clearance'})
 print(json.dumps({'valid_templates':len(good),'negative_rejected':len(negatives),'scope':'structure_only'}))
def svg(x):
 shape={'lamp':'M190 120 L410 120 L465 300 L135 300 Z M291 300 L309 300 L309 625 L291 625 Z M190 625 L410 625 L410 655 L190 655 Z','bottle':'M260 100 L340 100 L340 210 L395 275 L395 640 Q300 685 205 640 L205 275 L260 210 Z','disc':'M300 100 A240 240 0 1 1 299.99 100 Z'}[x['subject']]
 lines=[]
 for i,y in enumerate(range(105,690,11)):
  words=x['keywords'][i%6:]+x['keywords'][:i%6]
  lines.append(f'<text x="20" y="{y}" font-size="9" fill="white">{escape(" ".join(words)*5)}</text>')
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="800" viewBox="0 0 600 800"><title>{escape(x['brand'])} deterministic SVG demo</title><metadata>engine={x['engine']}; rights=self-authored-demo; no generative model inference</metadata><defs><clipPath id="silhouette"><path d="{shape}"/></clipPath></defs><rect width="600" height="800" fill="{x['background']}"/><rect x="270" width="60" height="22" fill="{x['accent']}"/><g clip-path="url(#silhouette)" font-family="DejaVu Sans Mono,monospace">{''.join(lines)}</g><text x="70" y="725" font-size="65" font-weight="bold" fill="{x['accent']}" font-family="DejaVu Sans,sans-serif">{escape(x['brand'])}</text><text x="70" y="758" font-size="19" fill="white" font-family="DejaVu Sans,sans-serif">{escape(x['tagline'])}</text><text x="70" y="786" font-size="12" fill="white">CODE-RENDERED DEMO / NOT AI IMAGE OUTPUT</text></svg>'''
def render():
 for x in load():
  assert not validate(x)
  (OUT/(x['id']+'.svg')).write_text(svg(x))
  prompt=f"Original demo specification: {x['subject']}, flat vector silhouette, tiny latin word texture, background {x['background']}, accent {x['accent']}, 3:4. Typeset exact brand {x['brand']} and tagline {x['tagline']} separately. No real trademarks. No model has executed this prompt."
  (OUT/(x['id']+'.prompt.txt')).write_text(prompt)
 print(json.dumps({'svg_files':3,'prompt_files':3,'size':[600,800],'model_inference':False}))
def verify():
 ns={'s':'http://www.w3.org/2000/svg'};results=[]
 for x in load():
  p=OUT/(x['id']+'.svg'); a=p.read_bytes();t=ET.fromstring(a)
  assert t.get('width')=='600' and t.get('height')=='800'
  assert len(t.findall('.//s:clipPath',ns))==1
  text=[e.text for e in t.findall('.//s:text',ns)]
  assert x['brand'] in text and x['tagline'] in text
  assert not t.findall('.//s:image',ns) and not t.findall('.//s:script',ns)
  assert a==svg(x).encode()
  results.append({'id':x['id'],'sha256':hashlib.sha256(a).hexdigest(),'checks':['dimensions','clip','brand','tagline','no_external_image','no_script','deterministic_rebuild']})
 save('verification.json',{'files':results,'checks':21,'scope':'XML/byte checks; aesthetics and font portability not proven'})
 print(json.dumps({'files':len(results),'structural_checks':21,'deterministic':True}))
def economics():
 rows=[]
 # Hypotheses only: no platform fee rate is asserted.
 for minutes in [2,5,10]:
  price=5;refund=0.1;gen=0.8;hour=30;fee=0
  margin=price*(1-refund)-gen-minutes/60*hour-fee
  rows.append({'price':price,'refund_probability':refund,'generation_cost':gen,'labor_minutes':minutes,'labor_hourly':hour,'fee_assumed':fee,'margin':round(margin,2)})
 save('economics.json',{'kind':'hypothetical_not_sales','rows':rows,'gross_claim_arithmetic':5*20000,'claim_verified':False})
 print(json.dumps({'hypothetical_margins':[r['margin'] for r in rows],'claimed_gross_arithmetic':100000,'real_orders':0}))
p=argparse.ArgumentParser();p.add_argument('step',choices=['init','lint','render','verify','economics']);a=p.parse_args();globals()[a.step]()
