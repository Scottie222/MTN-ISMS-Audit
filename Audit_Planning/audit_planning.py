#!/usr/bin/env python3
"""MTN ISMS - Audit Planning Module"""

import os
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCHEDULE = [
    {"phase": "Planning & Scoping",        "start": "2025-04-01", "end": "2025-04-14", "owner": "Lead Auditor"},
    {"phase": "Document Review",           "start": "2025-04-15", "end": "2025-04-25", "owner": "Audit Team"},
    {"phase": "Control Testing",           "start": "2025-04-28", "end": "2025-05-16", "owner": "Audit Team"},
    {"phase": "Interviews & Walkthroughs", "start": "2025-05-19", "end": "2025-05-30", "owner": "Lead Auditor"},
    {"phase": "Findings Analysis",         "start": "2025-06-02", "end": "2025-06-13", "owner": "Audit Team"},
    {"phase": "Draft Report",              "start": "2025-06-16", "end": "2025-06-27", "owner": "Lead Auditor"},
    {"phase": "Management Review",         "start": "2025-06-30", "end": "2025-07-11", "owner": "ISMS Committee"},
    {"phase": "Final Report",              "start": "2025-07-14", "end": "2025-07-18", "owner": "Lead Auditor"},
]

DOMAINS = [
    {"ref":"A.5","domain":"Organisational Controls","controls":37,"priority":"High"},
    {"ref":"A.6","domain":"People Controls","controls":8,"priority":"High"},
    {"ref":"A.7","domain":"Physical Controls","controls":14,"priority":"Medium"},
    {"ref":"A.8","domain":"Technological Controls","controls":34,"priority":"Critical"},
]


def generate_audit_plan():
    lines = []
    lines.append("# MTN Group ISMS — Internal Audit Plan")
    lines.append(f"\n**Generated:** {datetime.now().strftime('%d %B %Y')}\n")
    lines.append("---\n")
    lines.append("## 1. Audit Overview\n")
    lines.append("- **Organisation:** MTN Group Limited")
    lines.append("- **Standard:** ISO/IEC 27001:2022")
    lines.append("- **Audit Type:** Internal ISMS Audit")
    lines.append("- **Scope:** MTN South Africa ISMS boundary\n")
    lines.append("---\n")
    lines.append("## 2. Audit Objectives\n")
    for obj in [
        "Evaluate ISMS control effectiveness against ISO/IEC 27001:2022",
        "Identify control gaps and non-conformities across all Annex A domains",
        "Assess risk treatment effectiveness and residual risk levels",
        "Verify compliance with POPIA, GDPR, and applicable regulations",
        "Provide actionable recommendations to improve ISMS maturity",
    ]:
        lines.append(f"- {obj}")
    lines.append("\n---\n")
    lines.append("## 3. Annex A Domains in Scope\n")
    lines.append("| Ref | Domain | Controls | Priority |")
    lines.append("|-----|--------|----------|----------|")
    for d in DOMAINS:
        lines.append(f"| {d['ref']} | {d['domain']} | {d['controls']} | {d['priority']} |")
    lines.append(f"\n**Total Controls:** {sum(d['controls'] for d in DOMAINS)}\n")
    lines.append("\n---\n")
    lines.append("## 4. Audit Schedule\n")
    lines.append("| Phase | Start | End | Owner |")
    lines.append("|-------|-------|-----|-------|")
    for s in SCHEDULE:
        lines.append(f"| {s['phase']} | {s['start']} | {s['end']} | {s['owner']} |")
    lines.append("\n---\n")
    lines.append("## 5. Audit Criteria\n")
    for c in [
        "ISO/IEC 27001:2022 — Information Security Management Systems",
        "ISO/IEC 27002:2022 — Information Security Controls",
        "POPIA — Protection of Personal Information Act (South Africa)",
        "GDPR — General Data Protection Regulation (EU customers)",
        "MTN Group Information Security Policy v3.1",
    ]:
        lines.append(f"- {c}")

    out = os.path.join(BASE_DIR, 'audit_plan.md')
    with open(out, 'w') as f:
        f.write('\n'.join(lines))
    print(f"  Saved: {out}")


def generate_audit_checklist():
    checklist = [
        ("CL001","A.5.1","IS Policy","Is there an approved IS policy?","Doc Review"),
        ("CL002","A.5.2","IS Roles","Are IS roles and responsibilities defined?","Interview"),
        ("CL003","A.5.9","Asset Inventory","Is an accurate asset inventory maintained?","Doc Review"),
        ("CL004","A.5.15","Access Control Policy","Is access control policy documented?","Testing"),
        ("CL005","A.6.3","Security Awareness","Is security awareness training conducted?","Interview"),
        ("CL006","A.7.1","Physical Perimeters","Are physical perimeters defined and enforced?","Observation"),
        ("CL007","A.8.1","Endpoint Security","Are endpoint controls deployed on all devices?","Testing"),
        ("CL008","A.8.5","Secure Authentication","Is MFA enforced for privileged access?","Testing"),
        ("CL009","A.8.8","Vulnerability Mgmt","Is there a vulnerability management process?","Doc Review"),
        ("CL010","A.8.15","Logging & Monitoring","Are security logs collected and reviewed?","Testing"),
        ("CL011","A.8.24","Cryptography","Are cryptographic standards enforced?","Doc Review"),
        ("CL012","A.5.29","Business Continuity","Is a tested BCP/DRP in place?","Doc Review"),
        ("CL013","A.5.19","Supplier Security","Are supplier requirements contractually defined?","Doc Review"),
        ("CL014","A.5.25","Incident Management","Is there a tested incident response process?","Interview"),
        ("CL015","A.5.12","Data Classification","Is data classified per sensitivity?","Doc Review"),
    ]
    out = os.path.join(BASE_DIR, 'audit_checklist.csv')
    with open(out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','control_ref','area','question','method','finding','status'])
        for row in checklist:
            writer.writerow(list(row) + ['', 'Pending'])
    print(f"  Saved: {out}")


def main():
    print("\n[*] MTN ISMS Audit Planning — Starting...")
    generate_audit_plan()
    generate_audit_checklist()
    print("\n[+] Audit planning complete.\n")

if __name__ == '__main__':
    main()
