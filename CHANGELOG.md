# Changelog

All notable changes to pythtb-skill are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/). The current version is in `VERSION`
and is printed by every script's `--version`.

## [1.3.0] - 2026-08-31

Course reworked after Fabio's presentation review: linear navigation, every
notebook figure, full captions, committed PDF fallback.

### Changed
- The deck is now **flat**: one slide after another, single-level arrow
  navigation handled entirely by reveal.js (nothing intercepts the arrow
  keys). Each lecture opens with a generated **divider slide** (label, name,
  summary, level-coloured agenda) instead of the old overlay flash that could
  be cut mid-animation. The navigator is one row (lecture · position · global
  position, with mouse/Shift+arrow lecture jumps) plus the clickable
  per-lecture progress bar.
- Figure captions on the slides are the notebook's **full captions** (with
  figure number, section and cell), no longer truncated to the first sentence.
- All **69** notebook figures now appear in the course (was 63): the BBH model
  and bulk bands, the Kitaev physical-vs-BdG picture and BdG bands, the Weyl
  gap collapse and the Fu–Kane–Mele bulk bands joined as two new slides
  (`beyond-bbh-model`, `beyond-kitaev-model`) and two upgraded ones.

### Added
- `course/slides.pdf` — **committed PDF fallback** of the whole deck (77
  pages, one per slide, every figure with its full caption), rendered by the
  new `course/tools/make_slides_pdf.py` (`--index`, `--out`, `--quiet`,
  `--version`; Playwright) from reveal's print layout; a print stylesheet
  restores the slide padding reveal drops and hides the navigation chrome.
- `tests/test_course.py` now requires every provenance figure to be used,
  checks the flat structure and the PDF fallback (exists, is a PDF, one page
  per slide).

## [1.2.1] - 2026-08-31

### Changed
- Course prose reworded so that no tracked course file contains a term on the
  withheld-material list (`tests/test_no_held_material.py` scans tracked files
  only, so the generated notes were first checked once committed).

## [1.2.0] - 2026-08-31

Undergraduate course (playbook rule 22). Not yet published.

### Added
- `course/`: *Tight-Binding Physics with PythTB*, ten lectures (L0–L10) as a
  reveal.js 2-D grid — one vertical stack per lecture ordered intro → core →
  math — with an A4 companion handout and lecturer notes (every slide ends with
  an anticipated question). 65 slides, 63 of the notebook's 69 figures.
- `course/tools/extract_figures.py`: pulls every PNG output of the executed
  notebook into `course/deck/figs/` with `provenance.json` (section, cell,
  figure number, the notebook's own caption, SHA-256); `--check` fails when a
  figure drifted from the notebook. `--notebook`, `--outdir`, `--quiet`, `--version`.
- `course/tools/build_deck.py`: generates `deck/index.html`,
  `handout/handout.html` and `notes/LECTURER_NOTES.md` from the single content
  file `deck/content.en.js` (strict JSON); `--content`, `--check`, `--quiet`, `--version`.
- `course/tools/verify_deck.py` (`--index`, `--screens`, `--no-screens`),
  `build_pptx.py` (`--index`, `--out`), `make_handout.py` (`--src`, `--out`):
  optional Playwright tooling (`course/tools/requirements.txt`) — headless walk
  of every slide with overflow/console checks and screenshots, PPTX export with
  editable speaker notes, A4 PDF of the handout.
- `course/shared/`: theme, two-row section navigator and content loader (from
  the author's lecture decks) + vendored reveal.js 5.2.0 (MIT, `NOTICE`).
- `tests/test_course.py` (14 checks): content well-formed, level ordering per
  stack, every shown figure byte-identical to the notebook output with
  provenance, generated outputs fresh, every `data-t` key resolves, licences.

### Changed
- `tests/test_license.py` scans `course/tools/*.py` too; `tests/test_docs_guard.py`
  covers the five course tools; CI runs pyflakes over `course/tools` as well.

## [1.1.0] - 2026-08-31

Weekly upstream watch (playbook rule 23) and CI hardening. Not yet published.

### Added
- `scripts/watch_upstream.py`: anonymous weekly watch of github.com/pythtb/pythtb
  (releases, issues, pull requests, head of the default branch) and PyPI
  versions; `--weekly` writes `docs/watch/YYYY-WW.md` in the study repository,
  `--snapshot` / `--pull` / `--state-dir` / `--upstream-dir` / `--outdir` /
  `--log-dir` / `--quiet` / `--version`. Exit 1 when upstream is unreachable;
  one audit log per run (rule 12).
- `scripts/register_watch_task.ps1`: Windows Task Scheduler job (Mondays 08:00);
  `-DryRun`, `-Remove`, `-Version`.
- `pythtb_tools.audit_log()` (rule 12 JSON log per invocation).
- `tests/test_watch_upstream.py` (13 checks, offline) and an `audit_log` test.
- `.gitattributes` pins the vendored conformance checker to LF so the
  byte-identity wiring test survives a fresh Windows checkout.

### Changed
- CI: pyflakes runs over `scripts tests build docs` as its own step before the
  suite (rule 5) and the fast matrix now includes macOS (rule 19).
- Two pyflakes findings fixed (unused `kwant` names); the personal-path guard in
  `tests/test_notebooks.py` builds its needles by concatenation so the file
  passes the playbook's own scrub.

## [1.0.0] - 2026-08-30

First complete version, not yet published.

### Added
- `SKILL.md`: agent skill for PythTB 2.0 — model building, invariants, finite
  systems, Wannier90 import, and when to hand off to Kwant.
- `references/`: API map (v1.x → 2.0 + the 2.0.2 traps), invariant recipes and
  conventions, capability matrix vs Kwant, ecosystem/citing.
- `scripts/pythtb_tools.py`: verified helpers — Wilson-loop phases (workaround
  for the 2.0.2 float-cast bug), Wannier-centre-flow Z₂, safe `remove_orb`,
  PythTB → Kwant exporter; `--selftest`, `--version`.
- `scripts/verify_pythtb.py`: environment smoke test with `--data-dir`, `--version`.
- Two executed notebooks (`PythTB_Theory_and_Practice.ipynb`, 31 sections,
  72 checks, 69 captioned figures; `PythTB_Exercises_Solutions.ipynb`, 20
  exercises, 35 checks, 18 figures) generated from `build/` by
  `build/assemble.py` and executed/tallied by `build/execute.py`.
- Test suite (`tests/`): environment, tools, pinned upstream bugs (strict
  xfails), notebook integrity, docs guard, licence guard, Kwant cross-check,
  withheld-material guard. CI workflow for Linux/Windows × Python 3.12/3.13.
- `docs/USER_MANUAL.md` (+ HTML/PDF build), `AGENTS.md`, Apache-2.0 `LICENSE`,
  `NOTICE`, `CITATION.cff`.
