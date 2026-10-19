"""Run an R snippet against data/weather.csv and capture console output and the plot (SVG)."""
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_CSV = os.path.join(ROOT, "data", "weather.csv")
RSCRIPT = shutil.which("Rscript")

R_PRELUDE = r'''
suppressPackageStartupMessages({library(tidyr); library(dplyr); library(ggplot2)})
df <- read.csv("weather.csv", check.names = FALSE)
df$Date <- as.Date(df$Date)
if (requireNamespace("svglite", quietly = TRUE)) svglite::svglite("plot.svg", width = 7, height = 3) else svg("plot.svg", width = 7, height = 3)
'''

R_RUN = r'''
.code <- readLines("snippet.R", warn = FALSE)
.res <- tryCatch({ source(textConnection(.code), echo = FALSE, print.eval = TRUE); "ok" },
                 error = function(e) { message("Error: ", conditionMessage(e)); "error" })
invisible(dev.off())
'''


def run_r_snippet(code, timeout=60):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(DATA_CSV, os.path.join(tmp, "weather.csv"))
        with open(os.path.join(tmp, "snippet.R"), "w") as f:
            f.write(code)
        with open(os.path.join(tmp, "main.R"), "w") as f:
            f.write(R_PRELUDE + R_RUN)
        try:
            proc = subprocess.run([RSCRIPT, "main.R"], cwd=tmp, capture_output=True, text=True, timeout=timeout)
            out, err = proc.stdout, proc.stderr
        except subprocess.TimeoutExpired:
            out, err = "", "Timed out after {} s.".format(timeout)
        svg_path = os.path.join(tmp, "plot.svg")
        svg = open(svg_path).read() if os.path.exists(svg_path) else ""
    # a device with nothing printed still leaves a blank SVG behind; drop it
    drew = sum(svg.count(t) for t in ("<polyline", "<rect", "<path", "<line", "<text")) > 3
    return {"ok": "Error" not in err, "stdout": out, "stderr": err, "svg": svg if drew else ""}
