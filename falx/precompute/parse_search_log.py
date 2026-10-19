"""Turn Falx's console log (printed while synthesizing) into data/search_log.json.

Falx prints each program sketch it expands, followed by the partial programs that
survived its deduction step (indented). Sketches with nothing under them were
rejected before any argument was filled in.
Usage: python3 parse_search_log.py falx_stdout.txt
"""
import json, sys

lines = open(sys.argv[1]).read().split("\n")
starts = [i for i, l in enumerate(lines) if "table synthesis input" in l]

def parse(chunk):
    out, cur = [], None
    for l in chunk:
        if l.startswith("  t0") and cur is not None:
            cur["ok"].append(l.strip())
        elif l.startswith("t0"):
            cur = {"sketch": l.strip(), "ok": []}
            out.append(cur)
    return out

layers = [parse(lines[s + 2:(starts[k + 1] if k + 1 < len(starts) else len(lines))]) for k, s in enumerate(starts)]
json.dump({"line_layer": layers[0], "bar_layer": layers[1],
           "line_example_table": lines[starts[0] + 1], "bar_example_table": lines[starts[1] + 1]},
          open("../data/search_log.json", "w"))
for name, s in zip(("line", "bar"), layers):
    print(name, "sketches", len(s), "rejected outright", sum(1 for x in s if not x["ok"]), "partials kept", sum(len(x["ok"]) for x in s))
