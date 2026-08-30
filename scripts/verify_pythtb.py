# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Environment smoke test for the PythTB notebooks and tools.

Targets PythTB >= 2.0 (TBModel / Lattice / Mesh / WFArray API). Checks, in order:
  1. imports and versions
  2. a band-structure solve (SSH chain)
  3. the Berry-phase machinery (SSH Berry phases differ by pi between dimerisations)
  4. a Chern number (Haldane model, |C| = 1 for the lower band)
  5. presence of the Wannier90 silicon dataset used by the W90 section

Usage:
    python scripts/verify_pythtb.py                 # data expected in <repo>/data/w90_silicon
    python scripts/verify_pythtb.py --data-dir D    # elsewhere
    python scripts/verify_pythtb.py -q              # only the verdict
    python scripts/verify_pythtb.py --version
Exit code 0 when every check passes, 1 otherwise.
"""

import argparse
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))


def _version():
    try:
        with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "unknown"


def build_parser():
    ap = argparse.ArgumentParser(prog="verify_pythtb", description=__doc__.splitlines()[0])
    ap.add_argument("--data-dir", default=os.path.join(ROOT, "data", "w90_silicon"),
                    help="directory holding si.win / si_hr.dat / ... (default: <repo>/data/w90_silicon)")
    ap.add_argument("-q", "--quiet", action="store_true", help="print only the final verdict")
    ap.add_argument("--version", action="version", version=f"pythtb-skill {_version()}")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    all_ok = True

    def check(label, ok, detail=""):
        nonlocal all_ok
        all_ok &= bool(ok)
        if not args.quiet:
            print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))

    import matplotlib
    import pythtb
    import scipy
    from importlib.metadata import version as dist_version

    check("imports", True,
          f"pythtb {dist_version('pythtb')} (module reports {getattr(pythtb, '__version__', '?')}), "
          f"numpy {np.__version__}, scipy {scipy.__version__}, matplotlib {matplotlib.__version__}")

    from pythtb import Lattice, Mesh, TBModel, WFArray

    def ssh(t_intra, t_inter):
        lat = Lattice(lat_vecs=[[1.0]], orb_vecs=[[0.0], [0.5]], periodic_dirs=[0])
        m = TBModel(lat)
        m.set_hop(t_intra, 0, 1, [0])
        m.set_hop(t_inter, 1, 0, [1])
        return m

    kpts = np.array([[k] for k in np.linspace(0.0, 1.0, 51)])
    evals = ssh(1.0, 0.5).solve_ham(kpts)
    gap = evals[:, 1].min() - evals[:, 0].max()
    check("SSH band solve", np.isclose(gap, 1.0, atol=1e-10), f"gap = {gap:.6f} (expect 1.0)")

    def zak(m):
        mesh = Mesh(["k"])
        mesh.build_grid([61], k_endpoints=True)
        w = WFArray(m.lattice, mesh)
        w.solve_model(m)
        return float(np.squeeze(w.berry_phase(axis_idx=0, state_idx=[0])))

    dphi = (zak(ssh(1.0, 0.5)) - zak(ssh(0.5, 1.0))) % (2 * np.pi)
    check("SSH Berry phase (trivial vs topological differ by pi)",
          np.isclose(dphi, np.pi, atol=1e-6), f"delta phase = {dphi:.6f}")

    from pythtb.models import haldane

    h = haldane(delta=0.0, t1=-1.0, t2=0.15 * np.exp(1j * np.pi / 2))
    mesh2 = Mesh(["k", "k"])
    mesh2.build_grid(shape=(31, 31), k_endpoints=[True, True])
    w2 = WFArray(h.lattice, mesh2)
    w2.solve_model(h)
    c = float(w2.chern_number(state_idx=[0], plane=(0, 1)))
    check("Haldane Chern number", np.isclose(abs(c), 1.0, atol=1e-6), f"|C| = {abs(c):.8f}")

    needed = ["si.win", "si_hr.dat", "si_band.dat", "si_band.kpt", "si_centres.xyz"]
    present = os.path.isdir(args.data_dir) and all(
        os.path.exists(os.path.join(args.data_dir, f)) for f in needed)
    check("Wannier90 silicon dataset", present,
          args.data_dir if present else f"missing files in {args.data_dir} (W90 section will not run)")

    print("Environment OK." if all_ok else "Environment has problems — see FAIL lines above.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
