"""
generate_figures.py — Gambar 4 dan Gambar 5 untuk skripsi (hitam putih)
Jalankan: python generate_figures.py
Output: gambar4_ontologi_dag.png, gambar5_p0_distribution.png
"""

import json, sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Load data ──────────────────────────────────────────────────────────────────
with open('data/math_grade1.json') as f:
    data = json.load(f)

kcs  = data['knowledge_components']
rels = data['prerequisites']

G = nx.DiGraph()
for k in kcs:
    G.add_node(k['id'], **k)
for r in rels:
    G.add_edge(r[0], r[1])

kc_map  = {k['id']: k for k in kcs}
ALL_KCS = [k['id'] for k in kcs]

TOPIC_LABELS = {
    'bilangan':   'Bilangan',
    'operasi':    'Operasi Bilangan',
    'geometri':   'Geometri',
    'pengukuran': 'Pengukuran',
    'pola':       'Pola & Aljabar',
}

# Grayscale fill per domain (dari gelap ke terang)
TOPIC_FILL = {
    'bilangan':   '#1a1a1a',
    'operasi':    '#444444',
    'geometri':   '#777777',
    'pengukuran': '#aaaaaa',
    'pola':       '#cccccc',
}


def get_prior(kc_id: str) -> float:
    """P(L₀) dari posisi KC dalam graf ontologi."""
    ancestors  = len(nx.ancestors(G, kc_id))
    difficulty = kc_map[kc_id]['difficulty']
    base = 0.35 - (difficulty - 1) * 0.05 - ancestors * 0.015
    return round(max(0.05, min(0.35, base)), 3)


# ══════════════════════════════════════════════════════════════════════════════
# GAMBAR 4 — Graf Ontologi DAG, hitam putih
# ══════════════════════════════════════════════════════════════════════════════
POS = {
    'KC-B01': (0, 8),    'KC-B02': (0, 6.5),  'KC-B03': (1.5, 6.5),
    'KC-B04': (0.75, 5), 'KC-B05': (2.2, 5),  'KC-B06': (-0.8, 5),
    'KC-B07': (0.75, 3.5),'KC-B08': (0.75, 2),
    'KC-O01': (4.5, 5),  'KC-O02': (4.5, 3.5),'KC-O03': (5.5, 2),
    'KC-O04': (6.5, 5),  'KC-O05': (6.5, 3.5),'KC-O06': (7.5, 2),
    'KC-O07': (6, 0.5),
    'KC-G01': (10, 8),   'KC-G02': (9.2, 6.5),'KC-G03': (10.8, 5),
    'KC-P01': (12.5, 8), 'KC-P02': (12.5, 6.5),'KC-P03': (12.5, 5),
    'KC-A01': (12.5, 3.5),'KC-A02': (12.5, 2),
}

NAME_SHORT = {
    'KC-B01': 'Mengenal\nbilangan 1–10',
    'KC-B02': 'Membilang\n1–10',
    'KC-B03': 'Mengenal\nbilangan 11–20',
    'KC-B04': 'Membilang\n11–20',
    'KC-B05': 'Membanding\nbilangan',
    'KC-B06': 'Urutan\nbilangan',
    'KC-B07': 'Nilai tempat\nsatuan',
    'KC-B08': 'Nilai tempat\npuluhan',
    'KC-O01': 'Konsep\npenjumlahan',
    'KC-O02': 'Penjumlahan\ns.d. 10',
    'KC-O03': 'Penjumlahan\ns.d. 20',
    'KC-O04': 'Konsep\npengurangan',
    'KC-O05': 'Pengurangan\ns.d. 10',
    'KC-O06': 'Pengurangan\ns.d. 20',
    'KC-O07': 'Hub. + dan −',
    'KC-G01': 'Mengenal\nbangun datar',
    'KC-G02': 'Sifat\nbangun datar',
    'KC-G03': 'Mengelompok\nbangun datar',
    'KC-P01': 'Perbandingan\npanjang',
    'KC-P02': 'Perbandingan\nberat',
    'KC-P03': 'Urutan\nkejadian',
    'KC-A01': 'Mengenal\npola',
    'KC-A02': 'Melanjutkan\npola',
}

LABEL_OFFSET = {
    'KC-B01': (-1, 0), 'KC-B02': (-1, 0), 'KC-B03': (1, 0),
    'KC-B04': (-1, 0), 'KC-B05': (1, 0),  'KC-B06': (-1, 0),
    'KC-B07': (-1, 0), 'KC-B08': (-1, 0),
    'KC-O01': (-1, 0), 'KC-O02': (-1, 0), 'KC-O03': (-1, 0),
    'KC-O04': (1, 0),  'KC-O05': (1, 0),  'KC-O06': (1, 0),
    'KC-O07': (0, -0.9),
    'KC-G01': (1, 0),  'KC-G02': (-1, 0), 'KC-G03': (1, 0),
    'KC-P01': (1, 0),  'KC-P02': (1, 0),  'KC-P03': (1, 0),
    'KC-A01': (1, 0),  'KC-A02': (1, 0),
}

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Edges
for u, v in G.edges():
    x0, y0 = POS[u]
    x1, y1 = POS[v]
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(
            arrowstyle="-|>", color='#555555',
            lw=1.4, mutation_scale=13,
            connectionstyle="arc3,rad=0.05"
        )
    )

# Nodes
NODE_R = 0.52
for kc_id, (x, y) in POS.items():
    topic = kc_map[kc_id]['topic']
    fill  = TOPIC_FILL[topic]
    txt_c = 'white' if topic in ('bilangan', 'operasi', 'geometri') else '#111111'
    circle = plt.Circle((x, y), NODE_R, color=fill, zorder=3,
                         ec='#333333', lw=1.2)
    ax.add_patch(circle)
    short = kc_id.replace('KC-', '')
    ax.text(x, y, short, ha='center', va='center',
            fontsize=7.5, fontweight='bold', color=txt_c, zorder=4)

# Labels
for kc_id, (x, y) in POS.items():
    ox, oy = LABEL_OFFSET.get(kc_id, (1, 0))
    ax.text(
        x + ox * 0.75, y + oy * 0.75,
        NAME_SHORT[kc_id],
        ha='center' if oy != 0 else ('right' if ox < 0 else 'left'),
        va='center',
        fontsize=6, color='#222222', zorder=4, linespacing=1.3
    )

# Legend
patches = [
    mpatches.Patch(facecolor=TOPIC_FILL[t], edgecolor='#333',
                   label=TOPIC_LABELS[t], linewidth=0.8)
    for t in TOPIC_LABELS
]
ax.legend(handles=patches, loc='lower left', fontsize=8,
          framealpha=0.95, title='Domain', title_fontsize=8.5,
          edgecolor='#333')

ax.text(0.01, 0.015,
        'Arah panah: KC prasyarat → KC dependen',
        transform=ax.transAxes, fontsize=7, color='#444', va='bottom')

ax.set_title(
    'Gambar 4  Graf Ontologi Knowledge Component — Matematika Kelas 1 SD\n'
    '(23 KC, 22 relasi hasPrerequisite)',
    fontsize=10, fontweight='bold', pad=12, color='black'
)
ax.set_xlim(-2, 14.5)
ax.set_ylim(-0.5, 9.5)
ax.axis('off')
plt.tight_layout(pad=1.5)
plt.savefig('gambar4_ontologi_dag.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close()
print("✅ gambar4_ontologi_dag.png")


# ══════════════════════════════════════════════════════════════════════════════
# GAMBAR 5 — Distribusi P(L₀), hitam putih
# ══════════════════════════════════════════════════════════════════════════════
topic_order = [kc_map[k]['topic'] for k in ALL_KCS]
p0_onto     = [get_prior(k) for k in ALL_KCS]
labels      = [k.replace('KC-', '') for k in ALL_KCS]
x           = np.arange(len(ALL_KCS))
w           = 0.38

bar_gray = [TOPIC_FILL[kc_map[k]['topic']] for k in ALL_KCS]

fig, ax = plt.subplots(figsize=(14, 5.5))
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Bars: ontologi (filled gray) + flat prior (outline hatch)
ax.bar(x - w/2, p0_onto, w,
       label='P(L₀) Ontologi',
       color=bar_gray, edgecolor='white', linewidth=0.4, zorder=3)
ax.bar(x + w/2, [0.35]*len(ALL_KCS), w,
       label='Flat Prior (0,35) — Sequential Baseline',
       color='none', edgecolor='#555', linewidth=1.2,
       hatch='////', zorder=3)

# Value labels on ontology bars (only if < 0.35)
for i, val in enumerate(p0_onto):
    if val < 0.33:
        ax.text(x[i] - w/2, val + 0.006,
                f'{val:.2f}', ha='center', va='bottom',
                fontsize=5.5, color='#333')

# Horizontal flat line
ax.axhline(0.35, color='#333', linestyle='--', linewidth=1.3,
           alpha=0.7, zorder=4)

# Topic separators
topic_spans = []
cur = topic_order[0]; start = 0
for i in range(1, len(topic_order)):
    if topic_order[i] != cur:
        topic_spans.append((cur, start, i-1))
        cur = topic_order[i]; start = i
topic_spans.append((cur, start, len(topic_order)-1))

for t, s, e in topic_spans:
    if e < len(topic_order) - 1:
        ax.axvline(e + 0.5, color='#AAAAAA', lw=0.9, zorder=2)

# Topic labels on secondary x-axis
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks([(s+e)/2 for _, s, e in topic_spans])
ax2.set_xticklabels([TOPIC_LABELS[t] for t, _, _ in topic_spans],
                    fontsize=8, color='black')
ax2.tick_params(axis='x', length=0)

ax.set_xlabel('Knowledge Component', fontsize=10)
ax.set_ylabel('P(L₀)', fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=7.5, rotation=45, ha='right')
ax.set_ylim(0, 0.44)
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40])
ax.yaxis.grid(True, linestyle=':', alpha=0.5, zorder=0, color='#BBBBBB')
ax.set_axisbelow(True)

for spine in ax.spines.values():
    spine.set_color('#333')
    spine.set_linewidth(0.8)

ax.legend(loc='upper right', fontsize=8, framealpha=0.95, edgecolor='#333')

ax.set_title(
    'Gambar 5  Distribusi P(L₀) Hasil Ontologi vs Flat Prior (Sequential Baseline) per KC',
    fontsize=10, fontweight='bold', pad=26, color='black'
)

plt.tight_layout(pad=1.5)
plt.savefig('gambar5_p0_distribution.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close()
print("✅ gambar5_p0_distribution.png")


# ══════════════════════════════════════════════════════════════════════════════
# TABEL 4.3 — Print ke terminal (isi untuk dimasukkan ke Word manual)
# ══════════════════════════════════════════════════════════════════════════════
try:
    with open('data/estimated_params.json') as f:
        params = json.load(f).get('ontologi', {})
except Exception:
    params = {}

print("\n" + "="*75)
print("ISIAN TABEL 4.3 — Parameter BKT per Knowledge Component")
print("="*75)
print(f"{'KC ID':<8} {'Nama KC':<38} {'P(L₀)':>7} {'P(T)':>6} {'P(G)':>6} {'P(S)':>6} {'Diff':>5}")
print("-"*75)
for kc in kcs:
    kid = kc['id']
    p   = params.get(kid, {})
    p0  = get_prior(kid)
    pt  = p.get('p_transit', 0.10)
    pg  = p.get('p_guess',   0.25)
    ps  = p.get('p_slip',    0.10)
    d   = kc['difficulty']
    print(f"{kid:<8} {kc['name']:<38} {p0:>7.3f} {pt:>6.2f} {pg:>6.2f} {ps:>6.2f} {d:>5}")
print("-"*75)
print("P(L₀) dari ontologi; P(T), P(G), P(S) dari grid search log-likelihood")
