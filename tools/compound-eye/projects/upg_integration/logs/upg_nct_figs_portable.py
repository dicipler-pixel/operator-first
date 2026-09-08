# SCRIPT: UPG-NCT-FIGS
# Figures for Module I, noncommutative torus anchor.
#   fig_nct_domain.png : the admissible domain  delta + g^2 <= 4
#   fig_nct_floor.png  : the amplitude floor    w != 0  =>  delta >= 16/d^2

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK   = "#1b1f24"
LINE  = "#1a4f8a"
ACC   = "#b03a2e"
FILL  = "#dfe8f2"
WARN  = "#f2d7d2"

# ----------------------------------------------------------------- figure A
fig, ax = plt.subplots(figsize=(7.0, 4.6))

d_line = np.linspace(0, 4, 400)
ax.fill_between(d_line, 0, 4 - d_line, color=FILL, zorder=0)
ax.plot(d_line, 4 - d_line, color=LINE, lw=2.2, zorder=3)

tau2 = 0.30
ax.fill_between([0, 4], 0, tau2, color=WARN, zorder=1)
ax.axhline(tau2, color=ACC, lw=1.1, ls="--", zorder=2)

ds = np.array([2, 3, 4, 5, 7, 11, 17, 31, 53, 97])
delta = 4*np.sin(np.pi/ds)**2
g2 = 4*np.cos(np.pi/ds)**2
ax.plot(delta[1:], g2[1:], "o", ms=6.5, color=LINE, mec="white", mew=1.0, zorder=5)
ax.plot(delta[:1], g2[:1], "o", ms=8.5, color=ACC, mec="white", mew=1.2, zorder=6)

ax.annotate("", xy=(0.45, 2.55), xytext=(1.75, 1.35),
            arrowprops=dict(arrowstyle="->", color=LINE, lw=1.4))
ax.text(0.95, 1.72, "d increasing", fontsize=10.5, color=LINE, rotation=-31)
ax.annotate("d = 2", (delta[0], g2[0]), textcoords="offset points",
            xytext=(-98, 6), fontsize=9.5, color=ACC,
            arrowprops=dict(arrowstyle="-", color=ACC, lw=0.9))

ax.text(0.28, 3.30, r"$\delta + g^{2} \leq 4$", fontsize=21, color=INK)
ax.text(2.28, 2.10, "scalar relators", fontsize=10.5, color=LINE, rotation=-31)
ax.text(0.12, 0.10, "no admissible branch", fontsize=10.5, color=ACC)

ax.set_xlabel(r"defect   $\delta = \|R-I\|_F^{2}/d$", fontsize=11.5, color=INK)
ax.set_ylabel(r"branch guard   $g^{2}$", fontsize=11.5, color=INK)
ax.set_xlim(0, 4.35); ax.set_ylim(0, 4.35)
ax.set_xticks([0, 1, 2, 3, 4]); ax.set_yticks([0, 1, 2, 3, 4])
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=INK, labelsize=10)
fig.tight_layout()
fig.savefig("/workspace/scratch/8fecb5f5845b/tmp/upg/universal/projects/upg_integration/figures/fig_nct_domain.png", dpi=220)
plt.close(fig)

# ----------------------------------------------------------------- figure B
fig, ax = plt.subplots(figsize=(7.0, 4.6))

dd = np.linspace(3, 400, 3000)
floor = 16/dd**2
meas = 4*np.sin(np.pi/dd)**2
ax.fill_between(dd, 1e-6, floor, color=WARN, zorder=0)
ax.plot(dd, floor, color=ACC, lw=2.0, zorder=3)
ax.plot(dd, meas, color=LINE, lw=2.0, zorder=3)

dm = np.array([3, 5, 7, 11, 17, 31, 53, 97])
ax.plot(dm, 4*np.sin(np.pi/dm)**2, "o", ms=6.0, color=LINE,
        mec="white", mew=1.0, zorder=5)

ax.text(4.6, 0.0016, r"$w \neq 0 \;\Rightarrow\; \delta \geq 16/d^{2}$",
        fontsize=19, color=INK)
ax.text(38, 2.4e-4, "no integer record", fontsize=10.5, color=ACC)
ax.text(9.5, 0.62, "clock and shift", fontsize=10.5, color=LINE)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("dimension  $d$", fontsize=11.5, color=INK)
ax.set_ylabel(r"defect  $\delta$", fontsize=11.5, color=INK)
ax.set_xlim(3, 400); ax.set_ylim(8e-5, 6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(colors=INK, labelsize=10)
fig.tight_layout()
fig.savefig("/workspace/scratch/8fecb5f5845b/tmp/upg/universal/projects/upg_integration/figures/fig_nct_floor.png", dpi=220)
plt.close(fig)

print("figures written")
print("ratio measured/floor (asymptotic) =", 4*np.pi**2/16)
