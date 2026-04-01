# MTN Group — ISO 27001 ISMS Audit Tool

> ISO/IEC 27001:2022 Internal Audit & Continuous Monitoring simulation for MTN Group Limited.

## Quick Start
```powershell
# Install dependencies
pip install -r requirements.txt

# Run full audit
python run_audit.py
```

## Structure
```
MTN-ISMS-Internal-Audit/
├── data/                          # Input CSV data files
├── risk_engine/                   # Risk scoring engine
├── Audit_Planning/                # Audit plan + checklist
├── Control_Assessment/            # ISO 27001 Annex A controls
├── Findings_Recommendations/      # Audit findings + remediation
├── Continuous_Monitoring/         # KPI trends dashboard
├── Risk_Scoring/                  # Generated charts (output)
├── reports/                       # Generated HTML report (output)
├── scripts/                       # Bash utility scripts
└── requirements.txt               # Python dependencies
```

## Run Individual Modules
```powershell
python Audit_Planning\audit_planning.py
python risk_engine\risk_scoring.py
python Control_Assessment\control_assessment.py
python Findings_Recommendations\findings_analysis.py
python Continuous_Monitoring\continuous_monitoring.py
```

## Standard
ISO/IEC 27001:2022 | POPIA | GDPR
