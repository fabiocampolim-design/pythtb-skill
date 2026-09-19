# PythTB API map: v1.x → 2.0, and the 2.0.2 traps

Verified against pythtb 2.0.2 (PyPI, 2026-05-26) while executing the notebooks
in this repository. `pythtb.__version__` reports `2.0.0` for the 2.0.2 wheel —
use `importlib.metadata.version("pythtb")`.

## Object model

| v1.x (Vanderbilt's book, most published examples) | 2.0 | Notes |
|---|---|---|
| `tb_model(dim_k, dim_r, lat, orb, per=...)` | `Lattice(lat_vecs, orb_vecs, periodic_dirs)` then `TBModel(lattice)` | geometry and Hamiltonian are separate objects |
| `set_onsite(en, ind_i)` | same; callable onsites **need `ind_i`** | |
| `set_hop(t, i, j, R)` | same; 2.0.2 docstring convention is `H_ij` (was `t_ij`) | `mode="set"` / `"add"` |
| `solve_all(k_list, eig_vectors=True)` | `solve_ham(k, return_eigvecs=True)` | k shape `(nk, dim_k)`; **a single k squeezes the k axis** — wrap in `np.atleast_2d`; named parameters broadcast as `(nk, *param_shapes, nband)` (pass values as kwargs, not `param=`/`params=`) |
| `solve_one(k)` | `solve_ham(np.array([k]))` | **the `solve_all`/`solve_one` shims themselves are dead code in 2.0.2** — see trap 11 |
| `cut_piece(num, fin_dir, glue_edgs)` | `cut_piece(num_cells, periodic_dir, glue_edges=False)` | |
| `make_supercell(sc_red_lat)` | `make_supercell(...)` | |
| `remove_orb(to_remove)` → new model | **mutates in place, returns `None`** (docstring still shows `small = big.remove_orb([...])`) | use `copy()` first (`scripts/pythtb_tools.remove_orb_copy`) |
| `k_path(...)` | `k_path(nodes, nk, report=False)` → `(k_vec, k_dist, k_node)` | |
| `get_lat()`, `get_orb()`, `get_num_orbitals()` | properties `lat_vecs`, `orb_vecs`, `norb`, `recip_lat_vecs`, `parameters`, `nhops` | **not** methods |
| `w90(path, prefix)` | `W90(path, prefix)`; `.model(min_hopping_norm=...)`, `.w90_bands_consistency()` | 2.0.2 removed `fill_hermitian` (double-counted hoppings) |
| `wf_array(model, dims)` + `solve_on_grid` | `Mesh([...]).build_grid(shape, k_endpoints=...)` then `WFArray(lattice, mesh).solve_model(model)` | spinful models: `WFArray(..., spinful=True)`; flattened orbital order is orbital-major (`np.repeat(x, 2)`) |
| `berry_phase(occ, dir, contin, berry_evals)` | `berry_phase(axis_idx, state_idx, berry_evals=False, contin=True)` | `berry_evals=True` returns an ndarray `(n_transverse, n_states)` |
| `berry_flux(occ, dirs)` | `berry_flux(...)`, `berry_curvature(...)` | |
| — | `chern_number(state_idx, plane)` on `WFArray` **and** `TBModel.chern_number(plane, nks, occ_idxs, **params)` (autodiff of H(k)) | divides by the gap: raises `ZeroDivisionError` on some grids, returns a small wrong number silently on others — check the gap first |
| — | `wilson_loop(axis_idx, state_idx, wilson_evals=False)` | `wilson_evals=True` returns **cos φ** (float-cast bug); diagonalise the unitary (`pythtb_tools.wilson_phases`) |
| — | `axion_angle(nks, param_periods, return_second_chern=False, **params)` | needs a swept parameter with a period; 24³ mesh, `diff_order=6` ≈ 10 s, C₂ within 1 % |
| — | `local_chern_marker(...)`, `position_expectation`, `position_hwf`, `quantum_metric` | marker assumes crystalline `make_finite` models |
| — | `Wannier(wfa)`: `project`, `disentangle`, `maxloc`; `.wannier` has shape `(n_cells, n_wf, n_orb)` | `plot_decay` assumes ≥ 2D (crashes on chains) |
| — | `pythtb.models`: `ssh(v, w)`, `graphene(delta, t)`, `haldane(delta, t1, t2, phi)`, `kane_mele(delta, t, soc, rashba)`, `bhz(...)`, `checkerboard`, `fu_kane_mele(t, soc, dt)` | model library new in 2.0 |
| — | `TBModel.hamiltonian(k=None)` dense H; `velocity(...)`; symbolic/callable parameters, `use_tensorflow` batching | |

## Traps confirmed by execution (all pinned by tests or notebook checks)

1. `solve_ham` named-parameter broadcast order `(nk, *param_shapes, nband)`;
   single k squeezed; a `params={...}` dict kwarg raises (params go by name).
2. `remove_orb` in place / returns None (upstream docs bug, draft issue P2).
3. `wilson_loop(wilson_evals=True)` float array swallows complex eigenvalues →
   `ComplexWarning` + cos φ (draft issue P1).
4. `chern_number` / `axion_angle` divide by the gap: a genuinely gapless model
   can raise `ZeroDivisionError` on one grid and return a small, wrong,
   unwarned non-zero number on a slightly different grid — check the gap on
   the same grid, don't just "offset and rerun".
5. Spinful `WFArray` must be told `spinful=True`; orbital vectors are per orbital,
   spin doubles the flattened index. (This one at least raises loudly —
   `ValueError: Spinful setting of WFArray does not match the model.`)
6. `local_chern_marker` returns ~0 nonsense for single-cell point-cloud models
   (huge lattice vectors); the Bianco–Resta marker is five lines by hand.
7. `Wannier.plot_decay` crashes on 1D (`ssh(...)`: `ValueError: not enough
   values to unpack (expected 2, got 1)`); plot from `.wannier` yourself.
8. Convention I: orbital positions enter the Bloch phases, so hand-built
   Wilson loops need the boundary factor `u_n(k+G)_τ = e^{-2πi G·τ} u_n(k)_τ`.
9. numpy ≥ 2.5 removed 2-D `np.cross`; write the z-component by hand.
10. Windows: console is cp1252 → `PYTHONIOENCODING=utf-8`; `conda run -n env
    python -c "<multi-line>"` fails — call the env's `python.exe`.
11. `TBModel.solve_all`/`solve_one` are **dead code** in 2.0.2: they forward a
    `k_list=` keyword into `solve_ham`, whose real parameter is `k_pts` — so
    `k_list` lands in `**params` and every call raises
    `ValueError: Unknown parameter name(s): k_list`, with or without
    arguments, after the `FutureWarning`. Use `solve_ham` directly; this is an
    unreported upstream bug (new draft candidate P4).
12. A parametrized `Mesh` axis (e.g. the Rice–Mele pump, §10 and exercise I.5)
    must be named exactly after the model's own parameter:
    `Mesh(["k","l"], axis_names=["k","lmbda"])` works, the default axis name
    (`l_0`) or any other spelling raises `ValueError: Unknown parameter
    name(s): l_0`.
13. Spinful `hamiltonian()` is **not flattened** by default — shape
    `(norb,2,norb,2)` (finite) or `(nk,norb,2,norb,2)` (k-dependent) — while
    `solve_ham`'s eigenvectors default to the flattened `(nk,nstate,2·norb)`
    layout (`flatten_spin_axis=True`). Code that exports `hamiltonian()`
    for a spinful model (e.g. to `scipy.sparse` or Kwant) must reshape first;
    `scripts/pythtb_tools.to_kwant` now guards this explicitly.

## Where each is exercised

Main chapters §2 (object model), §7 (`remove_orb`), §8 (spin), §9 (Berry,
Wilson), §10 (parametrized `Mesh` axis naming), §12–13 (W90, Wannier), §14
(three Chern routes, marker), §20 (axion); `scripts/pythtb_tools.py
--selftest`; `tests/test_upstream_bugs.py`. Traps 11 and 13 (dead
`solve_all`/`solve_one`, spinful `hamiltonian()` layout) are documented here
from direct interpreter probing, not from a dedicated notebook check.
