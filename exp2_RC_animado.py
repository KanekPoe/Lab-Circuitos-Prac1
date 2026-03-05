"""
========================================================
 EXPERIMENTO 2 — Circuito RC Pasa-Altas  (ANIMADO)
 R=470Ω  rg=50Ω  C=0.1µF  f=1000Hz  Vm=5V
========================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec

# ── Parámetros ─────────────────────────────────────────
R  = 470; rg = 50; C = 0.1e-6; Vm = 5; f = 1000
omega   = 2 * np.pi * f
R_total = R + rg
Xc      = 1 / (omega * C)

H_jw    = (1j * omega * R * C) / (1 + 1j * omega * R_total * C)
mag     = abs(H_jw)
phi     = np.angle(H_jw)
phi_deg = np.degrees(phi)
Vo_amp  = Vm * mag
phi_teo = 90 - np.degrees(np.arctan(omega * R * C))

T        = 1 / f
t_window = 3 * T
N_pts    = 600
t_disp   = np.linspace(0, t_window, N_pts)

# ── Estética azul/rosa ─────────────────────────────────
BG    = '#060810'; GRID  = '#12183a'
BLUE  = '#4fc3f7'; PINK  = '#ff4081'; CYAN  = '#00e5ff'
AMBER = '#ffab40'; WHITE = '#e3f2fd'

fig = plt.figure(figsize=(13, 7), facecolor=BG)
fig.patch.set_facecolor(BG)
gs  = GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.38)

ax_osc = fig.add_subplot(gs[0, :])
ax_osc.set_facecolor(BG)
for sp in ax_osc.spines.values(): sp.set_edgecolor(GRID)
for y in np.arange(-6, 7, 1):    ax_osc.axhline(y, color=GRID, lw=0.6)
for x in np.linspace(0, t_window*1e3, 25): ax_osc.axvline(x, color=GRID, lw=0.6)
ax_osc.axhline(0, color='#1a2550', lw=1.2)
ax_osc.set_xlim(0, t_window * 1e3)
ax_osc.set_ylim(-6.5, 6.5)
ax_osc.set_xlabel('Tiempo [ms]', color=WHITE, fontsize=9)
ax_osc.set_ylabel('Voltaje [V]', color=WHITE, fontsize=9)
ax_osc.tick_params(colors=WHITE, labelsize=8)
ax_osc.set_title('  CH1/CH2 — CIRCUITO RC PASA-ALTAS | EXP.2  (ANIMACIÓN EN VIVO)',
                 color=BLUE, fontsize=11, pad=8, loc='left')

line_vi, = ax_osc.plot([], [], color=BLUE, lw=1.8,
                        label=f'vi(t)  entrada  {Vm}V  {f}Hz')
line_vo, = ax_osc.plot([], [], color=PINK, lw=1.8,
                        label=f'vo(t)  salida   {Vo_amp:.3f}V  φ=+{phi_deg:.1f}°')
ax_osc.legend(loc='upper right', facecolor='#090c1a',
              edgecolor=GRID, labelcolor=WHITE, fontsize=8)

dot_vi, = ax_osc.plot([], [], 'o', color=BLUE, ms=7, zorder=6)
dot_vo, = ax_osc.plot([], [], 'o', color=PINK, ms=7, zorder=6)

# Anotación de adelanto (flecha dinámica)
arrow_ann = ax_osc.annotate('', xy=(0,0), xytext=(0,0),
    arrowprops=dict(arrowstyle='<->', color=AMBER, lw=1.5))
label_ann = ax_osc.text(0, 6.2, '', color=AMBER, fontsize=7.5, ha='center')

# Panel fasorial ────────────────────────────────────────
ax_fas = fig.add_subplot(gs[1, 0], polar=True)
ax_fas.set_facecolor('#05070f')
ax_fas.spines['polar'].set_color(GRID)
ax_fas.tick_params(colors=WHITE, labelsize=6)
ax_fas.set_title('Fasores\n(rotando)', color=CYAN, fontsize=8, pad=10)
arr_vi = ax_fas.annotate('', xy=(0, Vm),      xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color=BLUE, lw=2.2))
arr_vo = ax_fas.annotate('', xy=(phi, Vo_amp), xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color=PINK, lw=2.2))

# Panel numérico ────────────────────────────────────────
ax_num = fig.add_subplot(gs[1, 1:])
ax_num.set_facecolor('#05070f'); ax_num.axis('off')
rows = [
    ('R carga',    f'{R} Ω',             WHITE),
    ('rg',         f'{rg} Ω',            WHITE),
    ('C',          f'{C*1e6:.1f} µF',    WHITE),
    ('Xc = 1/ωC', f'{Xc:.2f} Ω',        WHITE),
    ('τ = RC',     f'{R_total*C*1e6:.2f} µs', WHITE),
    ('|H(jω)|',    f'{mag:.4f}',         PINK),
    ('Vo amplitud',f'{Vo_amp:.4f} V',    PINK),
    ('φ medido',   f'+{phi_deg:.3f}°',   PINK),
    ('φ teórico',  f'+{phi_teo:.3f}°',   CYAN),
    ('Tipo',       'PASA-ALTAS  ⬆',      '#69f0ae'),
    ('Desfase',    'Salida ADELANTADA ▶','#69f0ae'),
]
yp = 0.95
for lbl, val, col in rows:
    ax_num.text(0.04, yp, lbl,  color=WHITE, fontsize=8.5, transform=ax_num.transAxes, va='top', fontfamily='monospace')
    ax_num.text(0.52, yp, val,  color=col,   fontsize=8.5, transform=ax_num.transAxes, va='top', fontfamily='monospace')
    yp -= 0.092

fig.text(0.01,0.98,'MADO-64 | Exp.2 — RC Pasa-Altas | R=470Ω C=0.1µF f=1kHz',
         color='#1a2550', fontsize=7.5, fontfamily='monospace')

# ── Animación ──────────────────────────────────────────
FRAMES   = 300
t_phase  = np.linspace(0, 2 * np.pi, FRAMES, endpoint=False)

def animate(i):
    phase_offset = t_phase[i]

    vi_vals = Vm     * np.sin(omega * t_disp - phase_offset)
    vo_vals = Vo_amp * np.sin(omega * t_disp - phase_offset + phi)

    line_vi.set_data(t_disp * 1e3, vi_vals)
    line_vo.set_data(t_disp * 1e3, vo_vals)

    dot_vi.set_data([t_disp[-1]*1e3], [vi_vals[-1]])
    dot_vo.set_data([t_disp[-1]*1e3], [vo_vals[-1]])

    # Flecha que muestra el adelanto entre cruces por cero
    t_cross_vi = (phase_offset) / omega
    t_cross_vo = t_cross_vi - phi / omega   # phi > 0 → vo cruza antes
    tc_vi_ms = (t_cross_vi % t_window) * 1e3
    tc_vo_ms = (t_cross_vo % t_window) * 1e3
    if 0 < tc_vi_ms < t_window*1e3 and 0 < tc_vo_ms < t_window*1e3:
        arrow_ann.xy      = (tc_vi_ms, 0.6)
        arrow_ann.xytext  = (tc_vo_ms, 0.6)
        label_ann.set_position(((tc_vi_ms + tc_vo_ms)/2, 1.0))
        label_ann.set_text(f'Δt adelanto = {abs(phi/(omega))*1e6:.1f} µs')

    # Fasores rotan
    angle_now = -phase_offset % (2*np.pi)
    arr_vi.xy     = (angle_now,       Vm)
    arr_vi.xytext = (0, 0)
    arr_vo.xy     = (angle_now + phi, Vo_amp)
    arr_vo.xytext = (0, 0)

    return line_vi, line_vo, dot_vi, dot_vo, label_ann

ani = animation.FuncAnimation(fig, animate, frames=FRAMES,
                               interval=25, blit=True)
plt.tight_layout()
plt.show()
