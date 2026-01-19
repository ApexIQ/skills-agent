import os
import shutil
import click
import requests
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

TEMPLATE_DIR = Path(__file__).parent / "templates"

def download_github_dir(repo_url, dest_dir):
    """Downloads a directory from GitHub using the API."""
    # Pattern: https://github.com/OWNER/REPO/tree/BRANCH/PATH
    match = re.search(r"github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)", repo_url)
    if not match:
        # Try raw content pattern or simpler repo/path
        match = re.search(r"github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)", repo_url)
        
    if not match:
        console.print("[red]Error: Invalid GitHub directory URL.[/red]")
        console.print("Expected: https://github.com/OWNER/REPO/tree/BRANCH/PATH")
        return False

    owner, repo, branch, path = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        items = response.json()
        
        # Check if the response is a list (directory contents)
        if not isinstance(items, list):
            console.print(f"[red]Error: URL must point to a directory, not a file.[/red]")
            return False

        dest_dir.mkdir(parents=True, exist_ok=True)
        
        with console.status(f"[bold blue]Downloading skill files...") as status:
            for item in items:
                if item["type"] == "file":
                    file_url = item["download_url"]
                    file_path = dest_dir / item["name"]
                    # Download file content
                    file_resp = requests.get(file_url)
                    file_resp.raise_for_status()
                    with open(file_path, "wb") as f:
                        f.write(file_resp.content)
                elif item["type"] == "dir":
                    # We only support shallow folders for now
                    pass
        
        # Verify if it's a valid skill
        if not (dest_dir / "SKILL.md").exists():
            console.print(f"[yellow]Warning: Downloaded folder does not contain SKILL.md.[/yellow]")
            
        return True
    except requests.exceptions.HTTPError as he:
        console.print(f"[red]GitHub API Error: {he.response.status_code} - {he.response.reason}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Download failed: {str(e)}[/red]")
        return False

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

@main.command(name="list")
def list_skills():
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
@click.argument("name_or_url")
def add(name_or_url):
    """Add a skill from local library or GitHub URL"""
    dest_dir = Path.cwd() / ".agents" / "skills"
    dest_dir.mkdir(parents=True, exist_ok=True)

    if name_or_url.startswith("http"):
        # Remote GitHub Add
        skill_name = name_or_url.split("/")[-1]
        dest_skill = dest_dir / skill_name
        
        if dest_skill.exists():
            console.print(f"[yellow]Skill '{skill_name}' already exists.[/yellow]")
            return
            
        if download_github_dir(name_or_url, dest_skill):
            console.print(f"[green][OK][/green] Successfully added remote skill: {skill_name}")
    else:
        # Local Add
        skill_name = name_or_url
        src_skill = TEMPLATE_DIR / ".agents" / "skills" / skill_name
        
        if not src_skill.exists():
            console.print(f"[red]Error: Skill '{skill_name}' not found in local library.[/red]")
            return
            
        dest_skill = dest_dir / skill_name
        if dest_skill.exists():
            console.print(f"[yellow]Skill '{skill_name}' already exists.[/yellow]")
            return
            
        shutil.copytree(src_skill, dest_skill)
        console.print(f"[green][OK][/green] Added skill: {skill_name}")

if __name__ == "__main__":
    main()
