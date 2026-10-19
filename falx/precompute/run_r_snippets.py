"""Run every R snippet once and record console output + SVG for the deck's offline mode.

Usage: python3 run_r_snippets.py   (needs Rscript with tidyr, dplyr, ggplot2, svglite)
"""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "server"))
from r_runner import run_r_snippet, RSCRIPT  # noqa: E402

assert RSCRIPT, "Rscript not found"
out = {}
for s in json.load(open(os.path.join(HERE, "r_snippets.json"))):
    r = run_r_snippet(s["code"])
    # keep SVG ids unique once several plots share one page
    r["svg"] = re.sub(r'(id="|url\(#|href="#)(c[a-zA-Z0-9]+)', lambda m: m.group(1) + s["id"] + "-" + m.group(2), r["svg"])
    r["stderr"] = "\n".join(l for l in r["stderr"].splitlines() if not l.startswith("Backtrace") and not re.match(r"^\s+(x|\d+\.)", l))
    out[s["id"]] = dict(s, **r)
    print("{:14s} ok={} svg={}KB {}".format(s["id"], r["ok"], len(r["svg"]) // 1024, r["stderr"][:80].replace("\n", " ")))
json.dump(out, open(os.path.join(HERE, "..", "data", "recorded_r.json"), "w"))
