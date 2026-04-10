# MTN Group — ISO 27001 ISMS Internal Audit Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![ISO 27001](https://img.shields.io/badge/Standard-ISO%2027001%3A2022-yellow?style=flat-square)
![POPIA](https://img.shields.io/badge/Compliance-POPIA-green?style=flat-square)
![GDPR](https://img.shields.io/badge/Compliance-GDPR-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

A fully automated ISO/IEC 27001:2022 internal audit and continuous monitoring simulation built for MTN Group Limited — Africa's largest telecommunications company. Covers end-to-end information security governance: risk assessment, control effectiveness evaluation, audit findings management, POPIA/GDPR compliance tracking, and a live ISMS KPI dashboard — all generated from Python with zero manual effort.

---

## Table of Contents

- [Why This Project Exists](#why-this-project-exists)
- [Company Profile](#company-profile)
- [What the Tool Does](#what-the-tool-does)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Running the Audit](#running-the-audit)
- [Generated Outputs](#generated-outputs)
- [Bash Scripts Reference](#bash-scripts-reference)
- [CI/CD Pipeline](#cicd-pipeline)
- [Audit Scope and Standards](#audit-scope-and-standards)
- [Risk Scoring Methodology](#risk-scoring-methodology)
- [ISMS Maturity Model](#isms-maturity-model)
- [Key Findings Summary](#key-findings-summary)
- [KPI Monitoring Targets](#kpi-monitoring-targets)
- [Requirements](#requirements)

---

## Why This Project Exists

MTN Group operates across 19 African and Middle Eastern markets, serving over 300 million subscribers and processing billions of financial transactions through its MoMo fintech platform. The scale of data handled — personal, financial, and operational — makes information security governance not just a regulatory requirement but a business-critical function.

This project simulates what a real ISO 27001 internal audit engagement looks like for an organisation of MTN's complexity. It demonstrates how to systematically assess information security controls against an international standard, quantify and visualise risk using a structured scoring methodology, track compliance trends over time using continuous monitoring KPIs, and produce professional audit deliverables that a CISO or audit committee would actually use.

The tool is built entirely in Python with no external audit software, making it reproducible, version-controlled, and extendable.

---

## Company Profile

| Field | Details |
|---|---|
| Organisation | MTN Group Limited |
| Founded | 1994 (as M-Cell) |
| Headquarters | Johannesburg, South Africa |
| CEO | Ralph Mupita |
| Subscribers | 300+ million across 19 markets |
| Services | Telecommunications, Fintech (MoMo), Cloud, Enterprise ICT |
| Stock Exchange | JSE: MTN |
| Revenue | ~ZAR 185 billion (FY2023) |
| Employees | 17,000+ |
| Key Regulations | POPIA (SA), GDPR (EU), NCC (Nigeria), ICASA (SA) |

MTN's data environment includes subscriber PII across 19 jurisdictions, mobile money transaction data for 60+ million MoMo users, enterprise cloud infrastructure, and critical national telecommunications infrastructure — all within scope of ISO 27001 certification.

---

## What the Tool Does

Running one command generates a complete audit suite:

```bash
python run_audit.py
```

| Function | What It Produces |
|---|---|
| Risk Assessment | Scores 15 risks using a 5×5 matrix, generates heatmap and domain analysis |
| Control Assessment | Evaluates 15 ISO 27001 Annex A controls, produces radar and gap analysis |
| Findings Management | Classifies 10 audit findings by severity, generates remediation plan |
| Continuous Monitoring | Tracks 8 security KPIs over 10 months, produces trend dashboards |
| Audit Planning | Generates full audit plan document, schedule, and 15-item checklist |

All five modules produce charts, CSV reports, markdown documents, and a self-contained HTML audit report.

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT DATA (CSV)                      │
│  risk_register.csv  │  control_assessment.csv           │
│  findings.csv       │  monitoring_metrics.csv            │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  run_audit.py (Master Runner)            │
│                                                          │
│  1. Audit Planning      → audit_plan.md + checklist     │
│  2. Risk Scoring        → heatmap + domain + pie charts │
│  3. Control Assessment  → radar + scores + gap report   │
│  4. Findings Analysis   → severity + category + remed.  │
│  5. Continuous Monitor  → KPI trends + vuln trend       │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                    OUTPUT FILES                          │
│  11 PNG charts  │  7 CSV reports  │  2 Markdown docs    │
│  1 Self-contained HTML audit report                      │
└─────────────────────────────────────────────────────────┘
```

Each module is a standalone Python script that reads from `data/`, processes the data, and writes outputs to its own folder. No database, no web server, no external dependencies beyond pandas and matplotlib.

---

## Project Structure

```
MTN-ISMS-Audit/
├── .github/
│   └── workflows/
│       └── isms_audit.yml
├── Audit_Planning/
│   ├── audit_planning.py
│   ├── audit_plan.md
│   └── audit_checklist.csv
├── Continuous_Monitoring/
│   ├── continuous_monitoring.py
│   ├── kpi_trends.png
│   ├── vulnerability_trend.png
│   └── kpi_summary.csv
├── Control_Assessment/
│   ├── control_assessment.py
│   ├── compliance_radar.png
│   ├── implementation_status.png
│   ├── compliance_scores.png
│   └── gap_analysis_report.csv
├── Findings_Recommendations/
│   ├── findings_analysis.py
│   ├── findings_by_severity.png
│   ├── findings_by_category.png
│   ├── remediation_status.png
│   ├── audit_findings_report.md
│   └── remediation_plan.csv
├── Risk_Scoring/
│   ├── risk_heatmap.png
│   ├── risk_by_domain.png
│   ├── risk_distribution.png
│   └── scored_risk_register.csv
├── data/
│   ├── risk_register.csv
│   ├── control_assessment.csv
│   ├── findings.csv
│   └── monitoring_metrics.csv
├── risk_engine/
│   └── risk_scoring.py
├── reports/
│   └── mtn_isms_audit_report.html
├── scripts/
│   ├── setup_project.sh
│   ├── run_audit.sh
│   ├── run_audit_planning.sh
│   ├── run_risk_scoring.sh
│   ├── run_control_assessment.sh
│   ├── run_findings.sh
│   ├── run_monitoring.sh
│   ├── generate_report.sh
│   ├── validate_data.sh
│   ├── lint_check.sh
│   └── clean.sh
├── run_audit.py
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
git clone https://github.com/Scottie222/MTN-ISMS-Audit.git
cd MTN-ISMS-Audit
pip install -r requirements.txt
python run_audit.py
```

---

## Running the Audit

```bash
# Run all 5 modules
python run_audit.py

# Run individual modules
python Audit_Planning/audit_planning.py
python risk_engine/risk_scoring.py
python Control_Assessment/control_assessment.py
python Findings_Recommendations/findings_analysis.py
python Continuous_Monitoring/continuous_monitoring.py
```

---

## Generated Outputs

| File | Location | Description |
|---|---|---|
| `audit_plan.md` | Audit_Planning/ | Full ISO 27001 audit plan document |
| `audit_checklist.csv` | Audit_Planning/ | 15-item control audit checklist |
| `risk_heatmap.png` | Risk_Scoring/ | 5×5 likelihood/impact heatmap |
| `risk_by_domain.png` | Risk_Scoring/ | Average risk score per domain |
| `risk_distribution.png` | Risk_Scoring/ | Risk level breakdown |
| `scored_risk_register.csv` | Risk_Scoring/ | Full risk register with scores |
| `compliance_radar.png` | Control_Assessment/ | Spider chart — compliance by domain |
| `implementation_status.png` | Control_Assessment/ | Implemented/Partial/Not Implemented |
| `compliance_scores.png` | Control_Assessment/ | Per-control compliance bar chart |
| `gap_analysis_report.csv` | Control_Assessment/ | Controls below 70% target |
| `findings_by_severity.png` | Findings_Recommendations/ | Critical/High/Medium/Low bar chart |
| `audit_findings_report.md` | Findings_Recommendations/ | Full structured findings report |
| `remediation_plan.csv` | Findings_Recommendations/ | Prioritised remediation actions |
| `kpi_trends.png` | Continuous_Monitoring/ | 6-panel KPI trend dashboard |
| `vulnerability_trend.png` | Continuous_Monitoring/ | Critical vulnerability count over time |
| `kpi_summary.csv` | Continuous_Monitoring/ | Latest KPI values vs targets |
| `mtn_isms_audit_report.html` | reports/ | Self-contained HTML audit report |

---

## Bash Scripts Reference

| Script | Command | Purpose |
|---|---|---|
| `setup_project.sh` | `bash setup_project.sh` | One-time setup: venv, deps, directory validation |
| `run_audit.sh` | `bash run_audit.sh` | Run all 5 modules with timestamped log file |
| `run_audit_planning.sh` | `bash scripts/run_audit_planning.sh` | Audit planning module only |
| `run_risk_scoring.sh` | `bash scripts/run_risk_scoring.sh` | Risk scoring module only |
| `run_control_assessment.sh` | `bash scripts/run_control_assessment.sh` | Control assessment module only |
| `run_findings.sh` | `bash scripts/run_findings.sh` | Findings analysis module only |
| `run_monitoring.sh` | `bash scripts/run_monitoring.sh` | Continuous monitoring only |
| `generate_report.sh` | `bash scripts/generate_report.sh` | Compile self-contained HTML report |
| `validate_data.sh` | `bash scripts/validate_data.sh` | Check all CSV files exist and have data |
| `lint_check.sh` | `bash scripts/lint_check.sh` | Run pylint on all Python modules |
| `clean.sh` | `bash scripts/clean.sh` | Delete all generated output files |

---

## CI/CD Pipeline

The `.github/workflows/isms_audit.yml` pipeline runs automatically on every push to `main`, every pull request targeting `main`, and every Monday at 06:00 UTC.

**Pipeline stages:**

1. Checkout repository
2. Set up Python 3.11
3. Install dependencies (pandas, matplotlib, numpy)
4. Validate all CSV data files
5. Run Audit Planning module
6. Run Risk Scoring Engine
7. Run Control Assessment module
8. Run Findings Analysis module
9. Run Continuous Monitoring module
10. Upload all outputs as GitHub Actions artifacts

Every commit automatically re-runs the full audit and stores the latest charts and reports as downloadable artifacts in the Actions tab.

---

## Audit Scope and Standards

| Standard / Regulation | Coverage |
|---|---|
| ISO/IEC 27001:2022 | All Annex A domains: A.5 Organisational, A.6 People, A.7 Physical, A.8 Technological |
| ISO/IEC 27002:2022 | 93 controls implementation guidance |
| ISO/IEC 27005 | Risk assessment methodology and risk treatment |
| ISO 19011:2018 | Audit methodology, planning, and reporting guidelines |
| POPIA 2013 | Protection of Personal Information Act — South Africa |
| GDPR 2018 | General Data Protection Regulation — EU data subjects |
| MTN Group IS Policy | Internal information security policy baseline v3.1 |

---

## Risk Scoring Methodology

```
Risk Score = Likelihood × Impact
```

| Score | Risk Level | Required Action |
|---|---|---|
| 20–25 | Critical | Immediate action < 30 days |
| 12–19 | High | Urgent action < 90 days |
| 6–11 | Medium | Planned remediation < 180 days |
| 1–5 | Low | Monitor and review annually |

**Likelihood Scale**

| Score | Label | Description |
|---|---|---|
| 1 | Rare | May occur only in exceptional circumstances |
| 2 | Unlikely | Could occur at some time |
| 3 | Possible | Might occur at some time |
| 4 | Likely | Will probably occur in most circumstances |
| 5 | Almost Certain | Expected to occur in most circumstances |

**Impact Scale**

| Score | Label | Description |
|---|---|---|
| 1 | Insignificant | Negligible impact on operations |
| 2 | Minor | Minor disruption, easily recovered |
| 3 | Moderate | Some disruption, moderate financial impact |
| 4 | Major | Significant disruption, regulatory attention likely |
| 5 | Critical | Severe disruption, regulatory breach, major financial loss |

---

## ISMS Maturity Model

| Score Range | Maturity Level | Description |
|---|---|---|
| 0–40% | Initial | Ad-hoc controls, no formal ISMS documented |
| 41–60% | Developing | Some controls implemented, significant gaps remain |
| 61–75% | Managed | Controls documented and partially effective |
| 76–90% | Optimised | Controls effective, regularly reviewed and improved |
| 91–100% | Leading | Continuous improvement embedded, industry best practice |

**Current MTN ISMS Maturity: Developing — 57.3% average compliance score**

Key improvement areas: Privileged Access Management, Third-Party Risk Assessment, Disaster Recovery Testing, and MFA enforcement across all systems.

---

## Key Findings Summary

| ID | Severity | Title | Status | Due Date |
|---|---|---|---|---|
| F001 | Critical | MFA Not Enforced on VPN and Admin Accounts | Open | 2025-05-31 |
| F002 | Critical | No PAM Solution Deployed | Open | 2025-05-31 |
| F003 | High | Patching Delays — 45+ Day Average | In Progress | 2025-06-15 |
| F004 | High | No Third-Party Risk Assessment Process | Open | 2025-09-30 |
| F005 | High | Incident Response Plan Never Tested | Open | 2025-06-30 |
| F006 | High | POPIA Gaps — No DSAR Workflow | In Progress | 2025-05-31 |
| F007 | High | DR Plan Untested for 18+ Months | Open | 2025-10-31 |
| F008 | Medium | Weak Cipher Usage — TLS 1.0/1.1 Active | In Progress | 2025-07-31 |
| F009 | Medium | CCTV Blind Spots in Data Centre | Open | 2025-08-31 |
| F010 | Medium | Security Training Annual Only | Open | 2025-07-31 |

---

## KPI Monitoring Targets

| KPI | Current (Apr 2025) | Target | Status |
|---|---|---|---|
| Patch Compliance | 80% | ≥90% | Below target |
| MFA Adoption | 72% | ≥95% | Below target |
| Incident MTTR | 40 hours | ≤24 hours | Below target |
| Phishing Click Rate | 9% | ≤5% | Below target |
| Critical Vulns Open | 23 | ≤10 | Below target |
| Training Completion | 83% | ≥95% | Below target |
| Access Review Complete | 72% | ≥90% | Below target |
| Backup Success Rate | 94% | ≥99% | Below target |

All KPIs are trending in the right direction. The tool tracks month-on-month improvement automatically each time new data is added to `monitoring_metrics.csv`.

---

## Requirements

```
pandas>=1.5.0
matplotlib>=3.6.0
numpy>=1.23.0
```

Python 3.8 or higher. Tested on Python 3.11 (Windows 11 and Ubuntu 24). No external audit software or internet connection required.

---

## Related GRC Portfolio Projects

| Project | Description |
|---|---|
| [StandardBank-Risk-Assessment](https://github.com/Scottie222/StandardBank-Risk-Assessment) | ISO 27001 Risk Assessment — Experian SA breach 2020 |
| [VendorRisk-SA](https://github.com/Scottie222/VendorRisk-SA) | Third-Party Vendor Risk Management Tool |
| [OpenVantage-ISMS](https://github.com/Scottie222/OpenVantage-ISMS) | Full ISO 27001:2022 ISMS Documentation Suite |
| [POPIA-GDPR-Compliance-Tracker](https://github.com/Scottie222/POPIA-GDPR-Compliance-Tracker) | Automated POPIA/GDPR compliance scoring |
| [LifeHealthcare-BCP](https://github.com/Scottie222/LifeHealthcare-BCP) | BCP/DR Tool — Life Healthcare ransomware 2020 |

---

*Built by Bakithi Scott Ngcampalala | Junior Security Administrator @ Open Vantage*
*LinkedIn: https://www.linkedin.com/in/bakithi-scott-ngcampalala-0051a4105*

---

*All audit data in this repository is simulated for demonstration and portfolio purposes only. MTN Group Limited is referenced as the audit subject to provide realistic organisational context. This tool does not represent the actual security posture of MTN Group.*