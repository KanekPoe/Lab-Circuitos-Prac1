"""
========================================================
 EXPERIMENTO 1 — Circuito RL Pasa-Bajas  (ANIMADO)
 R=470Ω  rg=50Ω  rL=50Ω  L=50mH  f=1000Hz  Vm=5V
========================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec

# ── Parámetros ─────────────────────────────────────────
R  = 470; rg = 50; rL = 50; L = 50e-3; Vm = 5; f = 1000
omega = 2 * np.pi * f
R_total = R + rg + rL

H_jw      = R / (R_total + 1j * omega * L)
mag       = abs(H_jw)
phi       = np.angle(H_jw)
phi_deg   = np.degrees(phi)
Vo_amp    = Vm * mag
phi_teo   = -np.degrees(np.arctan(omega * L / (rL + R)))

# ── Ventana de tiempo del "osciloscopio" ───────────────
T          = 1 / f
N_cycles   = 3
t_window   = N_cycles * T
N_pts      = 600
t_display  = np.linspace(0, t_window, N_pts)

# ── Estética ───────────────────────────────────────────
BG    = '#0a0f0a'; GRID  = '#1a2e1a'
GREEN = '#00ff41'; YEL   = '#ffdd00'; CYAN  = '#00e5ff'; WHITE = '#e8f5e9'

fig = plt.figure(figsize=(13, 7), facecolor=BG)
fig.patch.set_facecolor(BG)
gs  = GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.38)

# Panel principal osciloscopio
ax_osc = fig.add_subplot(gs[0, :])
ax_osc.set_facecolor(BG)
for sp in ax_osc.spines.values(): sp.set_edgecolor(GRID)
for y in np.arange(-6, 7, 1):    ax_osc.axhline(y, color=GRID, lw=0.6)
for x in np.linspace(0, t_window*1e3, 25): ax_osc.axvline(x, color=GRID, lw=0.6)
ax_osc.axhline(0, color='#2a4a2a', lw=1.2)
ax_osc.set_xlim(0, t_window * 1e3)
ax_osc.set_ylim(-6.5, 6.5)
ax_osc.set_xlabel('Tiempo [ms]', color=WHITE, fontsize=9)
ax_osc.set_ylabel('Voltaje [V]', color=WHITE, fontsize=9)
ax_osc.tick_params(colors=WHITE, labelsize=8)
ax_osc.set_title('  CH1/CH2 — CIRCUITO RL PASA-BAJAS | EXP.1  (ANIMACIÓN EN VIVO)',
                 color=GREEN, fontsize=11, pad=8, loc='left')

line_vi, = ax_osc.plot([], [], color=GREEN, lw=1.8,
                        label=f'vi(t)  entrada  {Vm}V  {f}Hz')
line_vo, = ax_osc.plot([], [], color=YEL,   lw=1.8,
                        label=f'vo(t)  salida   {Vo_amp:.3f}V  φ={phi_deg:.1f}°')
ax_osc.legend(loc='upper right', facecolor='#0d1a0d',
              edgecolor=GRID, labelcolor=WHITE, fontsize=8)

# Marcador de tiempo (línea vertical que barre)
time_marker, = ax_osc.plot([], [], color='#ffffff33', lw=1.0)

# Panel fasorial ────────────────────────────────────────
ax_fas = fig.add_subplot(gs[1, 0], polar=True)
ax_fas.set_facecolor('#050d05')
ax_fas.spines['polar'].set_color(GRID)
ax_fas.tick_params(colors=WHITE, labelsize=6)
ax_fas.set_title('Fasores\n(rotando)', color=CYAN, fontsize=8, pad=10)
arr_vi = ax_fas.annotate('', xy=(0, Vm),      xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.2))
arr_vo = ax_fas.annotate('', xy=(phi, Vo_amp), xytext=(0,0),
    arrowprops=dict(arrowstyle='->', color=YEL,   lw=2.2))

# Punto en tiempo real sobre la onda ────────────────────
dot_vi, = ax_osc.plot([], [], 'o', color=GREEN, ms=7, zorder=6)
dot_vo, = ax_osc.plot([], [], 'o', color=YEL,   ms=7, zorder=6)

# Panel de valores numéricos ────────────────────────────
ax_num = fig.add_subplot(gs[1, 1:])
ax_num.set_facecolor('#050d05'); ax_num.axis('off')
rows = [
    ('R total',    f'{R_total} Ω',        WHITE),
    ('L',          f'{L*1e3:.0f} mH',     WHITE),
    ('f',          f'{f} Hz',             WHITE),
    ('ω',          f'{omega:.1f} rad/s',  WHITE),
    ('|H(jω)|',    f'{mag:.4f}',          YEL),
    ('Vo amplitud',f'{Vo_amp:.4f} V',     YEL),
    ('φ medido',   f'{phi_deg:.3f}°',     YEL),
    ('φ teórico',  f'{phi_teo:.3f}°',     CYAN),
    ('Tipo',       'PASA-BAJAS  ⬇',       '#ff6b35'),
    ('Desfase',    'Salida ATRASADA  ◀',  '#ff6b35'),
]
yp = 0.95
for lbl, val, col in rows:
    ax_num.text(0.04, yp, lbl,  color=WHITE, fontsize=8.5, transform=ax_num.transAxes, va='top', fontfamily='monospace')
    ax_num.text(0.52, yp, val,  color=col,   fontsize=8.5, transform=ax_num.transAxes, va='top', fontfamily='monospace')
    yp -= 0.092

fig.text(0.01,0.98,'MADO-64 | Exp.1 — RL Pasa-Bajas | R=470Ω rL=50Ω L=50mH f=1kHz',
         color='#3a5a3a', fontsize=7.5, fontfamily='monospace')

# ── Animación ──────────────────────────────────────────
FRAMES  = 300
t_phase = np.linspace(0, 2 * np.pi, FRAMES, endpoint=False)  # fase que avanza

def animate(i):
    phase_offset = t_phase[i]           # cuánto ha "corrido" el tiempo

    # señales visibles en pantalla (ventana fija, señal se desplaza)
    vi_vals = Vm      * np.sin(omega * t_display - phase_offset)
    vo_vals = Vo_amp  * np.sin(omega * t_display - phase_offset + phi)

    line_vi.set_data(t_display * 1e3, vi_vals)
    line_vo.set_data(t_display * 1e3, vo_vals)

    # punto actual al borde derecho de la ventana
    dot_vi.set_data([t_display[-1]*1e3], [vi_vals[-1]])
    dot_vo.set_data([t_display[-1]*1e3], [vo_vals[-1]])

    # fasores rotan con el tiempo
    angle_now = -phase_offset % (2*np.pi)
    arr_vi.xy      = (angle_now,        Vm)
    arr_vi.xytext  = (0, 0)
    arr_vo.xy      = (angle_now + phi,  Vo_amp)
    arr_vo.xytext  = (0, 0)

    return line_vi, line_vo, dot_vi, dot_vo

ani = animation.FuncAnimation(fig, animate, frames=FRAMES,
                               interval=25, blit=True)
plt.tight_layout()
plt.show()
