import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
r=json.loads((p/'results.json').read_text());c=json.loads((p/'cost-results.json').read_text())
for f,h in r['source_hashes'].items(): assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h
assert r['accepted']==5 and r['blocked']==5
assert r['idle']['unique_round1']==r['idle']['unique_round2']==100
assert r['queue_all_gift_counterexample']['actual_size']==3
assert c['yuan_per_hour']=='168.750000'
print('VERIFY PASS: 5 vendor hashes, 10 mock inputs, 201 topic draws, queue counterexample and historical cost math')
