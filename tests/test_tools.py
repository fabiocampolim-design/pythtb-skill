# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""scripts/pythtb_tools.py — every helper against the physics it was extracted from."""

import os
import subprocess
import sys

import numpy as np
import pytest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "scripts"))
pythtb = pytest.importorskip("pythtb")
import pythtb_tools as T  # noqa: E402
from pythtb import Mesh, WFArray  # noqa: E402
from pythtb.models import graphene, kane_mele, ssh  # noqa: E402


def test_version_matches_version_file():
    with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as f:
        assert T.__version__ == f.read().strip()


def _ssh_phases(v, w):
    m = ssh(v=v, w=w)
    mesh = Mesh(["k"])
    mesh.build_grid([101], k_endpoints=True)
    wfa = WFArray(m.lattice, mesh)
    wfa.solve_model(m)
    phi_bp = float(np.squeeze(wfa.berry_phase(axis_idx=0, state_idx=[0])))
    phi_wl = float(T.wilson_phases(wfa, 0, [0]).ravel()[0])
    return phi_bp, phi_wl


@pytest.mark.parametrize("v,w", [(0.5, 1.0), (1.0, 0.5)])
def test_wilson_phases_equal_berry_phase(v, w):
    phi_bp, phi_wl = _ssh_phases(v, w)
    assert np.isclose(np.exp(1j * phi_wl), np.exp(1j * phi_bp), atol=1e-8)


def test_wilson_phases_distinguish_ssh_dimerisations():
    # models.ssh puts the orbitals at positions where the Zak phases are ±π/2 (Convention I);
    # what is gauge-invariant is that the two dimerisations differ by exactly π.
    _, topo = _ssh_phases(0.5, 1.0)
    _, triv = _ssh_phases(1.0, 0.5)
    assert np.isclose(np.exp(1j * (topo - triv)), -1.0, atol=1e-6)


def test_z2_from_wcc_counts_boundary_crossings():
    # two centres moving in opposite directions through the periodic boundary: 1 crossing each
    k = np.linspace(0, 1, 11)
    wcc = np.stack([0.9 + 0.3 * k, 0.1 - 0.3 * k], axis=1) % 1.0
    assert T.z2_from_wcc(wcc, ref=0.0) == 0          # both cross ref=0 → even
    assert T.z2_from_wcc(wcc, ref=0.15) == 1         # only the descending one crosses 0.15
    with pytest.raises(ValueError):
        T.z2_from_wcc(np.zeros((5, 3)), 0.3)


@pytest.mark.parametrize("delta,soc,expect", [(0.5, 0.2, 1), (2.5, 0.1, 0)])
def test_z2_wcc_flow_kane_mele(delta, soc, expect):
    assert T.z2_wcc_flow(kane_mele(delta=delta, t=1.0, soc=soc, rashba=0.05)) == expect


def test_remove_orb_copy():
    g = graphene(delta=0.0, t=-1.0)
    s = T.remove_orb_copy(g, 0)
    assert g.norb == 2 and s.norb == 1


def test_to_kwant_needs_kwant_or_matches():
    pytest.importorskip("kwant")
    flake = graphene(delta=0.1, t=-1.0).make_finite(periodic_dirs=[0, 1], num_cells=[4, 4])
    ev = np.sort(np.linalg.eigvalsh(T.to_kwant(flake).finalized().hamiltonian_submatrix()))
    assert np.allclose(ev, np.sort(flake.solve_ham()), atol=1e-10)


def test_audit_log_writes_one_json_record(tmp_path):
    import json
    path = T.audit_log(str(tmp_path), ["--weekly", "-q"], {"n": 1}, script="probe")
    assert os.path.dirname(path) == str(tmp_path / "logs") and os.path.basename(path).startswith("probe-")
    with open(path, encoding="utf-8") as f:
        rec = json.load(f)
    assert rec["script"] == "probe" and rec["version"] == T.__version__
    assert rec["argv"] == ["--weekly", "-q"] and rec["extra"] == {"n": 1} and rec["utc"].endswith("Z")


def test_cli_selftest_and_version():
    script = os.path.join(ROOT, "scripts", "pythtb_tools.py")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    out = subprocess.run([sys.executable, script, "--version"], capture_output=True, text=True, env=env)
    assert out.returncode == 0 and "pythtb-skill" in out.stdout
    out = subprocess.run([sys.executable, script, "--selftest", "-q"], capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stdout + out.stderr
