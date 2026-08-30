# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
from nbbuild import md, code

CELLS = [
md(r"""
# PythTB — Tight-Binding Physics from Theory to Code

**A comprehensive, executed tour of what PythTB can compute — and an honest map of what it cannot.**

PythTB is the tight-binding package written by Sinisa Coh and David Vanderbilt as the computational
companion to Vanderbilt's *Berry Phases in Electronic Structure Theory* (Cambridge, 2018). It is
deliberately an *educational* package: about 17 000 lines of pure Python + NumPy, no compiled core,
no solver zoo. Its center of gravity is exactly where Kwant's is weakest — **Berry phases, Wannier
functions, polarization, and topological invariants** — and vice versa: PythTB has **no concept of a
lead, a scattering region, or a conductance**.

This notebook is the sibling of the companion Kwant notebook (`Kwant_Theory_and_Practice.ipynb`,
same author) and follows the same contract: every claim is executed, every figure is generated
live, and physics checks print `PASS`/`FAIL` inline.

> **Version note.** This notebook was written and executed against **PythTB 2.0.2** (the 2025
> rewrite: `TBModel`, `Lattice`, `Mesh`, `WFArray`, `Wannier`, `W90`); it should run on any 2.0.x,
> and the two 2.0.2 bugs it works around are flagged where they occur (§7, §9). The 2.0 API is a
> major departure from the classic `tb_model`/`wf_array` API of v1.8 used in Vanderbilt's book and
> in most published examples; we flag the correspondence as we go. PythTB 2.0 also *gained*
> capabilities the classic version never had —
> native spin, built-in Chern numbers, Wilson loops, quantum geometry, an axion-angle routine, a local
> Chern marker, and in-package Wannierization — and this notebook exercises all of them.

**Contents**

- **Part I — Fundamentals**: the object model; chains, SSH, graphene, BN, flat bands; finite systems,
  supercells, defects; native spin; the Berry-phase machinery; the Thouless pump; 3D models; Wannier90
  import (silicon); Wannierization inside PythTB.
- **Part II — Topological matter**: Haldane, Kane–Mele, BHZ, BBH quadrupole, Kitaev chain (as a BdG
  hack), Weyl semimetals, Fu–Kane–Mele 3D TI and the axion angle.
- **Part III — Stretching PythTB**: Hofstadter butterfly, disorder and localization, a Penrose
  quasicrystal, and profiling the dense-diagonalization wall.
- **Part IV — What PythTB cannot do**: transport, sparse methods, continuum models, interactions —
  each demonstrated, not just asserted — and a capability matrix against Kwant.

### How to run this

One-time setup (Windows / miniconda):

```powershell
powershell -ExecutionPolicy Bypass -File .\install_pythtb_windows.ps1
```

This creates the conda env `pythtb` (Python 3.12, `pip install pythtb==2.0.2` plus the pins in
`requirements.txt`) and registers the Jupyter kernel **`Python 3.12 (miniconda - pythtb)`** that
this notebook is pinned to. Verify with `conda run -n pythtb python verify_pythtb.py`. A full
top-to-bottom run of this notebook takes about **two minutes** on a laptop (measured 2026-08-28:
1.5 min for 79 code cells); no single cell needs more than ~20 s.
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
  **FAIL**. A clean run has zero FAILs; the final cell of the notebook counts them.
"""),

code(r"""
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

rng = np.random.default_rng(2026)          # single seed for every stochastic cell

_CHECKS = {"pass": 0, "fail": 0}
_FIG = {"n": 0}

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

print("pythtb", pythtb.__version__, "| numpy", np.__version__)
t_notebook_start = time.time()
"""),
]
