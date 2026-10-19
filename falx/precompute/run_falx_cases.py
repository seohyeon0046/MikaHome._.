"""Re-run every recorded Falx case through the authors' synthesizer (heavy mode, one at a time).

Usage:  FALX_DIR=../vendor/falx ../.venv/bin/python run_falx_cases.py
Writes ../data/recorded_falx.json, which the deck uses when no live server is running.
"""
import json, os, sys, traceback
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "server"))
import falx_runner  # noqa: E402

spec = json.load(open(os.path.join(HERE, "falx_cases.json")))
datasets = dict(spec["datasets"])
datasets["weather"] = json.load(open(os.path.join(HERE, "..", "data", "weather.json")))
out = {}
for case in spec["cases"]:
    try:
        res = falx_runner.synthesize(datasets[case["data"]], case["tags"], "heavy")
        res["error"] = ""
    except Exception as exc:
        res = {"time_spent": 0, "status": "error", "result": [], "error": traceback.format_exc().strip().splitlines()[-1]}
    res.update({k: case[k] for k in ("id", "label", "data", "tags")})
    out[case["id"]] = res
    print("{:18s} {:7s} {:5.1f}s  {:2d} candidates  {}".format(case["id"], res["status"], res["time_spent"], len(res["result"]), res["error"]), flush=True)
json.dump(out, open(os.path.join(HERE, "..", "data", "recorded_falx.json"), "w"))
