"""Inline the recorded data into src/deck.html and write index.html (single self-contained file)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)
cases = json.load(open(P("precompute", "falx_cases.json")))
data = {
    "weather": json.load(open(P("data", "weather.json"))),
    "fig1": cases["datasets"]["fig1"],
    "falx": json.load(open(P("data", "recorded_falx.json"))),
    "r": json.load(open(P("data", "recorded_r.json"))),
    "search": json.load(open(P("data", "search_log.json"))),
    "figs": json.load(open(P("data", "figs.json"))),
}
blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
src = open(P("src", "deck.html")).read()
assert "/*__DATA__*/null" in src
page = src.replace("/*__DATA__*/null", blob)
# Full document for GitHub Pages / the local server
head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}img{max-width:100%}</style>\n'
open(P("index.html"), "w").write(head + page + "\n</html>\n")
# Body-only version for publishing as a claude.ai artifact (the host adds the document skeleton)
os.makedirs(P("docs"), exist_ok=True)
open(P("docs", "artifact.html"), "w").write(page)
print("index.html", round(os.path.getsize(P("index.html")) / 1e6, 2), "MB")
