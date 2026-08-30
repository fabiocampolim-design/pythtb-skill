# Changelog

All notable changes to pythtb-skill are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/). The current version is in `VERSION`
and is printed by every script's `--version`.

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
