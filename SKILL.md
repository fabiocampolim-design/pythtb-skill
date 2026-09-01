---
name: pythtb
description: Build and analyse tight-binding models with PythTB 2.0 — band structures, finite systems, Berry phases, Wannier centres, Chern and Z₂ invariants, Wilson loops, axion angle, Wannier90 import — and know precisely where PythTB stops (no transport, no sparse solvers) and how to hand a model to Kwant. Use this skill whenever the user mentions PythTB, tight-binding models, Berry phase / polarization / Chern number / Z₂ / Wilson loop / Wannier functions, SSH / graphene / Haldane / Kane–Mele / BHZ / BBH / Kitaev / Weyl / Fu–Kane–Mele models, or Wannier90 `_hr.dat` files — even without naming PythTB.
license: Apache-2.0
---

# PythTB 2.0

[PythTB](https://github.com/pythtb/pythtb) (Coh, Vanderbilt, Cole; GPL-3.0) is
the pure-Python tight-binding package behind Vanderbilt's *Berry Phases in
Electronic Structure Theory*. Version 2.0 (Nov 2025) rewrote the API:
`Lattice` → `TBModel` → `Mesh` + `WFArray` (Berry machinery), plus `Wannier`
and `W90`. Everything below was executed and checked in this repository's
notebooks against **pythtb 2.0.2**; the notebooks are the worked examples.

Pick the workflow that matches the task; each points to a reference file.

## 1. Build and solve a model

```python
from pythtb import Lattice, TBModel
lat = Lattice(lat_vecs=[[1.0]], orb_vecs=[[0.0], [0.5]], periodic_dirs=[0])  # SSH
m = TBModel(lat)
m.set_hop(v, 0, 1, [0]); m.set_hop(w, 1, 0, [1])        # H_ij convention (2.0.2 docstring)
k = np.array([[x] for x in np.linspace(0, 1, 101)])      # reduced coordinates, shape (nk, dim_k)
E = m.solve_ham(k)                                       # (nk, nband); single k is SQUEEZED
```

Ready-made models: `pythtb.models` (`ssh, graphene, haldane, kane_mele, bhz,
checkerboard, fu_kane_mele, ...`). Finite pieces: `cut_piece`, `make_finite`,
`make_supercell`; spin: `Lattice(..., spinful=True)`-style models need
`WFArray(..., spinful=True)`. Ground rules that save debugging time:

- `recip_lat_vecs`, `lat_vecs`, `orb_vecs`, `norb`, `parameters` are
  **properties**, not methods.
- `solve_ham(k, param=...)` broadcasts as `(nk, n_param, nband)` — k axis first.
- `remove_orb` **mutates in place and returns None** (docstring says otherwise):
  use `scripts/pythtb_tools.remove_orb_copy`.
- Callable onsites need `ind_i`; `np.cross` on 2-vectors is gone in numpy ≥ 2.5.
- Full v1.x → 2.0 correspondence and every trap: `references/api-map.md`.

## 2. Topological invariants (the core mission)

```python
from pythtb import Mesh, WFArray
mesh = Mesh(["k", "k"]); mesh.build_grid((31, 31), k_endpoints=[True, True])
wfa = WFArray(m.lattice, mesh); wfa.solve_model(m)
phi = wfa.berry_phase(axis_idx=0, state_idx=[0])            # Zak / Berry phase per k_perp
C   = wfa.chern_number(state_idx=[0], plane=(0, 1))          # also TBModel.chern_number
```

- **Z₂** (Kane–Mele, BHZ): Wannier-centre flow over half the BZ, parity of
  reference-line crossings — `scripts/pythtb_tools.z2_wcc_flow(model)`.
- **Wilson-loop phases**: `wilson_loop(wilson_evals=True)` returns cos φ in
  2.0.2 (float-cast bug) — use `pythtb_tools.wilson_phases(wfa, axis, states)`.
- **Axion angle / second Chern**: `wfa.axion_angle(nks, param_periods, return_second_chern=True)`
  with a swept parameter; ~10 s at 24³.
- `chern_number` / `axion_angle` raise `ZeroDivisionError` *exactly at* a gap
  closing — offset the grid by half a step. Convention I phases (orbital
  positions enter the Bloch phases): the boundary factor for manual loops is
  `u(k+G)_τ = e^{-2πi G·τ} u(k)_τ`. Recipes and conventions: `references/invariants.md`.

## 3. Finite systems and real space

`cut_piece(n, dir, glue_edges=False)` (ribbon), `make_finite(...)` (flake),
`solve_ham(return_eigvecs=True)` (eigenvectors are rows: `vec[n]`),
`position_expectation`, `position_hwf`, `local_chern_marker` (crystalline
`make_finite` models). Everything is **dense**: ~10³–10⁴ orbitals is the wall
(`eigh` is O(N³)); above that export `hamiltonian()` to scipy.sparse or KPM.

## 4. Real materials: Wannier90 import

```python
from pythtb import W90
w = W90("data/w90_silicon", "si")            # reads si_hr.dat, si_centres.xyz, si.win
m = w.model(min_hopping_norm=0.01)           # TBModel with 8 Wannier orbitals
```

Compare with `si_band.dat` to validate the cut-off. In-package Wannierization:
`Wannier(wfa).project(...)`, `.maxloc(...)`; `plot_decay` assumes ≥ 2D.

## 5. Know when to stop — hand-off to Kwant

PythTB has **no leads, no S-matrix, no conductance, no sparse solvers, no
continuum discretizer, no symmetry validation, no interactions**. When the
task is transport or > 10⁴ sites, export: `pythtb_tools.to_kwant(finite_model)`
gives a `kwant.Builder` with identical spectrum (one sublattice per orbital —
never `lat(*position)`). The full capability matrix and the failing-code
demonstrations: `references/limitations.md` and Part IV of the book (`chapters/PythTB_08_What_PythTB_Cannot_Do.ipynb`).

## Verifying your environment

`python scripts/verify_pythtb.py` (5 checks) and
`python scripts/pythtb_tools.py --selftest`. Pin **pythtb==2.0.2**
(`requirements.txt`): the traps above are version-specific and pinned by
strict-xfail tests in `tests/test_upstream_bugs.py`.

## Etiquette

PythTB is GPL-3.0 and is installed by the user from PyPI; this skill contains
none of its code. When something disagrees with reality, trust in this order:
the executed notebook output > PythTB's own docs/tutorials > this skill's
summaries — and consider an upstream issue (drafts of three known ones are
kept in the study folder next to this skill).
