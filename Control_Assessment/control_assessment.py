#!/usr/bin/env python3
"""MTN ISMS - Control Assessment Analysis"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'Control_Assessment')
os.makedirs(OUTPUT_DIR, exist_ok=True)

MTN_YELLOW = '#FFCB00'
MTN_DARK   = '#1A1A2E'
MTN_PANEL  = '#0D1B2A'
MTN_RED    = '#E63946'
MTN_GREEN  = '#2DC653'
MTN_BLUE   = '#4A90D9'


def load_controls():
    return pd.read_csv(os.path.join(DATA_DIR, 'control_assessment.csv'))


def plot_compliance_radar(df):
    domain_avg = df.groupby('domain')['compliance_score'].mean()
    domains = list(domain_avg.index)
    values = list(domain_avg.values)
    N = len(domains)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values += values[:1]
    fig, ax = plt.subplots(figsize=(9, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_PANEL)
    ax.plot(angles, values, color=MTN_YELLOW, linewidth=2)
    ax.fill(angles, values, color=MTN_YELLOW, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(domains, color='white', fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_yticks([20,40,60,80,100])
    ax.set_yticklabels(['20','40','60','80','100'], color='#888', fontsize=7)
    ax.grid(color='#333', linewidth=0.5)
    ax.spines['polar'].set_color('#333')
    ax.set_title('MTN ISMS — Control Compliance by Domain', color=MTN_YELLOW, fontsize=13, fontweight='bold', pad=20)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'compliance_radar.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def plot_implementation_status(df):
    df2 = df.copy()
    df2['impl_label'] = df2['implemented'].map({'Yes':'Implemented','No':'Not Implemented'}).fillna('Partial')
    pivot = df2.groupby(['domain','impl_label']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    colors = {'Implemented':MTN_GREEN,'Partial':MTN_YELLOW,'Not Implemented':MTN_RED}
    bottom = np.zeros(len(pivot))
    for col in ['Implemented','Partial','Not Implemented']:
        if col in pivot.columns:
            ax.bar(pivot.index, pivot[col], bottom=bottom, label=col,
                   color=colors[col], edgecolor=MTN_DARK, linewidth=0.5)
            bottom += pivot[col].values
    ax.set_ylabel('Number of Controls', color='white', fontsize=11)
    ax.set_title('MTN ISMS — Control Implementation Status by Domain', color=MTN_YELLOW, fontsize=13, fontweight='bold')
    ax.tick_params(colors='white')
    plt.xticks(rotation=30, ha='right', color='white')
    for spine in ['top','right']: ax.spines[spine].set_visible(False)
    for spine in ['bottom','left']: ax.spines[spine].set_color('#444')
    ax.legend(framealpha=0.3, labelcolor='white', facecolor=MTN_DARK, fontsize=9)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'implementation_status.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def plot_compliance_scores(df):
    df_sorted = df.sort_values('compliance_score', ascending=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    bar_colors = [MTN_RED if s < 40 else MTN_YELLOW if s < 70 else MTN_GREEN for s in df_sorted['compliance_score']]
    bars = ax.barh(df_sorted['control_name'], df_sorted['compliance_score'], color=bar_colors, edgecolor='none', height=0.6)
    for bar, val in zip(bars, df_sorted['compliance_score']):
        ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2, f'{val}%', va='center', color='white', fontsize=9)
    ax.axvline(x=70, color='white', linestyle='--', alpha=0.4, label='Target (70%)')
    ax.set_xlabel('Compliance Score (%)', color='white', fontsize=11)
    ax.set_title('MTN ISMS — Control Compliance Scores', color=MTN_YELLOW, fontsize=13, fontweight='bold')
    ax.tick_params(colors='white')
    ax.set_xlim(0, 110)
    for spine in ['top','right']: ax.spines[spine].set_visible(False)
    for spine in ['bottom','left']: ax.spines[spine].set_color('#444')
    ax.legend(framealpha=0.3, labelcolor='white', facecolor=MTN_DARK, fontsize=9)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'compliance_scores.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def main():
    print("\n[*] MTN ISMS Control Assessment — Starting...")
    df = load_controls()
    print("[*] Generating control visualisations...")
    plot_compliance_radar(df)
    plot_implementation_status(df)
    plot_compliance_scores(df)
    gaps = df[df['compliance_score'] < 70].sort_values('compliance_score')
    gaps.to_csv(os.path.join(OUTPUT_DIR, 'gap_analysis_report.csv'), index=False)
    print(f"  Saved: {os.path.join(OUTPUT_DIR, 'gap_analysis_report.csv')}")
    avg = df['compliance_score'].mean()
    print("\n============================================================")
    print("  MTN ISMS CONTROL ASSESSMENT SUMMARY")
    print("============================================================")
    print(f"  Controls Assessed    : {len(df)}")
    print(f"  Avg Compliance Score : {avg:.1f}%")
    print(f"  Not Implemented      : {len(df[df['implemented']=='No'])}")
    print(f"  Below Target (<70%)  : {len(gaps)}")
    print(f"  ISMS Maturity        : {'Developing' if avg < 60 else 'Managed' if avg < 80 else 'Optimised'}")
    print("============================================================")
    print("\n[+] Control assessment complete.\n")

if __name__ == '__main__':
    main()
