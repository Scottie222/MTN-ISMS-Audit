#!/usr/bin/env python3
"""MTN ISMS - Findings & Recommendations"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'Findings_Recommendations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

MTN_YELLOW = '#FFCB00'
MTN_DARK   = '#1A1A2E'
MTN_RED    = '#E63946'
MTN_GREEN  = '#2DC653'
MTN_ORANGE = '#FF6B35'
MTN_BLUE   = '#4A90D9'
SEV_COLORS = {'Critical':MTN_RED,'High':MTN_ORANGE,'Medium':MTN_YELLOW,'Low':MTN_GREEN}


def load_findings():
    return pd.read_csv(os.path.join(DATA_DIR, 'findings.csv'))


def plot_findings_by_severity(df):
    order = ['Critical','High','Medium','Low']
    counts = df['severity'].value_counts().reindex([s for s in order if s in df['severity'].values], fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    bars = ax.bar(counts.index, counts.values, color=[SEV_COLORS.get(s, MTN_BLUE) for s in counts.index],
                  edgecolor=MTN_DARK, linewidth=0.5, width=0.5)
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.1, str(val),
                ha='center', va='bottom', color='white', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Findings', color='white', fontsize=11)
    ax.set_title('MTN ISMS — Audit Findings by Severity', color=MTN_YELLOW, fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    for spine in ['top','right']: ax.spines[spine].set_visible(False)
    for spine in ['bottom','left']: ax.spines[spine].set_color('#444')
    ax.set_ylim(0, max(counts.values) + 1.5)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'findings_by_severity.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def plot_findings_by_category(df):
    cat_counts = df.groupby('category').size().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    bars = ax.barh(cat_counts.index, cat_counts.values, color=MTN_BLUE, edgecolor='none', height=0.5)
    for bar, val in zip(bars, cat_counts.values):
        ax.text(val+0.05, bar.get_y()+bar.get_height()/2, str(val), va='center', color='white', fontsize=11, fontweight='bold')
    ax.set_xlabel('Number of Findings', color='white', fontsize=11)
    ax.set_title('MTN ISMS — Findings by Category', color=MTN_YELLOW, fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    for spine in ['top','right']: ax.spines[spine].set_visible(False)
    for spine in ['bottom','left']: ax.spines[spine].set_color('#444')
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'findings_by_category.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def plot_remediation_status(df):
    status_counts = df['status'].value_counts()
    colors = {'Open':MTN_RED,'In Progress':MTN_YELLOW,'Closed':MTN_GREEN}
    fig, ax = plt.subplots(figsize=(7, 6))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_DARK)
    wedges, texts, autotexts = ax.pie(
        status_counts.values, labels=status_counts.index,
        colors=[colors.get(s, MTN_BLUE) for s in status_counts.index],
        autopct='%1.0f%%', startangle=90, pctdistance=0.72,
        wedgeprops={'linewidth':2,'edgecolor':MTN_DARK})
    for t in texts: t.set_color('white'); t.set_fontsize(11)
    for at in autotexts: at.set_color(MTN_DARK); at.set_fontsize(10); at.set_fontweight('bold')
    ax.set_title('MTN ISMS — Remediation Status', color=MTN_YELLOW, fontsize=14, fontweight='bold')
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'remediation_status.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def generate_findings_report(df):
    lines = ["# MTN Group ISMS — Audit Findings & Recommendations",
             f"\n**Report Date:** {datetime.now().strftime('%d %B %Y')}",
             "**Standard:** ISO/IEC 27001:2022\n", "---\n",
             "## Executive Summary\n",
             f"This audit identified **{len(df)} findings**. "
             f"**{len(df[df['severity']=='Critical'])} Critical** and "
             f"**{len(df[df['severity']=='High'])} High** severity findings require immediate attention. "
             f"**{len(df[df['status']=='Open'])}** findings remain open.\n", "---\n"]
    for sev in ['Critical','High','Medium','Low']:
        sev_df = df[df['severity']==sev]
        if len(sev_df) == 0: continue
        lines.append(f"## {sev} Findings\n")
        for _, row in sev_df.iterrows():
            lines.extend([
                f"### {row['finding_id']}: {row['title']}",
                f"- **Category:** {row['category']}",
                f"- **Control Ref:** {row['affected_control']}",
                f"- **Status:** {row['status']}",
                f"- **Due Date:** {row['due_date']}",
                f"\n**Description:** {row['description']}\n",
                f"**Recommendation:** {row['recommendation']}\n",
                "---\n"])
    out = os.path.join(OUTPUT_DIR, 'audit_findings_report.md')
    with open(out, 'w') as f:
        f.write('\n'.join(lines))
    print(f"  Saved: {out}")


def main():
    print("\n[*] MTN ISMS Findings & Recommendations — Starting...")
    df = load_findings()
    print("[*] Generating findings visualisations...")
    plot_findings_by_severity(df)
    plot_findings_by_category(df)
    plot_remediation_status(df)
    generate_findings_report(df)
    priority_map = {'Critical':1,'High':2,'Medium':3,'Low':4}
    df2 = df.copy()
    df2['priority'] = df2['severity'].map(priority_map)
    df2.sort_values(['priority','due_date'])[['finding_id','severity','title','category',
        'affected_control','recommendation','status','due_date']].to_csv(
        os.path.join(OUTPUT_DIR, 'remediation_plan.csv'), index=False)
    print(f"  Saved: {os.path.join(OUTPUT_DIR, 'remediation_plan.csv')}")
    print("\n============================================================")
    print("  MTN ISMS FINDINGS SUMMARY")
    print("============================================================")
    print(f"  Total      : {len(df)}")
    for s in ['Critical','High','Medium','Low']:
        print(f"  {s:<12} : {len(df[df['severity']==s])}")
    print(f"  Open       : {len(df[df['status']=='Open'])}")
    print(f"  In Progress: {len(df[df['status']=='In Progress'])}")
    print("============================================================")
    print("\n[+] Findings analysis complete.\n")

if __name__ == '__main__':
    main()
