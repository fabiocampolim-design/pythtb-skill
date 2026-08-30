# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Exercise IV.1, completed: the PythTB -> Kwant exporter gives identical spectra.

Needs an interpreter that can import BOTH pythtb and kwant; skips otherwise.
(On the maintainer's machine kwant lives in the miniconda base env and pythtb
in the `pythtb` env; run with
``PYTHONPATH=<dir containing a copy of the pythtb package> python -m pytest tests/test_kwant_crosscheck.py``
from the base env — result recorded in docs/02-findings-backlog.md N3.)

History: the first exporter (2026-08-22) built one square lattice and called
``lat(*position)``; Kwant reads those as integer lattice indices, orbitals
collapsed onto shared sites and Kwant raised "A hopping connects the following
site to itself". First run of this test (2026-08-28) caught it; the exporter
now gives each orbital its own sublattice.
"""

import numpy as np
import pytest

pythtb = pytest.importorskip("pythtb")
kwant = pytest.importorskip("kwant")
from pythtb.models import graphene, haldane  # noqa: E402


def to_kwant(model):
    """Translate a finite PythTB TBModel into a kwant.Builder (spinless). Same code as IV.1."""
    pos = model.orb_vecs @ model.lat_vecs
    dim = pos.shape[1]
    lat_k = kwant.lattice.general(np.eye(dim), basis=pos, norbs=1)
    syst = kwant.Builder()
    origin = (0,) * dim
    sites = [sub(*origin) for sub in lat_k.sublattices]
    H = model.hamiltonian()
    for i, s in enumerate(sites):
        syst[s] = float(np.real(H[i, i]))
    ii, jj = np.nonzero(np.triu(np.abs(H), 1) > 1e-12)
    for i, j in zip(ii, jj):
        syst[sites[int(i)], sites[int(j)]] = complex(H[i, j])
    return syst


@pytest.mark.parametrize("delta,t2", [(0.2, 0.15), (0.0, 0.1 * np.exp(1j * 0.7))])
def test_haldane_flake_spectra_agree(delta, t2):
    flake = haldane(delta=delta, t1=-1.0, t2=t2).make_finite(periodic_dirs=[0, 1],
                                                              num_cells=[6, 6])
    syst = to_kwant(flake).finalized()
    ev_k = np.sort(np.linalg.eigvalsh(syst.hamiltonian_submatrix()))
    ev_p = np.sort(flake.solve_ham())
    assert ev_k.shape == ev_p.shape
    assert np.allclose(ev_k, ev_p, atol=1e-10)


def test_positions_survive_export():
    flake = graphene(delta=0.0, t=-1.0).make_finite(periodic_dirs=[0, 1], num_cells=[3, 3])
    syst = to_kwant(flake).finalized()
    pos_k = np.array([s.pos for s in syst.sites])
    pos_p = flake.orb_vecs @ flake.lat_vecs
    # same set of positions, possibly reordered
    assert np.allclose(np.sort(pos_k, axis=0), np.sort(pos_p, axis=0), atol=1e-12)
