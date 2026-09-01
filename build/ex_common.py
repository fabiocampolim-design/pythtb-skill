# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Cells shared by the two exercise notebooks: the introduction paragraph and
the setup-cell template (instantiated per notebook by build/assemble.py)."""
from nbbuild import code

INTRO = r"""
Companion to the chapter notebooks of *PythTB — Tight-Binding Physics from Theory to Code*;
the exercise statements live at the end of each part there (chapters 3, 6, 7 and 8). Same
environment (`pythtb-mc` kernel), same conventions, same rule: every claim checks itself with
an inline **PASS/FAIL**, and every solution runs on its own after the setup cell below.
"""

SETUP_TEMPLATE = r"""
# ---- shared setup: this cell is identical in both exercise notebooks -----------
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML

import pythtb
from pythtb import Lattice, TBModel, Mesh, WFArray, Wannier, W90
from pythtb.models import graphene as graphene_factory
from pythtb.models import haldane, kane_mele, ssh, fu_kane_mele

plt.rcParams.update({"figure.dpi": 110, "figure.figsize": (7.0, 4.2),
                     "axes.grid": True, "grid.alpha": 0.3, "font.size": 10})
# the Wannier90 silicon data (exercise I.6) lives in data/ at the repository root
DATA_DIR = next((d for d in ("data", os.path.join("..", "data")) if os.path.isdir(d)), "data")
rng = np.random.default_rng(2026)
_CHECKS = {"pass": 0, "fail": 0}

def check(label, ok, detail=""):
    ok = bool(ok)
    _CHECKS["pass" if ok else "fail"] += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    return ok

_FIG = {"n": __FIG_OFFSET__}               # figure numbers run through both notebooks

def caption(text):
    '''Numbered caption rendered directly below the figure it describes.'''
    _FIG["n"] += 1
    display(HTML(
        f"<div style='max-width:780px;margin:2px 0 14px 12px;font-size:0.92em;"
        f"color:#444;border-left:3px solid #bbb;padding-left:10px'>"
        f"<b>Figure {_FIG['n']}.</b> {text}</div>"))

print("pythtb", pythtb.__version__, "| __CHAPTER__")
t_chapter_start = time.time()
"""


def setup_cell(chapter_label, fig_offset):
    """The shared setup code cell, instantiated for one exercise notebook."""
    src = SETUP_TEMPLATE.replace("__FIG_OFFSET__", str(int(fig_offset)))
    return code(src.replace("__CHAPTER__", chapter_label))
