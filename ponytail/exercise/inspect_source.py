"""Read static upstream task evidence without importing it."""
import hashlib
from pathlib import Path
p = Path(__file__).with_name('upstream-sql-user-reference.txt')
s = p.read_text(encoding='utf-8')
assert '# 3. sql-user' in s and 'def score_sql' in s and 'SQL_SEED' in s
print('PASS static upstream sql-user task inspected; upstream code NOT executed')
print('upstream commit e15862bb04d04285233a164460ced063941d9ef5')
print('sha256', hashlib.sha256(p.read_bytes()).hexdigest())
print('contract: get_user(conn, username) -> matching row or None')
