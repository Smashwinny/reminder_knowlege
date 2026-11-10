from pathlib import Path
p = Path("exercise/out/00-tree.obj")
lines = p.read_text().splitlines()
print(lines[0])
print("v", sum(1 for l in lines if l.startswith("v ")), "f", sum(1 for l in lines if l.startswith("f ")))
