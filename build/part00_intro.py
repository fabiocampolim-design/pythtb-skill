# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
from nbbuild import md, code

# The book-level introduction (chapter 0). ``__CHAPTER_LIST__`` is filled in by
# build/assemble.py with links to every chapter notebook.
INTRO_CELLS = [
md(r"""
# PythTB — Tight-Binding Physics from Theory to Code

**A comprehensive, executed tour of what PythTB can compute — and an honest map of what it cannot.**

PythTB is the tight-binding package written by Sinisa Coh and David Vanderbilt as the computational
companion to Vanderbilt's *Berry Phases in Electronic Structure Theory* (Cambridge, 2018). It is
deliberately an *educational* package: about 17 000 lines of pure Python + NumPy, no compiled core,
no solver zoo. Its center of gravity is exactly where Kwant's is weakest — **Berry phases, Wannier
functions, polarization, and topological invariants** — and vice versa: PythTB has **no concept of a
lead, a scattering region, or a conductance**.

This book is the sibling of the companion Kwant notebooks (same author) and follows the same
contract: every claim is executed, every figure is generated live, and physics checks print
`PASS`/`FAIL` inline. It is shipped as **one notebook per chapter** (this folder), each of which
runs on its own; section numbers (§1–31), figure numbers and cross-references are global, so
"§14" means section 14 wherever it lives. The list below and `README.md` link every chapter.

> **Version note.** This book was written and executed against **PythTB 2.0.2** (the 2025
> rewrite: `TBModel`, `Lattice`, `Mesh`, `WFArray`, `Wannier`, `W90`); it should run on any 2.0.x,
> and the two 2.0.2 bugs it works around are flagged where they occur (§7, §9). The 2.0 API is a
> major departure from the classic `tb_model`/`wf_array` API of v1.8 used in Vanderbilt's book and
> in most published examples; we flag the correspondence as we go. PythTB 2.0 also *gained*
> capabilities the classic version never had —
> native spin, built-in Chern numbers, Wilson loops, quantum geometry, an axion-angle routine, a local
> Chern marker, and in-package Wannierization — and these chapters exercise all of them.

**Contents** — one notebook per chapter, all in this folder

__CHAPTER_LIST__

### How to run this

One-time setup (Windows / miniconda):

```powershell
powershell -ExecutionPolicy Bypass -File .\install_pythtb_windows.ps1
```

This creates the conda env `pythtb` (Python 3.12, `pip install pythtb==2.0.2` plus the pins in
`requirements.txt`) and registers the Jupyter kernel **`Python 3.12 (miniconda - pythtb)`** that
every chapter is pinned to. Verify with `python scripts/verify_pythtb.py` from the repository root.
Running **all** chapters top-to-bottom takes about **two minutes** on a laptop in total; no single
cell needs more than ~20 s and no chapter more than about half a minute. The code cell at the
end of this chapter is the setup cell every chapter starts with — run it here to check the kernel.
"""),

md(r"""
### Conventions used throughout

- Units: $\hbar = e = a = 1$ unless stated; energies in units of the dominant hopping $t$; the
  Wannier90 silicon section uses eV and Å because the data does.
- Reduced coordinates: k-points and orbital positions are given in **fractional (reduced)
  coordinates** of the reciprocal / direct lattice vectors. $k \in [0,1)$ spans the Brillouin zone.
- **Phase convention.** PythTB uses *convention I* of Vanderbilt's book: the Bloch Hamiltonian
  carries orbital-position-resolved phases,

$$
H_{ij}(\mathbf{k}) \;=\; \sum_{\mathbf{R}} t_{ij}(\mathbf{R})\,
   e^{\,i\mathbf{k}\cdot(\mathbf{R} + \boldsymbol\tau_j - \boldsymbol\tau_i)},
$$

  where $\boldsymbol\tau_i$ are orbital positions inside the cell and $t_{ij}(\mathbf{R})$ is the
  hopping from orbital $i$ in the home cell to orbital $j$ in the cell at $\mathbf{R}$. This makes
  Berry phases equal to *physical* Wannier-center positions (polarization), at the cost of
  $H(\mathbf{k}+\mathbf{G}) \neq H(\mathbf{k})$ as matrices (they are unitarily related). Keep this
  in mind when comparing against papers using the other convention.
- `set_hop(t, i, j, R)` sets $t_{ij}(\mathbf{R}) = \langle i,\mathbf{0}|H|j,\mathbf{R}\rangle$; the
  Hermitian conjugate partner is implied — never set it yourself.
- Every section that makes a quantitative claim ends with an inline check that prints **PASS** or
  **FAIL**. A clean run has zero FAILs; the last cell of every chapter counts them.
"""),

]

CELLS = INTRO_CELLS

# The setup cell every chapter starts with. build/assemble.py substitutes
# ``__FIG_OFFSET__`` (figures numbered before this chapter, so numbering runs
# through the book) and ``__CHAPTER__`` (a label for the version line).
SETUP_TEMPLATE = r"""
# ---- shared setup: this cell is identical in every chapter of the book ----------
import os
import time
import warnings

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML

import pythtb
from pythtb import Lattice, TBModel, Mesh, WFArray, Wannier, W90

plt.rcParams.update({
    "figure.dpi": 110,
    "figure.figsize": (7.0, 4.2),
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 10,
})

# the Wannier90 silicon data (§12) lives in data/ at the repository root
DATA_DIR = next((d for d in ("data", os.path.join("..", "data")) if os.path.isdir(d)), "data")

rng = np.random.default_rng(2026)          # single seed for every stochastic cell

_CHECKS = {"pass": 0, "fail": 0}
_FIG = {"n": __FIG_OFFSET__}               # figure numbers run through the whole book

def check(label, ok, detail=""):
    '''Inline physics check; prints PASS/FAIL and tallies for the final summary.'''
    ok = bool(ok)
    _CHECKS["pass" if ok else "fail"] += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    return ok

def caption(text):
    '''Numbered caption rendered directly below the figure it describes.'''
    _FIG["n"] += 1
    display(HTML(
        f"<div style='max-width:780px;margin:2px 0 14px 12px;font-size:0.92em;"
        f"color:#444;border-left:3px solid #bbb;padding-left:10px'>"
        f"<b>Figure {_FIG['n']}.</b> {text}</div>"))

def draw_bonds(ax, xy, pairs, color="0.55", lw=1.0, ls="-", zorder=1):
    '''Draw a set of bonds (index pairs) between the 2D points xy on axis ax —
    used throughout to depict the actual system before computing on it.'''
    for i, j in pairs:
        ax.plot(xy[[i, j], 0], xy[[i, j], 1], ls, color=color, lw=lw, zorder=zorder)

print("pythtb", pythtb.__version__, "| numpy", np.__version__, "| __CHAPTER__")
t_chapter_start = time.time()
"""


def setup_cell(chapter_label, fig_offset):
    """The shared setup code cell, instantiated for one chapter."""
    src = SETUP_TEMPLATE.replace("__FIG_OFFSET__", str(int(fig_offset)))
    return code(src.replace("__CHAPTER__", chapter_label))
