"""Local presentation server.

Serves the interactive deck (index.html) and two live endpoints:
  POST /falx  -> runs the authors' Falx synthesizer on a demonstration
  POST /r     -> runs an R snippet against the weather data and returns text + SVG
  GET  /health -> tells the deck which live features are available

Bind to 127.0.0.1 only: /r executes R code on this machine.
"""
import argparse
import os

from flask import Flask, jsonify, request, send_from_directory

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__, static_folder=None)

try:
    import falx_runner
    FALX_OK, FALX_ERR = True, ""
except Exception as exc:  # keep the deck usable even if Falx fails to import
    falx_runner, FALX_OK, FALX_ERR = None, False, repr(exc)

from r_runner import RSCRIPT, run_r_snippet


@app.after_request
def no_cache(resp):
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.route("/paper")
def paper():
    return send_from_directory(ROOT, "paper.html")


@app.route("/health")
def health():
    return jsonify({"falx": FALX_OK, "falx_error": FALX_ERR, "r": bool(RSCRIPT)})


@app.route("/falx", methods=["POST"])
def falx():
    if not FALX_OK:
        return jsonify({"status": "error", "error": FALX_ERR, "result": []}), 503
    body = request.get_json(force=True)
    try:
        res = falx_runner.synthesize(body["data"], body["tags"], body.get("mode", "heavy"))
    except Exception as exc:
        return jsonify({"status": "error", "error": repr(exc), "result": []})
    return jsonify(res)


@app.route("/r", methods=["POST"])
def run_r():
    if not RSCRIPT:
        return jsonify({"ok": False, "stderr": "Rscript was not found on this machine."}), 503
    return jsonify(run_r_snippet(request.get_json(force=True).get("code", "")))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5050)))
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    print("Falx loaded:", FALX_OK, FALX_ERR)
    print("Rscript:", RSCRIPT or "not found (R demos fall back to recorded output)")
    print("Open http://{}:{}/".format(args.host, args.port))
    app.run(host=args.host, port=args.port, threaded=True)
