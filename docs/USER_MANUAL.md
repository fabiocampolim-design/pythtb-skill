# pythtb-skill — User Manual

Version 1.4.4 — 2026-09-04. Source: `docs/USER_MANUAL.md`; build HTML/PDF with
`python docs/build_manual.py` (`--outdir D`, `--no-pdf`, `--verbose`). Companions:
`SKILL.md` (teaches an AI agent how to *use* PythTB) and `AGENTS.md` (how to
*maintain* this repository). This manual and the README must never contradict
each other — a test checks the counts.

## 1. What you get

Four layers around **PythTB 2.0.2**, the pure-Python tight-binding package by
Coh, Vanderbilt and Cole:

1. **An AI-agent skill** — `SKILL.md` + `references/` (API map with every trap,
   invariant recipes, capability matrix vs Kwant, ecosystem). Clone the
   repository into `~/.claude/skills/pythtb` (Claude Code) or feed `SKILL.md`
   to any agent framework.
2. **A verified toolkit** — `scripts/pythtb_tools.py` (helpers: `wilson_phases`,
   `z2_from_wcc`, `z2_wcc_flow`, `remove_orb_copy`, `to_kwant`; run
   `--selftest`, `--version`, `--quiet`), `scripts/verify_pythtb.py`
   (5-check environment test; `--data-dir D`, `--quiet`, `--version`) and
   `scripts/watch_upstream.py` (weekly watch of the upstream GitHub repository
   and PyPI: `--weekly`, `--snapshot`, `--pull`, `--state-dir`, `--upstream-dir`,
   `--outdir`, `--log-dir`, `--quiet`, `--version`; scheduled on Windows by
   `scripts/register_watch_task.ps1`).
3. **A book of Jupyter notebooks, one per chapter** (`chapters/`), shipped **fully
   executed** (all outputs, figures and check results stored in the files), plus the
   tooling to rebuild and re-verify them. The 8 chapters (and an introduction)
   replace the former single 5 MB notebook, which crashed viewers: every file is
   now well under 1 MB, every chapter runs on its own, opens with its own table of
   contents and links to the previous and next chapter, and `chapters/README.md`
   is the index. Section numbers §1–31, figure numbers and cross-references are
   global to the book.
4. **An undergraduate course** — `course/`: *Tight-Binding Physics with PythTB*,
   ten lectures as offline reveal.js slides (`course/deck/index.html`; flat and
   linear — the arrow keys simply go to the next or previous slide, and a
   divider slide opens each lecture), with a **committed PDF fallback**
   (`course/slides.pdf`, one page per slide), an A4 handout
   (`course/handout/handout.html`) and lecturer notes
   (`course/notes/LECTURER_NOTES.md`). Every one of the notebook's 69 figures
   appears in both the slides and the PDF, each with the notebook's full
   caption, figure number and cell. Within each lecture the slides run
   intro → core → math; see `course/README.md` for the syllabus and keys.

| Notebook | Content |
|---|---|
| `chapters/PythTB_00_Introduction.ipynb` | chapter 0 — Introduction (what the book is, how to run it, conventions, the shared setup cell) |
| `chapters/PythTB_01_Foundations.ipynb` | chapter 1 — Foundations: chains, SSH, graphene and flat bands |
| `chapters/PythTB_02_Finite_Systems_and_Berry_Phases.ipynb` | chapter 2 — Finite systems, spin and the Berry-phase machinery |
| `chapters/PythTB_03_Three_Dimensions_and_Wannier.ipynb` | chapter 3 — Three dimensions, Wannier90 import and Wannierization |
| `chapters/PythTB_04_Chern_and_Z2.ipynb` | chapter 4 — Chern and Z₂ insulators: Haldane, Kane–Mele, BHZ |
| `chapters/PythTB_05_Higher_Order_and_Kitaev.ipynb` | chapter 5 — Higher-order topology and the Kitaev chain |
| `chapters/PythTB_06_Weyl_and_Axion.ipynb` | chapter 6 — Weyl semimetals and the axion angle |
| `chapters/PythTB_07_Stretching_PythTB.ipynb` | chapter 7 — Stretching PythTB: butterfly, disorder, quasicrystal, the wall |
| `chapters/PythTB_08_What_PythTB_Cannot_Do.ipynb` | chapter 8 — What PythTB cannot do |
| `chapters/PythTB_Exercises_I-II.ipynb` | Exercises and worked solutions — Parts I–II |
| `chapters/PythTB_Exercises_III-IV.ipynb` | Exercises and worked solutions — Parts III–IV |

The book (chapters 1–8) carries 72 inline physics checks and 69 captioned figures and
runs in about 2 minutes in total (no chapter needs more than ~30 s); the two exercise
notebooks hold 20 worked exercises (I.1 – IV.4) with 35 checks and 18 figures. Sizes:
6.4 MB in total, the largest chapter 1.01 MB (the former single notebook was 5.4 MB).

You can read them on GitHub or in any notebook viewer without installing anything;
to re-run or modify them, follow §3.

## 2. Contents at a glance

**Part I — Fundamentals (§1–13).** From wavefunctions to hoppings; the 2.0 object
model (`Lattice`, `TBModel`, `Mesh`, `WFArray`); SSH chain; graphene and boron
nitride; Lieb and kagome flat bands with compact localized states; finite systems
(`cut_piece`), supercells and defects (`make_supercell`, `remove_orb`); native spin
(`spinful=True`); the Berry-phase machinery and electric polarization; the Rice–Mele
Thouless pump; 3D models; importing a Wannier90 model of silicon (`W90`);
Wannierization inside PythTB (`Wannier`).

**Part II — Topological matter (§14–21).** Haldane model (Chern number three ways,
phase diagram, edge states); Kane–Mele Z₂ via Wannier-centre flow; BHZ quantum well
on a lattice; BBH quadrupole insulator and nested Wilson loops; Kitaev chain as a
BdG "hack" with Majorana end modes; Weyl semimetals (monopoles, sliced Chern numbers,
Fermi arcs); Fu–Kane–Mele 3D TI and the axion angle θ with second Chern number.

**Part III — Stretching PythTB (§21–24).** Hofstadter butterfly via Landau-gauge
magnetic supercells; Anderson localization and inverse participation ratios; a
Penrose quasicrystal from de Bruijn's pentagrid; the O(N³) dense-diagonalization wall.

**Part IV — What PythTB cannot do (§25–31).** Each limitation *demonstrated* with
failing code: no transport (leads, S-matrix, conductance), no sparse solvers/KPM,
no continuum discretizer or symbolic input, no symmetry validation (BdG pitfalls),
no interactions unless you write the loop (mean-field Hubbard, self-consistent BCS);
a capability matrix PythTB vs Kwant; where to go next.

**Exercises.** Trestle lattice; particle–hole breaking in graphene; (non-)fragility
of the Lieb flat band; BN polarization; a pump that pumps nothing; silicon conduction
bands; competing masses in Haldane; Kane–Mele phase map; QSH→QAH under exchange;
the corner-charge pump; a Zak phase for Kitaev; annihilating Weyl nodes; colouring
the butterfly (gap Chern numbers, Diophantine equation); other lattices and
relativistic Landau levels; 1D localization length; Ammann–Beenker quasicrystal;
exporting a PythTB model to Kwant; KPM by hand; non-collinear mean field; a
self-consistent Kitaev chain.

## 3. Installation

Requirements: Python 3.12 or 3.13, `pip`. Windows users with Miniconda can run the
installer; everyone else uses pip directly.

```powershell
# Windows / Miniconda — creates env "pythtb" and Jupyter kernel "pythtb-mc"
powershell -ExecutionPolicy Bypass -File .\install_pythtb_windows.ps1
# options: -EnvName NAME -KernelName NAME -PythonVersion 3.13 -SkipVerify
```

```bash
# any platform
python -m pip install -r requirements.txt
python -m ipykernel install --user --name pythtb-mc --display-name "Python 3.12 (pythtb)"
python scripts/verify_pythtb.py          # 5 checks, ends with "Environment OK."
python scripts/pythtb_tools.py --selftest
```

The notebooks are pinned to the kernel name **`pythtb-mc`**. If you registered a
different name, either select your kernel in Jupyter/VS Code once, or change
`KERNELSPEC` in `build/nbbuild.py` and re-assemble (§5).

Windows note: set `PYTHONIOENCODING=utf-8` before running the scripts from a
console — the notebooks print Greek letters and arrows.

## 4. Reading and running

- Start with `chapters/README.md` (the index) or `chapters/PythTB_00_Introduction.ipynb`.
  Open any chapter with the `pythtb-mc` kernel and run all cells — each chapter is
  self-contained (the setup cell is the same in all of them; a chapter that reuses a
  model from an earlier one rebuilds it in a short recap cell), its first cell is a
  table of contents with links to the previous and next chapter, and its last cell
  tallies the checks. Every physics claim prints `[PASS] label — detail` (or
  `[FAIL]`); every figure is followed by a numbered caption explaining what to look
  at and why. Figure numbers and section numbers run through the whole book.
- Nothing is downloaded at run time. §12 and exercise I.6 read the silicon Wannier90
  files from `data/w90_silicon/`; the setup cell finds it from `chapters/` (`../data`)
  or from the repository root.
- Runtime is about 2 minutes for all chapters on a laptop; no cell needs more than ~20 s.

## 5. Rebuilding (if you change anything)

The `.ipynb` files and `chapters/README.md` are generated. Edit the cell sources in
`build/part*.py` (book) or `build/ex_part*.py` (exercises), then:

```bash
python build/assemble.py            # --which main|exercises|all|<chapter key>, --outdir D, --log-dir D, --list, --verbose/--quiet
python build/execute.py             # --which, --indir D, --outdir D, --log-dir D, --kernel NAME, --timeout S, --tally-only, --verbose/--quiet
python -m pytest tests              # fast integrity suite (~40 s)
```

`assemble.py --list` prints the chapter keys (`00`–`08`, `ex1`, `ex2`), their part
modules and cell counts. The chapter layout — files, titles, which part module feeds
which chapter — is the `CHAPTERS` table in `build/assemble.py`; the tables of
contents, anchors, navigation links, figure-number offsets and the index are derived
from the `## N. Title` headings, so adding a section is just adding cells.

The course is generated too. Edit `course/deck/content.en.js` (strict JSON:
sections, slide order, levels, figures by provenance key, notes), then:

```bash
python course/tools/extract_figures.py   # PNG outputs of every book chapter -> course/deck/figs + provenance.json; --notebook F [F ...], --outdir D, --check, --quiet
python course/tools/build_deck.py        # -> deck/index.html, handout/handout.html, notes/LECTURER_NOTES.md; --content F, --check, --quiet
```

The committed PDF fallback is regenerated with the deck (Playwright env):
`python course/tools/make_slides_pdf.py` (`--index F`, `--out F.pdf`, `--quiet`,
`--version`) → `course/slides.pdf`; a test counts its pages against the deck.

Optional, in an environment with Playwright (`course/tools/requirements.txt`,
then `python -m playwright install chromium`): `course/tools/verify_deck.py`
(`--index F`, `--screens D`, `--no-screens`, `--quiet`) walks every slide headless
and reports console errors and overflow with a screenshot per slide;
`course/tools/build_pptx.py` (`--index F`, `--out F.pptx`, `--quiet`) exports
PowerPoint with the notes as speaker notes; `course/tools/make_handout.py`
(`--src F`, `--out F.pdf`, `--quiet`) prints the handout to A4 PDF. All five
tools print the version with `--version`.

`assemble.py` writes the notebooks without outputs; `execute.py` runs them on the
kernel (`--kernel`, default `pythtb-mc`; `--timeout` per cell, default 900 s) in
place or into `--outdir` (mirroring the `chapters/` layout), and tallies
PASS/FAIL/errors/figures/captions per notebook and per series (exit 0 only when
green; `--tally-only` just counts what the files already contain).
Both print a one-line summary by default (`--verbose` for detail, `--quiet` for
silence) and append an audit record — command line, versions, messages, outcome —
to `logs/assemble.log` / `logs/execute.log` (`--log-dir` to move it). nbconvert's
own output goes to `logs/nbconvert-<notebook>.log`.

## 6. Tests

`python -m pytest tests` runs in ~40 s and checks: the environment (pythtb 2.0.x,
SSH gap, Zak phases, Haldane Chern number, silicon dataset loads); every helper in
`scripts/pythtb_tools.py` against the physics it came from; the committed
notebooks (fully executed, 0 FAIL, 0 errors, caption per figure, minimum check
counts, cells identical to the `build/` sources, kernel pinned, no personal paths);
the two pythtb 2.0.2 bugs the notebooks work around, as *strict xfails* — if a
future pythtb fixes them the suite fails loudly so the notebook notes can be retired;
the upstream watch (delta/render/pagination helpers, an offline end-to-end weekly
run, exit code 1 when upstream is unreachable, the scheduler script's dry run);
the course (content file strict JSON, every slide listed once with a level, a layout
and notes ending in an anticipated question, intro → core → math inside each lecture,
every notebook figure used and byte-identical to the notebook output with its
provenance, the generated deck/handout/notes up to date, every text key in
`index.html` resolving, the committed `course/slides.pdf` with one page per slide,
the vendored reveal.js licence);
the docs (every CLI flag documented here and in `AGENTS.md`, README counts equal to
the executed notebooks, `VERSION` = `CHANGELOG.md` = `CITATION.cff`); and the licence
files (Apache-2.0 text with its disclaimers, `NOTICE`, the README disclaimer, an
SPDX header in every Python file).

`python -m pytest tests --run-notebooks` additionally re-executes every chapter notebook into
a temporary directory (~3 min; skipped if the kernel is not registered).
`tests/test_kwant_crosscheck.py` needs an interpreter with both `pythtb` and `kwant`
and skips otherwise.

## 7. Every feature and every known limitation

**Features (guarantees).**
- Every numerical claim in both notebooks is checked inline; the suite fails if any check fails.
- Every figure has an auto-numbered caption; every physical system is drawn before it is computed.
- Notebook text and code are the concatenation of `build/*.py` — reproducible, diff-able, testable.
- Fixed random seeds (`default_rng(2026)` etc.): outputs are deterministic.
- The Wannier90 silicon dataset is included with provenance and licence (`data/README.md`).
- All three PythTB 2.0.2 issues found while writing (Wilson-loop eigenvalue cast,
  `remove_orb` docstring, fragile upstream test) are documented with workarounds
  (§7, §9, `docs/02-findings-backlog.md`) and pinned by tests.
- Build and execute scripts expose all inputs/outputs on the command line and write audit logs.
- The course (`course/`) shows every figure the notebook generates — all 69, in the slides and in the committed PDF fallback, each under its full notebook caption — and `provenance.json` maps each one to its section, cell and figure number; the suite fails if a figure on disk no longer matches the notebook output or if one goes unused.
- A weekly upstream watch (`scripts/watch_upstream.py`) records what changed at github.com/pythtb/pythtb and on PyPI in `docs/watch/YYYY-WW.md` of the study repository; every run writes an audit log.

**Known limitations.**
- PythTB is pinned to **2.0.2**. Other 2.0.x versions should work; the classic 1.x API is not supported.
- Verified on Windows 10 / Python 3.12.13 (2026-08-28) and, since 2026-08-31, by CI (`.github/workflows/tests.yml`) on Linux, Windows and macOS × Python 3.12/3.13, including a full notebook re-execution on ubuntu.
- The Kwant cross-check (exercise IV.1) is **not** run inside the pythtb environment — Kwant is deliberately absent there. It passes in a separate environment (kwant 1.5.0), see backlog N3.
- The Part IV comparisons describe Kwant 1.5.0; a future Kwant may close some gaps in the capability matrix.
- The notebooks are dense-diagonalization only, by design: §24 measures the wall (~N³), Part IV explains the alternatives.
- The upstream mirror and the literature folder used while writing (`mirror/`, `papers/`) are not distributed — cite-and-link only.
- Figures are static matplotlib PNGs stored in the notebooks (no interactive widgets); that is why the book is split into chapter files of well under 1 MB each (the former single notebook was 5.4 MB and crashed viewers).
- The course slides set mathematics by hand in HTML (no MathJax) so that they work offline; complex derivations are sketched in the lecturer notes rather than typeset. The PPTX export is screenshots + editable notes, not editable slides.
- `scripts/register_watch_task.ps1` is Windows Task Scheduler only; on Linux/macOS run `watch_upstream.py --weekly` from cron.

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `Kernel not found: pythtb-mc` | Register the kernel (§3) or select another kernel once; VS Code users: `.vscode/settings.json` points at the conda env |
| `UnicodeEncodeError: 'charmap'` when running scripts | `set PYTHONIOENCODING=utf-8` (Windows console) |
| `ComplexWarning` from `wfarray.py` | Upstream bug P1; §9 silences it and shows the workaround |
| `remove_orb` returns `None` | Upstream docstring bug P2; call `.copy()` first, then `remove_orb` in place |
| `ZeroDivisionError` in `chern_number`/`axion_angle` | You are exactly at a gap closing; shift the parameter grid by half a step (§14, §20) |
| `FileNotFoundError: data/w90_silicon` | Run from the repository root (paths are relative) |
| `tests/test_notebooks.py` fails with "differs from build/ sources" | You edited a `chapters/*.ipynb` (or `chapters/README.md`) directly — re-run `build/assemble.py` and `build/execute.py` |
| A chapter fails with `NameError` when run on its own | It uses an object defined in an earlier chapter — add a `# recap` cell rebuilding it at the top of the part module (see chapters 2, 3, 8) |

## 9. Citing

PythTB: S. Coh and D. Vanderbilt, *Python Tight Binding (PythTB)* (2016),
DOI 10.5281/zenodo.12721315; version 2.0 by T. Cole, S. Coh and D. Vanderbilt
(https://github.com/pythtb/pythtb). Physics companion: D. Vanderbilt, *Berry Phases
in Electronic Structure Theory* (Cambridge, 2018). Full reference list for the
notebooks: §31 of the book (chapter 8).
