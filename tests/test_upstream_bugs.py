# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Pin the two pythtb 2.0.2 behaviours the notebooks work around.

Each test asserts the *workaround* is valid, and a companion test asserts that
the upstream bug is still present (marked xfail(strict=True)): when a pythtb
release fixes it, that test will XPASS, the suite will fail loudly, and the
notebook's "NB upstream bug" notes (§7, §9) can be retired.

See docs/02-findings-backlog.md P1, P2.
"""

import warnings

import numpy as np
import pytest

pythtb = pytest.importorskip("pythtb")
from pythtb import Mesh, WFArray  # noqa: E402
from pythtb.models import ssh  # noqa: E402


@pytest.fixture
def ssh_wfa():
    m = ssh(v=0.5, w=1.0)
    mesh = Mesh(["k"])
    mesh.build_grid([101], k_endpoints=True)
    w = WFArray(m.lattice, mesh)
    w.solve_model(m)
    return w


# --- P1: wilson_loop(wilson_evals=True) --------------------------------------

def test_wilson_unitary_reproduces_berry_phase(ssh_wfa):
    """Workaround: diagonalise the returned unitary yourself."""
    phi_bp = float(np.squeeze(ssh_wfa.berry_phase(axis_idx=0, state_idx=[0])))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", np.exceptions.ComplexWarning)
        U, _ = ssh_wfa.wilson_loop(axis_idx=0, state_idx=[0], wilson_evals=True)
    lam = np.linalg.eigvals(np.atleast_2d(np.squeeze(U)))
    phi_wl = float(-np.angle(lam[0]))
    assert np.isclose(np.exp(1j * phi_wl), np.exp(1j * phi_bp), atol=1e-8)


@pytest.mark.xfail(strict=True, reason="pythtb 2.0.2 wfarray.py: evals array is dtype=float, "
                                        "so wilson_evals returns cos(phi) instead of phi")
def test_wilson_evals_are_the_phases(ssh_wfa):
    phi_bp = float(np.squeeze(ssh_wfa.berry_phase(axis_idx=0, state_idx=[0])))
    with warnings.catch_warnings():
        warnings.simplefilter("error", np.exceptions.ComplexWarning)  # bug -> raises here
        _, ev = ssh_wfa.wilson_loop(axis_idx=0, state_idx=[0], wilson_evals=True)
    ev = np.asarray(ev).ravel()
    assert np.iscomplexobj(ev) or np.isclose(np.exp(1j * float(ev[0])), np.exp(1j * phi_bp), atol=1e-6)


# --- P2: remove_orb mutates in place ------------------------------------------

def test_remove_orb_workaround_copy_first():
    from pythtb.models import graphene
    g = graphene(delta=0.0, t=-1.0)
    small = g.copy()
    small.remove_orb(0)
    assert g.norb == 2 and small.norb == 1


@pytest.mark.xfail(strict=True, reason="docstring says a reduced model is *returned*; "
                                        "pythtb 2.0.2 mutates in place and returns None")
def test_remove_orb_returns_a_model():
    from pythtb.models import graphene
    g = graphene(delta=0.0, t=-1.0)
    small = g.remove_orb(0)
    assert small is not None and small.norb == 1 and g.norb == 2
