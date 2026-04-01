# MTN Group ISMS — Audit Findings & Recommendations

**Report Date:** 01 April 2026
**Standard:** ISO/IEC 27001:2022

---

## Executive Summary

This audit identified **10 findings**. **2 Critical** and **5 High** severity findings require immediate attention. **7** findings remain open.

---

## Critical Findings

### F001: MFA Not Enforced
- **Category:** Access Control
- **Control Ref:** A.9.4.2
- **Status:** Open
- **Due Date:** 2025-05-31

**Description:** Multi-Factor Authentication is not enforced on VPN and privileged accounts

**Recommendation:** Implement MFA across all remote access and admin accounts within 30 days

---

### F002: No PAM Solution
- **Category:** Access Control
- **Control Ref:** A.9.2.3
- **Status:** Open
- **Due Date:** 2025-05-31

**Description:** No Privileged Access Management solution deployed for admin accounts

**Recommendation:** Deploy CyberArk or equivalent PAM solution and enforce least privilege

---

## High Findings

### F003: Patching Delays
- **Category:** Operations
- **Control Ref:** A.12.6.1
- **Status:** In Progress
- **Due Date:** 2025-06-15

**Description:** Critical patches taking 45+ days to apply across server fleet

**Recommendation:** Implement automated patching with 14-day SLA for critical patches

---

### F004: No Third-Party Risk Process
- **Category:** Supplier Relations
- **Control Ref:** A.15.1.2
- **Status:** Open
- **Due Date:** 2025-09-30

**Description:** No formal vendor assessment or TPRA process for critical suppliers

**Recommendation:** Establish TPRA programme and conduct assessments on all Tier-1 vendors

---

### F005: IRP Not Tested
- **Category:** Incident Mgmt
- **Control Ref:** A.16.1.1
- **Status:** Open
- **Due Date:** 2025-06-30

**Description:** Incident Response Plan has not been tested via tabletop or simulation

**Recommendation:** Conduct quarterly tabletop exercises and annual full DR simulation

---

### F006: POPIA Gaps
- **Category:** Compliance
- **Control Ref:** A.18.1.1
- **Status:** In Progress
- **Due Date:** 2025-05-31

**Description:** Data subject rights requests process incomplete with no formal deletion workflow

**Recommendation:** Implement DSAR process and appoint Information Officer under POPIA

---

### F007: DR Plan Untested
- **Category:** Business Continuity
- **Control Ref:** A.17.1.2
- **Status:** Open
- **Due Date:** 2025-10-31

**Description:** Disaster Recovery plan not tested in over 18 months

**Recommendation:** Schedule and execute full DR failover test and document gaps

---

## Medium Findings

### F008: Weak Cipher Usage
- **Category:** Cryptography
- **Control Ref:** A.10.1.1
- **Status:** In Progress
- **Due Date:** 2025-07-31

**Description:** Legacy systems running TLS 1.0/1.1 and outdated cipher suites

**Recommendation:** Upgrade all systems to TLS 1.3 and disable deprecated protocols

---

### F009: CCTV Coverage Gaps
- **Category:** Physical Security
- **Control Ref:** A.11.1.1
- **Status:** Open
- **Due Date:** 2025-08-31

**Description:** Three blind spots identified in data centre perimeter CCTV coverage

**Recommendation:** Install additional cameras to eliminate blind spots and test coverage monthly

---

### F010: Annual-Only Security Training
- **Category:** HR Security
- **Control Ref:** A.7.2.2
- **Status:** Open
- **Due Date:** 2025-07-31

**Description:** Security awareness training conducted annually which is insufficient

**Recommendation:** Implement monthly phishing simulations and quarterly training modules

---
