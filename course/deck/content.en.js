/* SPDX-License-Identifier: Apache-2.0
   Copyright 2026 Fabio Campolim
   pythtb-skill course content, English. Strict JSON after the assignment:
   course/tools/build_deck.py, the handout, the lecturer notes and the tests all
   parse it. Figures are named by their provenance key (course/deck/figs). */
window.DECK_CONTENT = {
  "lang": "en",
  "deckTitle": "Tight-Binding Physics with PythTB",
  "deckSubtitle": "An undergraduate course in ten lectures",
  "author": "Fabio Campolim",
  "edition": "2026",
  "sections": {
    "welcome": {"name": "Welcome", "lecture": "L0", "notebook": "§0–1",
                "summary": "What tight binding is, how the course runs, and the one Hamiltonian everything else is a special case of."},
    "chain": {"name": "From atoms to bands", "lecture": "L1", "notebook": "§1–2",
              "summary": "A single orbital per atom, one hopping, and Bloch's theorem give the first band structure — and the first PythTB model."},
    "ssh": {"name": "The SSH chain", "lecture": "L2", "notebook": "§3, §6, §13",
            "summary": "Two sites per cell teach dimerization, gap closing, end states and the winding number — the whole of topology in one dimension."},
    "graphene": {"name": "Graphene & flat bands", "lecture": "L3", "notebook": "§4–7",
                 "summary": "Honeycomb Dirac cones, how a sublattice potential gaps them, exactly flat bands, ribbons, supercells and defects."},
    "spin3d": {"name": "Spin, 3D, materials", "lecture": "L4", "notebook": "§8, §11–12",
               "summary": "Spinful models with Rashba and Zeeman terms, the simple cubic crystal and its density of states, and real silicon from Wannier90."},
    "berry": {"name": "Berry phase & pumping", "lecture": "L5", "notebook": "§9–10",
              "summary": "The Berry phase as the position of charge, polarization as a Wannier centre, and the Thouless pump as a quantized flow."},
    "chern": {"name": "Chern insulators", "lecture": "L6", "notebook": "§14",
              "summary": "The Haldane model: Berry curvature, the Chern number, the phase diagram, chiral edge states and a real-space marker."},
    "z2": {"name": "Z₂ & spin Hall", "lecture": "L7", "notebook": "§15–16",
           "summary": "Time reversal changes the rules: Kramers pairs, band inversion, the Z₂ invariant from Wannier flow, helical edges."},
    "beyond": {"name": "Corners, Majoranas, Weyl", "lecture": "L8", "notebook": "§17–20",
               "summary": "Higher-order topology, superconductivity as extra orbitals, Weyl monopoles with Fermi arcs, and the axion angle."},
    "stretch": {"name": "Stretching PythTB", "lecture": "L9", "notebook": "§21–24",
                "summary": "Magnetic fields by Peierls phases, Anderson localization, a Penrose quasicrystal, and the O(N³) wall."},
    "limits": {"name": "Limits & what next", "lecture": "L10", "notebook": "§25–31",
               "summary": "What PythTB cannot do (transport, sparse, continuum, symmetry rails, interactions), where it goes wrong silently, and the road onward."},
    "close": {"name": "Close", "lecture": "", "notebook": "",
              "summary": "Where to go next."}
  },
  "stacks": [
    {"sec": "welcome", "slides": ["welcome-title", "welcome-why", "welcome-syllabus", "welcome-how", "welcome-math"]},
    {"sec": "chain", "slides": ["chain-atoms", "chain-object", "chain-bands", "chain-bloch"]},
    {"sec": "ssh", "slides": ["ssh-geometry", "ssh-bands", "ssh-gapmap", "ssh-ends", "ssh-wannier", "ssh-winding"]},
    {"sec": "graphene", "slides": ["graphene-lattice", "graphene-dirac", "graphene-cone", "graphene-flat", "graphene-kagome", "graphene-ribbons", "graphene-supercell", "graphene-math"]},
    {"sec": "spin3d", "slides": ["spin3d-spin", "spin3d-texture", "spin3d-cubic", "spin3d-dos", "spin3d-silicon", "spin3d-silicon-bands", "spin3d-math"]},
    {"sec": "berry", "slides": ["berry-charge", "berry-cycle", "berry-flow", "berry-finite", "berry-math"]},
    {"sec": "chern", "slides": ["chern-ingredients", "chern-curvature", "chern-phase", "chern-ribbon", "chern-marker", "chern-math"]},
    {"sec": "z2", "slides": ["z2-inversion", "z2-flow", "z2-edges", "z2-math"]},
    {"sec": "beyond", "slides": ["beyond-map", "beyond-bbh-model", "beyond-bbh", "beyond-kitaev-model", "beyond-kitaev", "beyond-weyl-geo", "beyond-weyl", "beyond-axion", "beyond-math"]},
    {"sec": "stretch", "slides": ["stretch-peierls", "stretch-butterfly", "stretch-disorder", "stretch-penrose", "stretch-penrose-spectrum", "stretch-wall", "stretch-math"]},
    {"sec": "limits", "slides": ["limits-list", "limits-bdg", "limits-hubbard", "limits-matrix", "limits-math"]},
    {"sec": "close", "slides": ["limits-close"]}
  ],
  "slides": {
    "welcome-title": {
      "level": "intro", "layout": "hero",
      "kicker": "pythtb-skill · undergraduate course",
      "title": "Tight-Binding Physics with PythTB",
      "sub": "From atoms to topological matter in ten lectures — every figure computed live in the companion notebook",
      "notes": "Set the contract on the first slide: nothing in this course is a cartoon. Every plot was produced by a cell of PythTB_Theory_and_Practice.ipynb and can be re-run by the students. The course assumes second-year quantum mechanics (the Schrödinger equation, matrices, eigenvalues) and nothing about solid-state physics. Q: \"Do I need to know Python?\" A: You need to read it; the notebook gives every model in full and the exercises ask you to modify, not to write from scratch."
    },
    "welcome-why": {
      "level": "intro", "layout": "text",
      "title": "Why tight binding?",
      "lead": "A crystal is 10<sup>23</sup> atoms. Tight binding keeps <strong>one number per atom</strong> (an energy) and <strong>one number per bond</strong> (a hopping) — and still predicts metals, insulators, and topological matter.",
      "bullets": [
        "Electrons sit on atomic orbitals and <em>hop</em> to neighbours: the Hamiltonian is a sparse matrix of hoppings.",
        "Periodicity turns that infinite matrix into a small matrix <span class='math'>H(k)</span> for each crystal momentum <span class='math'>k</span>.",
        "Its eigenvalues are the <strong>band structure</strong>; its eigenvectors carry the geometry — Berry phases, polarization, topology.",
        "PythTB does exactly this and nothing else: build a lattice model, solve it on paths and meshes, read out the geometry."
      ],
      "notes": "Give the students the mental model early: matrix elements are the whole theory. Contrast with density-functional theory (thousands of basis functions) — tight binding is what you get after you already know which orbitals matter. Q: \"Is this an approximation?\" A: Yes: it truncates the basis to a few orbitals and the hoppings to near neighbours. Lecture 4 shows how good it can be when the hoppings come from a real calculation (silicon)."
    },
    "welcome-syllabus": {
      "level": "intro", "layout": "syllabus",
      "title": "Ten lectures",
      "lead": "Each lecture is one vertical stack of slides: a picture first, the physics next, the equations last. Notebook sections are given for every lecture.",
      "notes": "Walk the syllabus once. Point out the three arcs: lectures 1–4 build models (chains, honeycombs, spin, 3D, materials), lectures 5–8 extract topology from the eigenvectors (Berry phase, Chern, Z₂, higher order), lectures 9–10 push the tool to its limits and beyond. Q: \"Which lectures can be skipped?\" A: 8 and 9 are enrichment; 1–7 and 10 form the spine."
    },
    "welcome-how": {
      "level": "core", "layout": "text",
      "title": "How each lecture is built",
      "lead": "The deck is a two-dimensional grid: <strong>→</strong> jumps between lectures, <strong>↓</strong> descends through one lecture from the simplest slide to the most mathematical.",
      "bullets": [
        "<span class='c-3'>intro</span> slides: one figure, plain language, no symbols beyond <span class='math'>E</span> and <span class='math'>k</span>.",
        "<span class='c-1'>core</span> slides: the physics and how PythTB computes it (which method, which object).",
        "<span class='c-violet'>math</span> slides: the formulas behind the figures, with the derivation sketched in the lecturer notes.",
        "To run the notebook: <code>install_pythtb_windows.ps1</code> (or <code>pip install -r requirements.txt</code>), then open <code>PythTB_Theory_and_Practice.ipynb</code>; exercises with solutions in <code>PythTB_Exercises_Solutions.ipynb</code>.",
        "Speaker view: press <code>S</code>. Section jump: <code>Shift+←/→</code>. Overview: <code>Esc</code>."
      ],
      "notes": "This slide is for the lecturer as much as for the students: the level chip at the top-right of every slide says where you are, so a first-year audience can stop after the core slides and a fourth-year audience can go straight to the math. Q: \"Where are the exercises?\" A: At the end of each Part of the notebook, with full solutions in the second notebook; the handout lists which exercises match which lecture."
    },
    "welcome-math": {
      "level": "math", "layout": "eq",
      "title": "The one Hamiltonian of the course",
      "lead": "Everything that follows is a special case of a second-quantized hopping Hamiltonian and its Bloch transform.",
      "eqs": [
        {"label": "real space", "math": "<span class='math'>H = Σ<sub>i</sub> ε<sub>i</sub> c<sup>†</sup><sub>i</sub>c<sub>i</sub> + Σ<sub>⟨ij⟩</sub> ( t<sub>ij</sub> c<sup>†</sup><sub>i</sub>c<sub>j</sub> + <span class='fn'>h.c.</span> )</span>"},
        {"label": "Bloch Hamiltonian", "math": "<span class='math'>H<sub>ab</sub>(k) = Σ<sub>R</sub> e<sup> i k·(R + τ<sub>b</sub> − τ<sub>a</sub>)</sup> H<sub>ab</sub>(R)</span>"},
        {"label": "eigenproblem", "math": "<span class='math'>H(k) u<sub>n</sub>(k) = E<sub>n</sub>(k) u<sub>n</sub>(k)</span>"}
      ],
      "bullets": [
        "<span class='math'>ε<sub>i</sub></span>: onsite energies; <span class='math'>t<sub>ij</sub></span>: hoppings (complex in general — hermiticity fixes the reverse hop).",
        "<span class='math'>R</span>: lattice vector, <span class='math'>τ<sub>a</sub></span>: orbital position in the cell. PythTB uses this <em>atomic gauge</em>: the phases carry the orbital positions, so Berry phases have the right meaning.",
        "<code>TBModel.set_onsite</code>, <code>set_hop</code>, <code>solve_path</code> / <code>solve_mesh</code> are these three lines."
      ],
      "notes": "Derive the Bloch transform on the board: write the Bloch sum |ψ_k⟩ = Σ_R e^{ik(R+τ)} |R, a⟩, take matrix elements, and show that the sum over R collapses because of translation invariance. Stress the atomic (periodic-in-τ) gauge: the alternative lattice gauge omits τ and gives a periodic H(k) but shifts Berry phases by k·τ — PythTB's choice is the one for which the Wannier centre is a position. Q: \"Why h.c.?\" A: A hop from j to i must have amplitude t_ij*, or the Hamiltonian is not Hermitian and energies become complex; PythTB adds it automatically, which is why set_hop must be called once per bond, never twice."
    },

    "chain-atoms": {
      "level": "intro", "layout": "fig-right", "fig": "s02-f1",
      "title": "One orbital per atom, one hop per bond",
      "lead": "The simplest crystal: a row of identical atoms, spacing <span class='math'>a</span>. Each has one orbital at energy <span class='math'>ε<sub>0</sub></span>; an electron hops to the neighbour with amplitude <span class='math'>t</span>.",
      "bullets": [
        "The figure is what PythTB stores: the sites, their onsite energy, the bond.",
        "Two numbers, <span class='math'>ε<sub>0</sub></span> and <span class='math'>t</span>, will produce a whole band of allowed energies.",
        "The sign of <span class='math'>t</span> is set by the orbital overlap: for s-orbitals it is negative."
      ],
      "notes": "Start from the hydrogen-molecule picture the students know: two orbitals, bonding and antibonding, split by 2|t|. A chain is the same thing repeated: a continuum of bonding-to-antibonding combinations labelled by k. Q: \"Why is t negative?\" A: The hopping is the matrix element of a negative potential between two positive s-orbital lobes; the bonding (even) combination is lower in energy, which is what t < 0 encodes."
    },
    "chain-object": {
      "level": "core", "layout": "code",
      "title": "The object model: <code>Lattice</code> → <code>TBModel</code>",
      "lead": "A PythTB model is a lattice (vectors + orbital positions) plus a table of onsite energies and hoppings. Nothing is solved until you ask.",
      "code": "from pythtb import Lattice, TBModel\n\nlat = Lattice(lat_vecs=[[1.0]], orb_vecs=[[0.0]])     # a = 1, one orbital at τ = 0\nchain = TBModel(dim_k=1, dim_r=1, lattice=lat)\nchain.set_onsite([0.0])                             # ε0\nchain.set_hop(-1.0, 0, 0, [1])                      # t = -1 from orbital 0 to its image in cell R = +1\n\nk_path, k_dist, k_nodes = chain.k_path([[-0.5], [0.0], [0.5]], nk=201)\nenergies = chain.solve_path(k_path)                 # shape (n_bands, nk)",
      "bullets": [
        "<code>dim_k</code> and <code>dim_r</code> can differ: a ribbon is <code>dim_k=1</code> in <code>dim_r=2</code>.",
        "<code>set_hop(t, i, j, R)</code> connects orbital <span class='math'>i</span> in the home cell to orbital <span class='math'>j</span> in cell <span class='math'>R</span>; the reverse hop is implied.",
        "Reduced coordinates everywhere: <span class='math'>k</span> in units of the reciprocal vectors, positions in units of the lattice vectors."
      ],
      "notes": "Show the code, then ask the class what the matrix H(k) is for this model before running it: a 1×1 matrix, ε0 + t e^{ik} + t e^{-ik}. Emphasize that solve_path returns energies indexed [band, k] in PythTB 2.0 — the reverse of the 1.x convention, and the most common mistake in student code. Q: \"What does R = [1] mean in 2D?\" A: A vector of integers, one per lattice direction; [1, 0] is the neighbour cell along the first lattice vector."
    },
    "chain-bands": {
      "level": "core", "layout": "fig", "fig": "s02-f2",
      "title": "The first band structure",
      "lead": "Numerical eigenvalues along the 1D Brillouin zone lie exactly on the analytic cosine. Bandwidth 4|<span class='math'>t</span>|, minimum at <span class='math'>k = 0</span>.",
      "notes": "Read the plot aloud: the horizontal axis is crystal momentum in units of 2π/a, the vertical axis is energy in units of |t|. The band is the set of all energies an electron can have; with one electron per atom it is half-filled and the chain is a metal. Q: \"Where are the atoms in this picture?\" A: Nowhere — k-space is the Fourier conjugate of the atom positions; a single band means every atom is equivalent."
    },
    "chain-bloch": {
      "level": "math", "layout": "eq",
      "title": "Bloch's theorem on one line",
      "eqs": [
        {"label": "Bloch state", "math": "<span class='math'>|ψ<sub>k</sub>⟩ = Σ<sub>n</sub> e<sup> i k n a</sup> |n⟩</span>"},
        {"label": "dispersion", "math": "<span class='math'>E(k) = ε<sub>0</sub> + 2t <span class='fn'>cos</span>(ka)</span>"},
        {"label": "near the bottom", "math": "<span class='math'>E ≈ ε<sub>0</sub> + 2t + |t| a<sup>2</sup> k<sup>2</sup>  ⇒  m* = ħ<sup>2</sup> / (2|t|a<sup>2</sup>)</span>"}
      ],
      "bullets": [
        "Translation by <span class='math'>a</span> commutes with <span class='math'>H</span>; its eigenvalues <span class='math'>e<sup>ika</sup></span> label the eigenstates.",
        "<span class='math'>k</span> and <span class='math'>k + 2π/a</span> give the same state: the Brillouin zone is <span class='math'>(−π/a, π/a]</span>.",
        "A stronger hop means a wider band and a lighter electron — the effective mass is set by <span class='math'>t</span>."
      ],
      "notes": "Do the one-line derivation: apply H to the Bloch sum, use H|n⟩ = ε0|n⟩ + t|n−1⟩ + t|n+1⟩, shift the summation index, and read off E(k). Then expand the cosine for the effective mass; this is the link to the free-electron picture the students already have. Q: \"What if there are two orbitals per atom?\" A: H(k) becomes 2×2 and there are two bands; that is exactly the next lecture."
    },

    "ssh-geometry": {
      "level": "intro", "layout": "fig-right", "fig": "s03-f1",
      "title": "Two sites per cell, alternating bonds",
      "lead": "Polyacetylene-style: bonds alternate strong, weak, strong, weak. The unit cell holds two orbitals, at <span class='math'>τ = 0</span> and <span class='math'>τ = ½</span>, joined by the <em>intracell</em> hop <span class='math'>v</span>; the <em>intercell</em> hop <span class='math'>w</span> joins cells.",
      "bullets": [
        "Same atoms, same spacing as the chain — only the hoppings alternate.",
        "One question decides everything to come: <strong>which bond is inside the unit cell?</strong>",
        "The choice looks arbitrary. It is not: it becomes physical the moment the chain ends."
      ],
      "notes": "This is the Su–Schrieffer–Heeger model. Draw the chain on the board twice with the cell boundary shifted by one bond and ask the class whether the two drawings describe different systems. For the infinite chain they do not; for a finite chain they do (the last cell is either complete or not). Q: \"Is this a real material?\" A: Polyacetylene: the Peierls distortion makes the C–C bonds alternate, which is why the model was invented in 1979."
    },
    "ssh-bands": {
      "level": "core", "layout": "fig", "fig": "s03-f2",
      "title": "One symbolic model, three insulators",
      "lead": "PythTB lets a hopping be a <em>parameter</em>. The same model evaluated at <span class='math'>w &lt; v</span>, <span class='math'>w = v</span>, <span class='math'>w &gt; v</span> gives two gapped band structures and one metal in between.",
      "bullets": [
        "Two orbitals per cell ⇒ two bands; the gap at the zone edge is <span class='math'>2|v − w|</span>.",
        "The two insulating cases look identical in energy — the difference is hidden in the eigenvectors.",
        "<code>set_hop</code> with a named parameter, then <code>solve_path(..., params={\"w\": ...})</code>: one build, many Hamiltonians."
      ],
      "notes": "Insist on the puzzle: the spectra for w = 0.5 and w = 1.5 (with v = 1) look the same after reflection, yet these will turn out to be different phases. Topology lives in wavefunctions, not energies. Q: \"How does PythTB store a symbolic hopping?\" A: As a callable evaluated at solve time; the model is built once and parameters are supplied per call, which is what makes phase diagrams cheap."
    },
    "ssh-gapmap": {
      "level": "core", "layout": "fig-right", "fig": "s03-f3",
      "title": "The gap closes at exactly one point",
      "lead": "The direct gap over the whole <span class='math'>(k, w)</span> plane vanishes only at <span class='math'>w = v</span>, <span class='math'>k = π</span>.",
      "bullets": [
        "To go from one insulator to the other you <em>must</em> close the gap: they are not adiabatically connected.",
        "That is the definition of distinct <strong>topological phases</strong> — inside a symmetry class, phases separated by a gap closing.",
        "The symmetry here: <em>chiral</em> (sublattice) symmetry — no hopping within a sublattice."
      ],
      "notes": "This slide plants the idea of adiabatic continuity: two Hamiltonians are equivalent if you can deform one into the other without closing the gap and without breaking the protecting symmetry. Add an onsite term ±Δ on the two sublattices (breaking chiral symmetry) and the two phases connect — a good exercise. Q: \"Why does the gap close at k = π and not elsewhere?\" A: Because |v + w e^{ik}| is smallest when e^{ik} = −1; the math slide makes this explicit."
    },
    "ssh-ends": {
      "level": "core", "layout": "two-figs", "fig": "s06-f1", "fig2": "s06-f2",
      "title": "Cut the chain: end modes appear",
      "lead": "<code>cut_piece</code> makes a finite chain. For <span class='math'>w &gt; v</span> two states sit in the middle of the gap, one per end, exponentially localized.",
      "bullets": [
        "The open spectrum versus dimerization (left): mid-gap states exist only on one side of <span class='math'>w = v</span>.",
        "Their profile (right): |ψ|<sup>2</sup> falls off as <span class='math'>(v/w)<sup>2n</sup></span>, on one sublattice only.",
        "<strong>Bulk–boundary correspondence</strong>: a bulk invariant (next slides) counts the protected end states."
      ],
      "notes": "Now resolve the puzzle from ssh-bands: the phase with w > v is the one whose finite chain ends on a weak bond, leaving an unpaired orbital at each end. The zero energy is protected by chiral symmetry, not by fine tuning: show that a random chiral-preserving perturbation moves the bulk bands but not the end modes. Q: \"Why exactly zero energy?\" A: Chiral symmetry maps E → −E; an isolated end state must be its own partner, so E = 0 (until the two ends hybridize, exponentially small in length)."
    },
    "ssh-wannier": {
      "level": "core", "layout": "fig-right", "fig": "s13-f1",
      "title": "Where the electron actually sits: the Wannier function",
      "lead": "Fourier-transform the occupied Bloch band back to real space and you get a localized orbital — the <strong>Wannier function</strong>. Its centre is the position of the electron's charge.",
      "bullets": [
        "Built here with PythTB's <code>Wannier</code> class (maximal localization inside PythTB, no external code).",
        "Exponential decay, like the end mode: the same length scale <span class='math'>ξ ∝ 1/ln(w/v)</span> governs both.",
        "In the trivial phase the centre is on the atom (<span class='math'>x̄ = 0</span>); in the topological phase it sits on the bond (<span class='math'>x̄ = ½</span>)."
      ],
      "notes": "This is the bridge to Berry phases: the Wannier centre is the Berry phase of the occupied band divided by 2π (lecture 5). For the SSH chain, chiral symmetry quantizes it to 0 or ½. Show the two cases in the notebook if time allows. Q: \"Is the Wannier function unique?\" A: No: a k-dependent phase choice (gauge) changes its shape, but not its centre modulo a lattice vector — that is why the centre, not the shape, is the physical quantity."
    },
    "ssh-winding": {
      "level": "math", "layout": "eq",
      "title": "The winding number",
      "eqs": [
        {"label": "Bloch Hamiltonian", "math": "<span class='math'>H(k) = d(k)·σ,   d(k) = ( v + w <span class='fn'>cos</span> k,  w <span class='fn'>sin</span> k,  0 )</span>"},
        {"label": "bands", "math": "<span class='math'>E<sub>±</sub>(k) = ± |v + w e<sup>ik</sup>| = ± √( v<sup>2</sup> + w<sup>2</sup> + 2vw <span class='fn'>cos</span> k )</span>"},
        {"label": "invariant", "math": "<span class='math'>ν = (1/2π) ∮ dk  ∂<sub>k</sub> <span class='fn'>arg</span>( v + w e<sup>ik</sup> ) ∈ {0, 1}</span>"}
      ],
      "bullets": [
        "<span class='math'>d(k)</span> traces a circle of radius <span class='math'>w</span> centred at <span class='math'>(v, 0)</span>; it encloses the origin iff <span class='math'>w &gt; v</span>.",
        "Chiral symmetry <span class='math'>σ<sub>z</sub> H σ<sub>z</sub> = −H</span> keeps <span class='math'>d<sub>z</sub> = 0</span>: the curve stays in a plane and the winding is well defined.",
        "Berry phase of the lower band <span class='math'>φ = πν</span>; Wannier centre <span class='math'>x̄ = φ/2π = ν/2</span>."
      ],
      "notes": "Derive d(k) from the 2×2 matrix (off-diagonal element v + w e^{ik} in the atomic gauge with the second orbital at τ = ½ the phase is e^{ik/2}-shifted; the winding is gauge independent). Draw the circle for both phases. Then connect to the Wannier centre: the Berry phase of a two-band model with d_z = 0 is half the solid angle swept, which is π for one winding. Q: \"What happens for w = v?\" A: The circle passes through the origin, |d| = 0 at k = π, and the winding number is undefined — the gap closing of ssh-gapmap."
    },

    "graphene-lattice": {
      "level": "intro", "layout": "two-figs", "fig": "s04-f1", "fig2": "s04-f2",
      "title": "The honeycomb: two sublattices, one hexagonal zone",
      "lead": "Graphene is a triangular lattice with a two-atom basis (A and B). Every A neighbours three B's. Its Brillouin zone is a hexagon whose corners <span class='math'>K</span>, <span class='math'>K'</span> will carry all the physics.",
      "bullets": [
        "Built-in <code>visualize</code> draws exactly what the model contains: positions and bonds.",
        "The band path <span class='math'>Γ–K–M–K'–Γ</span> visits every high-symmetry point once.",
        "One <span class='math'>p<sub>z</sub></span> orbital per carbon, hopping <span class='math'>t ≈ 2.7 eV</span> to nearest neighbours: the whole model."
      ],
      "notes": "Make the students count: two orbitals per cell, so two bands; one electron per orbital, so the lower band is exactly filled. Whether graphene is a metal or an insulator depends on whether the two bands touch. Q: \"Why not a square lattice?\" A: Carbon's sp² bonding makes 120° angles; the honeycomb is the geometry, not a choice. The Dirac cones are a consequence of the two-sublattice structure plus symmetry."
    },
    "graphene-dirac": {
      "level": "core", "layout": "two-figs", "fig": "s04-f3", "fig2": "s04-f4",
      "title": "Dirac cones — and how to gap them",
      "lead": "Left: graphene's bands touch at <span class='math'>K</span> and <span class='math'>K'</span> in linear crossings, coloured by sublattice weight. Right: boron nitride — same lattice, different atoms on A and B — opens a gap of <span class='math'>2Δ</span>.",
      "bullets": [
        "At the touching point the electron has <strong>zero effective mass</strong>: the dispersion is a cone, not a parabola.",
        "The colour shows the eigenvector: away from <span class='math'>K</span> the bands mix A and B equally; the sublattice potential <span class='math'>±Δ</span> polarizes them.",
        "<code>set_onsite([Δ, −Δ])</code> is the entire difference between graphene and BN."
      ],
      "notes": "The crossing is protected by two things together: inversion (A ↔ B) and time reversal. Breaking inversion with Δ gaps it (BN); breaking time reversal gaps it too, but differently — that is the Haldane model of lecture 6. Q: \"Why is it called Dirac?\" A: Near K the 2×2 Bloch Hamiltonian is v_F (q_x σ_x + q_y σ_y), the massless Dirac equation in two dimensions with the sublattice playing the role of spin."
    },
    "graphene-cone": {
      "level": "core", "layout": "fig", "fig": "s04-f5",
      "title": "The cone as a surface",
      "lead": "<code>solve_mesh</code> over a patch of the zone around <span class='math'>K</span>: the two bands form a double cone, isotropic to first order.",
      "notes": "This is the picture to keep for the rest of the course: a band touching in 2D is a point, and points are fragile — a gap can open by any symmetry-breaking mass term. Which mass term opens it decides the topology. Q: \"Is the cone perfectly circular?\" A: Only near the apex; further out the lattice trigonally warps it, visible as the triangular shape of the contours."
    },
    "graphene-flat": {
      "level": "core", "layout": "two-figs", "fig": "s05-f1", "fig2": "s05-f2",
      "title": "Exactly flat bands: the Lieb lattice",
      "lead": "Three sites per square cell (one corner, two edges). One band has <em>no dispersion at all</em> — and a compact localized state explains why in one picture.",
      "bullets": [
        "Flat band ⇒ infinite effective mass ⇒ interactions win over kinetic energy: the playground for magnetism and correlated phases.",
        "The localized state lives on the four edge sites around a plaquette with alternating signs: every hop out of it cancels.",
        "Bipartite geometry (corner sites outnumbered by edge sites) guarantees at least one zero-energy state per cell."
      ],
      "notes": "Let the students verify the compact localized state on the board: apply H to the alternating-sign state and show that each corner site receives +t − t = 0. Because there is one such state per cell, they span a whole band at E = 0. Q: \"Is the flat band stable?\" A: To any perturbation that preserves the bipartite structure, yes; a next-nearest-neighbour hopping bends it."
    },
    "graphene-kagome": {
      "level": "core", "layout": "two-figs", "fig": "s05-f3", "fig2": "s05-f4",
      "title": "The kagome lattice: flat band meets Dirac cone",
      "lead": "Corner-sharing triangles, three sites per cell. The spectrum has both a Dirac crossing at <span class='math'>K</span> and a flat band touching a dispersive one quadratically at <span class='math'>Γ</span>.",
      "bullets": [
        "Here the localized states are ring states around a hexagon, alternating in sign.",
        "The sign of <span class='math'>t</span> decides whether the flat band sits on top or at the bottom — a one-line experiment in the notebook.",
        "Real kagome metals (e.g. the AV<sub>3</sub>Sb<sub>5</sub> family) show exactly these features in photoemission."
      ],
      "notes": "Two motifs from one lattice: the honeycomb's Dirac cone (kagome is the line graph of the honeycomb) and the Lieb lattice's flat band. Ask which is more robust: the quadratic band touching at Γ is protected by the lattice symmetry and the flat band's existence by the ring-state construction. Q: \"Why quadratic touching, not linear?\" A: At Γ the flat band and the dispersive band belong to a two-dimensional representation; the touching must be even in k by symmetry."
    },
    "graphene-ribbons": {
      "level": "core", "layout": "two-figs", "fig": "s06-f3", "fig2": "s06-f4",
      "title": "Ribbons: finite across, infinite along",
      "lead": "<code>cut_piece</code> along one direction makes a strip: <code>dim_k = 1</code> inside <code>dim_r = 2</code>. Its band structure depends on the edge: the zigzag termination carries a <strong>flat edge band</strong> at <span class='math'>E = 0</span>.",
      "bullets": [
        "Projecting the 2D bands onto the strip's <span class='math'>k</span> gives the shaded continuum; states outside it live on the edges.",
        "Zigzag edges end on one sublattice: the edge state is the SSH end mode in disguise, with <span class='math'>k</span> as a parameter.",
        "Armchair edges mix both sublattices and have no such band."
      ],
      "notes": "Make the SSH connection explicit: for fixed transverse momentum k, a zigzag ribbon is a one-dimensional dimerized chain whose effective v/w ratio depends on k; the edge band exists precisely on the k-interval where that chain is topological (between the projections of K and K'). This is the first example of dimensional reduction, which returns in the Weyl lecture. Q: \"Why is the edge band exactly flat?\" A: Chiral symmetry at E = 0 plus the k-dependent SSH argument; any chiral-breaking term (next-nearest hopping) bends it."
    },
    "graphene-supercell": {
      "level": "core", "layout": "two-figs", "fig": "s07-f1", "fig2": "s07-f2",
      "title": "Supercells and defects",
      "lead": "<code>make_supercell</code> repeats the cell; the bands fold into a smaller zone (left). <code>remove_orb</code> deletes a site: a vacancy in graphene binds a zero-energy state on the other sublattice (right).",
      "bullets": [
        "Band folding creates no new physics — it re-labels the same states; the crossings at the new zone boundary are artefacts.",
        "Defects, disorder and edges all need supercells: this is how a periodic code describes a non-periodic object.",
        "The vacancy mode is a bipartite-lattice theorem (Lieb): sublattice imbalance ⇒ zero modes."
      ],
      "notes": "Two mechanical tools with one lesson: PythTB has no notion of 'a defect', only of unit cells, so anything non-periodic is built as a big periodic cell. Note the numerical cost — a 30×30 supercell is a 1800×1800 dense matrix, foreshadowing lecture 9. Q: \"Where does the vacancy state live?\" A: On the sublattice opposite to the removed atom, decaying as 1/r: a zero mode of a bipartite lattice with one more A than B site."
    },
    "graphene-math": {
      "level": "math", "layout": "eq",
      "title": "The honeycomb Bloch Hamiltonian",
      "eqs": [
        {"label": "two-band model", "math": "<span class='math'>H(k) = ( Δ  f(k) ; f*(k)  −Δ ),   f(k) = t Σ<sub>j=1</sub><sup>3</sup> e<sup> i k·δ<sub>j</sub></sup></span>"},
        {"label": "bands", "math": "<span class='math'>E<sub>±</sub>(k) = ± √( Δ<sup>2</sup> + |f(k)|<sup>2</sup> )</span>"},
        {"label": "near K", "math": "<span class='math'>f(K + q) ≈ ħv<sub>F</sub> (q<sub>x</sub> − i q<sub>y</sub>),   ħv<sub>F</sub> = 3ta<sub>cc</sub>/2</span>"}
      ],
      "bullets": [
        "<span class='math'>f(K) = 0</span> because the three phases <span class='math'>e<sup>iK·δ<sub>j</sub></sup></span> are the cube roots of unity: the Dirac point is a cancellation forced by symmetry.",
        "<span class='math'>Δ = 0</span>: massless cone, <span class='math'>E = ±ħv<sub>F</sub>|q|</span>. <span class='math'>Δ ≠ 0</span>: mass gap <span class='math'>2Δ</span> (boron nitride).",
        "Lieb flat band: the state <span class='math'>|ψ⟩ = |e<sub>1</sub>⟩ − |e<sub>2</sub>⟩ + |e<sub>3</sub>⟩ − |e<sub>4</sub>⟩</span> around a plaquette satisfies <span class='math'>H|ψ⟩ = 0</span> exactly."
      ],
      "notes": "Write f(k) explicitly with δ_j the three nearest-neighbour vectors and evaluate at K = (4π/3√3 a_cc, 0): the three terms are 1, ω, ω² and sum to zero. Expand to first order in q to get the Dirac form; the sign of the linear term differs at K' (opposite chirality), which matters for the Haldane model. Q: \"Is v_F universal?\" A: It is 3ta_cc/2ħ ≈ 10⁶ m/s for graphene; different lattices with Dirac cones have different velocities but the same 2×2 structure."
    },

    "spin3d-spin": {
      "level": "intro", "layout": "fig-right", "fig": "s08-f1",
      "title": "Spin, natively",
      "lead": "<code>spinful=True</code> doubles every orbital and lets hoppings be 2×2 matrices in spin space. A one-dimensional wire with <strong>Rashba</strong> spin–orbit coupling and a <strong>Zeeman</strong> field shows what that buys.",
      "bullets": [
        "Rashba: the spin rotates as the electron moves — two shifted parabolas with opposite spin.",
        "Zeeman: a field opens a gap where the two cross, at <span class='math'>k = 0</span>.",
        "Together: a <em>helical</em> gap — the recipe behind Majorana nanowires."
      ],
      "notes": "This is the first place the eigenvectors have internal structure students can visualize (spin). Keep the story concrete: an InSb nanowire in a magnetic field, the platform for the Majorana experiments of the 2010s; add superconductivity (lecture 8) and you have the proposal. Q: \"Why does Rashba shift the bands rather than split them at fixed k?\" A: The term is odd in k (α σ_y k): it acts like a momentum-dependent magnetic field, zero at k = 0."
    },
    "spin3d-texture": {
      "level": "core", "layout": "two-figs", "fig": "s08-f2", "fig2": "s08-f3",
      "title": "Spin–momentum locking",
      "lead": "Colour the bands by <span class='math'>⟨σ<sub>z</sub>⟩</span> (left) or plot the full texture <span class='math'>⟨σ<sub>y</sub>⟩, ⟨σ<sub>z</sub>⟩</span> along the band (right): the spin direction is fixed by the momentum.",
      "bullets": [
        "<code>plot_bands</code> can colour by any expectation value: the eigenvectors are one call away.",
        "<span class='math'>⟨σ<sub>y</sub>⟩</span> is odd in <span class='math'>k</span> (Rashba), <span class='math'>⟨σ<sub>z</sub>⟩</span> is even and peaks at <span class='math'>k = 0</span> (Zeeman).",
        "Inside the helical gap only one spin direction moves right and the other left: backscattering needs a spin flip."
      ],
      "notes": "Locking is the mechanism that makes edge states of topological insulators robust (lecture 7): if spin and direction are tied, a non-magnetic impurity cannot reverse the motion. Q: \"Where does the texture go when B → 0?\" A: ⟨σ_z⟩ vanishes everywhere; the two bands become pure ±σ_y eigenstates and cross at k = 0 — the gap needs both ingredients."
    },
    "spin3d-cubic": {
      "level": "core", "layout": "two-figs", "fig": "s11-f1", "fig2": "s11-f2",
      "title": "Three dimensions: the simple cubic crystal",
      "lead": "One orbital, six equal nearest-neighbour hops. The band is a sum of three cosines, bandwidth <span class='math'>12|t|</span>, checked analytically along a standard path.",
      "bullets": [
        "<code>dim_k = dim_r = 3</code>; the k-path visits <span class='math'>Γ, X, M, R</span>: each segment turns on one more cosine.",
        "Nothing new conceptually — but the mesh needed for a 3D integral grows as <span class='math'>n<sup>3</sup></span>.",
        "Reading dimension by dimension: <span class='math'>Γ–X</span> is the 1D chain of lecture 1."
      ],
      "notes": "Use this slide to normalize 3D: the same object model, one more lattice vector. The path labels follow the cubic convention (X = (½,0,0), M = (½,½,0), R = (½,½,½) in reduced coordinates). Q: \"Why is the band so simple?\" A: Separability: with only axis-aligned hops E is a sum of three independent 1D dispersions; any diagonal hop couples the directions."
    },
    "spin3d-dos": {
      "level": "core", "layout": "fig-right", "fig": "s11-f3",
      "title": "The density of states and its van Hove kinks",
      "lead": "Histogram 216 000 eigenvalues from a full 3D mesh: the density of states has kinks at <span class='math'>E = ±2t</span> where the band has saddle points.",
      "bullets": [
        "<span class='math'>g(E) dE</span> counts states per energy interval; it is what photoemission, heat capacity and tunnelling actually measure.",
        "In 1D a saddle gives a divergence, in 2D a logarithm, in 3D only a kink: dimensionality is visible in the DOS.",
        "Square-root edges at <span class='math'>±6t</span>: the free-electron behaviour returns near the band bottom."
      ],
      "notes": "The DOS is the first quantity that requires a mesh rather than a path — a good moment to introduce solve_mesh and k-point convergence (double the mesh, compare the histogram). Q: \"Why 216 000?\" A: 60³ points; the histogram noise scales as the inverse square root of the count per bin, and the students can see it in the wiggles."
    },
    "spin3d-silicon": {
      "level": "core", "layout": "fig-right", "fig": "s12-f1",
      "title": "A real material: silicon in the diamond structure",
      "lead": "Two interpenetrating fcc lattices, each atom tetrahedrally bonded to four neighbours. Tight-binding parameters for it can be <em>computed</em>, not guessed: Wannier90 turns a first-principles calculation into hoppings.",
      "bullets": [
        "The Wannier functions are sp<sup>3</sup>-like bond orbitals; the hoppings between them are the matrix elements of the DFT Hamiltonian.",
        "PythTB's <code>W90</code> class reads the standard <code>_hr.dat</code>, <code>_centres.xyz</code> and <code>.win</code> files.",
        "The data ships with PythTB (GPL, attributed); no DFT code is needed to follow along."
      ],
      "notes": "Position this as the answer to 'is tight binding an approximation?': done this way it is a controlled one, with the hoppings extracted from a converged first-principles calculation and truncated at a chosen distance. Q: \"What is Wannier90?\" A: A code that takes Bloch states from a DFT program and finds the unitary mixing that makes them maximally localized — lecture 2's Wannier function at industrial scale."
    },
    "spin3d-silicon-bands": {
      "level": "core", "layout": "two-figs", "fig": "s12-f2", "fig2": "s12-f3",
      "title": "Hoppings decay; truncate and compare",
      "lead": "Every hopping matrix element versus distance (left): exponential decay. Keep the hoppings above a threshold and compare with the Wannier90 reference bands (right): the truncated model tracks the first-principles bands.",
      "bullets": [
        "Exponential decay is the definition of a good tight-binding basis — and of a localized Wannier function.",
        "Truncation is a physical approximation with a controllable error: raise the cutoff, watch the bands converge.",
        "Below the gap the match is essentially perfect; the conduction bands are more sensitive."
      ],
      "notes": "This is the quality-control loop of real tight-binding work: extract, truncate, compare, repeat. Ask the students which bands they would trust for a transport calculation and why. Q: \"Why are the conduction bands worse?\" A: The Wannierization window was chosen for the valence manifold; conduction states are less localized and leak out of the frozen window."
    },
    "spin3d-math": {
      "level": "math", "layout": "eq",
      "title": "Spin–orbit on a lattice, and the DOS",
      "eqs": [
        {"label": "Rashba–Zeeman wire", "math": "<span class='math'>H(k) = −2t <span class='fn'>cos</span> k + 2α <span class='fn'>sin</span> k  σ<sub>y</sub> + B σ<sub>z</sub></span>"},
        {"label": "bands", "math": "<span class='math'>E<sub>±</sub>(k) = −2t <span class='fn'>cos</span> k ± √( (2α <span class='fn'>sin</span> k)<sup>2</sup> + B<sup>2</sup> )</span>"},
        {"label": "density of states", "math": "<span class='math'>g(E) = Σ<sub>n</sub> ∫<sub>BZ</sub> d<sup>3</sup>k/(2π)<sup>3</sup>  δ( E − E<sub>n</sub>(k) )</span>"}
      ],
      "bullets": [
        "The lattice Rashba term is <span class='math'>iα σ<sub>y</sub></span> on the bond (Hermitian partner <span class='math'>−iα σ<sub>y</sub></span>): a 2×2 hopping matrix in <code>set_hop</code>.",
        "Helical gap <span class='math'>2B</span> at <span class='math'>k = 0</span>; for <span class='math'>B = 0</span> the bands cross there — Kramers pairs, no gap allowed.",
        "Van Hove: <span class='math'>g(E)</span> is singular where <span class='math'>∇<sub>k</sub>E = 0</span>; the type of singularity depends on the dimension."
      ],
      "notes": "Two derivations: (1) diagonalize the 2×2 matrix at fixed k (it is a spin in an effective field (0, 2α sin k, B)); (2) for the DOS, change variables from k to E and show that the Jacobian 1/|∇E| is what diverges at critical points; in 3D the integrable singularity gives a kink. Q: \"Why does Kramers forbid the gap at B = 0?\" A: With time reversal Θ² = −1, states at k and −k are degenerate partners; at k = 0 the partner is the state itself, forcing a two-fold degeneracy."
    },

    "berry-charge": {
      "level": "intro", "layout": "fig-right", "fig": "s09-f1",
      "title": "Where is the electron's charge?",
      "lead": "In an insulator the occupied band is a cloud of charge in each cell. Its centre — the <strong>Wannier centre</strong> — is the electric polarization. Move the atoms, and the centre moves by a definite amount.",
      "bullets": [
        "The figure draws the polarization difference between two dimerizations: the charge centre shifts along the bond.",
        "PythTB's <code>Mesh</code> + <code>WFArray</code> compute the shift from the Bloch eigenvectors alone.",
        "Only <em>differences</em> of polarization are physical — the absolute value depends on the choice of unit cell."
      ],
      "notes": "Set up the modern theory of polarization in one sentence: polarization is a Berry phase. Historically the puzzle was that the dipole moment of an infinite periodic charge density is ill-defined; the resolution (King-Smith and Vanderbilt, 1993) was to use the phases of the Bloch states, which is what the rest of this lecture computes. Q: \"Why is the absolute value not physical?\" A: Shifting the cell boundary by one lattice vector moves the 'charge per cell' by e·a — polarization is defined modulo a quantum."
    },
    "berry-cycle": {
      "level": "core", "layout": "fig-right", "fig": "s10-f1",
      "title": "The Rice–Mele cycle",
      "lead": "Add a staggered onsite energy <span class='math'>±Δ</span> to the SSH chain. In the plane of (dimerization, <span class='math'>Δ</span>) the gap closes only at the origin. A cycle that <strong>encircles</strong> it is a Thouless pump.",
      "bullets": [
        "Along the loop the chain is always gapped: an adiabatic process.",
        "Yet after one full cycle charge has moved by exactly one electron per cell.",
        "The loop is a path in parameter space, and the pumped charge is a winding number around the gapless point."
      ],
      "notes": "Draw the (v−w, Δ) plane and the four cardinal points of the loop: pure SSH trivial, staggered potential, SSH topological, opposite potential. The gapless point at the centre is the metal of lecture 2. Q: \"What if the loop does not enclose the origin?\" A: The pumped charge is zero; the two points on the loop with the same parameters are connected without winding — a good exercise to run in the notebook."
    },
    "berry-flow": {
      "level": "core", "layout": "fig", "fig": "s10-f2",
      "title": "The Wannier centre winds once per cycle",
      "lead": "Track the Wannier centre as the pump parameter <span class='math'>λ</span> advances: it flows continuously across one full unit cell and returns to its starting value mod <span class='math'>a</span>. That integer is the pumped charge.",
      "notes": "This figure is the Thouless pump: the vertical axis is the position of the charge in units of a, the horizontal axis the pump parameter. The net displacement over one period is quantized because at λ = 0 and λ = 2π the Hamiltonian is the same and the centre must return to itself modulo a lattice vector. Q: \"Can the number be 2?\" A: Yes, with a loop that winds twice, or for a model with a different geometry; the integer is a Chern number in the (k, λ) torus."
    },
    "berry-finite": {
      "level": "core", "layout": "fig-right", "fig": "s10-f3",
      "title": "The pump seen from the ends",
      "lead": "In a finite chain the pumped charge has to go somewhere: as <span class='math'>λ</span> advances, a bound state peels off the valence band at one end, crosses the gap and joins the conduction band — one state per cycle.",
      "bullets": [
        "The spectral flow of the end states is the bulk Chern number made visible in a finite system.",
        "Bulk–boundary correspondence again: an integer computed from the bulk eigenvectors counts a boundary process.",
        "The same picture, with <span class='math'>λ</span> replaced by a transverse momentum, is the chiral edge state of lecture 6."
      ],
      "notes": "Laughlin's argument in miniature: charge transported through the bulk appears as a level crossing the gap at the edge. Point to the direction of the flow at the two ends (opposite). Q: \"Does the pump work at any speed?\" A: No — adiabatic means slow compared with the gap; otherwise the electron can be excited across the gap and the quantization is lost."
    },
    "berry-math": {
      "level": "math", "layout": "eq",
      "title": "Berry phase, polarization, pumped charge",
      "eqs": [
        {"label": "Berry phase of a band", "math": "<span class='math'>φ = i ∮ dk ⟨u<sub>k</sub>| ∂<sub>k</sub> u<sub>k</sub>⟩  =  −<span class='fn'>Im</span> <span class='fn'>ln</span> Π<sub>j</sub> ⟨u<sub>k<sub>j</sub></sub>| u<sub>k<sub>j+1</sub></sub>⟩</span>"},
        {"label": "polarization", "math": "<span class='math'>P = e a φ / 2π   (<span class='fn'>mod</span> e a),   x̄ = a φ / 2π</span>"},
        {"label": "Thouless pump", "math": "<span class='math'>ΔQ = e ∮ dλ ∂<sub>λ</sub>(φ/2π) = e · C,   C = (1/2π) ∫∫ dk dλ Ω<sub>kλ</sub> ∈ ℤ</span>"}
      ],
      "bullets": [
        "The discrete formula (King-Smith–Vanderbilt) is gauge invariant: an arbitrary phase on each <span class='math'>u<sub>k<sub>j</sub></sub></span> cancels in the product of overlaps.",
        "<code>WFArray.berry_phase</code> implements exactly that product; <code>berry_flux</code> the plaquette version of <span class='math'>Ω</span>.",
        "The pump integer is the Chern number of the occupied band on the <span class='math'>(k, λ)</span> torus — the same object as in lecture 6 with <span class='math'>λ → k<sub>y</sub></span>."
      ],
      "notes": "Derive the discrete Berry phase: write the continuum expression as a limit of ⟨u_j|u_{j+1}⟩ ≈ 1 + ⟨u|∂u⟩ dk and take the log; show the gauge cancellation. Then state without proof the polarization theorem (P = e x̄ per cell) and check its two limits in the SSH chain: 0 and ½. Q: \"What does the closure ⟨u_N|u_1⟩ require?\" A: In the atomic gauge, u at k + 2π is u at k times a position-dependent phase; PythTB handles the closure so the user does not have to — but only if the mesh is periodic (Mesh with endpoint included)."
    },

    "chern-ingredients": {
      "level": "intro", "layout": "fig-right", "fig": "s14-f1",
      "title": "Haldane's trick: complex hoppings, no magnetic field",
      "lead": "Graphene plus <em>directed</em> second-neighbour hoppings <span class='math'>t<sub>2</sub> e<sup>iφ</sup></span>, arrows clockwise around each hexagon. The net flux through the cell is zero — yet time reversal is broken.",
      "bullets": [
        "A complex hopping is a phase an electron picks up on a bond; going round a triangle, it accumulates <span class='math'>3φ</span> — a local flux.",
        "Opposite triangles carry opposite flux: no net field, no Landau levels, still a quantum Hall effect.",
        "Plus a sublattice potential <span class='math'>M</span> to compete with it: two masses, one phase diagram."
      ],
      "notes": "Historical framing: in 1988 Haldane asked whether the quantum Hall effect needs a magnetic field or only broken time reversal, and answered with this model. It was realized experimentally in 2013 (magnetic topological insulator films) and 2014 (cold atoms). Q: \"Why does a complex hopping break time reversal?\" A: Time reversal complex-conjugates the Hamiltonian; e^{iφ} → e^{−iφ} reverses the arrows, so unless φ = 0 or π the model is not invariant."
    },
    "chern-curvature": {
      "level": "core", "layout": "fig-right", "fig": "s14-f2",
      "title": "Berry curvature: where the geometry lives",
      "lead": "The Berry curvature <span class='math'>Ω(k)</span> of the occupied band over the Brillouin zone. It is concentrated near <span class='math'>K</span> and <span class='math'>K'</span>, where the gap is smallest — and it integrates to <span class='math'>2π</span> times an integer.",
      "bullets": [
        "<span class='math'>Ω</span> is the 2D analogue of the Berry phase per unit area; PythTB's <code>berry_flux</code> computes it plaquette by plaquette.",
        "Both valleys contribute with the same sign in the topological phase, opposite signs in the trivial one.",
        "The integral is the <strong>Chern number</strong> <span class='math'>C</span>; the Hall conductance is <span class='math'>C e<sup>2</sup>/h</span>."
      ],
      "notes": "Connect to lecture 5: Ω is the curl of the Berry connection, and integrating it over a closed surface (the torus) gives an integer for the same reason a magnetic monopole's flux is quantized. The valley picture is the key to the phase diagram: each Dirac point contributes ±½ depending on the sign of its mass. Q: \"Why is Ω peaked where the gap is small?\" A: Curvature ∝ 1/gap²: near a would-be Dirac point the eigenvector rotates fastest with k."
    },
    "chern-phase": {
      "level": "core", "layout": "fig", "fig": "s14-f3",
      "title": "The Haldane phase diagram",
      "lead": "Chern number over the <span class='math'>(φ, M/t<sub>2</sub>)</span> plane, computed point by point, against the analytic boundary <span class='math'>M = ±3√3 t<sub>2</sub> <span class='fn'>sin</span> φ</span>. Inside the lobes <span class='math'>C = ±1</span>; outside, <span class='math'>C = 0</span>.",
      "notes": "Every point of this figure is a full Berry-flux calculation — a good place to talk about cost (a mesh per point) and about the robustness of an integer-valued quantity: the numerics never return 0.7. The boundary is where the gap closes at K or K'. Q: \"What happens exactly on the boundary?\" A: The gap closes at one valley, C is undefined, and the system is a semimetal with a single Dirac cone — half of graphene."
    },
    "chern-ribbon": {
      "level": "core", "layout": "fig-right", "fig": "s14-f4",
      "title": "One chiral edge mode per edge",
      "lead": "Cut a ribbon in the <span class='math'>C = 1</span> phase and colour the bands by edge weight: a single state crosses the gap on each edge, moving in opposite directions on opposite edges.",
      "bullets": [
        "<em>Chiral</em>: one direction only. There is no state to backscatter into — the edge conducts without dissipation.",
        "The number of crossings (net, with sign) equals <span class='math'>C</span>: bulk–boundary correspondence in 2D.",
        "This is the quantum anomalous Hall effect: quantized <span class='math'>σ<sub>xy</sub></span> with no external field."
      ],
      "notes": "Compare with the zigzag graphene edge band of lecture 3 (flat, not chiral, not protected by topology) and with the pump's end-state flow of lecture 5 (same picture with λ → k along the edge). Q: \"What if the ribbon is narrow?\" A: The two edge modes hybridize with an amplitude exponentially small in width, opening a tiny gap; the crossing is exact only in the thermodynamic limit."
    },
    "chern-marker": {
      "level": "core", "layout": "fig-right", "fig": "s14-f5",
      "title": "Topology without k-space: the local Chern marker",
      "lead": "The Bianco–Resta marker evaluates <span class='math'>C</span> at each site of a finite flake from the projector onto occupied states and the position operators. In the bulk it reads the Chern number; at the edges it reverses sign so the total is zero.",
      "bullets": [
        "Needs no periodicity: works for disordered, amorphous or finite samples.",
        "Costs a full diagonalization of the flake — dense, <span class='math'>O(N<sup>3</sup>)</span>.",
        "PythTB gives the eigenvectors; the marker is twenty lines of numpy on top (in the notebook)."
      ],
      "notes": "This slide closes the loop between k-space and real space: the same integer, two computations. Mention that the sum over a finite sample must vanish (the marker is a commutator's trace), which is why the edge carries the opposite sign. Q: \"How large must the flake be?\" A: Bulk sites must be further from the edge than the localization length ∼ v_F/gap; a few dozen cells is enough for the Haldane model at typical parameters."
    },
    "chern-math": {
      "level": "math", "layout": "eq",
      "title": "Chern number and the Haldane masses",
      "eqs": [
        {"label": "curvature and Chern number", "math": "<span class='math'>Ω = ∂<sub>k<sub>x</sub></sub>A<sub>y</sub> − ∂<sub>k<sub>y</sub></sub>A<sub>x</sub>,  A = i⟨u|∇<sub>k</sub>u⟩,   C = (1/2π) ∫<sub>BZ</sub> Ω d<sup>2</sup>k ∈ ℤ</span>"},
        {"label": "lattice (Fukui–Hatsugai–Suzuki)", "math": "<span class='math'>C = (1/2π) Σ<sub>plaquettes</sub> <span class='fn'>Im</span> <span class='fn'>ln</span> ( U<sub>12</sub> U<sub>23</sub> U<sub>34</sub> U<sub>41</sub> ),   U<sub>ij</sub> = ⟨u<sub>i</sub>|u<sub>j</sub>⟩/|⟨u<sub>i</sub>|u<sub>j</sub>⟩|</span>"},
        {"label": "Haldane masses", "math": "<span class='math'>m<sub>K</sub> = M − 3√3 t<sub>2</sub> <span class='fn'>sin</span> φ,  m<sub>K'</sub> = M + 3√3 t<sub>2</sub> <span class='fn'>sin</span> φ,   C = ½[<span class='fn'>sgn</span>(m<sub>K'</sub>) − <span class='fn'>sgn</span>(m<sub>K</sub>)]</span>"}
      ],
      "bullets": [
        "Each gapped Dirac cone contributes <span class='math'>±½</span> to <span class='math'>C</span>, the sign being that of its mass; the total is an integer because the cones come in pairs.",
        "The plaquette formula is gauge invariant and exactly integer on any mesh — PythTB's <code>berry_flux</code> is this product.",
        "<span class='math'>σ<sub>xy</sub> = C e<sup>2</sup>/h</span> (TKNN): a transport coefficient equal to a topological integer."
      ],
      "notes": "Sketch the mass calculation: expand the Haldane Hamiltonian at K and K'. The sublattice term gives +M at both valleys, the t₂ term gives a σ_z coefficient −3√3 t₂ sin φ at K and +3√3 t₂ sin φ at K' (opposite because the second-neighbour phases wind oppositely at the two valleys). A massive 2D Dirac cone contributes sgn(m)/2 to C. Q: \"Why is the sum of two half-integers an integer here but not for a single cone?\" A: A lattice always has an even number of Dirac cones (fermion doubling); a single cone exists only on the surface of a 3D topological insulator."
    },

    "z2-inversion": {
      "level": "intro", "layout": "fig-right", "fig": "s16-f1",
      "title": "Band inversion: the switch",
      "lead": "In a HgTe quantum well the ordering of the <span class='math'>s</span>-like and <span class='math'>p</span>-like bands at <span class='math'>Γ</span> flips with the well thickness. Colour the BHZ bands by orbital character: for <span class='math'>M &gt; 0</span> the characters are swapped near <span class='math'>Γ</span> — the <strong>inverted</strong> regime.",
      "bullets": [
        "Inversion is a property of eigenvectors, invisible in the energies alone.",
        "It is the two-dimensional, time-reversal-symmetric cousin of the Haldane mass changing sign.",
        "Predicted 2006 (Bernevig, Hughes, Zhang), measured 2007 (König et al.): the quantum spin Hall effect."
      ],
      "notes": "Give the experimental story: quantized two-terminal conductance 2e²/h in HgTe wells thicker than 6.3 nm, independent of width — edge conduction. Then state what this lecture adds to lecture 6: time reversal is present, so the Chern number must vanish, and a new Z₂ invariant takes over. Q: \"Why does thickness invert the bands?\" A: Quantum confinement pushes the s-like level up and the p-like level down as the well gets thinner; below a critical thickness their order is the normal one."
    },
    "z2-flow": {
      "level": "core", "layout": "two-figs", "fig": "s15-f1", "fig2": "s16-f2",
      "title": "The Z₂ invariant from Wannier flow",
      "lead": "Hybrid Wannier centres <span class='math'>x̄(k<sub>y</sub>)</span> over half the zone, for Kane–Mele (left) and BHZ (right). In the topological phase the two centres <strong>switch partners</strong>: any horizontal line crosses them an odd number of times.",
      "bullets": [
        "Time reversal pairs the centres at <span class='math'>k<sub>y</sub> = 0</span> and <span class='math'>π</span>; in between they may swap. Z₂ counts whether they do (mod 2).",
        "PythTB: <code>WFArray.berry_phase(..., berry_evals=True)</code> along <span class='math'>k<sub>x</sub></span> for each <span class='math'>k<sub>y</sub></span>.",
        "The Wannier flow is the pump of lecture 5 with <span class='math'>k<sub>y</sub></span> as the pump parameter, restricted by time reversal to half a period."
      ],
      "notes": "This is the Soluyanov–Vanderbilt / Yu et al. method and the most reliable way to compute Z₂ without inversion symmetry. Walk through the crossing count on both figures. Note that the Chern number would be the net winding over the full zone, which vanishes here because the two centres wind oppositely — the Z₂ index is what survives. Q: \"Why only half the zone?\" A: Time reversal maps k_y → −k_y; the second half is the mirror image and contains no new information."
    },
    "z2-edges": {
      "level": "core", "layout": "two-figs", "fig": "s15-f2", "fig2": "s16-f3",
      "title": "Helical edge states: a Kramers pair per edge",
      "lead": "Ribbons in the topological phase carry, on each edge, <em>two</em> counter-propagating states with opposite spin (left, Kane–Mele). BHZ ribbons (right): edge states only in the inverted regime.",
      "bullets": [
        "Helical, not chiral: both directions exist on the same edge, but tied to opposite spins.",
        "Backscattering needs a spin flip, which time-reversal-invariant disorder cannot provide: the crossing is protected.",
        "Two edge pairs (Z₂ = 0) can gap each other; one pair (Z₂ = 1) cannot — that is why the invariant is mod 2."
      ],
      "notes": "Return to spin–momentum locking from lecture 4 for the protection argument, and to the Kramers theorem for why the crossing at the time-reversal-invariant momentum cannot be avoided. Q: \"What breaks the protection?\" A: A magnetic impurity (breaks time reversal) or inelastic spin-flip scattering; in experiments the quantization degrades above a few microns for exactly these reasons."
    },
    "z2-math": {
      "level": "math", "layout": "eq",
      "title": "Kane–Mele, Kramers, and the two ways to Z₂",
      "eqs": [
        {"label": "Kane–Mele", "math": "<span class='math'>H = t Σ<sub>⟨ij⟩</sub> c<sup>†</sup><sub>i</sub>c<sub>j</sub> + i λ<sub>SO</sub> Σ<sub>⟨⟨ij⟩⟩</sub> ν<sub>ij</sub> c<sup>†</sup><sub>i</sub> s<sub>z</sub> c<sub>j</sub> + λ<sub>v</sub> Σ<sub>i</sub> ξ<sub>i</sub> c<sup>†</sup><sub>i</sub>c<sub>i</sub></span>"},
        {"label": "time reversal", "math": "<span class='math'>Θ = i s<sub>y</sub> K,  Θ<sup>2</sup> = −1  ⇒  Kramers: E<sub>n</sub>(k) = E<sub>n'</sub>(−k), degenerate at TRIM</span>"},
        {"label": "Z₂", "math": "<span class='math'>ν = ( # crossings of x̄<sub>n</sub>(k<sub>y</sub>) with any line, k<sub>y</sub> ∈ [0, π] ) <span class='fn'>mod</span> 2   =   Π<sub>i=1</sub><sup>4</sup> δ<sub>i</sub>,  δ<sub>i</sub> = Π<sub>n occ</sub> ξ<sub>2n</sub>(Γ<sub>i</sub>)  (with inversion)</span>"}
      ],
      "bullets": [
        "Kane–Mele = two copies of Haldane with opposite <span class='math'>φ</span> for spin up and down (<span class='math'>s<sub>z</sub></span> conserved): <span class='math'>C<sub>↑</sub> = −C<sub>↓</sub> = 1</span>, <span class='math'>C = 0</span>, <span class='math'>ν = 1</span>.",
        "Rashba coupling breaks <span class='math'>s<sub>z</sub></span> conservation; the spin Chern numbers lose meaning but <span class='math'>ν</span> survives — that is its point.",
        "With inversion symmetry, Fu–Kane's parity product at the four TRIM gives <span class='math'>ν</span> from four numbers; without it, use the Wannier flow."
      ],
      "notes": "Present the Kane–Mele Hamiltonian term by term: ν_ij = ±1 for clockwise/anticlockwise second-neighbour paths (the Haldane phase at φ = π/2), s_z making the two spins see opposite fluxes, λ_v the sublattice mass. Show that at Rashba = 0 the model decouples into two Haldane models with C = ±1; then argue that the Z₂ classification (two phases) is all that remains when the decoupling is broken. Q: \"Where does 'mod 2' come from?\" A: Two Kramers pairs of edge states can be gapped by a time-reversal-symmetric coupling; only the parity of their number is protected."
    },

    "beyond-map": {
      "level": "intro", "layout": "table",
      "title": "Four more kinds of topological matter",
      "lead": "The same machinery — a lattice model, its eigenvectors, a Berry-phase quantity — classifies far more than Chern and Z₂ insulators. This lecture is a tour; each stop is a full notebook section.",
      "table": {
        "head": ["Model", "What is new", "Invariant", "Boundary signature"],
        "rows": [
          ["BBH quadrupole (§17)", "topology of the Wannier bands themselves", "nested Wilson loop, <span class='math'>q<sub>xy</sub> = ½</span>", "four corner states at zero energy"],
          ["Kitaev chain (§18)", "superconductivity as extra (hole) orbitals", "Pfaffian / winding, <span class='math'>|μ| &lt; 2t</span>", "one Majorana per end"],
          ["Weyl semimetal (§19)", "gapless but topological: monopoles in 3D", "sliced Chern number <span class='math'>C(k<sub>z</sub>)</span>", "Fermi arcs on the surface"],
          ["Fu–Kane–Mele + axion (§20)", "3D strong TI; magnetoelectric angle", "<span class='math'>θ ∈ {0, π}</span>, second Chern number", "half-quantized surface Hall effect"]
        ]
      },
      "notes": "A map slide: name the four systems, their notebook sections, and the single idea each introduces. Choose depth according to time — each core slide stands alone. Q: \"Are these all realized experimentally?\" A: Weyl semimetals (TaAs, 2015) and 3D TIs (Bi₂Se₃, 2009) unambiguously; quadrupole insulators in metamaterials and photonics; Majorana modes in nanowires remain debated."
    },
    "beyond-bbh-model": {
      "level": "core", "layout": "two-figs", "fig": "s17-f1", "fig2": "s17-f2",
      "title": "The BBH model: two SSH chains crossed",
      "lead": "Four orbitals per square cell, intracell bonds <span class='math'>γ</span> and intercell bonds <span class='math'>λ</span>, with one negative bond per plaquette — a π flux (left). The bulk bands come in two doubly-degenerate pairs with a full gap (right).",
      "bullets": [
        "SSH logic in both directions at once: <span class='math'>λ &gt; γ</span> is the candidate topological phase.",
        "The π flux per plaquette is essential: it keeps the bands degenerate and the Wannier bands gapped.",
        "Nothing in these bulk bands betrays the topology — the dipole moment vanishes by symmetry in every direction."
      ],
      "notes": "Build the model on the board as two interleaved SSH patterns; the dashed negative bond implements the π flux (product of signs around each plaquette = −1). Emphasize the negative result on purpose: bulk bands and even bulk polarization look completely trivial, which is why a new diagnostic (the nested Wilson loop, next slide) is needed. Q: \"Why the π flux?\" A: Without it the four bands are not doubly degenerate, the Wannier bands touch, and the quadrupole is not quantized — the flux enforces the anticommuting mirror symmetries that protect q_xy."
    },

    "beyond-bbh": {
      "level": "core", "layout": "two-figs", "fig": "s17-f3", "fig2": "s17-f4",
      "title": "Higher-order topology: the quadrupole insulator",
      "lead": "The Benalcazar–Bernevig–Hughes model has a gapped bulk, gapped edges, and <strong>four zero modes on the corners</strong> (left). The invariant lives one level down: the Wilson-loop eigenphases form <em>Wannier bands</em>, gapped and pinned at <span class='math'>±¼</span> by symmetry (right).",
      "bullets": [
        "Four orbitals per cell, intracell <span class='math'>γ</span> and intercell <span class='math'>λ</span> bonds, one negative sign per plaquette (a π flux): SSH in two directions at once.",
        "Corner charge <span class='math'>±e/2</span>, quadrupole moment <span class='math'>q<sub>xy</sub> = ½</span>: the boundary of the boundary carries the charge.",
        "Built by hand in the notebook from <code>berry_phase(berry_evals=True)</code> — a nested Wilson loop is a Wilson loop of a Wilson loop."
      ],
      "notes": "Present this as SSH squared: the topological phase is λ > γ in both directions, and the four corners are the four ends of two crossed chains. The nested Wilson loop is the Berry phase of the Wannier bands — the same computation applied to the output of itself. Q: \"Why is the corner charge protected?\" A: By the mirror symmetries that pin the Wannier bands at ±¼; break them and the corner charge can flow away."
    },
    "beyond-kitaev-model": {
      "level": "core", "layout": "two-figs", "fig": "s18-f1", "fig2": "s18-f2",
      "title": "Writing pairing as hopping: the BdG trick",
      "lead": "The physical chain has hopping <span class='math'>t</span> and p-wave pairing <span class='math'>Δ</span> that creates and destroys electron <em>pairs</em> (left, top) — not a hopping at all. Double the orbitals into a particle and a hole copy and it becomes one (left, bottom); the resulting BdG bands match the analytic dispersion exactly (right).",
      "bullets": [
        "PythTB never learns about superconductivity: it sees an ordinary two-orbital tight-binding model.",
        "The price of the trick: every state appears twice, at <span class='math'>E</span> and <span class='math'>−E</span>; only half the spectrum is physical.",
        "The gap closes at <span class='math'>k = 0</span> when <span class='math'>μ = −2t</span> and at <span class='math'>k = π</span> when <span class='math'>μ = +2t</span> — the boundaries of the topological phase."
      ],
      "notes": "Spell the mapping out once: c†c† terms connect the particle sector to the hole sector, so in the doubled basis they look like hoppings between the two copies; hermiticity of the original pairing becomes the particle–hole structure of the doubled matrix. The dashed analytic curve is E(k) = ±sqrt((2t cos k + μ)² + 4Δ² sin²k). Q: \"Is the doubling physical?\" A: No — it is bookkeeping. The physical Hilbert space has half the states; the E and −E eigenvectors describe the same quasiparticle, which is exactly why an E = 0 state can be its own partner (next slide)."
    },

    "beyond-kitaev": {
      "level": "core", "layout": "two-figs", "fig": "s18-f3", "fig2": "s18-f4",
      "title": "Superconductivity smuggled in: the Kitaev chain",
      "lead": "PythTB knows nothing about pairing. Double the orbitals — particles and holes — and write the Bogoliubov–de Gennes matrix as hoppings. Majorana end modes appear exactly for <span class='math'>|μ| &lt; 2t</span> (left), one per end (right).",
      "bullets": [
        "The BdG spectrum is symmetric by construction (particle–hole); a state at <span class='math'>E = 0</span> is its own antiparticle: a Majorana.",
        "Two Majoranas at opposite ends make one ordinary fermion that costs no energy to occupy: a two-fold degenerate ground state, the qubit.",
        "The trap: PythTB does not enforce particle–hole symmetry. Get the hole block wrong and the code runs happily — lecture 10."
      ],
      "notes": "Explain the doubling honestly: the BdG Hamiltonian is a trick to write a quadratic pairing term as a hopping between a particle and a hole orbital; the price is that every state appears twice (E and −E) and only half are physical. The E = 0 states are exceptional — their particle and hole parts coincide. Q: \"Is this the Majorana nanowire?\" A: In spirit: the Rashba–Zeeman wire of lecture 4 proximitized by a superconductor maps onto the Kitaev chain inside its helical gap."
    },
    "beyond-weyl-geo": {
      "level": "core", "layout": "two-figs", "fig": "s19-f1", "fig2": "s19-f2",
      "title": "Weyl semimetals: monopoles in the Brillouin zone",
      "lead": "Two bands touch at isolated points in a 3D zone (left): each node is a <strong>monopole of Berry curvature</strong>, with flux <span class='math'>±2π</span> through any surface around it, and nodes come in pairs of opposite charge. The direct gap along the <span class='math'>k<sub>z</sub></span> axis (right) collapses linearly at <span class='math'>k<sub>z</sub> = ±¼</span> and nowhere else.",
      "bullets": [
        "Gapless by topology, not by fine tuning: a point crossing in 3D cannot be removed by small perturbations (three parameters, three constraints).",
        "The minimal model breaks time reversal <em>or</em> inversion; here a two-orbital model with the nodes at <span class='math'>k<sub>z</sub> = ±¼</span>.",
        "A monopole pair is the 3D image of the Haldane phase transition, stretched along <span class='math'>k<sub>z</sub></span>."
      ],
      "notes": "Compare with graphene's Dirac point (2D): there a mass term gaps it; in 3D the three Pauli matrices are all used up by the momentum and no mass term exists — the node is stable. Q: \"Why must they come in pairs?\" A: The total Berry flux out of the whole Brillouin zone (a torus, closed) must vanish, so monopole charges sum to zero: the Nielsen–Ninomiya theorem."
    },
    "beyond-weyl": {
      "level": "core", "layout": "two-figs", "fig": "s19-f3", "fig2": "s19-f4",
      "title": "Sliced Chern numbers and Fermi arcs",
      "lead": "Fix <span class='math'>k<sub>z</sub></span> and you have a 2D insulator with a Chern number; <span class='math'>C(k<sub>z</sub>)</span> jumps by one at each node (left). Every slice with <span class='math'>C = 1</span> has a chiral edge state — stacked along <span class='math'>k<sub>z</sub></span>, they form a <strong>Fermi arc</strong> on the surface connecting the node projections (right).",
      "bullets": [
        "A Weyl semimetal is a Chern-number domain wall in momentum space.",
        "The arc is an open Fermi surface — impossible for any purely 2D system, the fingerprint seen in ARPES on TaAs.",
        "PythTB: a 2D model with <span class='math'>k<sub>z</sub></span> as a symbolic parameter, <code>berry_flux</code> per slice, then <code>cut_piece</code> for the slab."
      ],
      "notes": "Dimensional reduction is the through-line of the course: the ribbon from the 2D model (lecture 3), the pump from the parameter (lecture 5), now a family of 2D models from a 3D one. Q: \"Where does the arc end?\" A: At the surface projections of the two nodes, where the sliced Chern number changes and the edge state must disappear into the bulk."
    },
    "beyond-axion": {
      "level": "core", "layout": "two-figs", "fig": "s20-f1", "fig2": "s20-f2",
      "title": "The axion angle θ",
      "lead": "The Fu–Kane–Mele model on the diamond lattice at the time-reversal-symmetric point <span class='math'>β = π</span>: gapped bulk bands of a strong topological insulator (left). Driving <span class='math'>β</span> through a full adiabatic cycle winds the magnetoelectric angle <span class='math'>θ</span> by <span class='math'>2π</span> (right): a <strong>second Chern number</strong> equal to one.",
      "bullets": [
        "<span class='math'>θ</span> is the 3D analogue of the polarization Berry phase: an angle, defined mod <span class='math'>2π</span>, quantized to <span class='math'>0</span> or <span class='math'>π</span> by time reversal or inversion.",
        "<span class='math'>θ = π</span> is the strong topological insulator; the surface carries a half-quantized Hall conductance <span class='math'>e<sup>2</sup>/2h</span>.",
        "Computed here from the non-Abelian Berry connection on a 3D mesh — PythTB's <code>WFArray</code> in its most demanding use."
      ],
      "notes": "Position θ as the top of the hierarchy: Berry phase (1D) → Chern number (2D) → axion angle (3D) → second Chern number (4D, here parameter + 3D). The winding of θ over a cycle is the 4D analogue of the Thouless pump. Q: \"Is θ measurable?\" A: Yes — as a quantized Faraday/Kerr rotation and as the half-integer surface Hall effect in magnetically doped TI films (2017 onward)."
    },
    "beyond-math": {
      "level": "math", "layout": "eq",
      "title": "BdG, Weyl, axion: the formulas",
      "eqs": [
        {"label": "Kitaev BdG", "math": "<span class='math'>H = ½ Σ<sub>k</sub> Ψ<sup>†</sup><sub>k</sub> H<sub>BdG</sub>(k) Ψ<sub>k</sub>,   E(k) = ± √( (2t <span class='fn'>cos</span> k + μ)<sup>2</sup> + 4Δ<sup>2</sup> <span class='fn'>sin</span><sup>2</sup> k ),   topological for |μ| &lt; 2t</span>"},
        {"label": "Weyl node", "math": "<span class='math'>H(k<sub>0</sub> + q) = χ ħ v q·σ,   ∮<sub>S<sup>2</sup></sub> Ω·dS = 2π χ,  χ = ±1</span>"},
        {"label": "axion angle", "math": "<span class='math'>θ = −(1/4π) ∫<sub>BZ</sub> d<sup>3</sup>k ε<sup>abc</sup> <span class='fn'>Tr</span>[ A<sub>a</sub>∂<sub>b</sub>A<sub>c</sub> − (2i/3) A<sub>a</sub>A<sub>b</sub>A<sub>c</sub> ],   Δθ over a cycle = 2π C<sub>2</sub></span>"}
      ],
      "bullets": [
        "Particle–hole symmetry <span class='math'>Ξ H<sub>BdG</sub>(k) Ξ<sup>−1</sup> = −H<sub>BdG</sub>(−k)</span>: the hole block must be <span class='math'>−H*(−k)</span>. PythTB cannot check it for you.",
        "Chirality <span class='math'>χ = <span class='fn'>sgn</span> <span class='fn'>det</span>(∂H/∂k)</span> at the node; <span class='math'>C(k<sub>z</sub>)</span> changes by <span class='math'>χ</span> across it.",
        "<span class='math'>A</span> is the non-Abelian Berry connection of all occupied bands; only differences and the mod-<span class='math'>2π</span> value of <span class='math'>θ</span> are gauge invariant."
      ],
      "notes": "Derive the Kitaev dispersion from the 2×2 BdG matrix (ξ_k σ_z + 2Δ sin k σ_y with ξ_k = −2t cos k − μ); the gap closes at k = 0 or π when |μ| = 2t, which bounds the topological phase. For Weyl, show the monopole flux by mapping the node Hamiltonian onto a spin in a field q — the Berry curvature of a spin-½ is that of a monopole of charge ½ at the origin, giving 2π flux over the sphere. State the axion formula and check its dimensions; emphasize numerical subtleties (gauge smoothness, mesh convergence) rather than deriving. Q: \"Why is C₂ an integer?\" A: It is the second Chern number of the occupied bundle over the 4-torus (k, β); the same Gauss–Bonnet-type argument that quantizes C."
    },

    "stretch-peierls": {
      "level": "intro", "layout": "fig-right", "fig": "s21-f1",
      "title": "A magnetic field as phases on bonds",
      "lead": "PythTB has no magnetic field. It does have complex hoppings. The <strong>Peierls substitution</strong> turns a uniform field into a phase on every bond — in Landau gauge, hops along <span class='math'>x</span> stay real and hops along <span class='math'>y</span> pick up <span class='math'>e<sup>2πi φ x</sup></span>.",
      "bullets": [
        "<span class='math'>φ</span> = flux per plaquette in units of the flux quantum <span class='math'>h/e</span>.",
        "Going round one plaquette accumulates <span class='math'>2πφ</span>: the Aharonov–Bohm phase, gauge independent.",
        "For rational <span class='math'>φ = p/q</span> the phases repeat after <span class='math'>q</span> cells: a magnetic unit cell of <span class='math'>q</span> sites."
      ],
      "notes": "The Haldane model already used complex hoppings for local fluxes; here the flux is uniform and the price is a supercell that grows with the denominator q. Emphasize gauge freedom: the individual phases are unphysical, the plaquette products are not. Q: \"What about irrational flux?\" A: No finite magnetic cell exists; the spectrum is a Cantor set — exactly what the butterfly shows in the limit of large q."
    },
    "stretch-butterfly": {
      "level": "core", "layout": "fig", "fig": "s21-f2",
      "title": "The Hofstadter butterfly",
      "lead": "Every eigenvalue of the square lattice at every rational flux <span class='math'>p/q</span> with <span class='math'>q ≤ 32</span>, from <code>set_hop</code> and nothing else. Nested gaps at every scale; each gap carries a Chern number.",
      "notes": "Read the figure: at small flux the Landau-level fan emerges from the band edges (E ≈ ±4t + ħω_c(n + ½)); at φ = ½ the spectrum is symmetric with a Dirac point; the gaps nest inside gaps without end (a Cantor-set spectrum). The Chern numbers of the gaps satisfy a Diophantine equation (TKNN 1982 was written about this figure). Q: \"Has this been observed?\" A: Yes — in graphene on hexagonal boron nitride moiré superlattices (2013), where the large moiré cell makes one flux quantum reachable with laboratory fields."
    },
    "stretch-disorder": {
      "level": "core", "layout": "two-figs", "fig": "s22-f1", "fig2": "s22-f2",
      "title": "Anderson localization, one eigenvector at a time",
      "lead": "Random onsite energies on a 30×30 supercell. The inverse participation ratio of every eigenstate (left) separates extended from localized states; one band-centre state at weak versus strong disorder (right) shows what localization looks like.",
      "bullets": [
        "<span class='math'>IPR = Σ<sub>i</sub>|ψ<sub>i</sub>|<sup>4</sup></span>: <span class='math'>∼ 1/N</span> for an extended state, <span class='math'>∼ 1/ξ<sup>2</sup></span> for one localized on <span class='math'>ξ<sup>2</sup></span> sites.",
        "Band edges localize first; in 2D, in the thermodynamic limit, everything localizes — but the length can exceed the sample.",
        "No k-space: disorder is a supercell with one <code>set_onsite</code> per site, and a full dense diagonalization."
      ],
      "notes": "This is the notebook's demonstration that PythTB can do real-space physics as long as the matrix fits in memory. Stress the finite-size caveat: a localization length longer than 30 sites looks extended. Q: \"Why does 2D always localize?\" A: Scaling theory (1979): the conductance's logarithmic derivative is negative for d ≤ 2 without spin–orbit coupling, so any disorder eventually wins; with spin–orbit coupling (symplectic class) a metallic phase survives — an exercise in the notebook's spirit."
    },
    "stretch-penrose": {
      "level": "core", "layout": "fig-right", "fig": "s23-f1",
      "title": "A Penrose quasicrystal: order without periodicity",
      "lead": "De Bruijn's pentagrid generates a Penrose rhombus tiling; each vertex becomes a site, each rhombus edge a bond. Five-fold symmetry, no unit cell — a <code>dim_k = 0</code> model with a few thousand orbitals.",
      "bullets": [
        "Quasicrystals are ordered (sharp diffraction peaks) but not periodic: Bloch's theorem does not apply.",
        "PythTB treats it as one big finite molecule: geometry in, Hamiltonian out.",
        "The tiling is bipartite: the spectrum is symmetric about <span class='math'>E = 0</span>."
      ],
      "notes": "Historical hook: Shechtman's 1982 ten-fold diffraction pattern, Nobel prize 2011. Explain the pentagrid in a sentence (five families of parallel lines; each intersection is a rhombus) and move on to the spectrum. Q: \"Does k-space exist at all here?\" A: Not in the Bloch sense; there is a 5D periodic lattice of which the tiling is a slice, and that is how the diffraction peaks are indexed."
    },
    "stretch-penrose-spectrum": {
      "level": "core", "layout": "two-figs", "fig": "s23-f2", "fig2": "s23-f3",
      "title": "Spiky spectrum and confined states",
      "lead": "The density of states is spiky, riddled with gaps, with a δ-peak at <span class='math'>E = 0</span> that holds a finite fraction of all states (left). One such state (right) is strictly zero outside a few vertices: a <strong>confined state</strong>.",
      "bullets": [
        "Confined states are the Lieb-lattice localized states of lecture 3 returning in a non-periodic setting: local geometry, not translation symmetry, produces them.",
        "Their fraction is exactly computable (Kohmoto–Sutherland): a macroscopic degeneracy in a system with no symmetry to explain it.",
        "The remaining states are <em>critical</em>: neither extended nor localized, with power-law scaling at every length."
      ],
      "notes": "Show how the δ-peak is extracted: the integrated DOS has a plateau jump at E = 0 whose height is the confined-state fraction. Q: \"Why bipartite?\" A: Rhombus edges always join a vertex of one parity to the other in the pentagrid construction; bipartite hopping models have E ↔ −E symmetry, and their zero modes are counted by the sublattice imbalance of local clusters."
    },
    "stretch-wall": {
      "level": "core", "layout": "fig-right", "fig": "s24-f1",
      "title": "The performance wall",
      "lead": "Wall time of a full dense diagonalization versus matrix size, log-log. The slope is 3: <span class='math'>O(N<sup>3</sup>)</span>. PythTB has no sparse path — every <code>solve_*</code> call pays this.",
      "bullets": [
        "10<sup>3</sup> orbitals: fractions of a second. 10<sup>4</sup>: minutes and gigabytes. 10<sup>5</sup>: not with this tool.",
        "For large systems you want <em>a few</em> eigenvalues near a target (Lanczos, shift-invert) or none at all (kernel polynomial method).",
        "Those live in Kwant, scipy.sparse.linalg, and the KPM libraries — lecture 10."
      ],
      "notes": "Make the numbers concrete for the students' own laptops: a 5000×5000 complex Hermitian eigh takes about a minute and 400 MB; the next doubling is eight times slower. This is not a PythTB flaw but a design choice: dense LAPACK, always all eigenvalues. Q: \"Can I at least get only the eigenvalues?\" A: Yes (eig_vectors=False saves a factor ~3) but the scaling is unchanged."
    },
    "stretch-math": {
      "level": "math", "layout": "eq",
      "title": "Peierls phases, IPR, and the cost of dense algebra",
      "eqs": [
        {"label": "Peierls substitution", "math": "<span class='math'>t<sub>ij</sub> → t<sub>ij</sub> <span class='fn'>exp</span>( i (e/ħ) ∫<sub>r<sub>i</sub></sub><sup>r<sub>j</sub></sup> A·dl ),   Landau gauge A = (0, Bx, 0):  t<sub>y</sub>(x) = t e<sup> 2πi φ x/a</sup>,  φ = Ba<sup>2</sup>e/h</span>"},
        {"label": "Harper equation (φ = p/q)", "math": "<span class='math'>ψ<sub>x+1</sub> + ψ<sub>x−1</sub> + 2 <span class='fn'>cos</span>( 2π φ x + k<sub>y</sub> ) ψ<sub>x</sub> = (E/t) ψ<sub>x</sub>,   x = 1 … q</span>"},
        {"label": "inverse participation ratio", "math": "<span class='math'>IPR(ψ) = Σ<sub>i</sub> |ψ<sub>i</sub>|<sup>4</sup> / ( Σ<sub>i</sub> |ψ<sub>i</sub>|<sup>2</sup> )<sup>2</sup>  ∼  N<sup>−1</sup> (extended),  ξ<sup>−d</sup> (localized)</span>"}
      ],
      "bullets": [
        "The Harper equation is a <span class='math'>q×q</span> Bloch Hamiltonian for each <span class='math'>(k<sub>x</sub>, k<sub>y</sub>)</span>: the magnetic supercell in PythTB is exactly this matrix.",
        "Dense Hermitian diagonalization: <span class='math'>≈ (4/3 + 2) N<sup>3</sup></span> complex flops for values and vectors; memory <span class='math'>16N<sup>2</sup></span> bytes.",
        "Sparse alternatives cost <span class='math'>O(N)</span> per matrix–vector product; the number of products, not <span class='math'>N</span>, sets the time."
      ],
      "notes": "Derive the Landau-gauge phases from the line integral along a y-bond at position x, and show that the product of the four phases around a plaquette is e^{2πiφ} regardless of gauge. Reduce the 2D problem to the Harper equation by Fourier transforming along y. For the IPR, verify the two limits with a plane wave and a delta function. Q: \"Why can't PythTB just call a sparse solver?\" A: Its data model is a dense array of hoppings and its API promises every eigenvalue; a sparse path would be a different library — which is the subject of the last lecture."
    },

    "limits-list": {
      "level": "intro", "layout": "text",
      "title": "Five things PythTB cannot do",
      "lead": "Knowing a tool's edge is part of knowing the tool. Each of these is a notebook section with a worked demonstration of the limit — and a pointer to what to use instead.",
      "bullets": [
        "<strong>No transport</strong>: no leads, no scattering matrix, no conductance. → Kwant (§25).",
        "<strong>No sparse solvers, no KPM</strong>: every call is dense and <span class='math'>O(N<sup>3</sup>)</span>. → Kwant, scipy.sparse, KPM codes (§26).",
        "<strong>No continuum models</strong>: no <span class='math'>k·p</span> discretizer, no symbolic input. → Kwant's <code>continuum</code> (§27).",
        "<strong>No symmetry rails</strong>: a wrong BdG block runs without complaint (§28).",
        "<strong>No interactions</strong>: unless you write the self-consistent loop yourself (§29)."
      ],
      "notes": "This is a lecture about scientific honesty as much as about software. PythTB's scope is deliberate — a teaching and prototyping library whose entire API fits on one page — and the students should leave able to say which tool a given problem needs. Q: \"Why not just use Kwant for everything?\" A: Kwant has no Berry-phase machinery, no Wannier tools, and a heavier learning curve; the two are complementary, and the notebook's companion Kwant notebook does the transport half."
    },
    "limits-bdg": {
      "level": "core", "layout": "fig-right", "fig": "s28-f1",
      "title": "Silent wrongness",
      "lead": "A 'BdG Hamiltonian' whose hole block was deliberately corrupted. PythTB builds it, solves it, plots it — and the spectrum is no longer particle–hole symmetric. No error, no warning.",
      "bullets": [
        "PythTB checks hermiticity and nothing else; every other symmetry is the user's responsibility.",
        "The cure is a test: assert <span class='math'>E ↔ −E</span> symmetry on the spectrum, or check <span class='math'>Ξ H Ξ<sup>−1</sup> = −H</span> directly, every time you build a BdG model.",
        "The notebook's inline checks (<code>check(...)</code>) are this habit applied to every section."
      ],
      "notes": "Show the corrupted spectrum and let the class spot the asymmetry, then show what the correct one looks like (lecture 8). The larger lesson: a code that accepts any Hermitian matrix will accept a physically inconsistent one, and the only defence is a check written by the person who knows the physics. Q: \"Would Kwant catch this?\" A: Partly — its symmetry-aware builders and conservation laws can enforce particle–hole structure when told to; nothing catches a wrong model that is internally consistent."
    },
    "limits-hubbard": {
      "level": "core", "layout": "two-figs", "fig": "s29-f1", "fig2": "s29-f2",
      "title": "Interactions by hand: mean-field Hubbard on a zigzag ribbon",
      "lead": "A self-consistent loop around PythTB: guess the local moments, build the spin-dependent onsite energies, solve, recompute the moments, repeat. The converged solution (left) shows opposite magnetization on the two zigzag edges, painted on the ribbon (right).",
      "bullets": [
        "The flat edge band of lecture 3 has a huge density of states at the Fermi level: the Stoner criterion is met and the edges order.",
        "Antiferromagnetic across the ribbon, ferromagnetic along each edge: Fujita et al. (1996), later seen in STM.",
        "Thirty lines of Python; the physics is in the loop, PythTB is only the solver inside it."
      ],
      "notes": "Walk through the loop on the board: U n↑n↓ → U(⟨n↓⟩n↑ + ⟨n↑⟩n↓ − ⟨n↑⟩⟨n↓⟩), so each spin sees an onsite energy U⟨n_{−σ}⟩; iterate with mixing until the moments stop changing. Q: \"Is mean field trustworthy here?\" A: Qualitatively; the edge ordering survives in DMRG and quantum Monte Carlo, but the magnitude of the gap and the finite-temperature behaviour do not."
    },
    "limits-matrix": {
      "level": "core", "layout": "table",
      "title": "The capability matrix",
      "lead": "PythTB versus Kwant, honestly. Use both; know which one you are holding.",
      "table": {
        "head": ["", "PythTB 2.0", "Kwant 1.5"],
        "rows": [
          ["Band structures, k-paths, meshes", "yes, first-class", "yes (wraparound / Bands)"],
          ["Berry phase, curvature, Chern, Z₂ flow, axion", "<span class='c-3'>yes, built in</span>", "no (write it yourself)"],
          ["Wannier functions, Wannier90 import", "<span class='c-3'>yes</span>", "no"],
          ["Finite systems, ribbons, supercells, defects", "yes (dense)", "yes (sparse)"],
          ["Transport: leads, S-matrix, conductance", "<span class='c-hot'>no</span>", "<span class='c-3'>yes, first-class</span>"],
          ["Sparse eigensolvers, KPM, 10⁵+ sites", "<span class='c-hot'>no</span>", "<span class='c-3'>yes</span>"],
          ["Continuum k·p → lattice discretizer", "no", "yes (kwant.continuum)"],
          ["Symmetry enforcement (BdG, conservation laws)", "no", "partial"],
          ["Interactions / self-consistency", "loop by hand", "loop by hand"],
          ["Learning curve", "an afternoon", "a week"]
        ]
      },
      "notes": "Let the table speak; the notebook's §30 has the same matrix with the evidence for each cell. The one rule of thumb: geometry of eigenvectors → PythTB; anything with a lead attached → Kwant. Q: \"What about other codes?\" A: TBmodels and pybinding cover similar ground with different emphases (Wannier90 interoperability; large-scale KPM respectively); WannierTools for topological indices of real materials at scale."
    },
    "limits-math": {
      "level": "math", "layout": "eq",
      "title": "Mean field, and the equation PythTB does not solve",
      "eqs": [
        {"label": "Hubbard mean field", "math": "<span class='math'>U n<sub>i↑</sub>n<sub>i↓</sub> ≈ U( ⟨n<sub>i↓</sub>⟩ n<sub>i↑</sub> + ⟨n<sub>i↑</sub>⟩ n<sub>i↓</sub> − ⟨n<sub>i↑</sub>⟩⟨n<sub>i↓</sub>⟩ ),   m<sub>i</sub> = ⟨n<sub>i↑</sub>⟩ − ⟨n<sub>i↓</sub>⟩</span>"},
        {"label": "self-consistency", "math": "<span class='math'>ε<sub>iσ</sub><sup>(n+1)</sup> = U ⟨n<sub>i,−σ</sub>⟩<sup>(n)</sup>,   ⟨n<sub>iσ</sub>⟩ = Σ<sub>E<sub>α</sub>&lt;E<sub>F</sub></sub> |ψ<sub>α</sub>(i,σ)|<sup>2</sup>,   iterate until |m<sup>(n+1)</sup> − m<sup>(n)</sup>| &lt; tol</span>"},
        {"label": "Landauer–Büttiker (Kwant's problem)", "math": "<span class='math'>G = (e<sup>2</sup>/h) <span class='fn'>Tr</span>( t<sup>†</sup>t ) = (e<sup>2</sup>/h) Σ<sub>n</sub> T<sub>n</sub>,   S = ( r  t' ; t  r' )</span>"}
      ],
      "bullets": [
        "Mean field replaces a quartic operator by a quadratic one plus a constant: the result is again a tight-binding model, which is why the loop closes on PythTB.",
        "Convergence needs mixing (<span class='math'>m ← (1−α)m<sub>old</sub> + α m<sub>new</sub></span>) and a symmetry-breaking seed, or the loop returns the paramagnet.",
        "The scattering matrix needs semi-infinite leads and a Green's function: a different mathematical object from a Hamiltonian's eigenvalues."
      ],
      "notes": "Derive the mean-field decoupling by writing n = ⟨n⟩ + δn and dropping δn↑δn↓. Discuss the two failure modes of the loop (charge sloshing without mixing; the trivial paramagnetic fixed point without a seed). Then state Landauer–Büttiker and explain in one sentence why PythTB cannot do it: a lead is infinite in one direction and open, so the problem is not an eigenproblem. Q: \"Could I fake a lead with a long finite ribbon?\" A: You get standing waves, not transmission; the conductance needs the open boundary condition that Kwant's lead self-energy provides."
    },
    "limits-close": {
      "level": "intro", "layout": "hero",
      "kicker": "Where to go next",
      "title": "You can now build, solve, and classify",
      "sub": "Vanderbilt, <em>Berry Phases in Electronic Structure Theory</em> (the book PythTB was written for) · Asbóth, Oroszlány, Pályi, <em>A Short Course on Topological Insulators</em> · the PythTB documentation and examples · Kwant for transport · the companion notebook's exercises, with solutions",
      "notes": "Close with the arc: lecture 1's 1×1 matrix and lecture 8's axion angle were computed with the same three method calls. Point to the exercises (one set per Part in the notebook, with solutions) and to the two textbooks that the course silently follows. Q: \"What should I do first on my own?\" A: Rebuild one figure of this course from a blank notebook without looking — then change one parameter and predict the result before running it."
    }
  },
  "glossary": [
    ["Tight-binding model", "A Hamiltonian written in a basis of localized orbitals: onsite energies and hoppings, nothing else."],
    ["Bloch Hamiltonian H(k)", "The finite matrix obtained by Fourier transforming the hoppings; its eigenvalues are the bands."],
    ["Brillouin zone", "The unit cell of reciprocal space; k and k + G label the same state."],
    ["Reduced coordinates", "Positions in units of the lattice vectors, k in units of the reciprocal vectors — PythTB's convention everywhere."],
    ["Atomic gauge", "Bloch phases that include the orbital position τ; makes Berry phases equal to physical positions."],
    ["Chiral (sublattice) symmetry", "An operator anticommuting with H; forces the spectrum symmetric about zero and protects SSH end modes."],
    ["Berry phase", "The phase acquired by a band eigenvector transported around a closed loop in k; gauge invariant mod 2π."],
    ["Wannier centre", "Berry phase divided by 2π, in units of the lattice constant: the position of the band's charge."],
    ["Berry curvature Ω", "The local density of Berry phase in a 2D k-plane; its integral over the zone is 2π times the Chern number."],
    ["Chern number C", "Integer invariant of a 2D gapped band; equals the Hall conductance in units of e²/h and the number of chiral edge modes."],
    ["Z₂ invariant ν", "Parity-valued invariant of a time-reversal-symmetric 2D insulator; ν = 1 means one protected helical edge pair."],
    ["Kramers pair", "Two degenerate states related by time reversal when Θ² = −1; cannot be split by any time-reversal-symmetric perturbation."],
    ["Wilson loop", "The product of overlap matrices around a closed k-loop; its eigenphases are hybrid Wannier centres."],
    ["Bulk–boundary correspondence", "A bulk invariant fixes the number of protected boundary states."],
    ["Bogoliubov–de Gennes (BdG)", "The doubled particle–hole Hamiltonian that writes pairing as hopping; every eigenvalue appears with its negative."],
    ["Majorana mode", "A zero-energy BdG state equal to its own particle–hole partner; two of them make one fermion."],
    ["Weyl node", "A point band touching in 3D acting as a monopole of Berry curvature; nodes come in pairs of opposite chirality."],
    ["Axion angle θ", "The 3D magnetoelectric Berry-phase angle; θ = π characterizes a strong topological insulator."],
    ["Peierls substitution", "Multiplying each hopping by the phase e^{i(e/ħ)∫A·dl} to include a magnetic field."],
    ["Inverse participation ratio", "Σ|ψ_i|⁴ for a normalized state; ~1/N for extended, ~1/ξ^d for localized states."],
    ["Supercell", "A larger periodic cell built from copies of the primitive one; needed for defects, disorder and fields."],
    ["Density of states", "The number of states per unit energy; its singularities (van Hove) mark saddle points of the bands."]
  ]
};
