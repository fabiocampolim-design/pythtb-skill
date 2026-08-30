# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
from nbbuild import md, code

CELLS = [

md(r"""
# PythTB — Exercises and Worked Solutions

Companion to `PythTB_Theory_and_Practice.ipynb`; exercise statements live at the end of each part
there. Same environment (`pythtb-mc` kernel), same conventions, same rule: every claim checks
itself with an inline **PASS/FAIL**.
"""),

code(r"""
import time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML

import pythtb
from pythtb import Lattice, TBModel, Mesh, WFArray, Wannier, W90
from pythtb.models import graphene as graphene_factory
from pythtb.models import haldane, kane_mele, ssh, fu_kane_mele

plt.rcParams.update({"figure.dpi": 110, "figure.figsize": (7.0, 4.2),
                     "axes.grid": True, "grid.alpha": 0.3, "font.size": 10})
rng = np.random.default_rng(2026)
_CHECKS = {"pass": 0, "fail": 0}

def check(label, ok, detail=""):
    ok = bool(ok)
    _CHECKS["pass" if ok else "fail"] += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f" — {detail}" if detail else ""))
    return ok

_FIG = {"n": 0}

def caption(text):
    '''Numbered caption rendered directly below the figure it describes.'''
    _FIG["n"] += 1
    display(HTML(
        f"<div style='max-width:780px;margin:2px 0 14px 12px;font-size:0.92em;"
        f"color:#444;border-left:3px solid #bbb;padding-left:10px'>"
        f"<b>Figure {_FIG['n']}.</b> {text}</div>"))

print("pythtb", pythtb.__version__)
t_start = time.time()
"""),

# ------------------------------------------------------------------ I.1
md(r"""
## I.1 — The trestle

Two rails at heights 0 and ½ of a non-periodic transverse direction, hopping $t$ along each rail
and $t'$ on the diagonal rungs. The two bands repel through the rung coupling; at the zone boundary
the rail bands cross when the rung matrix element between the two boundary-symmetric combinations
vanishes — we locate the critical $t'/t$ numerically.
"""),

code(r"""
def trestle(t, tp):
    lat = Lattice(lat_vecs=[[1.0, 0.0], [0.0, 1.0]],
                  orb_vecs=[[0.0, 0.0], [0.5, 0.5]], periodic_dirs=[0])
    m = TBModel(lat)
    m.set_hop(t, 0, 0, [1, 0])
    m.set_hop(-t, 1, 1, [1, 0])           # opposite-sign rail so the bands cross
    m.set_hop(tp, 0, 1, [0, 0])
    m.set_hop(tp, 1, 0, [1, 0])
    return m

# the trestle, drawn: two rails with opposite hopping signs, diagonal rungs
fig, ax = plt.subplots(figsize=(7, 1.9))
for x in range(5):
    ax.plot([x], [0], "o", ms=13, color="C0", zorder=3)
    ax.plot([x + 0.5], [0.5], "o", ms=13, color="C3", zorder=3)
    if x < 4:
        ax.plot([x, x + 1], [0, 0], "-", color="k", lw=1.8)
        ax.plot([x + 0.5, x + 1.5], [0.5, 0.5], "-", color="k", lw=1.8)
    ax.plot([x, x + 0.5], [0, 0.5], "--", color="C2", lw=1.5)
    if x < 4:
        ax.plot([x + 0.5, x + 1], [0.5, 0], "--", color="C2", lw=1.5)
ax.annotate("+t", (1.5, -0.18), ha="center", fontsize=11)
ax.annotate("-t", (2.0, 0.66), ha="center", fontsize=11)
ax.annotate("t'", (0.13, 0.28), ha="center", fontsize=11, color="C2")
ax.set_xlim(-0.5, 5.2); ax.set_ylim(-0.35, 0.85); ax.axis("off")
plt.show()
caption("The trestle: two 1D rails with opposite-sign hoppings ±t (so their bands "
        "disperse oppositely and must cross) connected by diagonal rungs t' "
        "(dashed green). The rung coupling hybridizes the rails wherever their "
        "bands meet.")

k_vec = np.array([[k] for k in np.linspace(-0.5, 0.5, 201)])   # 1 periodic dir -> 1D k
tp_scan = np.linspace(0.0, 1.5, 61)
min_gap = np.array([np.diff(np.sort(trestle(1.0, tp).solve_ham(k_vec), axis=1),
                            axis=1).min() for tp in tp_scan])

fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
for tp in (0.2, 0.8):
    ev = trestle(1.0, tp).solve_ham(k_vec)
    axs[0].plot(k_vec[:, 0], ev, lw=1.5,
                label=None)
axs[0].set_xlabel("k"); axs[0].set_ylabel("E / t")
axs[0].set_title("trestle bands, t' = 0.2 and 0.8")
axs[1].plot(tp_scan, min_gap, "o-", ms=3)
axs[1].set_xlabel("t' / t"); axs[1].set_ylabel("minimum direct gap")
axs[1].set_title("the rung coupling gaps the rail crossing for any t' > 0")
fig.tight_layout(); plt.show()
caption("Left: trestle bands at two rung strengths — the rail crossing at "
        "k = ±π/2 is avoided as soon as t' ≠ 0. Right: the minimum direct gap "
        "versus t', zero only at exactly t' = 0 and growing linearly: an avoided "
        "crossing opens at first order in the coupling that connects the two "
        "crossing states.")

check("I.1: bands cross at t' = 0 and are gapped for every t' > 0",
      min_gap[0] < 1e-12 and np.all(min_gap[1:] > 1e-6),
      f"gap(t'=0) = {min_gap[0]:.1e}, gap(t'=0.075) = {min_gap[1]:.4f}")
"""),

# ------------------------------------------------------------------ I.2
md(r"""
## I.2 — Breaking particle–hole symmetry in graphene

Second-neighbour hopping $t'$ connects same-sublattice sites: it adds a *diagonal* term
$\varepsilon(\mathbf k) = 2t'\sum_i \cos \mathbf{K}\cdot\mathbf{a}_i$ to $H(\mathbf k)$, so it
shifts both bands equally and cannot open a gap — the Dirac touching survives, displaced to
$\varepsilon(K) = -3t'$. The touching is protected by inversion + time reversal (which pin the
off-diagonal part to zero at $K$), not by the chiral symmetry that $t'$ breaks.
"""),

code(r"""
def graphene_nnn(t, tp):
    lat = Lattice(lat_vecs=[[1.0, 0.0], [0.5, np.sqrt(3) / 2]],
                  orb_vecs=[[1/3, 1/3], [2/3, 2/3]], periodic_dirs=[0, 1])
    m = TBModel(lat)
    m.set_hop(t, 0, 1, [0, 0]); m.set_hop(t, 1, 0, [1, 0]); m.set_hop(t, 1, 0, [0, 1])
    for R in ([1, 0], [0, 1], [1, -1]):
        m.set_hop(tp, 0, 0, R)
        m.set_hop(tp, 1, 1, R)
    return m

tp = 0.1
g2 = graphene_nnn(-1.0, tp)
evK = np.atleast_2d(g2.solve_ham(np.array([[2/3, 1/3]])))[0]
gap_K = evK[1] - evK[0]
E_D = evK.mean()

k_vec, k_dist, k_node = g2.k_path([[0, 0], [2/3, 1/3], [1/2, 1/2], [0, 0]],
                                  nk=301, report=False)
ev = g2.solve_ham(k_vec)
fig, ax = plt.subplots()
ax.plot(k_dist, ev, lw=2)
ax.axhline(E_D, color="r", ls=":", lw=1, label=f"Dirac point at E = {E_D:.3f}")
ax.set_xticks(k_node, [r"$\Gamma$", "K", "M", r"$\Gamma$"])
ax.set_ylabel("E / t"); ax.legend()
ax.set_title("graphene + real NNN hopping: PH symmetry gone, Dirac point intact")
plt.show()
caption("Graphene with a real second-neighbour hopping: the spectrum is no "
        "longer symmetric about zero (compare the depths of the band extrema at "
        "Γ), but the Dirac touching survives untouched, merely displaced to "
        "E = −3t' (dotted). Particle-hole symmetry was never the Dirac point's "
        "bodyguard — inversion and time reversal are.")

check("I.2: Dirac touching survives t'", gap_K < 1e-12, f"gap at K = {gap_K:.1e}")
check("I.2: touching sits at E = -3t'", np.isclose(E_D, -3 * tp, atol=1e-10),
      f"E_D = {E_D:.6f} vs -3t' = {-3*tp:.6f}")
"""),

# ------------------------------------------------------------------ I.3
md(r"""
## I.3 — (Non-)fragility of the Lieb flat band

The flat-band eigenstates live **entirely on the edge sites** — the corner-site amplitude is
exactly zero (that zero is *how* the destructive interference works). The prediction follows
immediately: a corner–corner hop, however large, acts on a subspace the flat band does not touch
and leaves it **exactly flat**; a diagonal edge–edge hop acts directly inside the flat band's own
subspace and disperses it linearly in $t_2$. The naive "any perturbation kills a fine-tuned flat
band" intuition fails in an instructive way: what matters is not the size of the perturbation but
its matrix elements in the flat-band manifold.
"""),

code(r"""
def lieb_pert(t, t2_corner=0.0, t2_edge=0.0):
    lat = Lattice(lat_vecs=[[1, 0], [0, 1]],
                  orb_vecs=[[0, 0], [0.5, 0], [0, 0.5]], periodic_dirs=[0, 1])
    m = TBModel(lat)
    m.set_hop(t, 0, 1, [0, 0]); m.set_hop(t, 1, 0, [1, 0])
    m.set_hop(t, 0, 2, [0, 0]); m.set_hop(t, 2, 0, [0, 1])
    if t2_corner:
        m.set_hop(t2_corner, 0, 0, [1, 0]); m.set_hop(t2_corner, 0, 0, [0, 1])
    if t2_edge:                                # the two diagonal edge-edge bonds
        m.set_hop(t2_edge, 1, 2, [0, 0])
        m.set_hop(t2_edge, 1, 2, [1, -1])
    return m

k_mesh = lieb_pert(-1).k_uniform_mesh([25, 25])

def midband_width(m):
    ev = np.sort(m.solve_ham(k_mesh), axis=1)
    return ev[:, 1].max() - ev[:, 1].min(), max(ev[:, 2].min() - ev[:, 1].max(), 1e-12)

w_corner, _ = midband_width(lieb_pert(-1.0, t2_corner=0.4))
check("I.3: corner–corner hopping leaves the flat band EXACTLY flat",
      w_corner < 1e-12, f"width = {w_corner:.1e} at t2 = 0.4")

t2_scan = np.linspace(0, 0.5, 26)
width, gap = np.array([midband_width(lieb_pert(-1.0, t2_edge=t2)) for t2 in t2_scan]).T
ratio = width / gap
i_c = int(np.argmax(ratio > 0.10))
print(f"edge–edge case: width exceeds 10% of the gap at t2/t ≈ {t2_scan[i_c]:.3f}")

fig, ax = plt.subplots()
ax.plot(t2_scan, width, "o-", label="middle-band width (edge–edge $t_2$)")
ax.plot(t2_scan, gap, "s-", label="gap above it")
ax.axvline(t2_scan[i_c], color="r", ls="--", lw=1)
ax.set_xlabel(r"$t_2 / t$"); ax.set_ylabel("energy scale")
ax.legend(); ax.set_title("Lieb flat band: immune to corner–corner, killed by edge–edge")
plt.show()
caption("Flat-band fragility resolved by WHERE the perturbation acts: the "
        "middle-band width stays exactly zero under corner–corner hopping (the "
        "flat-band states have no corner amplitude to couple), while an edge–edge "
        "hopping of the same size disperses it linearly. The red line marks where "
        "the width reaches 10% of the gap.")

check("I.3: edge–edge hopping disperses the band; 10% threshold located",
      width[0] < 1e-12 and np.all(width[1:] > 1e-6) and 0 < i_c < len(t2_scan) - 1,
      f"threshold t2 = {t2_scan[i_c]:.3f}")
"""),

# ------------------------------------------------------------------ I.4
md(r"""
## I.4 — Polarization of boron nitride

The valence-band Berry phase along $k_1$, averaged over $k_2$, is the polarization component
$P_1$ (in units of $e$ per cell, mod 1). $C_3$ symmetry pins the valence Wannier center to one of
the honeycomb Wyckoff positions; flipping the sign of $\Delta$ moves it from one sublattice site to
the other — a polarization change of exactly $1/3 - 2/3 \equiv \pm 1/3$... or is it $1/2$? The
computation decides: the Wannier center follows the *anion*, and the two anion positions differ by
$(\tfrac13,\tfrac13)$, so each reduced component of $\mathbf P$ jumps by $1/3$ (mod 1). This is a
case where doing the integral corrects a plausible-sounding guess — the "$e/2$" of the exercise
statement is a trap, and honesty demands the code win.
"""),

code(r"""
def bn_polarization(delta, nk=41):
    m = graphene_factory(delta=delta, t=-1.0)
    mesh = Mesh(["k", "k"])
    mesh.build_grid((61, nk), k_endpoints=[True, False])
    wfa = WFArray(m.lattice, mesh)
    wfa.solve_model(m)
    phases = np.asarray(wfa.berry_phase(axis_idx=0, state_idx=[0], contin=True))
    return (phases.mean() / (2 * np.pi)) % 1.0

P_plus = bn_polarization(+0.65)
P_minus = bn_polarization(-0.65)
dP = (P_plus - P_minus) % 1.0
print(f"P1(Δ>0) = {P_plus:.6f},  P1(Δ<0) = {P_minus:.6f},  ΔP1 = {dP:.6f} (mod 1)")

check("I.4: polarizations are pinned to thirds by C3",
      min(abs(P_plus - round(P_plus * 3) / 3), 1 - abs(P_plus - round(P_plus * 3) / 3)) < 1e-3
      and min(abs(P_minus - round(P_minus * 3) / 3), 1 - abs(P_minus - round(P_minus * 3) / 3)) < 1e-3)
check("I.4: flipping Δ moves the Wannier center between sublattices (ΔP = 1/3 mod 1)",
      np.isclose(dP, 1/3, atol=1e-3) or np.isclose(dP, 2/3, atol=1e-3),
      f"ΔP1 = {dP:.5f}")
"""),

# ------------------------------------------------------------------ I.5
md(r"""
## I.5 — A pump that pumps nothing

Shift the Rice–Mele cycle so the $(v-w, \Delta)$ loop no longer encloses the gapless point
$(0,0)$: $\Delta(\lambda) = \Delta_0[1.5 + \sin 2\pi\lambda]$ never changes sign. The Wannier
center must now breathe and return — zero net winding, zero Chern number.
"""),

code(r"""
t0, d0, D0 = 1.0, 0.4, 0.6
lat_rm = Lattice(lat_vecs=[[1.0]], orb_vecs=[[0.0], [0.5]], periodic_dirs=[0])
rm2 = TBModel(lat_rm)
rm2.set_onsite([lambda lmbda: -D0 * (1.5 + np.sin(2 * np.pi * lmbda)),
                lambda lmbda: +D0 * (1.5 + np.sin(2 * np.pi * lmbda))])
rm2.set_hop(lambda lmbda: t0 + d0 * np.cos(2 * np.pi * lmbda), 0, 1, [0])
rm2.set_hop(t0, 1, 0, [1])

mesh = Mesh(["k", "l"], axis_names=["k", "lmbda"])
mesh.build_grid(shape=(41, 61), k_endpoints=True,
                lambda_start=0.0, lambda_stop=1.0, lambda_endpoints=True)
mesh.loop(axis_idx=1, component_idx=1, closed=True)
wfa = WFArray(lat_rm, mesh)
wfa.solve_model(rm2)
lam = mesh.get_axis_range(1, 1)
xbar = np.array(wfa.berry_phase(axis_idx=0, state_idx=[0], contin=True)) / (2 * np.pi)
C0 = float(wfa.chern_number(plane=(0, 1), state_idx=[0]))

fig, ax = plt.subplots()
ax.plot(lam, xbar, "o-", ms=3)
ax.set_xlabel(r"$\lambda$"); ax.set_ylabel(r"$\bar x(\lambda)$")
ax.set_title(f"off-center cycle: the Wannier center breathes, C = {C0:+.4f}")
plt.show()
caption("A Rice–Mele cycle whose (v−w, Δ) loop does NOT enclose the gapless "
        "point: the Wannier center oscillates and returns with zero net "
        "displacement, and the (k, λ) Chern number vanishes. Pumping is a "
        "topological property of the LOOP, not of how vigorously the parameters "
        "are driven.")

check("I.5: no winding, no pumped charge",
      abs(xbar[-1] - xbar[0]) < 1e-6 and abs(C0) < 1e-6,
      f"winding = {xbar[-1]-xbar[0]:+.2e}, C = {C0:+.2e}")
"""),

# ------------------------------------------------------------------ I.6
md(r"""
## I.6 — Silicon conduction bands

The 8-band silicon Wannier model was generated with the valence bands frozen (they are an isolated
group) while the 4 antibonding combinations were *disentangled* from higher DFT bands — so the
Wannier interpolation is variationally faithful for the valence group and only approximate above.
The Wannier90 reference bands themselves carry that asymmetry; we quantify it through the
truncation sensitivity: dropped small hoppings cost the conduction bands visibly more than the
valence bands, because their Wannier functions are less localized.
"""),

code(r"""
silicon = W90("data/w90_silicon", "si")
fermi_ev = 6.2285135
w90_kpt, w90_evals = silicon.bands_w90()[:2]

errs = {}
for cut in (1e-3, 1e-2):
    m = silicon.model(zero_energy=fermi_ev, min_hopping_norm=cut)
    e = np.abs(m.solve_ham(w90_kpt) - (w90_evals - fermi_ev))
    errs[cut] = e

fig, ax = plt.subplots()
for cut, marker in ((1e-3, "o"), (1e-2, "s")):
    ax.semilogy(np.arange(8), errs[cut].max(axis=0) * 1000, marker + "-",
                label=f"min |t| = {cut} eV")
ax.axvline(3.5, color="gray", ls=":", lw=1)
ax.text(1.0, ax.get_ylim()[1] * 0.5, "valence", ha="center")
ax.text(5.5, ax.get_ylim()[1] * 0.5, "conduction", ha="center")
ax.set_xlabel("band index"); ax.set_ylabel("max |error| (meV)")
ax.legend(); ax.set_title("silicon: truncation error per band — conduction pays more")
plt.show()
caption("Truncation error of the silicon Wannier model, resolved band by band "
        "(valence 0–3, conduction 4–7) for two hopping cutoffs. The conduction "
        "bands, built from less-localized antibonding/disentangled Wannier "
        "functions, lose accuracy faster when distant hoppings are discarded — "
        "localization quality translates directly into interpolation quality.")

for cut in (1e-3, 1e-2):
    ev_err = errs[cut]
    val, cond = ev_err[:, :4].mean(), ev_err[:, 4:].mean()
    print(f"cut {cut}: mean error valence {1000*val:.2f} meV, conduction {1000*cond:.2f} meV")
check("I.6: conduction bands interpolate worse than valence bands",
      errs[1e-3][:, 4:].mean() > errs[1e-3][:, :4].mean()
      and errs[1e-2][:, 4:].mean() > errs[1e-2][:, :4].mean())
"""),

# ------------------------------------------------------------------ II.1
md(r"""
## II.1 — Competing masses in the Haldane model

At the two valleys the gap is $|\Delta \mp 3\sqrt3\, t_2 \sin\phi|$: the Semenoff mass $\Delta$ has
the *same* sign at $K$ and $K'$, the Haldane mass alternates. Crossing the phase boundary closes
the gap at exactly one valley — the other stays open, which is why the Chern number changes by
$\pm 1$ and not $\pm 2$.
"""),

code(r"""
t2v, phiv = 0.15, np.pi / 2
crit = 3 * np.sqrt(3) * t2v * np.sin(phiv)
d_scan = np.linspace(0.2, 1.3, 67) * crit   # 67 points puts Delta = crit on the grid
K_pt, Kp_pt = np.array([[2/3, 1/3]]), np.array([[1/3, 2/3]])
gap_K = np.array([np.diff(np.atleast_2d(haldane(delta=d, t1=-1.0, t2=t2v, phi=phiv)
                          .solve_ham(K_pt)))[0, 0] for d in d_scan])
gap_Kp = np.array([np.diff(np.atleast_2d(haldane(delta=d, t1=-1.0, t2=t2v, phi=phiv)
                           .solve_ham(Kp_pt)))[0, 0] for d in d_scan])

# which valley carries which mass depends on the factory's sign conventions:
# compare the SET {gap_K, gap_K'} against the analytic set {|Δ-m_H|, Δ+m_H}
gap_soft = np.minimum(gap_K, gap_Kp)
gap_hard = np.maximum(gap_K, gap_Kp)

fig, ax = plt.subplots()
ax.plot(d_scan / crit, gap_K, "o-", ms=3, label="gap at K")
ax.plot(d_scan / crit, gap_Kp, "s-", ms=3, label="gap at K'")
ax.plot(d_scan / crit, 2 * np.abs(d_scan - crit), "k--", lw=1,
        label=r"$2|\Delta - 3\sqrt{3}\, t_2|$")
ax.plot(d_scan / crit, 2 * (d_scan + crit), "k:", lw=1,
        label=r"$2(\Delta + 3\sqrt{3}\, t_2)$")
ax.axvline(1.0, color="r", ls="--", lw=1)
ax.set_xlabel(r"$\Delta \,/\, 3\sqrt{3}\, t_2\sin\phi$"); ax.set_ylabel("valley gap")
ax.legend(fontsize=8)
ax.set_title("Haldane transition: one valley closes, the other never does")
plt.show()
caption("Valley-resolved gaps across the Haldane transition: one valley's gap "
        "closes linearly at Δ = 3√3 t₂ sinφ while the other's keeps growing — the "
        "numerics landing exactly on 2|Δ ∓ m_H| (guides). A Chern number can only "
        "change by the chirality of the single Dirac cone that closes, which is "
        "why the transition steps C by 1 and not by 2.")

# onsite energies are ±Δ, so the K-point splitting is 2|m|: gaps = 2|Δ ∓ m_H|
check("II.1: valley gaps match 2|Δ ∓ 3√3 t₂ sinφ|",
      np.allclose(gap_soft, 2 * np.abs(d_scan - crit), atol=1e-10)
      and np.allclose(gap_hard, 2 * (d_scan + crit), atol=1e-10))
check("II.1: at the transition only one valley is gapless",
      np.min(gap_soft) < 1e-10 and np.min(gap_hard) > 2 * crit)
"""),

# ------------------------------------------------------------------ II.2
md(r"""
## II.2 — Kane–Mele phase map

Automating the Wannier-flow parity of §15 over the $(\Delta, \lambda_{SO})$ plane and comparing
with the analytic boundary $\Delta = 3\sqrt3\,\lambda_{SO}$ (exact at Rashba = 0; we keep a small
Rashba to make the test non-trivial and stay clear of the boundary itself).
"""),

code(r"""
def z2_from_wcc(w, ref):
    def arc(a, b):
        return (b - a + 0.5) % 1.0 - 0.5
    crossings = 0
    for r in range(len(w) - 1):
        w1, w2 = w[r], w[r + 1]
        d_keep = [arc(w1[0], w2[0]), arc(w1[1], w2[1])]
        d_swap = [arc(w1[0], w2[1]), arc(w1[1], w2[0])]
        d = d_keep if sum(map(abs, d_keep)) <= sum(map(abs, d_swap)) else d_swap
        for a, dd in zip(w1, d):
            if dd > 0 and (ref - a) % 1.0 < dd:
                crossings += 1
            elif dd < 0 and (a - ref) % 1.0 < -dd:
                crossings += 1
    return crossings % 2

def km_z2(delta, soc, rashba=0.05):
    m = kane_mele(delta=delta, t=1.0, soc=soc, rashba=rashba)
    mesh = Mesh(["k", "k"])
    mesh.build_grid((41, 31), k_endpoints=[True, True])
    wfa = WFArray(m.lattice, mesh, spinful=True)
    wfa.solve_model(m)
    wcc = np.asarray(wfa.berry_phase(axis_idx=0, state_idx=[0, 1],
                                     berry_evals=True, contin=False)) / (2 * np.pi) % 1.0
    ky = mesh.get_axis_range(1, 1)
    return z2_from_wcc(wcc[ky <= 0.5 + 1e-9], 0.31)

socs = np.linspace(0.05, 0.30, 6)
dels = np.linspace(0.2, 2.4, 6)
zmap = np.zeros((len(dels), len(socs)), int)
t0 = time.time()
for i, dv in enumerate(dels):
    for j, sv in enumerate(socs):
        zmap[i, j] = km_z2(dv, sv)
print(f"36-point phase map in {time.time()-t0:.1f} s")

fig, ax = plt.subplots(figsize=(6.2, 4.6))
im = ax.pcolormesh(socs, dels, zmap, cmap="coolwarm", shading="auto", vmin=0, vmax=1)
soc_line = np.linspace(socs[0], socs[-1], 100)
ax.plot(soc_line, 3 * np.sqrt(3) * soc_line, "k--", lw=1.5,
        label=r"$\Delta = 3\sqrt{3}\,\lambda_{SO}$")
fig.colorbar(im, label=r"$\mathbb{Z}_2$", ticks=[0, 1])
ax.set_xlabel(r"$\lambda_{SO}$"); ax.set_ylabel(r"$\Delta$")
ax.legend(); ax.set_title("Kane–Mele phase map from automated WCC parity")
plt.show()
caption("The Kane–Mele phase diagram mapped by running the Wannier-flow parity "
        "of §15 at every grid point: Z₂ = 1 (red) below the analytic boundary "
        "Δ = 3√3 λ_SO (dashed), 0 above, with only near-boundary points shifted "
        "slightly by the small Rashba term. An invariant that can be evaluated "
        "blindly on a grid is an invariant that can map phase diagrams.")

analytic = (dels[:, None] < 3 * np.sqrt(3) * socs[None, :]).astype(int)
agree = (zmap == analytic)
# tolerate points within 10% of the boundary (small Rashba shifts it slightly)
dist = np.abs(dels[:, None] - 3 * np.sqrt(3) * socs[None, :]) / (3 * np.sqrt(3) * socs[None, :])
agree_far = agree | (dist < 0.10)
check("II.2: WCC parity reproduces the analytic phase boundary",
      np.all(agree_far), f"{agree.sum()}/{agree.size} grid points agree outright")
"""),

# ------------------------------------------------------------------ II.3
md(r"""
## II.3 — From quantum spin Hall to quantum anomalous Hall

An exchange field $M_z s_z$ splits the two time-reversed BHZ blocks: one block's mass is pushed
through zero while the other's grows. In the window where exactly one block is inverted the total
Chern number is $\pm 1$ — a quantum anomalous Hall phase engineered from a QSH parent, the
mechanism behind the Cr-doped (Bi,Sb)₂Te₃ experiments (2013).
"""),

code(r"""
def bhz_exchange(M, Mz, A=1.0, B=1.0):
    s0 = np.eye(2); sz = np.diag([1.0, -1.0])
    lat = Lattice(lat_vecs=[[1, 0], [0, 1]], orb_vecs=[[0, 0], [0, 0]],
                  periodic_dirs=[0, 1])
    m = TBModel(lat, spinful=True)
    # exchange enters ORBITAL-ANTISYMMETRICALLY (different g-factors of the E1/H1
    # bands): only then does it shift the block masses M -> M ± Mz rather than
    # rigidly shifting both blocks' energies
    m.set_onsite([[(M - 4 * B), 0, 0, Mz], [-(M - 4 * B), 0, 0, -Mz]])
    for R in ([1, 0], [0, 1]):
        m.set_hop(B * s0, 0, 0, R)
        m.set_hop(-B * s0, 1, 1, R)
    m.set_hop(A / (2j) * sz, 0, 1, [1, 0])
    m.set_hop(-A / (2j) * sz, 0, 1, [-1, 0], allow_conjugate_pair=True)
    m.set_hop(-A / 2 * s0, 0, 1, [0, 1])
    m.set_hop(A / 2 * s0, 0, 1, [0, -1], allow_conjugate_pair=True)
    return m

Mz_scan = np.linspace(0.0, 9.0, 31) + 0.017          # offset avoids exact closings
C_scan = []
for Mz in Mz_scan:
    try:
        C_scan.append(float(bhz_exchange(1.0, Mz).chern_number(
            plane=(0, 1), nks=(25, 25), occ_idxs=[0, 1])))
    except ZeroDivisionError:
        C_scan.append(np.nan)
C_scan = np.array(C_scan)

fig, ax = plt.subplots()
ax.plot(Mz_scan, np.round(C_scan), "o-", ms=4)
ax.set_xlabel(r"exchange field $M_z$"); ax.set_ylabel("total Chern number")
ax.set_title("BHZ + exchange: QSH (C=0) → QAH (|C|=1) → trivial (C=0)")
plt.show()
caption("Total Chern number of the BHZ model versus exchange field: the QSH "
        "phase (C = 0, but Z₂ = 1) gives way to a quantum anomalous Hall window "
        "with |C| = 1 once the exchange field un-inverts ONE spin block "
        "(Mz > M), and to a fully trivial phase when it un-inverts the other "
        "(Mz > 8B − M). This QSH-parent route is precisely how the QAH effect was "
        "first realized experimentally in magnetically doped (Bi,Sb)₂Te₃.")

C_r = np.round(C_scan[~np.isnan(C_scan)])
check("II.3: a |C| = 1 QAH window opens between two C = 0 phases",
      np.any(np.abs(C_r) == 1) and C_r[0] == 0 and C_r[-1] == 0,
      f"C sequence: {C_r[::4]}")
"""),

# ------------------------------------------------------------------ II.4
md(r"""
## II.4 — The corner-charge pump

Drive BBH around $\gamma(\lambda) = 1 + 0.8\cos 2\pi\lambda$ with a chiral-symmetry-breaking
onsite $\delta(\lambda) = 0.8\sin 2\pi\lambda$ staggered between the two sublattice pairs. At
$\lambda = 1/2$ the system passes through the quadrupole phase with the onsite term off — corner
modes at zero — while at $\lambda = 0$ it is trivial. The four corner levels must traverse the gap:
a quantized *quadrupole* pump, one dimension of hierarchy above Rice–Mele.
"""),

code(r"""
def bbh_pump(lmbda, lam_inter=1.0):
    g = 1.0 + 0.8 * np.cos(2 * np.pi * lmbda)
    d = 0.8 * np.sin(2 * np.pi * lmbda)
    lat = Lattice(lat_vecs=[[1, 0], [0, 1]],
                  orb_vecs=[[0, 0], [0.5, 0], [0, 0.5], [0.5, 0.5]],
                  periodic_dirs=[0, 1])
    m = TBModel(lat)
    m.set_onsite([d, -d, -d, d])
    m.set_hop(g, 0, 1, [0, 0]); m.set_hop(g, 2, 3, [0, 0])
    m.set_hop(g, 0, 2, [0, 0]); m.set_hop(-g, 1, 3, [0, 0])
    m.set_hop(lam_inter, 1, 0, [1, 0]); m.set_hop(lam_inter, 3, 2, [1, 0])
    m.set_hop(lam_inter, 2, 0, [0, 1]); m.set_hop(-lam_inter, 3, 1, [0, 1])
    return m

lam_grid = np.linspace(0, 1, 41)
spec = np.array([np.sort(bbh_pump(l).make_finite(periodic_dirs=[0, 1],
                 num_cells=[8, 8]).solve_ham()) for l in lam_grid])

fig, ax = plt.subplots()
ax.plot(lam_grid, spec[:, ::6], "k-", lw=0.3)
mid = np.abs(spec) < 0.55
for i, l in enumerate(lam_grid):
    ax.plot([l] * mid[i].sum(), spec[i][mid[i]], "r.", ms=3)
ax.set_xlabel(r"$\lambda$"); ax.set_ylabel("E")
ax.set_ylim(-1.6, 1.6)
ax.set_title("BBH pump: corner levels (red) traverse the gap over one cycle")
plt.show()
caption("The quadrupole pump: finite-sample BBH spectrum along the drive cycle, "
        "with in-gap states highlighted. The four corner levels detach from the "
        "bands, meet at zero at the chiral-symmetric point λ = ½ (where the model "
        "is in its quadrupole phase), and traverse to the other band — corner "
        "charge is pumped by e/2 per corner per cycle, the higher-order echo of "
        "the Rice–Mele pump one dimension of boundary down.")

E0_half = np.abs(spec[len(lam_grid) // 2]).min()
n_zero_half = int((np.abs(spec[len(lam_grid) // 2]) < 1e-3).sum())
check("II.4: four corner zero modes at λ = 1/2", n_zero_half == 4,
      f"|E|min = {E0_half:.1e}, count = {n_zero_half}")
check("II.4: no mid-gap states at λ = 0 (trivial point)",
      np.abs(spec[0]).min() > 0.3, f"|E|min(λ=0) = {np.abs(spec[0]).min():.3f}")
check("II.4: spectrum returns after a full cycle",
      np.allclose(spec[0], spec[-1], atol=1e-10))
"""),

# ------------------------------------------------------------------ II.5
md(r"""
## II.5 — A Zak phase for the Kitaev chain

The lower BdG band's Berry phase jumps by $\pi$ at $\mu = 2t$ — numerically crisp, but its
*meaning* needs care. The BdG "valence band" is not a physical filling: the redundancy
$\mathcal{C}H\mathcal{C}^{-1} = -H$ means we diagonalize each degree of freedom twice, and the Zak
phase works as a class-D indicator here only because particle-hole symmetry quantizes it — a fact
we asserted, and PythTB cannot certify (§28). The honest invariant is the Pfaffian sign
$\mathrm{sgn}[\mathrm{Pf}\,iH(0)\cdot\mathrm{Pf}\,iH(\pi)]$; the Zak phase is its shadow.
"""),

code(r"""
def kitaev(mu, t=1.0, Delta=0.6):
    lat = Lattice(lat_vecs=[[1.0]], orb_vecs=[[0.0], [0.0]], periodic_dirs=[0])
    m = TBModel(lat)
    m.set_onsite([-mu, +mu])
    m.set_hop(-t, 0, 0, [1]); m.set_hop(+t, 1, 1, [1])
    m.set_hop(-Delta, 0, 1, [1])
    m.set_hop(+Delta, 0, 1, [-1], allow_conjugate_pair=True)
    return m

mu_scan = np.linspace(0.5, 3.5, 61)
zak = []
for mu in mu_scan:
    m = kitaev(mu)
    mesh = Mesh(["k"]); mesh.build_grid([81], k_endpoints=True)
    wfa = WFArray(m.lattice, mesh); wfa.solve_model(m)
    zak.append(float(np.squeeze(wfa.berry_phase(axis_idx=0, state_idx=[0]))) % (2 * np.pi))
zak = np.array(zak)

fig, ax = plt.subplots()
ax.plot(mu_scan, zak, "o-", ms=3)
ax.axvline(2.0, color="r", ls="--", lw=1)
ax.set_yticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])
ax.set_xlabel(r"$\mu / t$"); ax.set_ylabel("Zak phase of the lower BdG band")
ax.set_title("Kitaev chain: the Berry phase jumps by π at the topological transition")
plt.show()
caption("Zak phase of the lower BdG band versus chemical potential: pinned to π "
        "throughout the topological phase, to 0 in the trivial one, jumping "
        "discontinuously at μ = 2t where the bulk gap closes. The quantization is "
        "enforced by particle-hole symmetry — a fact WE must supply, since PythTB "
        "computes the number without knowing the symmetry class it lives in.")

# circular statistics: phases live on a circle, so flatness is |<e^{iφ}>| ≈ 1
z_topo = np.exp(1j * zak[mu_scan < 1.9])
z_triv = np.exp(1j * zak[mu_scan > 2.1])
dphi = np.abs(np.angle(z_topo.mean() / z_triv.mean()))
check("II.5: Zak phase is flat on both sides and jumps by π at μ = 2t",
      np.abs(z_topo.mean()) > 0.9999 and np.abs(z_triv.mean()) > 0.9999
      and abs(dphi - np.pi) < 1e-2,
      f"|Δφ| = {dphi:.5f}")
"""),

# ------------------------------------------------------------------ II.6
md(r"""
## II.6 — Annihilating Weyl nodes

Adding $b\,\sigma_z$ shifts the mass: nodes sit where $\cos K_z = \cos K_0 + b$ on the $k_z$
axis. For $b > 0$ they merge at $\Gamma$ at $b_c^+ = 1 - \cos K_0$ and leave a plain trivial
insulator. The $b < 0$ channel is where the exercise earns its keep: the continuum picture
("nodes annihilate at the boundary, leaving a Chern stack") is **wrong on the lattice**. Solve
the mass conditions at *all* high-symmetry columns: the original nodes at $\Gamma$-column die at
$b_c^- = -1 - \cos K_0$, but at exactly the same coupling the mass at the $X$ columns
($\cos K_z = 2 + \cos K_0 + b$) starts changing sign — a **new pair of Weyl-node families is born
at $(\pi, 0, k_z)$ and $(0, \pi, k_z)$** the instant the old ones die. Past $b_c^-$ the slice
Chern number is $+1$ between the new nodes and $-1$ outside them. The lesson generalizes:
fermion-doubling partners lurk at every zone corner of a lattice regularization, and no package —
PythTB or Kwant — will warn you when your continuum reasoning walks past one.
"""),

code(r"""
K0 = np.pi / 2
sx_ = np.array([[0, 1], [1, 0]], dtype=complex)
sy_ = np.array([[0, -1j], [1j, 0]])
sz_ = np.diag([1.0, -1.0]).astype(complex)

def weyl_b(b):
    lat = Lattice(lat_vecs=np.eye(3), orb_vecs=[[0, 0, 0]], periodic_dirs=[0, 1, 2])
    m = TBModel(lat, spinful=True)
    m.set_onsite([[0, 0, 0, 2 + np.cos(K0) + b]])
    m.set_hop(-0.5j * sx_ - 0.5 * sz_, 0, 0, [1, 0, 0])
    m.set_hop(-0.5j * sy_ - 0.5 * sz_, 0, 0, [0, 1, 0])
    m.set_hop(-0.5 * sz_, 0, 0, [0, 0, 1])
    return m

b_c = -1 - np.cos(K0)
kz_line = np.linspace(0, 0.5, 401)
k_line = np.stack([np.zeros_like(kz_line), np.zeros_like(kz_line), kz_line], axis=1)

b_scan = np.linspace(-1.4, 0.0, 29)
node_pos, min_gap = [], []
for b in b_scan:
    gap = np.diff(weyl_b(b).solve_ham(k_line), axis=1).ravel()
    min_gap.append(gap.min())
    # on a discrete kz grid a true node shows up as a near-closing at the grid scale
    node_pos.append(kz_line[np.argmin(gap)] if gap.min() < 0.02 else np.nan)

fig, ax = plt.subplots()
ax.plot(b_scan, node_pos, "o", ms=4, label=r"node position $k_z(b)$")
ax.plot(b_scan, np.arccos(np.clip(np.cos(K0) + b_scan, -1, 1)) / (2 * np.pi),
        "k--", lw=1, label=r"$\arccos(\cos K_0 + b)/2\pi$")
ax.axvline(b_c, color="r", ls="--", lw=1, label=f"$b_c = {b_c:.0f}$")
ax.set_xlabel("b"); ax.set_ylabel(r"$k_z$ of the node")
ax.legend(fontsize=8); ax.set_title("Weyl nodes slide to the zone boundary and annihilate")
plt.show()
caption("Weyl node position along kz as the σz field b is tuned: the numerically "
        "detected gap minima (circles) follow the analytic arccos law (dashed) "
        "until the nodes meet at the zone boundary at b = −1. What happens beyond "
        "is the exercise's real lesson — see the slice Chern numbers below.")

gap_after = np.array(min_gap)[b_scan < b_c - 0.05]
check("II.6: nodes exist up to b_c⁻ and the gap opens beyond",
      np.all(np.array(min_gap)[b_scan > b_c + 0.05] < 0.02)
      and np.all(gap_after > 1e-3),
      f"b_c⁻ = {b_c:.2f}")

# slice Chern numbers on both sides of the two annihilation channels
def weyl_slice_b(b):
    lat = Lattice(lat_vecs=np.eye(2), orb_vecs=[[0, 0]], periodic_dirs=[0, 1])
    m = TBModel(lat, spinful=True)
    m.set_onsite(lambda kz: [0, 0, 0, 2 + np.cos(K0) + b - np.cos(2 * np.pi * kz)],
                 ind_i=0)
    m.set_hop(-0.5j * sx_ - 0.5 * sz_, 0, 0, [1, 0])
    m.set_hop(-0.5j * sy_ - 0.5 * sz_, 0, 0, [0, 1])
    return m

# b = +1.3: clean Γ annihilation, trivial insulator
kz_probe = (np.arange(10) + 0.5) / 10 - 0.5
C_triv = [float(weyl_slice_b(+1.3).chern_number(plane=(0, 1), nks=(25, 25),
          occ_idxs=[0], kz=kz)) for kz in kz_probe]
print("b = +1.3 (Γ annihilation):        C(kz) =", np.round(C_triv, 2))
check("II.6: Γ annihilation leaves a trivial insulator (C = 0 at every kz)",
      np.allclose(np.round(C_triv), 0))

# b = -1.3: the lattice surprise — new X-column nodes at cos(Kz) = 2 + cos(K0) + b
kz_X = np.arccos(2 + np.cos(K0) - 1.3) / (2 * np.pi)
print(f"predicted new node position on the X columns: kz = ±{kz_X:.4f}")
sl_m = weyl_slice_b(-1.3)
C_in = [float(sl_m.chern_number(plane=(0, 1), nks=(31, 31), occ_idxs=[0], kz=kz))
        for kz in (0.02, 0.06)]                       # inside the new node pair
C_out = [float(sl_m.chern_number(plane=(0, 1), nks=(31, 31), occ_idxs=[0], kz=kz))
         for kz in (0.30, 0.45)]                      # outside it
print(f"b = -1.3: C(|kz| < {kz_X:.3f}) = {np.round(C_in, 3)},  "
      f"C(|kz| > {kz_X:.3f}) = {np.round(C_out, 3)}")
check("II.6: past b_c⁻ NEW nodes at the X columns flip the slice Chern to +1",
      np.allclose(np.round(C_in), 1) and np.allclose(np.round(C_out), -1),
      "the continuum 'clean annihilation' picture fails on the lattice")
# gap must close at the predicted X-column node
gap_X = np.abs(weyl_b(-1.3).solve_ham(np.array([[0.5, 0.0, kz_X]]))).min()
check("II.6: gap closes at the predicted new node (0.5, 0, kz_X)",
      gap_X < 1e-8, f"|E| = {gap_X:.1e}")
"""),
]
