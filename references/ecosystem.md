# The PythTB ecosystem: repositories, versions, community, citing

State as of 2026-08-28.

## Repositories and releases

| Item | Value |
|---|---|
| Canonical repo | https://github.com/pythtb/pythtb (org `pythtb`; also `pythtb/.github`, `conda-forge/pythtb-feedstock`) |
| Docs | https://pythtb.readthedocs.io (2.0 only — 1.8 docs removed 2026-06); tutorials incl. the ICTP-MARVEL 2026 tutorial notebooks in `docs/source/_static/talk/` |
| Classic site | http://www.physics.rutgers.edu/pythtb (v1.x examples; all portable to 2.0 with `references/api-map.md`) |
| Releases | 2.0.0 2025-11-11 (modular rewrite), 2.0.1 2026-01-29 (Wannier spinful fix, `models.ssh` intercell fix), **2.0.2 2026-05-26 on PyPI** (nn_bonds return type, `plot_bands` spin projection, removed `W90.model(fill_hermitian)`, faster `hamiltonian()`); no code commits on `main` since |
| Authors | Trey Cole (2.x maintainer), Sinisa Coh, David Vanderbilt |
| Licence | GPL-3.0-or-later; `CITATION.cff` DOI 10.5281/zenodo.12721315 |
| Community | GitHub issues only (no list/forum found). Open items relevant to users: #99 `plot_bands` docstring mismatch, #94 Binder lacks plotly, #62 Peierls substitution, #60 density of states, #53 band-gap checks, #52 visualizations, #50 `write_tb` in W90 |
| Upstream tests | `pytest tests` in the repo: 102 pass, 1 fails on Windows/OpenBLAS (`test_examples/haldane/edge` compares raw eigenvectors — phase freedom) |

## Physics companions

- D. Vanderbilt, *Berry Phases in Electronic Structure Theory* (Cambridge, 2018) — the book PythTB accompanies.
- Asbóth, Oroszlány, Pályi, *A Short Course on Topological Insulators* (Springer, 2016).
- Bernevig & Hughes, *Topological Insulators and Topological Superconductors* (Princeton, 2013).
- Benalcazar, Bernevig, Hughes, Science **357**, 61 (2017) — quadrupole insulator.
- Armitage, Mele, Vishwanath, Rev. Mod. Phys. **90**, 015001 (2018) — Weyl/Dirac semimetals.
- Hofstadter, Phys. Rev. B **14**, 2239 (1976); de Bruijn, Indag. Math. **84**, 39 (1981) — butterfly, Penrose pentagrid.
- Bianco & Resta, Phys. Rev. B **84**, 241106 (2011) — local Chern marker.

## Citing

PythTB: S. Coh and D. Vanderbilt, *Python Tight Binding (PythTB)* (2016),
http://www.physics.rutgers.edu/pythtb, DOI 10.5281/zenodo.12721315; version 2.0
by T. Cole, S. Coh and D. Vanderbilt. This skill: see `CITATION.cff`.
