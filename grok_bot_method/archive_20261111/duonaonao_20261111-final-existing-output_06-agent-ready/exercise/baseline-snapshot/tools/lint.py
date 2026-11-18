import ast, pathlib, sys
errors = []
for p in [*pathlib.Path("src").glob("*.py"), *pathlib.Path("tests").glob("*.py")]:
    text = p.read_text()
    ast.parse(text)
    errors += [str(p) + ": whitespace" for line in text.splitlines() if line.rstrip() != line or "\t" in line]
print(errors)
sys.exit(bool(errors))
