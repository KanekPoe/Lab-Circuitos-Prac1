"""
========================================================
 EXPERIMENTO 3 — Circuito RLC Serie Pasa-Banda (ANIMADO)
 R=1000Ω  rg=50Ω  rL=50Ω  L=60mH  C=10nF  Vm=5V
 ► Usa el SLIDER para barrer la frecuencia y ver
   cómo cambia la amplitud y el desfase en vivo,
   igual que en el laboratorio con el generador.
========================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider, Button

# ── Parámetros fijos ───────────────────────────────────
R  = 1000; rg = 50; rL = 50; L = 60e-3; C = 10e-9; Vm = 5
R_total = R + rg + rL
fo  = 1 / (2 * np.pi * np.sqrt(L * C))
fp  = 0.9 * fo

def H(omega_val):
    num = 1j * omega_val * R / L
    den = (1j*omega_val)**2 + (R_total/L)*1j*omega_val + 1/(L*C)
    return num / den

# ── Estado mutable ─────────────────────────────────────
state = {'f': fp, 'paused': False}

T_win  = lambda f: 3 / f
N_pts  = 800

# ── Figura ─────────────────────────────────────────────
BG    = '#080a08'; GRID  = '#1a2a1a'
GREEN = '#00ff41'; CYAN  = '#00e5ff'; PINK  = '#ff4081'
AMBER = '#ffab40'; WHITE = '#e8ffe8'; PURPLE= '#b39ddb'

fig = plt.figure(figsize=(14, 9), facecolor=BG)
fig.patch.set_facecolor(BG)
gs = GridSpec(3, 3, figure=fig,
              top=0.93, bottom=0.18, hspace=0.55, wspace=0.38)

# ── Panel osciloscopio principal ───────────────────────
ax_osc = fig.add_subplot(gs[0, :])
ax_osc.set_facecolor(BG)
for sp in ax_osc.spines.values(): sp.set_edgecolor(GRID)
for y in np.arange(-6,7,1): ax_osc.axhline(y, color=GRID, lw=0.6)
ax_osc.axhline(0, color='#1a3a1a', lw=1.2)
ax_osc.set_ylim(-6.5, 6.5)
ax_osc.set_xlabel('Tiempo [ms]', color=WHITE, fontsize=9)
ax_osc.set_ylabel('Voltaje [V]', color=WHITE, fontsize=9)
ax_osc.tick_params(colors=WHITE, labelsize=8)

line_vi, = ax_osc.plot([], [], color=CYAN,  lw=1.8, label='vi(t) entrada')
line_vo, = ax_osc.plot([], [], color=GREEN, lw=2.0, label='vo(t) salida')
dot_vi,  = ax_osc.plot([], [], 'o', color=CYAN,  ms=8, zorder=6)
dot_vo,  = ax_osc.plot([], [], 'o', color=GREEN, ms=8, zorder=6)
title_txt = ax_osc.set_title('', color=GREEN, fontsize=10, pad=6, loc='left')
leg = ax_osc.legend(loc='upper right', facecolor='#0a120a',
                    edgecolor=GRID, labelcolor=WHITE, fontsize=8)

# ── Panel Bode (amplitud) ──────────────────────────────
ax_bode = fig.add_subplot(gs[1, :2])
ax_bode.set_facecolor(BG)
for sp in ax_bode.spines.values(): sp.set_edgecolor(GRID)
f_sw  = np.logspace(2, 6, 1500)
w_sw  = 2*np.pi*f_sw
H_dB  = 20*np.log10(np.abs([H(w) for w in w_sw]) + 1e-12)
phi_sw= np.degrees([np.angle(H(w)) for w in w_sw])
for yg in np.arange(-70,5,10): ax_bode.axhline(yg, color=GRID, lw=0.5)
ax_bode.semilogx(f_sw, H_dB, color=PURPLE, lw=1.8, label='|H(jf)| dB')
ax_bode.axvline(fo, color=AMBER, lw=1.4, ls='--', label=f'fo={fo:.0f}Hz')
ax_bode.set_xlim(f_sw[0], f_sw[-1])
ax_bode.set_ylim(-70, 5)
ax_bode.set_xlabel('Frecuencia [Hz]', color=WHITE, fontsize=8)
ax_bode.set_ylabel('|H| [dB]',        color=WHITE, fontsize=8)
ax_bode.tick_params(colors=WHITE, labelsize=7, which='both')
ax_bode.set_title('  Bode — Amplitud  (punto rojo = frecuencia actual)',
                  color=PURPLE, fontsize=8, pad=4, loc='left')
ax_bode.legend(facecolor='#0a120a', edgecolor=GRID, labelcolor=WHITE, fontsize=7)
bode_dot, = ax_bode.plot([], [], 'o', color=PINK, ms=9, zorder=6)

# ── Panel fase ─────────────────────────────────────────
ax_phase = fig.add_subplot(gs[2, :2])
ax_phase.set_facecolor(BG)
for sp in ax_phase.spines.values(): sp.set_edgecolor(GRID)
for yg in np.arange(-90,100,30): ax_phase.axhline(yg, color=GRID, lw=0.5)
ax_phase.semilogx(f_sw, phi_sw, color='#80cbc4', lw=1.8, label='∠H(jf) °')
ax_phase.axvline(fo, color=AMBER, lw=1.4, ls='--')
ax_phase.axhline(0,  color='#2a4a2a', lw=1.0)
ax_phase.set_xlim(f_sw[0], f_sw[-1])
ax_phase.set_ylim(-100, 100)
ax_phase.set_xlabel('Frecuencia [Hz]', color=WHITE, fontsize=8)
ax_phase.set_ylabel('Fase [°]',        color=WHITE, fontsize=8)
ax_phase.tick_params(colors=WHITE, labelsize=7, which='both')
ax_phase.set_title('  Bode — Fase',    color='#80cbc4', fontsize=8, pad=4, loc='left')
ax_phase.legend(facecolor='#0a120a', edgecolor=GRID, labelcolor=WHITE, fontsize=7)
phase_dot, = ax_phase.plot([], [], 'o', color=PINK, ms=9, zorder=6)

# ── Panel info ─────────────────────────────────────────
ax_info = fig.add_subplot(gs[1:, 2])
ax_info.set_facecolor('#04080a'); ax_info.axis('off')
info_lines = {}
static_rows = [
    ('R',    f'{R} Ω',           WHITE),
    ('rg',   f'{rg} Ω',          WHITE),
    ('rL',   f'{rL} Ω',          WHITE),
    ('L',    f'{L*1e3:.0f} mH',  WHITE),
    ('C',    f'{C*1e9:.0f} nF',  WHITE),
    ('fo',   f'{fo:.1f} Hz',     AMBER),
    ('fp',   f'{fp:.1f} Hz',     '#ff6b6b'),
]
yp = 0.99
ax_info.text(0.04, yp, '── CIRCUITO RLC ──', color=CYAN, fontsize=7.5,
             transform=ax_info.transAxes, va='top', fontfamily='monospace')
yp -= 0.07
for lbl, val, col in static_rows:
    ax_info.text(0.04, yp, lbl,  color=WHITE, fontsize=8, transform=ax_info.transAxes, va='top', fontfamily='monospace')
    ax_info.text(0.55, yp, val,  color=col,   fontsize=8, transform=ax_info.transAxes, va='top', fontfamily='monospace')
    yp -= 0.07
ax_info.text(0.04, yp, '── EN TIEMPO REAL ──', color=CYAN, fontsize=7.5,
             transform=ax_info.transAxes, va='top', fontfamily='monospace')
yp -= 0.07

dyn_labels = ['f actual', '|H|', 'Vo amp', 'φ', 'Relación f/fo', 'Estado']
dyn_txts   = {}
for lbl in dyn_labels:
    ax_info.text(0.04, yp, lbl, color=WHITE, fontsize=8,
                 transform=ax_info.transAxes, va='top', fontfamily='monospace')
    dyn_txts[lbl] = ax_info.text(0.55, yp, '---', color=GREEN, fontsize=8,
                                  transform=ax_info.transAxes, va='top', fontfamily='monospace')
    yp -= 0.07

# ── Slider de frecuencia ───────────────────────────────
ax_sl = fig.add_axes([0.12, 0.07, 0.60, 0.025], facecolor='#0d1a0d')
slider_f = Slider(ax_sl, 'Frecuencia [Hz]', fo*0.2, fo*3.0,
                  valinit=fp, color=GREEN, track_color='#1a2a1a')
slider_f.label.set_color(WHITE)
slider_f.valtext.set_color(CYAN)

# Botón pausa ──────────────────────────────────────────
ax_btn = fig.add_axes([0.80, 0.055, 0.10, 0.04], facecolor='#1a2a1a')
btn_pause = Button(ax_btn, '⏸ PAUSA', color='#1a2a1a', hovercolor='#2a4a2a')
btn_pause.label.set_color(WHITE)

def toggle_pause(event):
    state['paused'] = not state['paused']
    btn_pause.label.set_text('▶ PLAY' if state['paused'] else '⏸ PAUSA')

btn_pause.on_clicked(toggle_pause)

def update_slider(val):
    state['f'] = slider_f.val

slider_f.on_changed(update_slider)

fig.text(0.01, 0.97,
         'MADO-64 | Exp.3 — RLC Pasa-Banda | Usa el SLIDER para barrer la frecuencia',
         color='#1a3a1a', fontsize=7.5, fontfamily='monospace')

# ── Animación ──────────────────────────────────────────
FRAMES  = 300
t_phase = np.linspace(0, 2*np.pi, FRAMES, endpoint=False)

def animate(i):
    if state['paused']:
        return line_vi, line_vo, dot_vi, dot_vo, bode_dot, phase_dot

    f_cur  = state['f']
    w_cur  = 2 * np.pi * f_cur
    H_cur  = H(w_cur)
    mag_c  = abs(H_cur)
    phi_c  = np.angle(H_cur)
    phi_d  = np.degrees(phi_c)
    Vo_c   = Vm * mag_c

    # ventana de tiempo adaptativa a la frecuencia
    tw = 3 / f_cur
    t_d = np.linspace(0, tw, N_pts)
    ph_off = t_phase[i]

    vi_v = Vm   * np.sin(w_cur * t_d - ph_off)
    vo_v = Vo_c * np.sin(w_cur * t_d - ph_off + phi_c)

    line_vi.set_data(t_d * 1e3, vi_v)
    line_vo.set_data(t_d * 1e3, vo_v)
    dot_vi.set_data([t_d[-1]*1e3], [vi_v[-1]])
    dot_vo.set_data([t_d[-1]*1e3], [vo_v[-1]])

    ax_osc.set_xlim(0, tw * 1e3)
    # rejilla dinámica
    for line in ax_osc.get_lines():
        if line not in [line_vi, line_vo, dot_vi, dot_vo]:
            pass

    # color según posición respecto a fo
    ratio = f_cur / fo
    if   ratio < 0.97:  col_title = '#ffab40'; estado = f'f < fo  (adelanto φ=+{abs(phi_d):.1f}°)'
    elif ratio > 1.03:  col_title = PINK;       estado = f'f > fo  (atraso  φ={phi_d:.1f}°)'
    else:               col_title = GREEN;       estado = f'≈ RESONANCIA  φ≈0°'

    line_vo.set_color(col_title)
    dot_vo.set_color(col_title)

    title_txt.set_text(
        f'  CH1/CH2 — RLC PASA-BANDA | EXP.3  '
        f'f={f_cur:.0f}Hz  Vo={Vo_c:.3f}V  φ={phi_d:+.1f}°')
    title_txt.set_color(col_title)

    # actualizar punto en Bode
    H_dB_cur = 20*np.log10(mag_c + 1e-12)
    bode_dot.set_data([f_cur], [H_dB_cur])
    phase_dot.set_data([f_cur], [phi_d])

    # actualizar texto dinámico
    dyn_txts['f actual'].set_text(f'{f_cur:.1f} Hz')
    dyn_txts['|H|'].set_text(f'{mag_c:.4f}')
    dyn_txts['Vo amp'].set_text(f'{Vo_c:.4f} V')
    dyn_txts['φ'].set_text(f'{phi_d:+.2f}°')
    dyn_txts['Relación f/fo'].set_text(f'{ratio:.3f}')
    dyn_txts['Estado'].set_text(estado[:18])
    for k, txt in dyn_txts.items():
        txt.set_color(col_title)

    return line_vi, line_vo, dot_vi, dot_vo, bode_dot, phase_dot, title_txt

ani = animation.FuncAnimation(fig, animate, frames=FRAMES,
                               interval=25, blit=False)
plt.show()
