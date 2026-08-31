# Tight-Binding Physics with PythTB — the course

An undergraduate course in ten lectures built on the companion notebook
`PythTB_Theory_and_Practice.ipynb`. **Every figure on every slide is a figure
produced by a notebook cell** — the deck shows the notebook's own caption,
figure number and cell under each image, and a test fails if a figure on disk
no longer matches the notebook output.

```
course/
  deck/index.html         the slides (reveal.js, offline; open in a browser)   GENERATED
  deck/content.en.js      THE SOURCE: sections, slides, levels, figures, notes
  deck/figs/*.png         figures extracted from the notebook + provenance.json  GENERATED
  handout/handout.html    A4 companion handout (syllabus, key ideas, equations,
                          glossary); handout.pdf via make_handout.py           GENERATED
  notes/LECTURER_NOTES.md every slide's notes with the anticipated question   GENERATED
  shared/                 theme.css, nav.js, loader.js + vendored reveal.js 5.2.0 (MIT)
  tools/                  extract_figures.py, build_deck.py (stdlib) ·
                          verify_deck.py, build_pptx.py, make_handout.py (Playwright, optional)
```

## Syllabus

| | Lecture | Notebook |
|---|---|---|
| L0 | Welcome — what tight binding is, how the course runs, the one Hamiltonian | §0–1 |
| L1 | From atoms to bands — the monatomic chain, Bloch's theorem, the first band structure | §1–2 |
| L2 | The SSH chain — dimerization, gap closing, end states, Wannier centre, winding number | §3, §6, §13 |
| L3 | Graphene & flat bands — Dirac cones and how to gap them, Lieb/kagome, ribbons, supercells | §4–7 |
| L4 | Spin, 3D, materials — Rashba + Zeeman, simple cubic and its DOS, silicon from Wannier90 | §8, §11–12 |
| L5 | Berry phase & pumping — polarization as a Wannier centre, the Thouless pump | §9–10 |
| L6 | Chern insulators — the Haldane model, Berry curvature, phase diagram, chiral edges, local marker | §14 |
| L7 | Z₂ & spin Hall — band inversion, Kramers pairs, Wannier flow, helical edges (Kane–Mele, BHZ) | §15–16 |
| L8 | Corners, Majoranas, Weyl — BBH quadrupole, Kitaev chain, Weyl monopoles and Fermi arcs, axion angle | §17–20 |
| L9 | Stretching PythTB — Peierls phases and the butterfly, Anderson localization, Penrose, the O(N³) wall | §21–24 |
| L10 | Limits & what next — five things PythTB cannot do, silent wrongness, mean-field Hubbard, PythTB vs Kwant | §25–31 |

Each lecture is one **vertical stack** of slides ordered *intro → core → math*
(the chip at the top-right of every slide says which): a first-year audience
stops after the core slides, a fourth-year audience goes on to the equations.
Every slide has lecturer notes ending with an anticipated student question and
its answer (`S` opens the speaker view).

## Presenting

Open `deck/index.html` in any modern browser — no server, no network.

| Key | Action |
|---|---|
| `→` / `←`, clicker | next / previous slide (linear through the whole grid) |
| `Shift+→` / `Shift+←`, bottom-right buttons | jump to the next / previous lecture |
| bottom-right lower row | next / previous slide within the lecture (restart on ←) |
| `S` | speaker view with the notes |
| `Esc` | overview grid |
| click the progress bar | jump to that lecture |

PowerPoint: `python course/tools/build_pptx.py` writes a `.pptx` with one
full-bleed screenshot per slide and the notes as editable speaker notes.

## Rebuilding

The content file is the only thing to edit. From `pythtb-skill/`:

```bash
python course/tools/extract_figures.py     # notebook outputs -> deck/figs/*.png + provenance.json
python course/tools/build_deck.py          # content.en.js -> index.html, handout.html, LECTURER_NOTES.md
python -m pytest tests/test_course.py      # provenance fresh, outputs fresh, every slide well-formed
```

Both stdlib tools accept `--check` (exit 1 when their outputs are stale); the
suite runs those checks. When the notebook is re-executed (`build/execute.py`)
the figures must be re-extracted, or `test_course.py` says which ones drifted.

Optional tooling (headless Chromium, not needed to present or to run the suite):

```bash
python -m pip install -r course/tools/requirements.txt && python -m playwright install chromium
python course/tools/verify_deck.py         # walk every slide: console errors, overflow, screenshots
python course/tools/build_pptx.py          # course/build/<title>.pptx
python course/tools/make_handout.py        # course/handout/handout.pdf (A4)
```

## Content model (`deck/content.en.js`)

Strict JSON after `window.DECK_CONTENT =`, so Python and the browser read the
same file. `sections` (name, lecture label, notebook range, summary),
`stacks` (the order of slides in each vertical stack), `slides` (per slide:
`level` ∈ intro/core/math, `layout` ∈ hero · text · syllabus · eq · code ·
fig · fig-right · fig-left · two-figs · table, `title`, `lead`, `bullets`,
`eqs`, `code`, `table`, `fig`/`fig2` as provenance keys such as `s14-f3`,
`notes` with a `Q:`/`A:` pair), `glossary`. Prose may contain HTML; math is
set by hand with `<span class='math'>` (italic serif) and `<span class='fn'>`
(roman functions) — no MathJax, so the deck works offline. A second language
is a second content file with the same keys.

## Licence

Course material: Apache-2.0 (see `../LICENSE`, `../NOTICE`). `shared/reveal/`
is reveal.js 5.2.0 by Hakim El Hattab and contributors, MIT (`shared/reveal/LICENSE`).
PythTB (GPL-3.0-or-later) is used through its public API; the figures are the
notebook's own output.
