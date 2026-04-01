#!/usr/bin/env python3
"""MTN ISMS - Risk Scoring Engine"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'Risk_Scoring')
os.makedirs(OUTPUT_DIR, exist_ok=True)

MTN_YELLOW = '#FFCB00'
MTN_DARK   = '#1A1A2E'
MTN_RED    = '#E63946'
MTN_GREEN  = '#2DC653'


def load_risk_register():
    return pd.read_csv(os.path.join(DATA_DIR, 'risk_register.csv'))


def calculate_risk_scores(df):
    df = df.copy()
    df['risk_score'] = df['likelihood'] * df['impact']
    def classify(s):
        if s >= 20: return 'Critical'
        elif s >= 12: return 'High'
        elif s >= 6: return 'Medium'
        return 'Low'
    df['risk_level'] = df['risk_score'].apply(classify)
    return df


def plot_risk_heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    cmap = LinearSegmentedColormap.from_list('risk', ['#2DC653','#8CC63F','#FFCB00','#FF6B35','#E63946'], N=256)
    matrix = np.zeros((5, 5))
    for _, row in df.iterrows():
        l, i = int(row['likelihood']) - 1, int(row['impact']) - 1
        if 0 <= l < 5 and 0 <= i < 5:
            matrix[4 - i][l] += 1
    score_matrix = np.array([[l * i for l in range(1, 6)] for i in range(5, 0, -1)])
    ax.imshow(score_matrix, cmap=cmap, aspect='auto', vmin=1, vmax=25, extent=[-0.5, 4.5, -0.5, 4.5])
    for i in range(5):
        for j in range(5):
            count = int(matrix[4 - i][j])
            score = (j + 1) * (i + 1)
            color = 'white' if score > 12 else MTN_DARK
            ax.text(j, i, f'{score}\n({count})', ha='center', va='center', color=color, fontsize=9, fontweight='bold')
    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels(['1\nRare','2\nUnlikely','3\nPossible','4\nLikely','5\nAlmost Certain'], color='white', fontsize=9)
    ax.set_yticklabels(['1\nInsig.','2\nMinor','3\nModerate','4\nMajor','5\nCritical'], color='white', fontsize=9)
    ax.set_xlabel('Likelihood', color='white', fontsize=11, labelpad=10)
    ax.set_ylabel('Impact', color='white', fontsize=11, labelpad=10)
    ax.set_title('MTN ISMS — Risk Heatmap (ISO 27001)', color=MTN_YELLOW, fontsize=14, fontweight='bold', pad=15)
    patches = [mpatches.Patch(color='#2DC653', label='Low (1-5)'),
               mpatches.Patch(color='#FFCB00', label='Medium (6-11)'),
               mpatches.Patch(color='#FF6B35', label='High (12-19)'),
               mpatches.Patch(color='#E63946', label='Critical (20-25)')]
    ax.legend(handles=patches, loc='lower right', framealpha=0.3, labelcolor='white', facecolor=MTN_DARK, fontsize=9)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'risk_heatmap.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def plot_risk_by_domain(df):
    domain_avg = df.groupby('domain')['risk_score'].mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    bar_colors = [MTN_RED if v >= 15 else MTN_YELLOW if v >= 10 else MTN_GREEN for v in domain_avg.values]
    bars = ax.barh(domain_avg.index, domain_avg.values, color=bar_colors, edgecolor='none', height=0.6)
    for bar, val in zip(bars, domain_avg.values):
        ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2, f'{val:.1f}', va='center', color='white', fontsize=10, fontweight='bold')
    ax.set_xlabel('Average Risk Score', color='white', fontsize=11)
    ax.set_title('MTN ISMS — Average Risk Score by Domain', color=MTN_YELLOW, fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    for spine in ['top','right']: ax.spines[spine].set_visible(False)
    for spine in ['bottom','left']: ax.spines[spine].set_color('#444')
    ax.set_xlim(0, 30)
    ax.axvline(x=20, color=MTN_RED, linestyle='--', alpha=0.5, label='Critical threshold')
    ax.legend(framealpha=0.3, labelcolor='white', facecolor=MTN_DARK, fontsize=9)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'risk_by_domain.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def plot_risk_distribution(df):
    level_order = ['Critical','High','Medium','Low']
    level_colors = {'Critical':MTN_RED,'High':'#FF6B35','Medium':MTN_YELLOW,'Low':MTN_GREEN}
    counts = df['risk_level'].value_counts().reindex([l for l in level_order if l in df['risk_level'].values])
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    wedges, texts, autotexts = ax.pie(counts.values, labels=counts.index,
        colors=[level_colors[l] for l in counts.index], autopct='%1.0f%%',
        startangle=90, pctdistance=0.75, wedgeprops={'linewidth':2,'edgecolor':MTN_DARK})
    for t in texts: t.set_color('white'); t.set_fontsize(11)
    for at in autotexts: at.set_color(MTN_DARK); at.set_fontsize(10); at.set_fontweight('bold')
    ax.set_title('MTN ISMS — Risk Level Distribution', color=MTN_YELLOW, fontsize=14, fontweight='bold')
    ax.legend([f'{l}: {c}' for l, c in zip(counts.index, counts.values)],
              loc='lower center', bbox_to_anchor=(0.5,-0.1), ncol=2,
              framealpha=0.3, labelcolor='white', facecolor=MTN_DARK, fontsize=10)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'risk_distribution.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def main():
    print("\n[*] MTN ISMS Risk Scoring Engine — Starting...")
    df = load_risk_register()
    df = calculate_risk_scores(df)
    print("[*] Generating risk visualisations...")
    plot_risk_heatmap(df)
    plot_risk_by_domain(df)
    plot_risk_distribution(df)
    df.to_csv(os.path.join(OUTPUT_DIR, 'scored_risk_register.csv'), index=False)
    print(f"  Saved: {os.path.join(OUTPUT_DIR, 'scored_risk_register.csv')}")
    print("\n============================================================")
    print("  MTN ISMS RISK SCORING SUMMARY")
    print("============================================================")
    print(f"  Total Risks    : {len(df)}")
    for level in ['Critical','High','Medium','Low']:
        print(f"  {level:<12} : {len(df[df['risk_level']==level])}")
    print(f"  Highest Score  : {df['risk_score'].max()}")
    print(f"  Average Score  : {df['risk_score'].mean():.1f}")
    print("============================================================")
    print("\n[+] Risk scoring complete.\n")

if __name__ == '__main__':
    main()
