# Falx Interactive Paper

**▶ 발표 자료 열기 / Open the deck: https://seohyeon0046.github.io/MikaHome._./falx/**

**▶ 새 디자인 (annotated paper): https://seohyeon0046.github.io/MikaHome._./falx/paper.html**

An interactive presentation of **Falx: Synthesis-Powered Visualization Authoring** (Wang et al., CHI 2021).
The slides are one scrollable web page. Every Falx demo runs the authors' own synthesizer, and the paper's R workflow runs in real R.

발표용 인터랙티브 페이지입니다. Falx 데모는 저자들이 공개한 합성기를 그대로 실행하고, 논문의 R 코드도 실제 R에서 실행합니다.

## Quick start (live mode)

Needs `git`, [`uv`](https://docs.astral.sh/uv/) and, for live R panels, R with `tidyr`, `dplyr`, `ggplot2`, `svglite`.

```bash
./run.sh            # first run: clones Falx, builds a Python 3.8 env (~1–2 min)
# open http://127.0.0.1:5050
```

The badge in the top bar turns green (`Live · Falx + R`) when the page is talking to the local server.
- **Synthesize** sends any demonstration you build to Falx on your machine.
- **Run in R** executes the code in the R workbench, which you can edit.

Docker alternative (no local Python or R needed):

```bash
docker build -t falx-deck . && docker run --rm -p 5050:5050 falx-deck
```

## Offline mode

Open `index.html` directly, or host it on GitHub Pages (in this repository: `/falx/`). Without the server the page replays runs recorded with the same code (`data/recorded_falx.json`, `data/recorded_r.json`) and labels them as recorded. Demonstrations that were not recorded show a message asking for the local server.

## Presenting

- Two looks of the same deck: `index.html` (classic) and `paper.html` (annotated paper, forest and linen). With the server: `http://127.0.0.1:5050/` and `http://127.0.0.1:5050/paper`.

- **Story** mode scrolls; **Present** mode shows one scene at a time (← / → or PageUp / PageDown).
- The Korean script with timings and click cues is in [`docs/script_ko.md`](docs/script_ko.md).

## Layout

| Path | What it is |
|---|---|
| `index.html` | The built deck (self-contained, ~1.8 MB) |
| `src/deck.html` | Deck source; `python3 build_deck.py` inlines `data/` into `index.html` and `docs/artifact.html` |
| `server/app.py` | Local server: serves the deck, `POST /falx`, `POST /r`, `GET /health` |
| `server/falx_runner.py` | Thin wrapper around the authors' `/falx` endpoint logic; adds the ggplot2 export |
| `server/r_runner.py` | Runs an R snippet against `data/weather.csv`, returns console text + SVG |
| `precompute/` | Scripts that regenerate the recorded runs and the search log |
| `data/` | Weather data (from the Falx repo), recorded runs, parsed search log, cropped paper figures |
| `docs/` | Script and the artifact build |

## Regenerating the recorded runs

```bash
FALX_DIR=vendor/falx .venv/bin/python precompute/run_falx_cases.py   # Falx cases in precompute/falx_cases.json
python3 precompute/run_r_snippets.py                                  # R snippets in precompute/r_snippets.json
python3 build_deck.py
```

## Notes on reproduction

- Falx is pinned to commit `fcae5e5` of [Mestway/falx](https://github.com/Mestway/falx) (BSD-2-Clause). It needs Python 3.8 and pandas 1.1; current Python fails on import.
- The single-bar Figure 2 demonstration raises `IndexError` in the released code; two bars work.
- Three R listings in Section 2.1 do not run as printed; the deck shows both the printed and the corrected versions.

Paper: https://doi.org/10.1145/3411764.3445249 · Figures reproduced from the paper for discussion.
