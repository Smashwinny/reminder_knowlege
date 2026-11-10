#!/usr/bin/env python3
"""Local, zero-dependency merge-gate teaching lab. No remote, no merge.
All approvals are SYNTHETIC FIXTURES, not independent review.
"""
import argparse, ast, json, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent
WORK = ROOT / 'runs-v2'

def cmd(args, cwd=None, check=True):
    p = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    print('$ ' + ' '.join(map(str, args)))
    print(p.stdout + p.stderr, end='')
    print('exit_code=' + str(p.returncode))
    if check and p.returncode:
        raise RuntimeError(args)
    return p

def put(root, path, data):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding='utf-8')

def sha(repo):
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()

def commit(repo, message):
    cmd(['git', 'add', '.'], repo)
    cmd(['git', 'commit', '-m', message], repo)
    return sha(repo)

def checks(repo):
    # Trusted runner supplied by this lab, not read from candidate CI.
    t = cmd([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], repo, False)
    l = cmd([sys.executable, str(ROOT / 'lab.py'), 'lint', '--repo', str(repo)], repo, False)
    return {'sha': sha(repo), 'checks': {'tests': t.returncode == 0, 'lint': l.returncode == 0}}

def lint(repo):
    errors = []
    paths = list((repo / 'src').glob('*.py')) + list((repo / 'tests').glob('*.py'))
    for p in paths:
        text = p.read_text()
        try:
            ast.parse(text)
        except SyntaxError:
            errors.append(str(p.relative_to(repo)) + ': syntax error')
        for i, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                errors.append(f'{p.relative_to(repo)}:{i}: trailing whitespace')
            if '\t' in line:
                errors.append(f'{p.relative_to(repo)}:{i}: tab forbidden')
    print(json.dumps({'lint_files': len(paths), 'errors': errors}, ensure_ascii=False))
    return bool(errors)

def gate(repo, base, evidence, author='bot', reviewer='synthetic-human'):
    """Policy lives OUTSIDE candidate repository; output is eligibility only."""
    head = sha(repo)
    changed = subprocess.check_output(['git', 'diff', '--name-only', base, head], cwd=repo, text=True).splitlines()
    errors = []
    if not changed:
        errors.append('empty diff')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=repo, text=True).strip():
        errors.append('dirty worktree')
    # Allowlist fails closed; protects tests, CI, AGENTS and policy from automatic changes.
    if any(not (p.startswith('docs/') or p.startswith('src/')) for p in changed):
        errors.append('protected or unknown path')
    if evidence.get('sha') != head:
        errors.append('stale CI SHA')
    for name in ('tests', 'lint'):
        if evidence.get('checks', {}).get(name) is not True:
            errors.append('required check not green: ' + name)
    if any(p.startswith('src/') for p in changed) and (not reviewer or reviewer == author):
        errors.append('independent approval absent (fixture)')
    return {'sha': head, 'changed': changed, 'eligible': not errors, 'reasons': errors,
            'review_is_synthetic': True, 'merged': False}

def step1():
    if (WORK / 'base').exists():
        raise RuntimeError('runs/base exists: use fresh extraction to repeat; never overwrite')
    r = WORK / 'base'; r.mkdir(parents=True)
    put(r, '.gitignore', '__pycache__/\n*.pyc\n')
    put(r, 'AGENTS.md', '# Agent contract\n\n## Scope\nEdit src/ or docs/ only. Tests, CI and this file require owner review.\n\n## Validate\npython3 -m unittest discover -s tests -v\npython3 tools/lint.py\n\n## Stop\nNever push, merge, deploy, use secrets, or claim independent review.\n')
    put(r, 'src/calc.py', 'def add(a, b):\n    return a + b\n')
    put(r, 'tests/test_calc.py', 'import unittest\nfrom src.calc import add\n\n\nclass TestCalc(unittest.TestCase):\n    def test_positive(self):\n        self.assertEqual(add(2, 3), 5)\n\n    def test_negative(self):\n        self.assertEqual(add(-2, 3), 1)\n\n    def test_zero(self):\n        self.assertEqual(add(0, 0), 0)\n')
    put(r, 'docs/architecture.md', '# Architecture\nPure arithmetic, no I/O.\n')
    put(r, 'tools/lint.py', 'import ast, pathlib, sys\nerrors = []\nfor p in [*pathlib.Path("src").glob("*.py"), *pathlib.Path("tests").glob("*.py")]:\n    text = p.read_text()\n    ast.parse(text)\n    errors += [str(p) + ": whitespace" for line in text.splitlines() if line.rstrip() != line or "\\t" in line]\nprint(errors)\nsys.exit(bool(errors))\n')
    put(r, 'ci.sh', '#!/bin/sh\nset -eu\npython3 -m unittest discover -s tests -v\npython3 tools/lint.py\n')
    put(r, '.github/workflows/ci.yml', 'name: educational-ci\non: [push, pull_request]\npermissions:\n  contents: read\njobs:\n  validate:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: "3.11"\n      - run: python3 -m unittest discover -s tests -v\n      - run: python3 tools/lint.py\n')
    cmd(['git', 'init', '-b', 'main'], r)
    cmd(['git', 'config', 'user.name', 'Local educational fixture'], r)
    cmd(['git', 'config', 'user.email', 'fixture@example.invalid'], r)
    base = commit(r, 'baseline contract, tests and CI')
    (WORK / 'base-sha.txt').write_text(base)
    print('BASE_SHA=' + base)
    cmd(['git', 'remote', '-v'], r)

def step2():
    result = checks(WORK / 'base')
    assert all(result['checks'].values())
    (WORK / 'baseline-ci.json').write_text(json.dumps(result, indent=2))
    print('BASELINE_VALIDATED=' + json.dumps(result))

def scenario(name, edit, expected, mutate=None, reviewer='synthetic-human'):
    r = WORK / name
    if r.exists():
        raise RuntimeError('refusing to overwrite ' + str(r))
    shutil.copytree(WORK / 'base', r, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    edit(r)
    head = commit(r, name)
    evidence = checks(r)
    if mutate:
        mutate(evidence)
    result = gate(r, (WORK / 'base-sha.txt').read_text(), evidence, reviewer=reviewer)
    assert result['eligible'] is expected, result
    (WORK / (name + '.json')).write_text(json.dumps(result, indent=2))
    print('RESULT=' + json.dumps({'scenario': name, **result}, ensure_ascii=False))
    return result

def step3():
    scenario('good-docs', lambda r: put(r, 'docs/usage.md', '# Usage\nadd(2,3) is 5.\n'), True)
    scenario('good-code', lambda r: put(r, 'src/calc.py', 'def add(a, b):\n    """Add two values without I/O."""\n    return a + b\n'), True)

def step4():
    scenario('bad-regression', lambda r: put(r, 'src/calc.py', 'def add(a, b):\n    return a - b\n'), False)
    scenario('bad-lint', lambda r: put(r, 'src/calc.py', 'def add(a, b):\n    return a + b  \n'), False)

def step5():
    def doc(r):
        put(r, 'docs/new.md', '# New\nKnown fixture.\n')
    scenario('bad-policy', lambda r: put(r, '.github/workflows/ci.yml', '# checks disabled\n'), False)
    scenario('bad-stale', doc, False, lambda e: e.update(sha='old-untrusted-sha'))
    scenario('bad-missing', doc, False, lambda e: e['checks'].pop('lint'))
    scenario('bad-self-review', lambda r: put(r, 'src/calc.py', 'def add(a, b):\n    """Sum."""\n    return a + b\n'), False, reviewer='bot')
    results = [json.loads(p.read_text()) for p in WORK.glob('*.json') if p.name != 'baseline-ci.json']
    assert len(results) == 8
    print('SUMMARY=' + json.dumps({'scenarios': len(results), 'eligible': sum(x['eligible'] for x in results), 'blocked': sum(not x['eligible'] for x in results), 'actual_remote_merges': 0, 'independent_reviews_performed': 0}))

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('step', choices=['1','2','3','4','5','lint']); p.add_argument('--repo', type=pathlib.Path)
    a = p.parse_args()
    if a.step == 'lint':
        sys.exit(lint(a.repo.resolve()))
    globals()['step' + a.step]()
