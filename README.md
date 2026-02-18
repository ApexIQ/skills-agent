# skillsmith

[![PyPI version](https://img.shields.io/pypi/v/skillsmith.svg)](https://pypi.org/project/skillsmith/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**One command to make your repo agent-ready.**

`skillsmith` gives AI coding assistants the project context they need to work reliably: structure, rules, state files, and reusable skills. It bootstraps a portable `.agent/` workspace, wires platform-specific instruction files, and can expose skills over MCP for on-demand use.

## Why skillsmith

Without project structure, agents lose context, repeat mistakes, and drift.

With `skillsmith`, every repo gets:

- A standard agent workspace (`.agent/`)
- Shared project memory (`PROJECT.md`, `ROADMAP.md`, `STATE.md`)
- Platform-specific instruction files (Claude, Gemini, Cursor, Windsurf, Copilot)
- A skill layer for repeatable workflows and better execution quality
- Optional MCP server for dynamic skill retrieval

## Install

```bash
pip install skillsmith
```

For MCP support:

```bash
pip install skillsmith[mcp]
```

## 60-Second Quick Start

```bash
skillsmith init
```

This scaffolds:

- `AGENTS.md`
- `CLAUDE.md`, `GEMINI.md`
- `.cursorrules`, `.cursor/rules/skillsmith.mdc`
- `.windsurfrules`
- `.github/copilot-instructions.md`
- `.agent/` with state files, guides/plans/workflows, and starter skills

## Core Capabilities

### 1) Project Bootstrapping

```bash
skillsmith init
skillsmith init --minimal
skillsmith init --agents-md-only
skillsmith init --all
skillsmith init --category <category>
skillsmith init --tag <tag>
```

### 2) Skill Discovery and Management

```bash
skillsmith list
skillsmith list --list-categories
skillsmith list --category <category>
skillsmith list --tag <tag>

skillsmith add <skill-name>
skillsmith add <github-directory-url>

skillsmith update
skillsmith update --force

skillsmith lint
skillsmith lint --local
skillsmith lint --spec agentskills
```

### 3) Workflow and Health Tooling

```bash
skillsmith compose "build a saas mvp"
skillsmith doctor
skillsmith doctor --fix
skillsmith budget
```

### 5) Context Management

Save a snapshot of your `.agent/` before big changes or long breaks:

```bash
skillsmith snapshot                          # save current state
skillsmith snapshot -n "before refactor"    # save with a note
skillsmith snapshot --list                   # list all snapshots
skillsmith snapshot --restore 2026-02-19_10-30-00.zip
```

Watch for context drift in the background:

```bash
skillsmith watch                  # poll every 30s
skillsmith watch --interval 60    # poll every 60s
skillsmith watch --stale-hours 8  # warn after 8h instead of 24h
```

`watch` detects:
- Git branch switches → prompts you to update `STATE.md`
- `STATE.md` staleness → warns when context is older than N hours
- New or removed skills in `.agent/skills/`

### 4) MCP Server

Run via stdio (default):

```bash
skillsmith serve
```

Run via HTTP:

```bash
skillsmith serve --transport http --host localhost --port 47731
```

MCP tools exposed:

- `list_skills`
- `get_skill(name)`
- `search_skills(query)`
- `compose_workflow(goal)`

## Platform Integration

### Claude Code

```bash
claude mcp add skillsmith -- skillsmith serve
```

HTTP mode:

```bash
claude mcp add --transport http skillsmith http://localhost:47731/mcp
```

### Cursor (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "skillsmith": {
      "command": "skillsmith",
      "args": ["serve"]
    }
  }
}
```

## Current Status

- Package version: `0.5.0`
- CLI scaffolding and management commands are implemented
- Starter lifecycle skills are bundled
- MCP server is available with optional dependency install
- Context management: `snapshot` and `watch` commands

## Development

Run from source:

```bash
PYTHONPATH=src python -m skillsmith.cli --help
```

## License

MIT. See `LICENSE`.
