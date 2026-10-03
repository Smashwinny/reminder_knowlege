import re, json

html = open(r'F:/reminder/tools/tmp_dy_acc007e7.html', encoding='utf-8', errors='replace').read()
idx = html.find('window._ROUTER_DATA')
start = html.find('{', idx)
# decode progressively? Try direct loads from start to end of file
raw = html[start:]
# find the end of the JSON: the script may end with </script>; try rfind of '}'
for end in (raw.rfind('</script>'), len(raw)):
    frag = raw[:end].rstrip().rstrip(';')
    try:
        data = json.loads(frag)
        print("parsed OK, end=", end)
        break
    except Exception as e:
        print("fail end=", end, e)
else:
    data = None

if data:
    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, path + "/" + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + f"[{i}]")
        else:
            s = str(o)
            if any(t in s for t in ('Rust', 'rust', 'Postgres', 'postgres', 'github', '二进制')) or any(t in path for t in ('desc', 'nickname')):
                print(path, '=>', s[:1500])
    walk(data)
