# 🤝 CONTRIBUTING GUIDELINES  
SystemMonitor Pro AI  
BYLICKILABS – Intelligence Systems & Communications  
Contact: **bylicki@mail.de**
 
---

## 📌 Introduction
Thank you for your interest in contributing to **SystemMonitor Pro AI**.  
Contributions help improve quality, stability and feature coverage.

We welcome:
- bug reports  
- improvement suggestions  
- new features/modules  
- documentation contributions  
- security reviews and feedback  

These guidelines will help you contribute in a structured and efficient way.

---

## 🧭 Code of Conduct

For all interactions and contributions:

- Be respectful and professional  
- No harassment, discrimination or toxic behaviour  
- Keep technical discussions constructive and focused  
- Give and accept feedback in a positive and solution-oriented manner  

Severe violations may result in rejected contributions or blocked users.

---

## 🐛 Bug Reports

When reporting a bug, please include:

- **Short description** of the issue  
- **Reproduction steps** (step by step)  
- **Expected vs. actual behaviour**  
- **System details**:
  - Windows version (e.g. Windows 10 Pro 22H2)  
  - Python version (e.g. 3.11.x)  
- **Logs / error messages** (tracebacks, console output)  
- Optional: screenshots or short screencasts  

⚠ Security-related bugs should **not** be submitted as public issues → see SECURITY.md and use **bylicki@mail.de**.

---

## 🚀 Feature Requests

For feature suggestions or enhancements, please describe:

- Which problem is being solved?  
- Who benefits from the feature (target user)?  
- What would the ideal workflow look like?  
- Any similar tools/features as reference?  
- Optional: technical ideas (new tab, new module, new AI analysis, etc.)  

The clearer and more structured the request, the easier we can review and consider it.

---

## 🔧 Pull Request Guidelines

Before opening a pull request, we recommend:

1. **Fork** the repository on GitHub  
2. Create a dedicated branch, for example:
   - `feature/ai-forecasting-improvement`
   - `fix/process-monitor-crash`
3. Develop and test changes locally  
4. Follow PEP8 style conventions where possible  
5. Use meaningful commit messages, such as:
   - `Add JSON export for event log`
   - `Fix crash when killing terminated process`
6. In the PR description, clearly explain:
   - What was changed?  
   - Which problem is solved?  
   - How was it tested?  
   - Any breaking changes?  

PRs with clear scope, tests and documentation are more likely to be reviewed quickly.

---

## 🧪 Testing & Quality Assurance

Before submitting a PR, please make sure:

- The application starts without errors (`python main.py`).  
- Dashboard displays metrics (CPU/RAM/Disk/Net) correctly.  
- Process monitor is stable, including the “kill process” action.  
- Events are correctly written into the AI event log.  
- Export functions (JSON, profiling) work without errors.  
- There are no obvious performance issues (e.g. busy loops, blocking calls in UI thread).  

If you add unit or integration tests, please describe them in the PR.

---

## 📦 Development Environment Setup

### 1️⃣ Clone repository
```bash
git clone https://github.com/bylickilabs/SystemMonitorProAI.git
cd SystemMonitorProAI
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run application
```bash
python main.py
```

---

## 🧩 High-Level Architecture

- `main.py` – entry point, application & UI bootstrap  
- `ui_main.py` – main window, tabs, language switch, event handling  
- `ui_components.py` – UI components (cards, tables, graphs, heatmap, event log)  
- `monitoring.py` – backend logic for system metrics & AI analytics  
- `config.py` – metadata, configuration, constants  

For larger refactorings, please open an issue first to discuss your proposal.

---

## 💬 Contact

For questions, larger proposals or collaboration ideas:

📧 **bylicki@mail.de**  
