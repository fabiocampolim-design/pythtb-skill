# pythtb-skill

![tests](https://img.shields.io/badge/tests-pytest%20%2B%20107%20notebook%20checks-brightgreen)
![python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)
![pythtb](https://img.shields.io/badge/pythtb-2.0.2-informational)
![platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![license](https://img.shields.io/badge/license-Apache--2.0-green)

**An AI-agent skill, a verified Python toolkit, two fully executed notebooks and
an undergraduate course for [PythTB 2.0](https://github.com/pythtb/pythtb), the
pure-Python tight-binding package behind Vanderbilt's *Berry Phases in Electronic
Structure Theory*.**

This repository packages practical, executed knowledge about PythTB in a form
that both humans and AI coding agents can use: a skill definition
([`SKILL.md`](SKILL.md)) that teaches an agent the workflows and the traps,
plain Python helpers that implement the awkward parts (`scripts/`), distilled
reference documentation (`references/`), and two notebooks in which **every
physics claim is executed and checked** — from the first band structure to
axion angles, quasicrystals and Hofstadter butterflies, ending with an honest
map of what PythTB cannot do and how to hand a model to Kwant.

> PythTB is written by Sinisa Coh, David Vanderbilt and Trey Cole (GPL-3.0).
> **This is an unofficial, independent project** — not affiliated with or
> endorsed by the PythTB authors.

> **Feedback is highly appreciated.** Open an issue for anything wrong, unclear
> or missing — especially: a physics check you believe asserts the wrong thing,
> a PythTB capability not exercised here, a trap you hit that the API map
> does not list, or a platform where the notebooks do not run.

## Features

- **Agent skill** — `SKILL.md` gives an agent the five workflows (build/solve,
  invariants, finite systems, Wannier90 import, hand-off to Kwant) with the
  ground rules that cost the most debugging time, each pointing to a
  reference file.
- **Verified helpers** (`scripts/pythtb_tools.py`, numpy + pythtb only):
  `wilson_phases` (the workaround for the pythtb 2.0.2 bug where
  `wilson_loop(wilson_evals=True)` returns cos φ), `z2_wcc_flow` /
  `z2_from_wcc` (Fu–Kane Z₂ from Wannier-centre flow with circular tracking),
  `remove_orb_copy` (the documented, non-mutating behaviour), `to_kwant`
  (finite model → `kwant.Builder` with identical spectrum). `--selftest`
  runs the built-in checks.
- **Environment check** — `scripts/verify_pythtb.py`: five checks (imports,
  SSH gap, Zak phases, Haldane Chern number, silicon dataset) in seconds.
- **Upstream watch** — `scripts/watch_upstream.py --weekly` reports new
  releases, issues, pull requests, `main` commits and PyPI versions of
  PythTB since the previous run (anonymous GitHub/PyPI API, ~5 requests);
  `scripts/register_watch_task.ps1` schedules it weekly on Windows.
- **Two executed notebooks.** `PythTB_Theory_and_Practice.ipynb` — 31 sections
  in four parts, **72 inline physics checks, 69 captioned figures**, ~1.5 min
  to run; `PythTB_Exercises_Solutions.ipynb` — 20 worked exercises, **35
  checks, 18 figures**. Every system is drawn before it is computed on; every
  figure has a numbered caption saying what to look at and why.
- **An undergraduate course** (`course/`) — *Tight-Binding Physics with PythTB*,
  ten lectures as offline reveal.js slides with a committed **PDF fallback**
  (`course/slides.pdf`), an A4 handout and lecturer notes with an anticipated
  question per slide. Navigation is deliberately plain: the arrow keys go to
  the next or previous slide, nothing else. All 69 notebook figures appear in
  both the slides and the PDF, each under its full notebook caption with its
  figure number and cell (a test fails if one drifts or goes unused). Within
  each lecture the slides run intro → core → math, so the same deck serves a
  first- and a fourth-year audience.
- **Curated references** — the v1.x → 2.0 API map with every trap confirmed
  by execution, invariant recipes and conventions, the PythTB-vs-Kwant
  capability matrix, and the ecosystem/citing page (`references/`).
- **Reproducible by construction.** The notebooks are generated from
  `build/*.py`; a test fails if the committed notebooks drift from the
  sources, contain a failed check or an uncaptioned figure. Fixed random seeds.
- **Pinned, guarded environment.** `pythtb==2.0.2`; the two upstream bugs the
  notebooks work around are strict-xfail tests — when upstream fixes them the
  suite says so. Docs are guarded too: a test fails when a CLI flag is
  undocumented or the counts above drift.

## Using it as an AI-agent skill

For [Claude Code](https://claude.com/claude-code) (or any agent framework that
understands skill directories):

```bash
git clone <this repository> ~/.claude/skills/pythtb      # user-level install
```

or per project: clone into `<project>/.claude/skills/pythtb`. The agent then
consults the skill whenever a task involves tight-binding models, Berry phases
or topological invariants. Other frameworks can ingest `SKILL.md` as a system
instruction and expose `scripts/` on the path.

## Using it as a plain Python toolkit

No AI required — the scripts are ordinary Python (3.12+):

```bash
python -m pip install -r requirements.txt
python scripts/verify_pythtb.py                 # 5 checks -> "Environment OK."
python scripts/pythtb_tools.py --selftest       # helper checks
python scripts/watch_upstream.py --weekly       # what changed upstream since last week
python -m ipykernel install --user --name pythtb-mc --display-name "Python 3.12 (pythtb)"
jupyter lab PythTB_Theory_and_Practice.ipynb    # or just read it on GitHub
python -m pytest tests                          # test suite (~40 s; no kwant needed)
```

The course: open `course/deck/index.html` in a browser (arrows navigate, `S`
opens the speaker view) or read `course/slides.pdf`; syllabus, keys and
rebuild commands in **[course/README.md](course/README.md)**.

Windows + Miniconda: `powershell -ExecutionPolicy Bypass -File .\install_pythtb_windows.ps1`
creates the env and kernel in one go. Full instructions, troubleshooting and
the complete feature/limitation list: **[docs/USER_MANUAL.md](docs/USER_MANUAL.md)**.
Working with an agent on this repository itself? Hand it **[AGENTS.md](AGENTS.md)**.

## What the notebooks cover

| Part | Sections | Highlights |
|---|---|---|
| I — Fundamentals | §1–13 | object model; SSH; graphene/BN; Lieb & kagome flat bands with exact compact localized states; finite systems, supercells, defects; native spin; Berry phases & polarization; Thouless pump; 3D; **Wannier90 import of silicon**; in-package Wannierization |
| II — Topological matter | §14–20 | Haldane (Chern three ways, real-space local Chern marker); Kane–Mele & BHZ Z₂ via Wannier-centre flow; **BBH quadrupole, nested Wilson loops**; Kitaev chain as a BdG hack; Weyl monopoles & Fermi arcs; **Fu–Kane–Mele axion angle θ + second Chern number** |
| III — Stretching PythTB | §21–24 | Hofstadter butterfly (Landau-gauge supercells); Anderson localization; **Penrose quasicrystal** from de Bruijn's pentagrid; the O(N³) wall, measured |
| IV — What PythTB cannot do | §25–31 | no transport, no sparse/KPM, no continuum, no symmetry rails, no interactions — each *demonstrated*; **capability matrix vs Kwant**; where to go next |

In total: 107 inline `[PASS]`/`[FAIL]` checks and 87 figures with 87 numbered
captions across the two notebooks. The checks caught a dozen wrong physical
claims during writing (BN's polarization jump is e/3, not e/2; the Lieb flat
band survives corner–corner hopping; only the BBH Wannier *centroid* is
pinned…) and the same discipline surfaced three upstream issues, kept as
drafts in the study folder next to this repository until they are filed.

## Honest comparison with neighbours

| If you want… | Use | Why not this |
|---|---|---|
| The official way in | [PythTB tutorials](https://pythtb.readthedocs.io) and the ICTP-MARVEL tutorials in the upstream repo | Shorter, canonical, maintained by the authors. This project goes wider and checks everything, but is a third-party view. |
| Z₂ / Chern from DFT with convergence bookkeeping | [Z2Pack](https://z2pack.greschd.ch) | `z2_wcc_flow` is a verified pedagogical implementation, not a production invariant calculator. |
| Berry-phase post-processing of real Wannier90 models at speed | [WannierBerri](https://wannier-berri.org) | PythTB (and this project) are dense and slow by design. |
| Transport, leads, conductance, large sparse systems | [Kwant](https://kwant-project.org) — see the companion Kwant notebook | PythTB has none of it; Part IV shows exactly where the line is and `to_kwant` crosses it. |
| KPM, C++ speed, big lattices without transport | [PyBinding](https://pybinding.site) | Exercise IV.2 does KPM in 30 lines to show the idea, not to compete. |

## Roadmap

- **Validated:** full execution on Windows 10 / Python 3.12.13 / pythtb 2.0.2
  (2026-08-29); Kwant cross-check of `to_kwant` with kwant 1.5.0 (2026-08-28);
  the upstream test suite run on the same machine (102 pass, 1 platform-fragile).
- **CI-validated 2026-08-31** (first push): Linux, Windows and macOS ×
  Python 3.12/3.13 — fast suite on all six, plus a full re-execution of both
  notebooks on ubuntu (130 checks green in 68 s). Formerly listed here as
  "untested until CI runs".
- **Planned:** file the three upstream issues; answer upstream #62 (Peierls
  substitution) and #60 (DOS) with the recipes from §21 and exercise IV.2;
  a `hofstadter(p, q)` supercell helper in `pythtb_tools`; interactive 3D
  Weyl/BZ figures; a section on quantum geometry (`quantum_metric`) once the
  upstream API settles.

## How it was built

Written with Claude Code (Claude Fable 5) between 2026-08-21 and 2026-08-30:
one scaffold session, a part-by-part executed build, an illustration/pedagogy
pass, a senior-review pass (tests, docs, the Kwant cross-check — which found a
real bug in the exporter) and a restructuring into the skill + toolkit +
notebooks shape. Effort ≈ 6 working sessions.

| Role (CRediT) | Fabio Campolim | Claude |
|---|---|---|
| Conceptualization, scope, physics targets | ● | ○ |
| Methodology (check-everything contract, skill/toolkit/notebook shape) | ● | ● |
| Software (cell sources, helpers, build tooling, tests) | ○ | ● |
| Validation (every check, upstream suite, Kwant cross-check) | ○ | ● |
| Investigation (API traps, upstream bugs) | ○ | ● |
| Writing – original draft | ○ | ● |
| Writing – review & editing, decisions on scope and presentation | ● | ○ |
| Supervision, project administration | ● | ○ |

● lead ○ support

## Licence

[Apache License 2.0](LICENSE) — see `LICENSE` and `NOTICE`. This project uses
PythTB through its public Python API and contains no PythTB source code, so it
carries its own licence; PythTB itself stays GPL-3.0 and is installed by you
from PyPI. The one piece of upstream material redistributed here,
`data/w90_silicon/` (Wannier90 output for silicon from the PythTB tutorials),
keeps its GPL-3.0-or-later licence with attribution (`data/README.md`). You may
use, modify and redistribute this project, including commercially, provided
the licence and notice travel with it; contributions are accepted under the
same terms (section 5).

### Disclaimer

This software is provided **as is**, without warranties or conditions of any
kind, express or implied, including but not limited to any warranty of
merchantability, fitness for a particular purpose, title or non-infringement.
In no event shall the author be liable for any damages of any character —
direct, indirect, special, incidental or consequential — or for any other
claim or liability, whether in contract, tort or otherwise, arising from, out
of or in connection with the software or its use, even if advised of the
possibility of such damages (Apache License 2.0, sections 7 and 8). The
physics in the notebooks is checked numerically, not refereed: you alone are
responsible for any use of the results, for the software you install alongside
this project, and for complying with the licences of PythTB, Kwant and every
other third-party package it touches.

This is an independent project. It is not affiliated with, endorsed by or
supported by the PythTB authors or Rutgers University; *PythTB* is used here
only to name the package this project works with.
