import py_compile, sys
[py_compile.compile(f, doraise=True) for f in ('app.py', 'test_app.py', 'miniflask.py')]
print('BUILD OK')
