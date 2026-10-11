import os

# The command text that got pasted into the page files by mistake
BAD = """grep -rl 'id="stormcanvas"' views | xargs perl -0777 -pi -e 's/<canvas id="stormcanvas".*?<\\/script>\\n?//s'"""

targets = ["storm2.html"]
for root, dirs, files in os.walk("views"):
    dirs[:] = [d for d in dirs if d not in ("node_modules", "dist")]
    for f in files:
        if f.endswith((".html", ".htm")):
            targets.append(os.path.join(root, f))

fixed = 0
for p in targets:
    try:
        s = open(p, encoding="utf-8").read()
    except Exception:
        continue
    if BAD in s:
        n = s.count(BAD)
        s = s.replace(BAD, "")
        open(p, "w", encoding="utf-8").write(s)
        fixed += 1
        print("cleaned", p, "(removed", n, "copies)")

left = 0
for p in targets:
    try:
        if "xargs perl" in open(p, encoding="utf-8").read():
            print("STILL HAS BAD TEXT:", p)
            left += 1
    except Exception:
        pass
print("done. files cleaned:", fixed, "| files still bad:", left)
