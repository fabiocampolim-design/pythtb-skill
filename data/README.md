# data/

## `w90_silicon/` — Wannier90 output for bulk silicon

Used by notebook §12 (`W90("data/w90_silicon", "si")`) and exercise I.6.

| File | Content |
|---|---|
| `si.win` | Wannier90 input: 8 Wannier functions from 12 bands, disentanglement window, Si atoms at (0,0,0) and (¼,¼,¼)-equivalent fractional positions |
| `si_hr.dat` | real-space Hamiltonian H(R) — what `W90` actually reads |
| `si_centres.xyz` | Wannier centres (needed for the orbital positions / Convention I phases) |
| `si_band.dat`, `si_band.kpt` | Wannier90's own interpolated bands along a k-path, used as the reference the notebook compares against |

**Provenance.** Copied verbatim from the PythTB repository,
`docs/source/tutorials/silicon_w90/` (https://github.com/pythtb/pythtb, commit
`125ef73`, 2026-06-05), where it is the dataset of the official W90 tutorial.
The originating DFT run is the Wannier90 silicon example (Quantum ESPRESSO, 8
bands sp³). Licence: GNU GPL-3.0-or-later, as the PythTB repository — see the
third-party notice in `../LICENSE`. The raw `.amn/.mmn/.chk/.eig/.wout` files
shipped upstream under `unused/` are not needed by any cell and are not kept here.

No personal or measured data lives in this directory.
