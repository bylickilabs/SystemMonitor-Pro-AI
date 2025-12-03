# 🔐 SECURITY POLICY  
SystemMonitor Pro AI  
BYLICKILABS – Intelligence Systems & Communications  
Security Contact: **bylicki@mail.de**
 
---

## 📌 Introduction
The security of **SystemMonitor Pro AI** is a top priority.  
The application is designed to run fully locally on the user's system and does not send any data to external servers or cloud services.  
Despite this offline architecture, a professional approach to vulnerabilities, disclosure and security quality is essential.

This security policy defines:
- how to report vulnerabilities  
- how we handle security reports  
- which versions are supported  
- which security principles apply to the application  

---

## 🛡 Supported Versions

| Version | Security Status |
|--------|-----------------|
| **1.x.x** | ✔ Receives security updates |
| **0.x.x** | ✖ No longer supported |

Security-related changes are communicated through **GitHub Releases** and the **CHANGELOG**.

---

## 📝 Reporting Vulnerabilities

If you discover a vulnerability or potentially critical behaviour, please report it **confidentially** to:

📧 **bylicki@mail.de**

Please include, where possible:
- short description of the issue  
- affected version (e.g. 1.0.0)  
- operating system (e.g. Windows 10/11)  
- steps to reproduce  
- a note on potential impact  

⚠ **Important:**  
Please **do not** publish sensitive security details in public GitHub issues or forums.  
Use the email address above or the GitHub Security Advisory system instead.

---

## 🔒 Responsible Disclosure

We are committed to a professional and responsible security lifecycle:

- **Acknowledgement** of the report: within **48 hours**
- **Initial analysis and risk assessment**: within **5 business days**
- **Fix or mitigation** (depending on severity):
  - critical: typically within **72 hours**
  - high: within **7 days**
  - medium/low: within **14 days**

After a fix has been released, security-relevant changes will be documented in the CHANGELOG.

---

## 🔧 Security Architecture of SystemMonitor Pro AI

SystemMonitor Pro AI follows a defensive and local-first security design:

- No cloud or server communication  
- No telemetry or hidden data collection  
- All AI/analytics logic is executed locally  
- No storage of passwords or confidential secrets  
- Exported data (JSON / profiling) remains local and fully visible to the user  
- Relies on established and vetted libraries (e.g. `psutil`, `PySide6`)  

Registry access (Windows) is limited to:
- Optional autostart configuration under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`

---

## 🔍 Security Testing & Penetration Testing Guidelines

Allowed (recommended):
- Local security testing on your own systems  
- Analysis of exported data (JSON, profiling)  
- Load testing of monitoring functionality  
- Verification of process management behaviour  

Not allowed:
- Attacks against third-party systems using this software  
- Public distribution of exploits without prior responsible disclosure  
- Misuse of the application for malicious purposes  

---

## 🛡 Recommendations for Users

- Only install versions from trusted sources (e.g. official GitHub repository).  
- Verify hashes/signatures when provided.  
- Prefer running the application with standard user privileges (no admin rights required).  
- Share export/log files only with trusted parties and after reviewing their content.  
