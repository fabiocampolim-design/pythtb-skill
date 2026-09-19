# Topological invariants with PythTB 2.0 — recipes and conventions

Each recipe was executed in the chapter notebooks under `chapters/` (section in
brackets; §14–20 are chapters 4–6) with an inline check; parameter values quoted are the ones that pass.

## Grids and endpoints

`Mesh(["k", ...]).build_grid(shape, k_endpoints=[True, ...])` includes k = 1
(reduced units). `WFArray.solve_model(model)` fills the eigenvectors. Despite
appearances, `k_endpoints` does **not** change Berry phases or Chern numbers —
`wilson_loop`/`berry_phase` close the loop with the PBC phase factor
themselves (`wfarray.py`), and `k_endpoints=True` vs `False` gives the
identical SSH Zak phase and Haldane Chern number to machine precision. Offset
a parameter grid by half a step only to dodge a specific gap-closing k-point
(see below) — not as a general rule for invariants.
`model.chern_number(...)`/`model.axion_angle(...)` **divide by the gap and go
silent on it**: on a genuinely gapless model a coarse grid can raise
`ZeroDivisionError`, but a slightly finer grid can instead return a small,
wrong, non-zero number with no warning at all — check the gap over the same
grid before trusting either result, don't just "offset and rerun".

A parametrized `Mesh` axis (Rice–Mele pump [§10], exercise I.5) must be named
**exactly** after the model's own parameter: `Mesh(["k","l"],
axis_names=["k","lmbda"])` works when the model's onsite/hop is a callable of
`lmbda`; the default axis name (`l_0`) or any other spelling fails with
`ValueError: Unknown parameter name(s): l_0`. This is unrelated to
`k_endpoints` above and to `axion_angle`'s own `param_periods=` argument.

## Berry / Zak phase and polarization [§9, §10]

```python
phi = wfa.berry_phase(axis_idx=0, state_idx=[0])             # per transverse k
P   = phi / (2*np.pi)  (mod 1)  ×  e / a                      # polarization, Convention I
```
SSH (orbitals at 0, ½ — Convention I): phase is **∓π/2** (v ≶ w), i.e. Wannier
centre at ¼ or ¾, not 0 or π — the polarization difference between the two
phases is the physical ½ (e) that matters. BN polarization jump is **e/3**;
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
for this convention (orbitals at 0, ½) the pair centroid sits near ¼, but that
number is a Convention-I artefact of the orbital positions, not the
quantized invariant. The invariant is the nested-loop polarization **jump of
½ between the topological and trivial models** for the same Wannier sector
(run the same `nested_polarization` on both, subtract) — not the ¼ value
alone, and not a difference between two sectors within one model.

## Slices and Weyl nodes [§19]

Treat k_z as a symbolic parameter and compute the 2D Chern number per slice
(`model.chern_number(..., kz=value)`); the jump between slices counts the
monopole charge. Mass term must be `2 + cos k₀ − cos kx − cos ky − cos kz` so
slices invert *between* the nodes. Fermi arcs: surface spectral weight of a
slab (`cut_piece` along one direction).

## Axion angle and second Chern number [§20]

```python
beta, theta, c2 = model.axion_angle(nks=(24,24,24), param_periods=..., return_second_chern=True, beta=...)
```
`axion_angle` is a **`TBModel`** method (not `WFArray`) — it sweeps the model's
own parameters internally. Fu–Kane–Mele with C₂: θ = π at the TRS point, C₂ = 1
over the (k, β) cycle.

## Real-space marker [§14]

`local_chern_marker` on a crystalline `make_finite` flake gives the interior
plateau C = ±1. On arbitrary point clouds compute Bianco–Resta by hand:
`C(r) = −(4π/A) Im[P X P Y P]_rr` with `P = V_occ V_occ†` from
`solve_ham(return_eigvecs=True)` (eigenvectors are rows).

## BdG "hack" [§18, exercise II.5]

Superconductivity = extra orbitals for holes; PythTB cannot validate
particle-hole symmetry, so check `H = −τ_x H* τ_x` yourself before trusting a
Majorana. Kitaev: Berry phase of the lower BdG band jumps by π at μ = 2t.
