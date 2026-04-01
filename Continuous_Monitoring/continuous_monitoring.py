#!/usr/bin/env python3
"""MTN ISMS - Continuous Monitoring Dashboard"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'Continuous_Monitoring')
os.makedirs(OUTPUT_DIR, exist_ok=True)

MTN_YELLOW = '#FFCB00'
MTN_DARK   = '#1A1A2E'
MTN_PANEL  = '#0D1B2A'
MTN_RED    = '#E63946'
MTN_GREEN  = '#2DC653'
MTN_BLUE   = '#4A90D9'
MTN_ORANGE = '#FF6B35'
MTN_PURPLE = '#9B59B6'
MTN_CYAN   = '#1ABC9C'


def load_metrics():
    df = pd.read_csv(os.path.join(DATA_DIR, 'monitoring_metrics.csv'))
    df['month'] = pd.to_datetime(df['month'])
    return df


def plot_kpi_trends(df):
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(MTN_DARK)
    gs = gridspec.GridSpec(3, 2, hspace=0.45, wspace=0.35)
    axes = [fig.add_subplot(gs[i // 2, i % 2]) for i in range(6)]
    kpis = [
        ('patch_compliance_pct',    'Patch Compliance (%)',          MTN_GREEN,  90),
        ('mfa_adoption_pct',        'MFA Adoption (%)',              MTN_BLUE,   95),
        ('incident_mttr_hours',     'Incident MTTR (Hours)',         MTN_RED,    24),
        ('phishing_click_rate_pct', 'Phishing Click Rate (%)',       MTN_ORANGE, 5),
        ('training_completion_pct', 'Security Training Completion (%)', MTN_PURPLE, 95),
        ('backup_success_pct',      'Backup Success Rate (%)',       MTN_CYAN,   99),
    ]
    months = df['month'].dt.strftime('%b %y')
    for ax, (col, title, color, target) in zip(axes, kpis):
        ax.set_facecolor(MTN_PANEL)
        ax.plot(range(len(df)), df[col], color=color, linewidth=2.5, marker='o',
                markersize=5, markerfacecolor='white', markeredgecolor=color)
        ax.axhline(y=target, color='white', linestyle='--', alpha=0.4, linewidth=1, label=f'Target: {target}')
        ax.fill_between(range(len(df)), df[col], alpha=0.15, color=color)
        ax.set_title(title, color='white', fontsize=10, fontweight='bold', pad=8)
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(months, rotation=30, fontsize=7, color='#aaa')
        ax.tick_params(colors='#aaa', axis='y')
        ax.grid(color='#1e2d3d', linewidth=0.5)
        for spine in ax.spines.values(): spine.set_color('#1e2d3d')
        latest = df[col].iloc[-1]
        prev   = df[col].iloc[-2]
        improving = (col not in ['incident_mttr_hours','phishing_click_rate_pct','vuln_critical_open'] and latest > prev) or \
                    (col in ['incident_mttr_hours','phishing_click_rate_pct','vuln_critical_open'] and latest < prev)
        trend_color = MTN_GREEN if improving else MTN_RED
        trend_arrow = '▲' if latest > prev else '▼'
        ax.text(0.98, 0.92, f'{latest:.0f} {trend_arrow}', transform=ax.transAxes,
                color=trend_color, fontsize=11, fontweight='bold', ha='right')
        ax.legend(fontsize=7, framealpha=0.3, labelcolor='#aaa', facecolor=MTN_PANEL)
    fig.suptitle('MTN ISMS — Continuous Monitoring KPI Dashboard',
                 color=MTN_YELLOW, fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out = os.path.join(OUTPUT_DIR, 'kpi_trends.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def plot_vulnerability_trend(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(MTN_DARK)
    ax.set_facecolor(MTN_PANEL)
    months = df['month'].dt.strftime('%b %y')
    ax.fill_between(range(len(df)), df['vuln_critical_open'], color=MTN_RED, alpha=0.3)
    ax.plot(range(len(df)), df['vuln_critical_open'], color=MTN_RED, linewidth=2.5,
            marker='o', markersize=6, markerfacecolor='white', markeredgecolor=MTN_RED)
    ax.axhline(y=10, color=MTN_YELLOW, linestyle='--', alpha=0.6, label='Target: ≤10')
    for i, val in enumerate(df['vuln_critical_open']):
        ax.text(i, val+0.5, str(int(val)), ha='center', color='white', fontsize=9, fontweight='bold')
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(months, rotation=30, color='white', fontsize=9)
    ax.set_ylabel('Open Critical Vulnerabilities', color='white', fontsize=11)
    ax.set_title('MTN ISMS — Critical Vulnerability Trend', color=MTN_YELLOW, fontsize=14, fontweight='bold')
    ax.tick_params(colors='white')
    ax.grid(color='#1e2d3d', linewidth=0.5)
    for spine in ax.spines.values(): spine.set_color('#1e2d3d')
    ax.legend(framealpha=0.3, labelcolor='white', facecolor=MTN_PANEL, fontsize=10)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'vulnerability_trend.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=MTN_DARK)
    plt.close()
    print(f"  Saved: {out}")


def export_kpi_summary(df):
    latest = df.iloc[-1]
    targets = {'patch_compliance_pct':(90,'higher'),'mfa_adoption_pct':(95,'higher'),
               'incident_mttr_hours':(24,'lower'),'phishing_click_rate_pct':(5,'lower'),
               'vuln_critical_open':(10,'lower'),'training_completion_pct':(95,'higher'),
               'access_review_complete_pct':(90,'higher'),'backup_success_pct':(99,'higher')}
    names  = {'patch_compliance_pct':'Patch Compliance','mfa_adoption_pct':'MFA Adoption',
               'incident_mttr_hours':'Incident MTTR (hrs)','phishing_click_rate_pct':'Phishing Click Rate',
               'vuln_critical_open':'Critical Vulns Open','training_completion_pct':'Training Completion',
               'access_review_complete_pct':'Access Review Complete','backup_success_pct':'Backup Success Rate'}
    rows = []
    for col,(target,direction) in targets.items():
        val = latest[col]
        status = 'On Target' if (direction=='higher' and val>=target) or (direction=='lower' and val<=target) else 'Below Target'
        rows.append({'KPI':names[col],'Current':val,'Target':target,'Status':status})
    import pandas as pd_inner
    out = os.path.join(OUTPUT_DIR, 'kpi_summary.csv')
    pd_inner.DataFrame(rows).to_csv(out, index=False)
    print(f"  Saved: {out}")
    on_target = sum(1 for r in rows if r['Status']=='On Target')
    print(f"  KPIs On Target: {on_target}/{len(rows)}")


def main():
    print("\n[*] MTN ISMS Continuous Monitoring — Starting...")
    df = load_metrics()
    print("[*] Generating monitoring visualisations...")
    plot_kpi_trends(df)
    plot_vulnerability_trend(df)
    export_kpi_summary(df)
    print("\n[+] Continuous monitoring complete.\n")

if __name__ == '__main__':
    main()
