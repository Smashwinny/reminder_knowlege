"""Structural observations, not model/cost/performance benchmark metrics."""
import json
from test_lookup import metrics, ROOT
for name in ['minimal', 'layered']:
    print(name, json.dumps(metrics(ROOT / (name + '.py')), sort_keys=True))
print('LIMIT: same authored contract; no general security, model efficacy, speed, or cost conclusion')
