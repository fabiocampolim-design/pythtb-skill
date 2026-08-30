# Topological invariants with PythTB 2.0 — recipes and conventions

Each recipe was executed in `PythTB_Theory_and_Practice.ipynb` (section in
brackets) with an inline check; parameter values quoted are the ones that pass.

## Grids and endpoints

`Mesh(["k", ...]).build_grid(shape, k_endpoints=[True, ...])` includes k = 1
(reduced units): needed for Berry phases around a full loop and for Chern
numbers via Berry fluxes. `WFArray.solve_model(model)` fills the eigenvectors.
Offset a parameter grid by half a step whenever a scan crosses a gap closing
(`chern_number`, `axion_angle` divide by the gap).

## Berry / Zak phase and polarization [§9, §10]

```python
phi = wfa.berry_phase(axis_idx=0, state_idx=[0])             # per transverse k
P   = phi / (2*np.pi)  (mod 1)  ×  e / a                      # polarization, Convention I
```
SSH: 0 or π (Wannier centre on the strong bond); BN polarization jump is **e/3**;
Rice–Mele pump: track `phi` continuously over the cycle (`contin=True`), the
winding is the pumped charge. Flatness of a Zak-phase *scan*: use circular
statistics `|⟨e^{iφ}⟩|`, not `np.std`.

## Chern number, three ways [§14]

1. `wfa.chern_number(state_idx=[0], plane=(0, 1))` — plaquette Berry fluxes.
2. `model.chern_number(plane=(0,1), nks=(31,31), occ_idxs=[0])` — autodiff H(k).
3. `∫ wfa.berry_curvature(...)` over the BZ / 2π.
Haldane at `t2 = 0.15 e^{iπ/2}`: C = −1 for the lower band. Valley gaps are
`2|Δ ∓ 3√3 t₂ sin φ|`. Joint invariants of touching bands: pass both indices.

## Z₂ from Wannier-centre flow [§15, §16]

```python
wcc = wfa.berry_phase(axis_idx=0, state_idx=[0, 1], berry_evals=True, contin=False) / (2π) % 1
z2  = pythtb_tools.z2_from_wcc(wcc[k1 <= 0.5], ref=0.31)     # parity of crossings
```
Track the two centres by the smaller total arc (keep vs swap) so that
crossings through the periodic boundary are counted correctly. Kane–Mele:
Z₂ = 1 for Δ < 3√3 λ_SO; BHZ: an orbital-antisymmetric exchange `[M_z, −M_z]`
drives QSH → |C| = 1 → trivial (window 0 → 1 → 0 over M_z ∈ [0, 9]).

## Wilson loops and nested Wilson loops [§9, §17]

Diagonalise the returned unitary yourself (`pythtb_tools.wilson_phases`);
φ = −arg λ matches `berry_phase`. BBH quadrupole: the Wannier *bands* disperse —
only the pair centroid is pinned at ¼ (mod ½); the nested Wilson loop's
invariant is the ½ difference between the two nested phases (there is a
geometric offset), not either phase alone.

## Slices and Weyl nodes [§19]

Treat k_z as a symbolic parameter and compute the 2D Chern number per slice
(`model.chern_number(..., kz=value)`); the jump between slices counts the
monopole charge. Mass term must be `2 + cos k₀ − cos kx − cos ky − cos kz` so
slices invert *between* the nodes. Fermi arcs: surface spectral weight of a
slab (`cut_piece` along one direction).

## Axion angle and second Chern number [§20]

```python
beta, theta, c2 = wfa.axion_angle(nks=(24,24,24), param_periods=..., return_second_chern=True, beta=...)
```
Fu–Kane–Mele with C₂: θ = π at the TRS point, C₂ = 1 over the (k, β) cycle.

## Real-space marker [§14]

`local_chern_marker` on a crystalline `make_finite` flake gives the interior
plateau C = ±1. On arbitrary point clouds compute Bianco–Resta by hand:
`C(r) = −(4π/A) Im[P X P Y P]_rr` with `P = V_occ V_occ†` from
`solve_ham(return_eigvecs=True)` (eigenvectors are rows).

## BdG "hack" [§18, exercise II.5]

Superconductivity = extra orbitals for holes; PythTB cannot validate
particle-hole symmetry, so check `H = −τ_x H* τ_x` yourself before trusting a
Majorana. Kitaev: Berry phase of the lower BdG band jumps by π at μ = 2t.
