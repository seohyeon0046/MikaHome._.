"""Inline the recorded data into src/deck.html and write index.html (single self-contained file)."""
import base64, json, os
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
    # Fictional persona illustrations (generated for this deck, backgrounds removed)
    "personas": {n: "data:image/webp;base64," + base64.b64encode(open(P("data", "personas", n + ".webp"), "rb").read()).decode()
                 for n in ("eunice", "amelia", "eunice_av", "amelia_av")},
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

# Second look ("annotated paper"): same deck, extra stylesheet and a small script layered on top
FONTS_OLD = "family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500"
assert FONTS_OLD in page
paper = page.replace("<title>Falx Interactive Paper</title>", "<title>Falx Paper Look</title>", 1).replace(FONTS_OLD, FONTS_OLD + "&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700", 1)
i = paper.index("</style>") + len("</style>")
paper = paper[:i] + "\n<style>\n" + open(P("src", "look_paper.css")).read() + "</style>" + paper[i:]
paper += "\n<script>\n" + open(P("src", "look_paper.js")).read() + "</script>\n"
open(P("paper.html"), "w").write(head + paper + "\n</html>\n")
open(P("docs", "artifact_paper.html"), "w").write(paper)
print("paper.html", round(os.path.getsize(P("paper.html")) / 1e6, 2), "MB")
