# 🤖 AGENTS.md - Context & Instructions for AI Agents

> **Start Here:** This file is the primary entry point for AI Agents working on this project.

## 🧠 Prime Directives (The "GSD" Protocol)

1.  **Read `.agent/STATE.md` First:** Before doing anything, orient yourself by reading the current project state.
2.  **Atomic Execution:** Break complex tasks into small, verified steps.
    - Discuss -> Plan -> Execute -> Verify.
3.  **Update State:** After every significant step, update `.agent/STATE.md`.
4.  **No Hallucinations:** If you are unsure, ask the user or check the code. Do not guess.

## 📂 Project Structure

- **`.agent/`**: Your brain. Stores skills, plans, and state.
    - **`skills/`**: "How-to" guides for specific tasks.
    - **`params/`**: Project-specific constraints.
    - **`PROJECT.md`**: High-level vision and tech stack.
    - **`ROADMAP.md`**: Strategic milestones.
    - **`STATE.md`**: Current tactical status.

## 🛠 Active Skills

Run `skillsmith list` to see available skills. specialized instructions are in `.agent/skills/`.
