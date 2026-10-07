#!/usr/bin/env python3
"""Verify fixed public notes and sanitized website-note copies, offline."""
import hashlib,json,re
from pathlib import Path
base=Path(__file__).resolve().parent
manifest=json.loads((base/'read_manifest.json').read_bytes()); checks=[]
def check(label,path,size,digest):
 b=path.read_bytes(); h=hashlib.sha256(b).hexdigest()
 assert len(b)==size,(label,'byte count',len(b),size)
 assert h==digest,(label,'sha256',h,digest)
 checks.append({'label':label,'bytes':len(b),'sha256':h,'passed':True})
i=manifest['index']
assert i['commit']=='1f61909da967cea8bc68dbfaffc642a4331b3352'
check('fixed public index',base/i['localCopy'],i['bytes'],i['sha256'])
index=json.loads((base/i['localCopy']).read_bytes())
assert index['sourceCommit']==i['bodySourceCommit']=='1043e9d6080bff7af9724162e2c44559fab63e40'
assert len(index['notes'])==i['allMetadataEntriesScanned']==394
assert 3<=len(manifest['publicFullNotes'])<=5
for n in manifest['publicFullNotes']:
 original=next(x for x in index['notes'] if x['path']==n['path'])
 assert (original['bytes'],original['sha256'],original['url'])==(n['bytes'],n['sha256'],n['url'])
 check(n['title'],base/n['localCopy'],n['bytes'],n['sha256'])
w=manifest['website']
assert (w['pages'],w['nextCursor'],w['totalNotes'],w['totalChunks'])==(2,None,2,9)
assert sum(n['chunks'] for n in w['notes'])==w['totalChunks']
for n in w['notes']: check('website '+n['project'],base/n['localCopy'],n['bytes'],n['sha256'])
for p in [base/'read_manifest.json',base/'knowledge_check.md',*[base/n['localCopy'] for n in w['notes']]]:
 assert not re.search(r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b',p.read_text()),('Private identifier in distributable knowledge copy',p.name)
print(json.dumps({'allPassed':True,'checks':checks,'sanitizedWebsiteMetadata':True,'scope':'Exact local copies and source-snapshot linkage only; not user mastery, latest vault scan, or Toolbox runtime validation'},ensure_ascii=False,indent=2))
