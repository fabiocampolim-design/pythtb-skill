# AGENTS.md — machine-oriented description of this repository

Hand this file to an AI agent (or read it yourself) before changing anything
in this repository. It is the complete contract: what exists, how it is built,
how it is verified, and the rules that must not be broken. Keep it in sync with
`README.md` and `docs/USER_MANUAL.md` whenever a feature changes —
`tests/test_docs_guard.py` fails when a CLI flag or a count drifts.
(`SKILL.md` is the *other* agent file: it teaches an agent how to use PythTB,
not how to maintain this repository.)

## 1. What this repository is

`pythtb-skill` = an AI-agent skill (`SKILL.md` + `references/`), a verified
helper module (`scripts/pythtb_tools.py`), an environment check
(`scripts/verify_pythtb.py`), a weekly upstream watch (`scripts/watch_upstream.py`
+ `scripts/register_watch_task.ps1`), a book of executed chapter notebooks on
**PythTB 2.0.2** in which every physics claim is checked inline, and an
undergraduate course (`course/`) whose every figure is a notebook output. Licence
Apache-2.0 (`LICENSE`, `NOTICE`); version in `VERSION` (1.3.0), history in
`CHANGELOG.md`, citation in `CITATION.cff`.

| Path | Role |
|---|---|
| `SKILL.md` | agent skill: five PythTB workflows + ground rules; frontmatter `name: pythtb`, `license: Apache-2.0` |
| `references/api-map.md`, `invariants.md`, `limitations.md`, `ecosystem.md` | distilled, verified reference docs the skill points to |
| `scripts/pythtb_tools.py` | helpers: `wilson_phases`, `z2_from_wcc`, `z2_wcc_flow`, `remove_orb_copy`, `to_kwant`; CLI `--selftest`, `--quiet`, `--version`; `build_parser()` exposed |
| `scripts/verify_pythtb.py` | 5-check environment smoke test; CLI `--data-dir`, `--quiet`, `--version`; `build_parser()` exposed |
| `scripts/watch_upstream.py` | weekly upstream watch of github.com/pythtb/pythtb + PyPI (rule 23): `--weekly` writes `../docs/watch/YYYY-WW.md`, `--snapshot`, `--pull`, `--state-dir`, `--upstream-dir`, `--outdir`, `--log-dir`, `--quiet`, `--version`; exit 1 when unreachable; `build_parser()` exposed |
| `scripts/register_watch_task.ps1` | Windows Task Scheduler job for the watch (Mondays 08:00): `-Python`, `-Day`, `-At`, `-Remove`, `-DryRun`, `-Version` |
| `chapters/` | **the book, one notebook per chapter** (Parts I–IV, §1–31, 72 checks, 69 figures) + two exercise notebooks (I.1–IV.4, 35 checks, 18 figures); `chapters/README.md` is the generated index. Every notebook is self-contained: generated header (title, TOC with `sec-N`/`ex-X-n` anchors, prev/index/next links), the shared setup cell, the part's cells, a generated tally cell |
| `chapters/PythTB_00_Introduction.ipynb` | chapter 0: Introduction |
| `chapters/PythTB_01_Foundations.ipynb` | chapter 1: Foundations: chains, SSH, graphene and flat bands |
| `chapters/PythTB_02_Finite_Systems_and_Berry_Phases.ipynb` | chapter 2: Finite systems, spin and the Berry-phase machinery |
| `chapters/PythTB_03_Three_Dimensions_and_Wannier.ipynb` | chapter 3: Three dimensions, Wannier90 import and Wannierization |
| `chapters/PythTB_04_Chern_and_Z2.ipynb` | chapter 4: Chern and Z₂ insulators: Haldane, Kane–Mele, BHZ |
| `chapters/PythTB_05_Higher_Order_and_Kitaev.ipynb` | chapter 5: Higher-order topology and the Kitaev chain |
| `chapters/PythTB_06_Weyl_and_Axion.ipynb` | chapter 6: Weyl semimetals and the axion angle |
| `chapters/PythTB_07_Stretching_PythTB.ipynb` | chapter 7: Stretching PythTB: butterfly, disorder, quasicrystal, the wall |
| `chapters/PythTB_08_What_PythTB_Cannot_Do.ipynb` | chapter 8: What PythTB cannot do |
| `chapters/PythTB_Exercises_I-II.ipynb` | Exercises and worked solutions — Parts I–II |
| `chapters/PythTB_Exercises_III-IV.ipynb` | Exercises and worked solutions — Parts III–IV |
| `build/part*.py`, `build/ex_part*.py`, `build/ex_common.py` | **source of truth** for the notebook cells (`CELLS` lists); `part00_intro.py` holds the introduction and the shared `SETUP_TEMPLATE`, `ex_common.py` the exercises' intro + setup template |
| `build/assemble.py` | `CHAPTERS` table (key, file, title, part, series, part modules) → `chapters/*.ipynb` (no outputs) + `chapters/README.md`; `chapter_cells(key)` is the single truth a test compares against; flags `--which` (all/main/exercises/key), `--outdir`, `--log-dir`, `--list`, `--verbose`, `--quiet` |
| `build/execute.py` | execute every chapter on kernel `pythtb-mc`, store outputs, tally per notebook and per series; flags `--which`, `--indir`, `--outdir`, `--log-dir`, `--kernel`, `--timeout`, `--tally-only`, `--verbose`, `--quiet` |
| `build/nbbuild.py`, `build/buildlog.py` | cell/notebook writer (`KERNELSPEC`); audit logger |
| `course/deck/content.en.js` | **source of truth for the course**: sections, stacks (slide order), slides (level intro/core/math, layout, figure keys, notes with Q/A), glossary; strict JSON after `window.DECK_CONTENT =` |
| `course/tools/extract_figures.py` | chapter-notebook PNG outputs (all book chapters in order) → `course/deck/figs/sNN-fK.png` + `provenance.json` (chapter, section, cell, figure number, caption, SHA-256); flags `--notebook` (one or more), `--outdir`, `--check`, `--quiet`, `--version`; `build_parser()` exposed |
| `course/tools/build_deck.py` | content → `deck/index.html` (FLAT reveal.js deck, single-level arrow navigation, one generated divider slide per lecture), `handout/handout.html` (A4), `notes/LECTURER_NOTES.md`; flags `--content`, `--check`, `--quiet`, `--version`; `build_parser()` exposed |
| `course/tools/verify_deck.py` | optional (Playwright): walk every slide, console errors, geometry overflow, screenshots; flags `--index`, `--screens`, `--no-screens`, `--quiet`, `--version` |
| `course/tools/build_pptx.py`, `make_handout.py` | optional (Playwright, python-pptx): PPTX with speaker notes (`--index`, `--out`, `--quiet`, `--version`); handout PDF (`--src`, `--out`, `--quiet`, `--version`) |
| `course/tools/make_slides_pdf.py` | renders the deck's print layout to the **committed** PDF fallback `course/slides.pdf` (one page per slide, all figures, full captions); flags `--index`, `--out`, `--quiet`, `--version`; `build_parser()` exposed |
| `course/slides.pdf` | the presentation without a browser — regenerate and commit it with every deck change (a test counts its pages) |
| `course/shared/` | `theme.css`, `nav.js` (DeckNav), `loader.js` (data-t injection, nested keys) + vendored reveal.js 5.2.0 (MIT) |
| `course/README.md` | syllabus, presenting keys, rebuild commands, content model |
| `docs/USER_MANUAL.md`, `docs/build_manual.py` | user manual; `build_manual.py --outdir`, `--no-pdf`, `--verbose` → HTML (+ PDF with pandoc/xelatex) |
| `install_pythtb_windows.ps1` | conda env + kernel installer (`-EnvName -KernelName -PythonVersion -SkipVerify`) |
| `requirements.txt` | pins (`pythtb==2.0.2`) |
| `data/w90_silicon/` | Wannier90 silicon dataset (upstream GPL data, `data/README.md`) |
| `tests/` | pytest suite, see §4 |
| `.github/workflows/tests.yml` | CI: fast suite on Linux/Windows/macOS × 3.12/3.13, plus a full execution of every chapter notebook |

The study material around this product (upstream audit, findings backlog,
issue drafts, mirrors, withheld sections) lives in the parent folder and is
**not** part of this repository.

## 2. Environment

- Python 3.12, packages from `requirements.txt`; kernel name **`pythtb-mc`**
  (display "Python 3.12 (miniconda - pythtb)"). The notebooks' `kernelspec` is
  pinned to that name; `build/nbbuild.py:KERNELSPEC` is the single place it is defined.
- Windows console: set `PYTHONIOENCODING=utf-8` before any Python that prints the
  notebooks (they contain Greek letters and arrows).
- Kwant is intentionally absent from the pythtb env. `tests/test_kwant_crosscheck.py`
  and `test_tools.py::test_to_kwant_*` skip unless both `kwant` and `pythtb` import.
- Every script reads the version from `VERSION` and prints it with `--version`.

## 3. Workflows

### Change a notebook
1. Edit the relevant `build/part*.py` (book) or `build/ex_part*.py` (exercises).
   Cells are `md(r"""...""")` / `code(r"""...""")` tuples in a `CELLS` list.
   Every figure must be followed by `caption("...")` (exactly one call per figure,
   never in a loop — the assembler counts the calls to offset the figure numbers
   of the following chapters); every physics claim by `check(label, condition, detail)`.
   A chapter must run on its own: if it needs a model defined in an earlier
   chapter, rebuild it in a `# recap` code cell at the top of the part module
   (chapters 2, 3 and 8 do this). The shared setup cell lives in
   `part00_intro.SETUP_TEMPLATE` / `ex_common.SETUP_TEMPLATE` — never copy it into a part.
2. `python build/assemble.py` (or `--which main|exercises|<key>`; `--list` shows the keys).
   Also regenerates `chapters/README.md`.
3. `python build/execute.py` (same `--which`; ~2 min for everything, ≤ 30 s per chapter).
   Exit code ≠ 0 means a `[FAIL]`, an error output, an unexecuted cell or an nbconvert
   failure — read `logs/execute.log` and `logs/nbconvert-*.log`. The notebooks run
   with `chapters/` as working directory; the setup cell resolves `DATA_DIR`
   (`data/` or `../data/`), so never hard-code `data/…` in a cell.
4. `python -m pytest tests` (fast) — must be green before committing; update the
   counts in `README.md`, `docs/USER_MANUAL.md` and this file if they changed
   (`test_docs_guard.py` tells you). If any figure changed, also
   `python course/tools/extract_figures.py`, `build_deck.py`, `make_slides_pdf.py`.
5. Commit the `.py` sources **and** the executed `chapters/*.ipynb` + `chapters/README.md`
   together. A notebook above 1.5 MB fails the suite — split the part module and add
   a row to `CHAPTERS` in `build/assemble.py` instead.

### Change the course
1. Edit `course/deck/content.en.js` only (never `index.html`, the handout or
   the notes — they are generated and a test compares them). Keep each stack
   ordered intro → core → math; every slide needs `notes` with `Q:` and `A:`.
   **Every provenance figure must be used** (a test enforces it).
2. Figures are referenced by provenance key (`s14-f3` = §14, third figure).
   After any notebook re-execution run `python course/tools/extract_figures.py`.
3. `python course/tools/build_deck.py`, then regenerate the committed PDF
   fallback in an env with Playwright: `python course/tools/make_slides_pdf.py`
   (a test counts its pages against the deck).
4. `python -m pytest tests/test_course.py`; optional visual check:
   `course/tools/verify_deck.py` and look at `course/tools/screens/`.

### Add a helper to `scripts/pythtb_tools.py`
Extract it from a notebook cell that already has a passing check; add a test in
`tests/test_tools.py`; add it to `selftest()`; document it in `SKILL.md`, the
module docstring, `README.md` Features and `docs/USER_MANUAL.md`; bump `VERSION`
and add a `CHANGELOG.md` entry (rule: every behaviour change bumps the version).

### Add a section or a chapter
Append `md`/`code` cells to the right part module; keep the `## N. Title` numbering
continuous (§1–31 through the book; `## X.n — Title` in the exercises) — the
assembler derives the TOCs, anchors and the index from these headings. A new
chapter is a new part module plus a row in `CHAPTERS` (`build/assemble.py`); the
introduction's chapter list and `chapters/README.md` follow automatically. Update
the capability matrix (§30) and `references/limitations.md` if the new section
changes what PythTB is claimed to do.

### Release
Bump `VERSION`, add the `CHANGELOG.md` section, update `CITATION.cff`
(`version`, `date-released`), run the full suite (`--run-notebooks`), commit,
`git tag -a vX.Y.Z`. GitHub releases are made by the owner.

### Rebuild the environment
`powershell -ExecutionPolicy Bypass -File .\install_pythtb_windows.ps1`, then
`python scripts/verify_pythtb.py`.

## 4. Tests (`python -m pytest tests`)

| File | What it guards | Needs |
|---|---|---|
| `test_environment.py` | pythtb importable and 2.0.x; SSH gap; Zak phases differ by π; Haldane Chern; W90 silicon loads | pythtb |
| `test_tools.py` | every helper in `scripts/pythtb_tools.py` against the physics it came from; `audit_log`; `--selftest`/`--version` CLI | pythtb (+ kwant for `to_kwant`) |
| `test_watch_upstream.py` | delta/render/pagination helpers, an offline end-to-end `--weekly` run, exit 1 on unreachable upstream, the scheduler script's `-DryRun`/`-Version` | none (PowerShell for the last one, else skipped) |
| `test_upstream_bugs.py` | the two pythtb 2.0.2 bugs the notebooks work around: the workaround passes, the bug itself is a **strict xfail** (XPASS = upstream fixed it → retire the notes) | pythtb |
| `test_notebooks.py` | every committed chapter notebook: 0 FAIL / 0 error / 0 unexecuted, caption == figure count, cells identical to `build/assemble.chapter_cells()`, `chapters/README.md` identical to `index_markdown()`, ≤ 1.5 MB per file, header with a TOC entry + anchor per section and resolving prev/index/next links, shared setup cell first and green tally cell last, figure numbers continuous through the book, book-wide minimum PASS/figure counts, kernel pinned, no personal paths or private codenames. `--run-notebooks` re-executes every chapter into a temp dir | pythtb (+ kernel for the slow test) |
| `test_kwant_crosscheck.py` | exercise IV.1 completed: PythTB→Kwant exporter reproduces spectra and positions | pythtb **and** kwant |
| `test_course.py` | the course: content strict JSON, every slide listed once with level/layout/notes+Q/A, intro→core→math per stack, **every** notebook figure used and byte-identical to the notebook output (`extract_figures --check`), generated deck/handout/notes fresh (`build_deck --check`), a divider per lecture, every `data-t` key resolves, the committed `course/slides.pdf` with one page per slide, reveal.js licence + NOTICE, SPDX, `--version` of the six tools | — |
| `test_docs_guard.py` | every CLI flag of every script appears in this file and the manual; README/manual counts equal the executed notebooks' tallies and state the number of chapters; every chapter file is named in the manual and here; `VERSION` = `CHANGELOG` = `CITATION.cff` | — |
| `test_license.py` | Apache-2.0 `LICENSE` with disclaimers, `NOTICE`, README `## Licence` + `### Disclaimer`, SPDX header in every `.py` | — |
| `test_no_held_material.py` | no tracked text file contains a token whose hash is listed in `tests/held_terms.txt` (material withheld from publication) | git |

All tests skip (never fail) when a dependency is absent.

## 5. Hard rules (do not violate)

1. Never edit the `.ipynb` files by hand; `test_notebooks.py` will fail. Never edit
   `course/deck/index.html`, `course/handout/handout.html` or `course/notes/`;
   `test_course.py` will fail — edit `course/deck/content.en.js` and rebuild.
2. Never add upstream (PythTB) source code, downloaded literature, personal
   paths, e-mail addresses or private project codenames (tests scan for them).
3. Never send anything upstream (issues, PRs) from this repository — drafts and
   their status live in the study folder next to it.
4. Never claim a cell count, PASS count or "0 errors" without running
   `build/execute.py` (or `--tally-only`) and quoting its output.
5. Backslash-heavy strings (LaTeX): patch with an editor tool, not through a bash
   heredoc on Windows (`\v`, `\f` collapse into control characters).
6. Every `.py` file starts with `# SPDX-License-Identifier: Apache-2.0` and the
   copyright line; never strip the disclaimer from `LICENSE` or `README.md`.
7. Commit author: the GitHub noreply identity configured in the repo; trailer
   `Co-Authored-By: Claude <model> <noreply@anthropic.com>`. Every behaviour
   change bumps `VERSION` and gets a `CHANGELOG.md` line.

## 6. File schemas

- **Part module**: `CELLS: list[tuple[str, str]]` with kind `"md"` or `"code"`.
  Helpers available in every code cell of every chapter (the shared setup cell,
  `part00_intro.SETUP_TEMPLATE`): `check(label, ok, detail="")`, `caption(text)`,
  `draw_bonds(ax, xy, pairs, ...)`, `DATA_DIR`, a seeded `rng =
  np.random.default_rng(2026)` (re-seeded per chapter), `t_chapter_start`.
  The exercise notebooks share `ex_common.SETUP_TEMPLATE` (`check`, `caption`,
  `DATA_DIR`, model factories). `build/assemble.py` substitutes `__FIG_OFFSET__`
  and `__CHAPTER__` in the templates and `__CHAPTER_LIST__` in the introduction.
- **Chapter table** (`build/assemble.CHAPTERS`): `Chapter(key, file, title, part,
  series, parts)`; `series` is `main` or `exercises`; `outputs(root)` maps keys to paths.
- **Course content** (`course/deck/content.en.js`): `{lang, deckTitle, deckSubtitle,
  author, edition, sections: {key: {name, lecture, notebook, summary}}, stacks:
  [{sec, slides: [id]}], slides: {id: {level, layout, title, lead?, bullets?[],
  eqs?[{label, math}], code?, table?{head, rows}, fig?, fig2?, kicker?, sub?, notes}},
  glossary: [[term, definition]]}`. `lecture` empty = not a lecture (the closing stack).
- **Figure provenance** (`course/deck/figs/provenance.json`): `{notebooks: [chapter
  files in order], figures: {"sNN-fK.png": {chapter, section, heading, cell, figure,
  caption, sha256, bytes}}}` (`cell` is the index inside that chapter notebook).
- **Audit log** (`logs/<tool>.log`): blocks of `=== <tool> <iso-timestamp>`, `cmd:`,
  `cwd:`, `versions:`, `INFO|WARN|ERROR|DEBUG <msg>` lines, `outcome: rc=<n> wall=<s>`.
- **Tally** (`build/execute.py:tally(path)`): dict with `cells, code, pass, fail,
  errors, figures, captions, unexecuted, fail_labels`.
- **`z2_from_wcc(wcc, ref)`** input: array `(n_k, 2)` of the two occupied Wannier
  centres in [0, 1) sampled over half the BZ; output 0 or 1.
- **`wilson_phases(wfa, axis_idx, state_idx)`** output: array
  `(*transverse_shape, n_states)` of phases in (−π, π], sign as `berry_phase`.
