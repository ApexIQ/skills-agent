import os
import shutil
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

TEMPLATE_DIR = Path(__file__).parent / "templates"

@click.group()
def main():
    """Agentic Skills Library CLI"""
    pass

@main.command()
@click.option("--minimal", is_flag=True, help="Create minimal structure without optional skills")
@click.option("--agents-md-only", is_flag=True, help="Only create AGENTS.md")
def init(minimal, agents_md_only):
    """Initialize .agents and AGENTS.md structure"""
    cwd = Path.cwd()
    
    # 1. Handle AGENTS.md
    agents_md = cwd / "AGENTS.md"
    if not agents_md.exists():
        template_agents_md = TEMPLATE_DIR / "AGENTS.md"
        if template_agents_md.exists():
            shutil.copy(template_agents_md, agents_md)
            console.print("[green][OK][/green] Created AGENTS.md")
        else:
            # Fallback inline template
            with open(agents_md, "w") as f:
                f.write("# AGENTS.md\n\n> This file provides AI coding agents with context about this project.\n\n## Project Overview\n\n## Setup Commands\n\n## Testing Workflows\n\n## Coding Style\n")
            console.print("[green][OK][/green] Created AGENTS.md (default template)")
    
    if agents_md_only:
        return

    # 2. Handle .agents folder
    agents_dir = cwd / ".agents"
    agents_dir.mkdir(exist_ok=True)
    
    template_agents_dir = TEMPLATE_DIR / ".agents"
    if template_agents_dir.exists():
        # Copy everything EXCEPT skills (handled separately)
        for item in template_agents_dir.iterdir():
            if item.name == "skills":
                continue
                
            dest = agents_dir / item.name
            if item.is_dir():
                # For directories like guides, plans, workflows: 
                # mkdir and copy contents (or copytree if not exists)
                if not dest.exists():
                    shutil.copytree(item, dest)
                    console.print(f"[green][OK][/green] Created .agents/{item.name}/")
                else:
                    # If folder exists, copy individual files (don't overwrite whole folder)
                    for subitem in item.iterdir():
                        if subitem.is_file() and not (dest / subitem.name).exists():
                            shutil.copy(subitem, dest / subitem.name)
                            console.print(f"[green][OK][/green] Added {subitem.name} to .agents/{item.name}/")
            else:
                # For files like prd.md, status.md
                if not dest.exists():
                    shutil.copy(item, dest)
                    console.print(f"[green][OK][/green] Created .agents/{item.name}")
        
        # 3. Handle skills (unless minimal)
        if not minimal:
            src_skills = template_agents_dir / "skills"
            dest_skills_dir = agents_dir / "skills"
            dest_skills_dir.mkdir(exist_ok=True)
            
            if src_skills.exists():
                for skill_folder in src_skills.iterdir():
                    if skill_folder.is_dir():
                        dest_skill = dest_skills_dir / skill_folder.name
                        if not dest_skill.exists():
                            shutil.copytree(skill_folder, dest_skill)
                            console.print(f"[blue][INFO][/blue] Added skill: {skill_folder.name}")
    
    console.print("\n[bold green]Successfully initialized .agents structure![/bold green]")

@main.command()
def list():
    """List all available portable skills"""
    skills_dir = TEMPLATE_DIR / ".agents" / "skills"
    if not skills_dir.exists():
        console.print("[red]Error: Templates not found.[/red]")
        return
        
    table = Table(title="Available Skills")
    table.add_column("Skill", style="cyan")
    table.add_column("Description", style="white")
    
    for skill_folder in sorted(skills_dir.iterdir()):
        if skill_folder.is_dir():
            skill_md = skill_folder / "SKILL.md"
            description = "No description found"
            if skill_md.exists():
                with open(skill_md, "r") as f:
                    content = f.read()
                    if "description:" in content:
                        for line in content.split("\n"):
                            if "description:" in line:
                                description = line.split("description:")[1].strip()
                                break
            table.add_row(skill_folder.name, description)
            
    console.print(table)

@main.command()
@click.argument("skill_name")
def add(skill_name):
    """Add a specific skill to your .agents/skills folder"""
    src_skill = TEMPLATE_DIR / ".agents" / "skills" / skill_name
    if not src_skill.exists():
        console.print(f"[red]Error: Skill '{skill_name}' not found.[/red]")
        return
        
    dest_dir = Path.cwd() / ".agents" / "skills"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    dest_skill = dest_dir / skill_name
    if dest_skill.exists():
        console.print(f"[yellow]Skill '{skill_name}' already exists.[/yellow]")
        return
        
    shutil.copytree(src_skill, dest_skill)
    console.print(f"[green][OK][/green] Added skill: {skill_name}")

if __name__ == "__main__":
    main()
