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
+ `scripts/register_watch_task.ps1`) and two executed Jupyter notebooks on
**PythTB 2.0.2** in which every physics claim is checked inline. Licence
Apache-2.0 (`LICENSE`, `NOTICE`); version in `VERSION` (1.1.0), history in
`CHANGELOG.md`, citation in `CITATION.cff`.

| Path | Role |
|---|---|
| `SKILL.md` | agent skill: five PythTB workflows + ground rules; frontmatter `name: pythtb`, `license: Apache-2.0` |
| `references/api-map.md`, `invariants.md`, `limitations.md`, `ecosystem.md` | distilled, verified reference docs the skill points to |
| `scripts/pythtb_tools.py` | helpers: `wilson_phases`, `z2_from_wcc`, `z2_wcc_flow`, `remove_orb_copy`, `to_kwant`; CLI `--selftest`, `--quiet`, `--version`; `build_parser()` exposed |
| `scripts/verify_pythtb.py` | 5-check environment smoke test; CLI `--data-dir`, `--quiet`, `--version`; `build_parser()` exposed |
| `scripts/watch_upstream.py` | weekly upstream watch of github.com/pythtb/pythtb + PyPI (rule 23): `--weekly` writes `../docs/watch/YYYY-WW.md`, `--snapshot`, `--pull`, `--state-dir`, `--upstream-dir`, `--outdir`, `--log-dir`, `--quiet`, `--version`; exit 1 when unreachable; `build_parser()` exposed |
| `scripts/register_watch_task.ps1` | Windows Task Scheduler job for the watch (Mondays 08:00): `-Python`, `-Day`, `-At`, `-Remove`, `-DryRun`, `-Version` |
| `PythTB_Theory_and_Practice.ipynb` | main notebook: Parts I–IV, §1–31, 116 cells, 72 checks, 69 figures |
| `PythTB_Exercises_Solutions.ipynb` | 20 worked exercises (I.1–IV.4), 44 cells, 35 checks, 18 figures |
| `build/part*.py`, `build/ex_part*.py` | **source of truth** for the notebook cells (`CELLS` lists) |
| `build/assemble.py` | part modules → `.ipynb` (no outputs); flags `--which`, `--outdir`, `--log-dir`, `--list`, `--verbose`, `--quiet` |
| `build/execute.py` | execute on kernel `pythtb-mc`, store outputs, tally; flags `--which`, `--indir`, `--outdir`, `--log-dir`, `--kernel`, `--timeout`, `--tally-only`, `--verbose`, `--quiet` |
| `build/nbbuild.py`, `build/buildlog.py` | cell/notebook writer (`KERNELSPEC`); audit logger |
| `docs/USER_MANUAL.md`, `docs/build_manual.py` | user manual; `build_manual.py --outdir`, `--no-pdf`, `--verbose` → HTML (+ PDF with pandoc/xelatex) |
| `install_pythtb_windows.ps1` | conda env + kernel installer (`-EnvName -KernelName -PythonVersion -SkipVerify`) |
| `requirements.txt` | pins (`pythtb==2.0.2`) |
| `data/w90_silicon/` | Wannier90 silicon dataset (upstream GPL data, `data/README.md`) |
| `tests/` | pytest suite, see §4 |
| `.github/workflows/tests.yml` | CI: fast suite on Linux/Windows × 3.12/3.13, plus a full notebook execution |

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
1. Edit the relevant `build/part*.py` (main) or `build/ex_part*.py` (exercises).
   Cells are `md(r"""...""")` / `code(r"""...""")` tuples in a `CELLS` list.
   Every figure must be followed by `caption("...")`; every physics claim by
   `check(label, condition, detail)`.
2. `python build/assemble.py` (or `--which main|exercises`).
3. `python build/execute.py` (same `--which`; ~1.5 min per notebook). Exit code ≠ 0
   means a `[FAIL]`, an error output, an unexecuted cell or an nbconvert failure —
   read `logs/execute.log` and `logs/nbconvert-*.log`.
4. `python -m pytest tests` (fast) — must be green before committing; update the
   counts in `README.md`, `docs/USER_MANUAL.md` and this file if they changed
   (`test_docs_guard.py` tells you).
5. Commit the `.py` sources **and** the executed `.ipynb` together.

### Add a helper to `scripts/pythtb_tools.py`
Extract it from a notebook cell that already has a passing check; add a test in
`tests/test_tools.py`; add it to `selftest()`; document it in `SKILL.md`, the
module docstring, `README.md` Features and `docs/USER_MANUAL.md`; bump `VERSION`
and add a `CHANGELOG.md` entry (rule: every behaviour change bumps the version).

### Add a section
Append `md`/`code` cells to the right part module; keep the `## N. Title` numbering
continuous (§1–31 in the main notebook; `## X.n — Title` in the exercises); update
the "Contents" list in `build/part00_intro.py`, the capability matrix (§30) and
`references/limitations.md` if the new section changes what PythTB is claimed to do.

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
| `test_notebooks.py` | committed notebooks: 0 FAIL / 0 error / 0 unexecuted, caption == figure count, minimum PASS counts, cells identical to `build/` sources, kernel pinned, no personal paths or private codenames. `--run-notebooks` re-executes both into a temp dir | pythtb (+ kernel for the slow test) |
| `test_kwant_crosscheck.py` | exercise IV.1 completed: PythTB→Kwant exporter reproduces spectra and positions | pythtb **and** kwant |
| `test_docs_guard.py` | every CLI flag of every script appears in this file and the manual; README/manual counts equal the executed notebooks' tallies; `VERSION` = `CHANGELOG` = `CITATION.cff` | — |
| `test_license.py` | Apache-2.0 `LICENSE` with disclaimers, `NOTICE`, README `## Licence` + `### Disclaimer`, SPDX header in every `.py` | — |
| `test_no_held_material.py` | no tracked text file contains a token whose hash is listed in `tests/held_terms.txt` (material withheld from publication) | git |

All tests skip (never fail) when a dependency is absent.

## 5. Hard rules (do not violate)

1. Never edit the `.ipynb` files by hand; `test_notebooks.py` will fail.
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
  Helpers available in every code cell of the main notebook (defined in
  `part00_intro.py`'s setup cell): `check(label, ok, detail="")`, `caption(text)`,
  `draw_bonds(ax, xy, pairs, ...)`, a seeded `rng = np.random.default_rng(2026)`.
  The exercises notebook defines its own `check`/`caption` in `ex_part1_2.py`.
- **Audit log** (`logs/<tool>.log`): blocks of `=== <tool> <iso-timestamp>`, `cmd:`,
  `cwd:`, `versions:`, `INFO|WARN|ERROR|DEBUG <msg>` lines, `outcome: rc=<n> wall=<s>`.
- **Tally** (`build/execute.py:tally(path)`): dict with `cells, code, pass, fail,
  errors, figures, captions, unexecuted, fail_labels`.
- **`z2_from_wcc(wcc, ref)`** input: array `(n_k, 2)` of the two occupied Wannier
  centres in [0, 1) sampled over half the BZ; output 0 or 1.
- **`wilson_phases(wfa, axis_idx, state_idx)`** output: array
  `(*transverse_shape, n_states)` of phases in (−π, π], sign as `berry_phase`.
