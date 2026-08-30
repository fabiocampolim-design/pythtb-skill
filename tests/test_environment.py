# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Environment checks — the same five checks as verify_pythtb.py, as pytest cases.

They skip cleanly when pythtb is not importable (rule 5: absent dependency
means skip, never fail).
"""

import os

import numpy as np
import pytest

pythtb = pytest.importorskip("pythtb")
from pythtb import Lattice, Mesh, TBModel, WFArray  # noqa: E402
from pythtb.models import haldane  # noqa: E402


def _ssh(t_intra, t_inter):
    lat = Lattice(lat_vecs=[[1.0]], orb_vecs=[[0.0], [0.5]], periodic_dirs=[0])
    m = TBModel(lat)
    m.set_hop(t_intra, 0, 1, [0])
    m.set_hop(t_inter, 1, 0, [1])
    return m


def test_pythtb_version_is_the_pinned_one():
    # requirements.txt pins 2.0.2; the package reports 2.0.0 in __version__ (upstream quirk),
    # so check the installed distribution instead.
    from importlib.metadata import version
    assert version("pythtb").startswith("2.0"), version("pythtb")


def test_ssh_gap():
    m = _ssh(1.0, 0.5)
    k = np.array([[x] for x in np.linspace(0.0, 1.0, 51)])
    ev = m.solve_ham(k)
    gap = ev[:, 1].min() - ev[:, 0].max()
    assert np.isclose(gap, 1.0, atol=1e-10)


def _zak(m):
    mesh = Mesh(["k"])
    mesh.build_grid([61], k_endpoints=True)
    w = WFArray(m.lattice, mesh)
    w.solve_model(m)
    return float(np.squeeze(w.berry_phase(axis_idx=0, state_idx=[0])))


def test_ssh_zak_phases_differ_by_pi():
    d = (_zak(_ssh(1.0, 0.5)) - _zak(_ssh(0.5, 1.0))) % (2 * np.pi)
    assert np.isclose(d, np.pi, atol=1e-6)


def test_haldane_chern_number():
    h = haldane(delta=0.0, t1=-1.0, t2=0.15 * np.exp(1j * np.pi / 2))
    mesh = Mesh(["k", "k"])
    mesh.build_grid(shape=(31, 31), k_endpoints=[True, True])
    w = WFArray(h.lattice, mesh)
    w.solve_model(h)
    c = float(w.chern_number(state_idx=[0], plane=(0, 1)))
    assert np.isclose(abs(c), 1.0, atol=1e-6)


def test_w90_silicon_dataset_present_and_loads(repo_root):
    d = os.path.join(repo_root, "data", "w90_silicon")
    for f in ["si.win", "si_hr.dat", "si_band.dat", "si_band.kpt", "si_centres.xyz"]:
        assert os.path.exists(os.path.join(d, f)), f
    from pythtb import W90
    si = W90(d, "si")
    m = si.model(min_hopping_norm=0.01)
    assert m.norb == 8
