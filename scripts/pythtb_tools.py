# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Verified helpers around PythTB 2.0 (https://github.com/pythtb/pythtb).

Everything here was extracted from the executed notebooks of this repository,
where each function is exercised by an inline check, and is covered again by
``tests/test_tools.py``. PythTB itself is GPL-3.0; this module only *calls* it.

Functions
---------
wilson_phases(wfa, axis_idx, state_idx, ...)
    Individual Wilson-loop phases φ_n (mod 2π) from the Wilson unitary — the
    workaround for the pythtb 2.0.2 bug where ``wilson_loop(wilson_evals=True)``
    stores complex eigenvalues in a float array and returns cos φ.
z2_from_wcc(wcc, ref)
    Fu–Kane Z₂ from a Wannier-centre (hybrid Wannier charge centre) flow over
    half the Brillouin zone: parity of the crossings of a reference line, with
    the two centres tracked through their smallest arc (circular statistics).
z2_wcc_flow(model, occ, nk=(41, 31), ref=0.31, spinful=True)
    Z₂ of a spinful 2D model directly from a ``TBModel``.
remove_orb_copy(model, to_remove)
    The behaviour the ``remove_orb`` docstring promises: a *new* model with the
    orbitals removed, the original untouched (pythtb 2.0.2 mutates in place).
to_kwant(model)
    Finite (``dim_k == 0``) spinless ``TBModel`` → ``kwant.Builder`` with one
    sublattice per orbital (positions survive exactly). Needs kwant.

Command line
------------
    python scripts/pythtb_tools.py --selftest      # run the built-in checks
    python scripts/pythtb_tools.py --version
"""

import argparse
import datetime
import importlib
import json
import os
import platform
import sys
import warnings

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))


def version():
    """Version string read from the repository's VERSION file."""
    try:
        with open(os.path.join(_HERE, "..", "VERSION"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "unknown"


__version__ = version()


def audit_log(outdir, argv, extra=None, script="pythtb_tools", log_dir=None):
    """Playbook rule 12: one JSON log per invocation under ``<outdir>/logs/``
    (or exactly ``log_dir`` when a caller passes its ``--log-dir``).

    Returns the path written. Never raises on a serialisation problem — values
    that are not JSON fall back to ``str``.
    """
    logdir = log_dir or os.path.join(outdir, "logs")
    os.makedirs(logdir, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(logdir, f"{script}-{stamp}.log")
    record = {"script": script, "version": __version__, "utc": stamp,
              "argv": list(argv), "python": sys.version.split()[0],
              "platform": platform.platform(), "extra": extra or {}}
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(record, indent=2, default=str) + "\n")
    return path


# --------------------------------------------------------------------------- #
# Wilson loops
# --------------------------------------------------------------------------- #
def wilson_phases(wfa, axis_idx, state_idx, **kwargs):
    """Wilson-loop phases φ_n along ``axis_idx`` for the states in ``state_idx``.

    Returns an array of shape ``(*transverse_shape, n_states)`` with φ_n in
    (−π, π], using the same sign convention as ``WFArray.berry_phase``
    (φ = −arg λ for the eigenvalues λ of the Wilson unitary). Extra keyword
    arguments are passed to ``WFArray.wilson_loop``.

    Why not ``wilson_loop(wilson_evals=True)``? In pythtb 2.0.2 that path
    allocates the eigenvalue array as ``float`` and silently returns cos φ
    (with a numpy ``ComplexWarning``). The unitary itself is correct, so we
    diagonalise it here.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", np.exceptions.ComplexWarning)
        out = wfa.wilson_loop(axis_idx=axis_idx, state_idx=list(state_idx),
                              wilson_evals=True, **kwargs)
    U = np.asarray(out[0] if isinstance(out, tuple) else out)
    n = len(state_idx)
    U = U.reshape(-1, n, n) if U.ndim >= 2 else U.reshape(1, 1, 1)
    lam = np.linalg.eigvals(U)
    phases = -np.angle(lam)
    return phases.reshape(*(U.shape[:-2] or (1,)), n)


# --------------------------------------------------------------------------- #
# Z2 from Wannier-centre flow
# --------------------------------------------------------------------------- #
def _arc(a, b):
    """Signed shortest displacement from a to b on the unit circle [0, 1)."""
    return (b - a + 0.5) % 1.0 - 0.5


def z2_from_wcc(wcc, ref):
    """Fu–Kane Z₂ from a hybrid-Wannier-centre flow.

    ``wcc`` is an array ``(n_k_transverse, 2)`` of the two occupied centres
    (in units of the lattice vector, mod 1) sampled from k = 0 to k = π along
    the transverse direction; ``ref`` is the reference line in [0, 1) — choose
    one that no centre sits on. The two centres are followed through the
    pairing (keep / swap) with the smaller total arc, and each signed crossing
    of the reference line is counted; Z₂ is the parity of the count.
    """
    wcc = np.asarray(wcc) % 1.0
    if wcc.ndim != 2 or wcc.shape[1] != 2:
        raise ValueError("wcc must have shape (n_k, 2) — two occupied centres per k")
    crossings = 0
    for r in range(len(wcc) - 1):
        w1, w2 = wcc[r], wcc[r + 1]
        d_keep = [_arc(w1[0], w2[0]), _arc(w1[1], w2[1])]
        d_swap = [_arc(w1[0], w2[1]), _arc(w1[1], w2[0])]
        d = d_keep if sum(map(abs, d_keep)) <= sum(map(abs, d_swap)) else d_swap
        for a, dd in zip(w1, d):
            if dd > 0 and (ref - a) % 1.0 < dd:
                crossings += 1
            elif dd < 0 and (a - ref) % 1.0 < -dd:
                crossings += 1
    return crossings % 2


def z2_wcc_flow(model, occ=(0, 1), nk=(41, 31), ref=0.31, spinful=True):
    """Z₂ of a 2D (spinful) ``TBModel`` with two occupied bands via WCC flow.

    Builds a ``(nk[0], nk[1])`` k-grid with endpoints, computes the Berry-phase
    eigenvalues (individual Wannier centres) along axis 0 for every k₁, keeps
    the half k₁ ∈ [0, ½] and applies :func:`z2_from_wcc`.
    """
    from pythtb import Mesh, WFArray

    mesh = Mesh(["k", "k"])
    mesh.build_grid(tuple(nk), k_endpoints=[True, True])
    wfa = WFArray(model.lattice, mesh, spinful=spinful)
    wfa.solve_model(model)
    wcc = np.asarray(wfa.berry_phase(axis_idx=0, state_idx=list(occ),
                                     berry_evals=True, contin=False)) / (2 * np.pi) % 1.0
    k1 = mesh.get_axis_range(1, 1)
    return z2_from_wcc(wcc[k1 <= 0.5 + 1e-9], ref)


# --------------------------------------------------------------------------- #
# Model surgery
# --------------------------------------------------------------------------- #
def remove_orb_copy(model, to_remove):
    """Return a copy of ``model`` with orbitals ``to_remove`` removed.

    pythtb 2.0.2's ``TBModel.remove_orb`` mutates in place and returns None
    although its docstring shows ``small = big.remove_orb([...])``; this
    function gives the documented behaviour without touching ``model``.
    """
    new = model.copy()
    new.remove_orb(to_remove)
    return new


# --------------------------------------------------------------------------- #
# Export to Kwant
# --------------------------------------------------------------------------- #
def to_kwant(model):
    """Translate a finite, spinless PythTB ``TBModel`` into a ``kwant.Builder``.

    Every orbital becomes its own Kwant sublattice (basis vector), so arbitrary
    positions survive exactly. Onsites come from the diagonal of
    ``model.hamiltonian()``, hoppings from its upper triangle.

    Do **not** build one square lattice and call ``lat(*position)``: Kwant
    reads those arguments as integer lattice indices, orbitals collapse onto
    shared sites and Kwant refuses the resulting self-hopping (a bug in an
    earlier version of this exporter, caught by ``tests/test_kwant_crosscheck.py``).
    """
    import kwant  # optional dependency

    if getattr(model, "dim_k", 0) not in (0, None) and model.dim_k != 0:
        raise ValueError("to_kwant handles finite (dim_k == 0) models only")
    pos = np.asarray(model.orb_vecs) @ np.asarray(model.lat_vecs)
    dim = pos.shape[1]
    lat = kwant.lattice.general(np.eye(dim), basis=pos, norbs=1)
    syst = kwant.Builder()
    origin = (0,) * dim
    sites = [sub(*origin) for sub in lat.sublattices]
    H = model.hamiltonian()
    for i, s in enumerate(sites):
        syst[s] = float(np.real(H[i, i]))
    ii, jj = np.nonzero(np.triu(np.abs(H), 1) > 1e-12)
    for i, j in zip(ii, jj):
        syst[sites[int(i)], sites[int(j)]] = complex(H[i, j])
    return syst


# --------------------------------------------------------------------------- #
# Self-test / CLI
# --------------------------------------------------------------------------- #
def selftest(verbose=True):
    """Run the built-in checks; returns the number of failures."""
    from pythtb import Mesh, WFArray
    from pythtb.models import graphene, kane_mele, ssh

    fails = 0

    def rep(label, ok, detail=""):
        nonlocal fails
        fails += 0 if ok else 1
        if verbose:
            print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))

    m = ssh(v=0.5, w=1.0)
    mesh = Mesh(["k"])
    mesh.build_grid([101], k_endpoints=True)
    w = WFArray(m.lattice, mesh)
    w.solve_model(m)
    phi_bp = float(np.squeeze(w.berry_phase(axis_idx=0, state_idx=[0])))
    phi_wl = float(wilson_phases(w, 0, [0]).ravel()[0])
    rep("wilson_phases agrees with berry_phase (SSH, topological)",
        np.isclose(np.exp(1j * phi_wl), np.exp(1j * phi_bp), atol=1e-8),
        f"{phi_wl:+.6f} vs {phi_bp:+.6f}")

    z_topo = z2_wcc_flow(kane_mele(delta=0.5, t=1.0, soc=0.2, rashba=0.05))
    z_triv = z2_wcc_flow(kane_mele(delta=2.5, t=1.0, soc=0.1, rashba=0.05))
    rep("z2_wcc_flow: Kane–Mele topological (Δ < 3√3 λ) gives 1", z_topo == 1, str(z_topo))
    rep("z2_wcc_flow: Kane–Mele trivial (Δ > 3√3 λ) gives 0", z_triv == 0, str(z_triv))

    g = graphene(delta=0.0, t=-1.0)
    small = remove_orb_copy(g, 0)
    rep("remove_orb_copy leaves the original untouched", g.norb == 2 and small.norb == 1)

    try:
        importlib.import_module("kwant")
        flake = graphene(delta=0.1, t=-1.0).make_finite(periodic_dirs=[0, 1], num_cells=[4, 4])
        ev_k = np.sort(np.linalg.eigvalsh(to_kwant(flake).finalized().hamiltonian_submatrix()))
        rep("to_kwant reproduces the PythTB spectrum", np.allclose(ev_k, np.sort(flake.solve_ham()), atol=1e-10))
    except ImportError:
        if verbose:
            print("[SKIP] to_kwant (kwant not installed)")
    return fails


def build_parser():
    ap = argparse.ArgumentParser(prog="pythtb_tools", description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true", help="run the built-in checks and exit")
    ap.add_argument("--version", action="version", version=f"pythtb-skill {__version__}")
    ap.add_argument("-q", "--quiet", action="store_true", help="only the final verdict")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.selftest:
        n = selftest(verbose=not args.quiet)
        print("selftest OK" if n == 0 else f"selftest: {n} FAILED")
        return 0 if n == 0 else 1
    build_parser().print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
