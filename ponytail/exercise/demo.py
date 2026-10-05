"""Show an observable result from an isolated fake in-memory database."""
import argparse
from contextlib import closing
import minimal
import layered
from test_lookup import fresh
p = argparse.ArgumentParser()
p.add_argument('implementation', choices=['minimal', 'layered'])
p.add_argument('username')
a = p.parse_args()
with closing(fresh()) as conn:
    print({'minimal': minimal, 'layered': layered}[a.implementation].get_user(conn, a.username))
