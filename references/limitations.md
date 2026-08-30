# What PythTB cannot do — and what to use instead

Each row is *demonstrated* with failing or hand-written code in Part IV of
`PythTB_Theory_and_Practice.ipynb` (§25–§30). Kwant column: version 1.5.0.

| Capability | PythTB 2.0.2 | Kwant 1.5 |
|---|---|---|
| Leads, scattering matrix, conductance | ✗ nothing represents an open boundary (§25) | ✓ core mission |
| Sparse solvers / large systems | ✗ dense `eigh` only, ~10³–10⁴ orbitals (§24, §26) | ✓ MUMPS, ~10⁶ sites |
| KPM / spectral methods | ✗ (30 lines by hand, exercise IV.2) | ✓ `kwant.kpm` |
| Continuum → lattice discretizer | ✗ manual (§16, §27) | ✓ `kwant.continuum`, symbolic |
| Symmetry declaration / validation | ✗ Hermiticity only (§28) | ✓ PHS/TRS/conservation, Qsymm |
| Local operators (current, density) | partial (`position_expectation`, `velocity`) | ✓ `kwant.operator` |
| Interactions / self-consistency | ✗ write the loop (§29: mean-field Hubbard, BCS) | ✗ likewise |
| **Berry phase / Wilson loops** | ✓ core mission (`WFArray`) | ✗ roll your own |
| Chern number, one call | ✓ three routes (§14) | ✗ |
| Z₂ via Wannier-centre flow | ✓ (§15, §16) | ✗ (external: Z2Pack) |
| Axion angle θ, second Chern number | ✓ unique (§20) | ✗ |
| Quantum metric / geometric tensor | ✓ | ✗ |
| Local Chern marker | ✓ `make_finite` crystals (§14) | ✗ |
| Electric polarization, Thouless pumps | ✓ (§9, §10) | ✗ |
| Maximally-localized Wannier functions | ✓ in-package (§13) | ✗ |
| Wannier90 / DFT import | ✓ `W90` (§12) | ✗ |
| Native spin structure | ✓ `spinful=True` (§8) | matrices by hand |
| Superconductivity (BdG) | hack via orbitals (§18) | hack via matrices, S-matrix aware |
| Magnetic fields | Peierls by hand (§21) | Peierls by hand + gauge helpers |
| Disorder | onsite lists, dense only (§22) | ✓ at scale, with transport |
| Parametrized Hamiltonians | ✓ symbolic strings/callables, broadcast | value functions |
| GPU offload | dense batching (`use_tensorflow`) | ✗ |
| Install on Windows | `pip install pythtb` — pure Python | conda-forge builds |
| Codebase | ~1.7×10⁴ lines of Python | compiled core + Python API |

**The workflow they add up to:** build or import the model where it is easiest
(PythTB's `W90` for real materials, Kwant's discretizer for continuum devices),
compute *bulk topology* in PythTB, then rebuild the same hoppings in Kwant
(`scripts/pythtb_tools.to_kwant`) when a number must flow through a terminal:
the invariants predict, the S-matrix measures.

**Neighbours worth knowing:** Z2Pack (Wannier-centre-flow invariants for TB and
DFT with convergence bookkeeping), WannierBerri (fast Berry-phase
post-processing of Wannier90 models), TBmodels (Wannier90-centric model I/O),
PyBinding (C++ core, KPM built in), sisl (DFT interfacing at scale).
