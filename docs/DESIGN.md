# Design notes — pythtb-skill

The decisions behind this repository, what each one cost, and what was rejected.
`README.md` is the product page, `AGENTS.md` the inventory and contract; this file is the
*why*. The division of labour is in the README's CRediT table: scope, physics targets and
every presentation and publication decision are the author's; the check-everything
methodology was set jointly; the code, checks and drafts were produced by the AI assistant
and kept only after the author's review.

## 1. The problem framing

PythTB is the pure-Python tight-binding package behind Vanderbilt's *Berry Phases in
Electronic Structure Theory*. Its tutorials are canonical but short, and an AI agent asked
to "compute the Z₂ invariant with PythTB" has no verified reference for the traps
(orbital conventions, Wannier-centre flow, what PythTB cannot do). This repository is
four things sharing one verified core: an agent skill (`SKILL.md` + `references/`), a
helper toolkit (`scripts/pythtb_tools.py`), a book of executed chapter notebooks in which
every physics claim is asserted inline (107 checks, 87 figures), and an undergraduate
course whose every figure is a notebook output.

## 2. Decisions and their trade-offs

| Decision | Why | What it costs / what was rejected |
|---|---|---|
| **The notebooks are generated from Python sources** (`build/part*.py` hold the cells; `build/assemble.py` writes the notebooks; `build/execute.py` runs them and tallies checks). | Notebook JSON diffs are unreviewable; sources make every cell a reviewable, testable line, and `chapter_cells(key)` is a single truth the suite compares against. | Editing a notebook directly is forbidden and lost at the next assemble; contributors must learn the build. Rejected: hand-edited notebooks. |
| **Check everything.** Each physics statement is an `assert` in the cell that makes it (sum rules, quantised invariants, agreement with the analytic phase boundary, cross-checks against Kwant). | A course that states a result without checking it is not distinguishable from a wrong one; the checks are what make an AI-built text trustworthy. | Checks cost cells and run time; a tightened tolerance can break a chapter. The Kwant cross-check found a real bug in the exporter, which is the argument for keeping them. |
| **Chapter notebooks, each under 1 MB, with a TOC and continuous figure numbering** (1.4.0). | Monoliths at several MB crashed editors and sessions. | The reader loses the one-file book; `chapters/README.md` (generated) is the index. |
| **`z2_wcc_flow` and friends are pedagogical implementations, not production invariant calculators.** | Showing the method in thirty readable lines is the point; Z2Pack and WannierBerri exist for production. | No convergence bookkeeping, dense and slow by design; the README comparison table says so. |
| **Course content lives in one JSON-like source** (`course/deck/content.en.js`); figures are extracted from the executed chapters with a provenance record (`provenance.json`: chapter, cell, figure number, caption). | Every slide figure must be traceable to the cell that made it; no figure enters the deck by hand. | A figure change in the book means re-extracting; the deck cannot show a figure the book does not. |
| **PythTB 2.0.2 pinned; Wannier90 silicon data kept as upstream GPL data with its own README.** | The chapters assert numerical values; a new PythTB release must be re-verified, not silently absorbed. The dataset is data, not code, and is labelled as such. | Lag behind upstream (mitigated by the weekly watch, `scripts/watch_upstream.py`). |
| **Apache-2.0, `NOTICE` with licence-by-origin, independence from the PythTB project stated.** | Nothing of PythTB is vendored; the name is used to identify the package taught. | Findings for upstream go through the author, never from the repository. |
| **Published by `git subtree split` of the study repository's product folder.** | The study repo holds upstream clones and drafts that must never be public. | The public history is short and rebuilt; contributors do not see the study history. |

## 3. Out of scope

Transport (leads, conductance — that is Kwant, and `to_kwant` marks the border), DFT
inputs beyond the shipped Wannier90 example, performance work, and anything PythTB cannot
do (chapter 8 lists it deliberately).

## 4. Open questions

Real-data survival of the toolkit on larger Wannier90 models; a PyPI name for the toolkit
(pinned); translated READMEs and manual (portfolio pin); the profile pin on GitHub is the
author's.
