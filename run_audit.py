#!/usr/bin/env python3
"""
MTN ISMS Audit Tool — Master Runner
Executes all modules in sequence and generates the full audit package
"""

import sys
import os
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║          MTN GROUP — ISO 27001 ISMS AUDIT TOOL               ║
║       Internal Audit & Continuous Monitoring System          ║
╠══════════════════════════════════════════════════════════════╣
║  Standard : ISO/IEC 27001:2022                               ║
║  Scope    : MTN South Africa ISMS                            ║
║  Coverage : POPIA | GDPR | Annex A Controls                  ║
╚══════════════════════════════════════════════════════════════╝
"""

MODULES = [
    {
        "name": "Audit Planning",
        "script": os.path.join(BASE_DIR, "Audit_Planning", "audit_planning.py"),
        "description": "Generating audit plan, schedule, and checklist"
    },
    {
        "name": "Risk Scoring Engine",
        "script": os.path.join(BASE_DIR, "risk_engine", "risk_scoring.py"),
        "description": "Scoring risks and generating heatmaps"
    },
    {
        "name": "Control Assessment",
        "script": os.path.join(BASE_DIR, "Control_Assessment", "control_assessment.py"),
        "description": "Assessing ISO 27001 Annex A control effectiveness"
    },
    {
        "name": "Findings Analysis",
        "script": os.path.join(BASE_DIR, "Findings_Recommendations", "findings_analysis.py"),
        "description": "Analysing audit findings and generating remediation plan"
    },
    {
        "name": "Continuous Monitoring",
        "script": os.path.join(BASE_DIR, "Continuous_Monitoring", "continuous_monitoring.py"),
        "description": "Generating KPI trend dashboards"
    },
]


def run_module(module):
    print(f"\n{'─' * 62}")
    print(f"  ▶  {module['name']}")
    print(f"     {module['description']}")
    print(f"{'─' * 62}")
    result = subprocess.run(
        [sys.executable, module['script']],
        capture_output=True, text=True
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            print(f"  {line}")
    if result.returncode != 0:
        print(f"\n  [ERROR] {module['name']} failed:")
        print(result.stderr)
        return False
    return True


def print_output_summary():
    print(f"\n{'═' * 62}")
    print("  OUTPUT FILES GENERATED")
    print(f"{'═' * 62}")
    dirs = ["Audit_Planning","Risk_Scoring","Control_Assessment",
            "Findings_Recommendations","Continuous_Monitoring"]
    for d in dirs:
        full_path = os.path.join(BASE_DIR, d)
        if os.path.exists(full_path):
            files = os.listdir(full_path)
            if files:
                print(f"\n  {d}/")
                for f in sorted(files):
                    fpath = os.path.join(full_path, f)
                    size = os.path.getsize(fpath)
                    size_str = f"{size // 1024}KB" if size > 1024 else f"{size}B"
                    print(f"    ├── {f} ({size_str})")


def main():
    print(BANNER)
    print(f"  Started: {datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    results = []
    for module in MODULES:
        success = run_module(module)
        results.append((module['name'], success))

    print(f"\n{'═' * 62}")
    print("  EXECUTION SUMMARY")
    print(f"{'═' * 62}")
    all_ok = True
    for name, ok in results:
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"  {status}  {name}")
        if not ok:
            all_ok = False

    print_output_summary()
    print(f"\n  Finished: {datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    if all_ok:
        print("\n  ✓ MTN ISMS Audit completed successfully.\n")
    else:
        print("\n  ⚠ Some modules failed. Review errors above.\n")
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
