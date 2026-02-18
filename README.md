# 🧠 skillsmith

[![PyPI version](https://img.shields.io/pypi/v/skillsmith.svg)](https://pypi.org/project/skillsmith/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Portable agentic skills library for professional AI engineering.**

`skillsmith` is a CLI tool that scaffolds industry-standard `.agent` structures into any project. It imbues your AI coding assistants with project-agnostic "expertise" across the entire software lifecycle.

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

- **600+ Skills (Categorized)**: Massive library organized into 9 broad categories (Security, Data-AI, Infrastructure...).
- **Tag-Based Bundles**: Install skills by topic tags (e.g., `python`, `react`, `aws`) using simple CLI flags.
- **23 Core Skills**: Out-of-the-box expertise for TDD, Security Audits, Context Engineering, and more.
- **AGENTS.md Standard**: Native support for the [agents.md](https://agents.md) open standard ("README for Agents").
- **Agentic Workflows**: Pre-defined templates for agentic loops, sub-agent coordination, and memory management.
- **Project Structure**: Scaffolds dedicated folders for `guides/`, `plans/`, and `workflows/`.
- **Portable & Modular**: Add only the skills you need for your specific tech stack.

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
├── AGENTS.md           # High-level context for AI agents
└── .agent/
    ├── skills/         # Modular expertise (SKILL.md files)
    ├── guides/         # Project-specific style & architecture docs
    ├── plans/          # Active implementation plans and RFCs
    ├── workflows/      # Automated tasks and deployment templates
    ├── prd.md          # Standard blueprint for new features
    └── status.md       # Global project state tracker
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
skillsmith lint --local
```

---

## 🗺️ Future Plans

We are evolving `skillsmith` into a central hub for agentic expertise. Our upcoming roadmap includes:

- **Central Skill Registry**: A hosted platform to browse, search, and share community-verified skills.
- **Framework Integrations**: Native scaffolding for Agno, LangChain, CrewAI, and more.
- **TUI Mode**: An interactive terminal interface for selecting and managing skills.
- **Agent Self-Installation**: APIs that allow agents to autonomously search for and install the skills they need to complete a task.

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
