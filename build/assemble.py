# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Assemble the notebooks from the part modules in this directory.

Each part module defines ``CELLS = [("md", ...), ("code", ...), ...]``; the
notebook is the concatenation of its parts, written with the kernel the
project is pinned to (``pythtb-mc``). Cell *outputs* are not produced here —
run ``build/execute.py`` afterwards to execute the notebook in place.

Usage:
    python build/assemble.py                     # both notebooks into the repo root
    python build/assemble.py --which main        # only PythTB_Theory_and_Practice.ipynb
    python build/assemble.py --which exercises
    python build/assemble.py --outdir out/ -v    # elsewhere, chatty
    python build/assemble.py --list              # show parts and cell counts, write nothing

Every invocation appends an audit record to ``<log-dir>/assemble.log``
(default ``<outdir>/logs``) with the command line, versions and outcome.
"""

import argparse
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nbbuild import write_notebook  # noqa: E402
from buildlog import AuditLog  # noqa: E402

NOTEBOOKS = {
    "main": (
        "PythTB_Theory_and_Practice.ipynb",
        [
            "part00_intro",
            "part01a_foundations",
            "part01b_finite_berry",
            "part01c_3d_w90",
            "part02a_chern_z2",
            "part02b_hoti_kitaev",
            "part02c_weyl_axion",
            "part03_stretching",
            "part04_limitations",
        ],
    ),
    "exercises": (
        "PythTB_Exercises_Solutions.ipynb",
        ["ex_part1_2", "ex_part3_4"],
    ),
}


def collect(parts):
    """Return (cells, [(part_name, n_cells), ...]) for the given part modules."""
    cells = []
    per_part = []
    for name in parts:
        mod = importlib.import_module(name)
        per_part.append((name, len(mod.CELLS)))
        cells.extend(mod.CELLS)
    return cells, per_part


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--which", choices=["main", "exercises", "all"], default="all",
                    help="which notebook(s) to assemble (default: all)")
    ap.add_argument("--outdir", default=os.path.normpath(os.path.join(HERE, "..")),
                    help="directory receiving the .ipynb files (default: repository root)")
    ap.add_argument("--log-dir", default=None,
                    help="where the audit log goes (default: <outdir>/logs)")
    ap.add_argument("--list", action="store_true",
                    help="print parts and cell counts, do not write anything")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("-v", "--verbose", action="store_true")
    g.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args(argv)

    log = AuditLog("assemble", args.outdir, args.log_dir, verbose=args.verbose,
                   quiet=args.quiet, dry=args.list)
    which = list(NOTEBOOKS) if args.which == "all" else [args.which]
    rc = 0
    try:
        for key in which:
            fname, parts = NOTEBOOKS[key]
            cells, per_part = collect(parts)
            for name, n in per_part:
                log.debug(f"  {name:<28s} {n:4d} cells")
            if args.list:
                log.info(f"{fname}: {len(cells)} cells from {len(parts)} parts")
                continue
            os.makedirs(args.outdir, exist_ok=True)
            out = os.path.join(args.outdir, fname)
            write_notebook(cells, out, echo=False)
            log.info(f"wrote {out} ({len(cells)} cells)")
    except Exception as exc:  # noqa: BLE001 - the audit log must record any failure
        log.error(f"FAILED: {exc!r}")
        rc = 1
    log.close(rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
