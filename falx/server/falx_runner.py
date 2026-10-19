"""Thin wrapper around the authors' Falx synthesizer (github.com/Mestway/falx).

It mirrors the /falx endpoint of the original server (server/server.py in the
Falx repository) and additionally returns the ggplot2 script that Falx can
export for each candidate. Nothing in the synthesis itself is changed.
"""
import collections
import collections.abc
import os
import sys
import time

# Falx was written for Python 3.7/3.8. These aliases are harmless there and let
# newer interpreters import the namedlist dependency.
for _name in ("Mapping", "Sequence", "Iterable", "MutableMapping", "Callable"):
    if not hasattr(collections, _name):
        setattr(collections, _name, getattr(collections.abc, _name))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALX_DIR = os.environ.get("FALX_DIR", os.path.join(ROOT, "vendor", "falx"))
sys.path.insert(0, FALX_DIR)
sys.path.insert(0, os.path.join(FALX_DIR, "server"))

import flask  # noqa: E402
import markupsafe  # noqa: E402

if not hasattr(flask, "escape"):  # Flask >= 2.3 dropped flask.escape
    flask.escape = markupsafe.escape

_cwd = os.getcwd()
os.chdir(os.path.join(FALX_DIR, "server"))
import server as falx_server  # noqa: E402  (the authors' server module)
from falx.interface import FalxInterface  # noqa: E402
from falx.utils import vis_utils  # noqa: E402
os.chdir(_cwd)

# Same budgets as the original server: a fast "lightweight" thread and a
# slower "heavy" thread.
MODES = {
    "lightweight": dict(time_limit_sec=5, solution_sketch_limit=2, solution_limit=3),
    "heavy": dict(time_limit_sec=20, solution_sketch_limit=5, solution_limit=10),
}


def synthesize(data, tags, mode="heavy"):
    cfg = MODES.get(mode, MODES["heavy"])
    input_data, visual_elements = falx_server.input_preprocessing(data, tags)
    start = time.time()
    result = FalxInterface.synthesize(
        inputs=[input_data],
        raw_trace=visual_elements,
        extra_consts=[],
        group_results=True,
        config={
            "solution_sketch_limit": cfg["solution_sketch_limit"],
            "solution_limit": cfg["solution_limit"],
            "time_limit_sec": cfg["time_limit_sec"],
            "vis_backend": "vegalite",
            "max_prog_size": 3,
            "grammar": falx_server.GRAMMAR,
        },
    )
    elapsed = time.time() - start

    out = []
    for key in result:
        prog, design = result[key][0]
        spec = design.to_vl_obj()
        values = spec["data"]["values"]
        spec = vis_utils.post_process_spec(spec, values)
        if spec is None:
            continue
        spec["data"] = {"values": values}
        try:
            gg = design.to_ggplot2()
            gg = [l if "fromJSON" not in l else l.split("<-")[0] + "<- fromJSON('<transformed data>')" for l in gg]
        except Exception as exc:  # export is best effort
            gg = ["# ggplot2 export failed: {}".format(exc)]
        out.append({"rscript": str(prog), "vl_spec": spec, "ggplot2": gg})

    return {
        "time_spent": elapsed,
        "status": "timeout" if elapsed >= cfg["time_limit_sec"] else "ok",
        "mode": mode,
        "result": out,
    }
