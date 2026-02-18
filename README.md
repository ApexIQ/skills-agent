# 🧠 skillsmith

[![PyPI version](https://img.shields.io/pypi/v/skillsmith.svg)](https://pypi.org/project/skillsmith/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The universal agent platform. One install. Every AI coding tool. Instantly smart.**

`skillsmith` is a CLI tool that scaffolds industry-standard `.agent` structures into any project and automatically configures **every major AI coding assistant** — Gemini CLI, Claude Code, Cursor, Windsurf, and GitHub Copilot — to use your project's skills, context, and workflows.

---

## 🚀 Quick Start

Initialize a new project with best-practice agent context in seconds:

```bash
# Install the library
pip install skillsmith

# Scaffold the .agent structure and AGENTS.md
skillsmith init
```

---

## ✨ Key Features

- **🌐 Universal Agent Platform** *(v0.3.0)*: Auto-generates platform-specific config files for Gemini, Claude, Cursor, Windsurf, and Copilot.
- **600+ Skills (Categorized)**: Massive library organized into 9 broad categories (Security, Data-AI, Infrastructure...).
- **GSD Protocol**: Built-in Discuss → Plan → Execute → Verify workflow for reliable agent output.
- **Smart Append**: If platform config files already exist, skillsmith appends its config without overwriting your rules.
- **23 Core Skills**: Out-of-the-box expertise for TDD, Security Audits, Context Engineering, and more.
- **AGENTS.md Standard**: Native support for the [agents.md](https://agents.md) open standard ("README for Agents").
- **State Management**: `PROJECT.md`, `ROADMAP.md`, and `STATE.md` templates prevent AI context rot.
- **Portable & Modular**: Add only the skills you need for your specific tech stack.

### 🔌 Platform Compatibility

| Platform | Auto-Generated File | Format Source |
|---|---|---|
| **Gemini CLI** | `GEMINI.md` | [geminicli.com](https://geminicli.com) |
| **Claude Code** | `CLAUDE.md` | [docs.anthropic.com](https://docs.anthropic.com) |
| **Cursor** | `.cursorrules` + `.cursor/rules/skillsmith.mdc` | [cursor.com/docs](https://cursor.com/docs) |
| **Windsurf** | `.windsurfrules` | [docs.windsurf.com](https://docs.windsurf.com) |
| **GitHub Copilot** | `.github/copilot-instructions.md` | [docs.github.com](https://docs.github.com) |

---

## 🛠 Included Skills library

The library contains **626 skills** across 9 major categories:
1. **Architecture** (60 skills)
2. **Business** (37 skills)
3. **Data-AI** (92 skills)
4. **Development** (81 skills)
5. **General** (128 skills)
6. **Infrastructure** (78 skills)
7. **Security** (112 skills)
8. **Testing** (22 skills)
9. **Workflow** (16 skills)

Run `skillsmith list --list-categories` to explore.

| Category | Skill | Description |
|----------|-------|-------------|
| **AI Strategy** | `memory-patterns` | Manage agent context window and long-term memory. |
| | `prompt-engineering` | Best practices for few-shot and chain-of-thought prompts. |
| **Engineering** | `test-driven-development` | Structured TDD (Red → Green → Refactor) for agents. |
| **Security** | `security-audit` | OWASP-based security checklists for automated reviews. |
| **Fullstack** | `fastapi-best-practices` | Patterns for high-performance Python backends. |

---

## 📖 Directory Structure

When you run `skillsmith init`, it creates:

```text
.
├── AGENTS.md                          # Universal agent instructions (Codex, OpenCode)
├── GEMINI.md                          # Gemini CLI auto-loads this
├── CLAUDE.md                          # Claude Code auto-loads this
├── .cursorrules                       # Cursor auto-loads this
├── .windsurfrules                     # Windsurf auto-loads this
├── .cursor/rules/skillsmith.mdc       # Cursor modern rule format
├── .github/copilot-instructions.md    # GitHub Copilot auto-loads this
└── .agent/
    ├── skills/         # Modular expertise (SKILL.md files)
    ├── guides/         # Project-specific style & architecture docs
    ├── plans/          # Active implementation plans and RFCs
    ├── workflows/      # Automated tasks and deployment templates
    ├── PROJECT.md      # Vision, tech stack, architecture
    ├── ROADMAP.md      # Strategic milestones and phases
    ├── STATE.md        # Current task context (read FIRST every session)
    └── prd.md          # Standard blueprint for new features
```

---

## 💻 CLI Commands

### Initialize Project
Scaffold the full structure including all 23 skills.
```bash
skillsmith init
```

### Minimal Scaffolding
Create the directory structure and templates without the pre-built skills.
```bash
skillsmith init --minimal
```

### Install by Category or Tag
Install bundles of skills for specific domains.
```bash
# Install all Security skills
skillsmith init --category security

# Install all Python skills
skillsmith init --tag python
```

### List Available Skills
View the library of portable expertise.
```bash
skillsmith list

# Filter by category
skillsmith list --category data-ai

# Filter by tag
skillsmith list --tag react
```

### Update Skills
Sync local project skills with the library and latest best practices.
```bash
skillsmith update
```

### Validate Skills
Verify skill structure, metadata, and link integrity.
```bash
# Basic validation
skillsmith lint --local

# AgentSkills.io standard compliance (adopted by Anthropic, Microsoft, OpenAI, Google)
skillsmith lint --spec agentskills
```

### Compose a Workflow
Generate a workflow by composing relevant skills for a goal.
```bash
skillsmith compose "build a saas mvp"
skillsmith compose "fix a security vulnerability" --max-skills 5
```
Outputs a numbered workflow `.md` to `.agent/workflows/<goal-slug>.md`.

### Health Check
Verify your entire skillsmith setup across all AI platforms.
```bash
skillsmith doctor

# Auto-fix missing platform files
skillsmith doctor --fix
```

### Context Budget
Analyze token usage across all platform files and skills.
```bash
skillsmith budget
```

---

## 🗺️ Roadmap

### ✅ Released
- **v0.1.0** — Core CLI, AGENTS.md standard, skill scaffolding.
- **v0.2.0** — 600+ skills, GSD workflow integration, categories & tags.
- **v0.3.0** — Universal Agent Platform: auto-generates config for Gemini, Claude, Cursor, Windsurf, Copilot. GSD state files (PROJECT.md, ROADMAP.md, STATE.md). Smart append (never overwrites existing config).

### 🔜 Planned
- **v0.4.0** — Bundles (role-based curated skill sets: Web Wizard, Security Engineer, etc.).
- **v0.5.0** — Workflows (ordered multi-step execution playbooks).
- **Central Skill Registry**: A hosted platform to browse, search, and share community-verified skills.
- **Agent Self-Installation**: APIs that allow agents to autonomously search for and install skills.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🤝 Contributing

Contributions are welcome! If you have a portable skill that could benefit other developers, please open a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingSkill`)
3. Commit your Changes (`git commit -m 'feat: add AmazingSkill'`)
4. Push to the Branch (`git push origin feature/AmazingSkill`)
5. Open a Pull Request

---

Developed with ❤️ by **ApexIQ**
