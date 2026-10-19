#!/usr/bin/env bash
# Start the deck with a live Falx backend (and live R if Rscript is installed).
set -euo pipefail
cd "$(dirname "$0")"
FALX_COMMIT=fcae5e536f44c19780ae9f00b94e397723924757
PORT="${PORT:-5050}"

if [ ! -d vendor/falx ]; then
  echo "==> Fetching Falx (authors' code, BSD-2) at ${FALX_COMMIT:0:7}"
  git clone --quiet https://github.com/Mestway/falx.git vendor/falx
  git -C vendor/falx checkout --quiet "$FALX_COMMIT"
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required: curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "==> Creating Python 3.8 environment (Falx needs 2020-era pandas)"
  uv venv --quiet -p 3.8 .venv
  uv pip install --quiet -p .venv/bin/python -r server/requirements.txt
fi

if command -v Rscript >/dev/null 2>&1; then
  Rscript -e 'for (p in c("tidyr","dplyr","ggplot2","svglite")) if (!requireNamespace(p, quietly=TRUE)) install.packages(p, repos="https://cloud.r-project.org")' >/dev/null 2>&1 || true
else
  echo "==> Rscript not found: R panels will show recorded output."
fi

exec .venv/bin/python server/app.py --port "$PORT"
