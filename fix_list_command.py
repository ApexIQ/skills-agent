"""
Patch script: fixes the list_skills command in src/skillsmith/cli.py
Bug: list --tag/--category always returned empty because it iterated
     only the 1 local template skill instead of the 625-skill catalog JSON.
Fix: rewrite list_skills to iterate catalog directly.
"""
from pathlib import Path

cli_path = Path(__file__).parent / "src" / "skillsmith" / "cli.py"
content = cli_path.read_bytes().decode("utf-8")

# ── Locate the old list_skills block ─────────────────────────────────────────
START = '@main.command(name="list")'
# The exact bytes after the old function, before the `add` command
END_SENTINEL = "\r\n\r\n@main.command()\r\n@click.argument"

start_idx = content.find(START)
end_idx   = content.find(END_SENTINEL, start_idx)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: Could not locate list_skills block (start={start_idx}, end={end_idx})")
    exit(1)

old_block = content[start_idx:end_idx]
print(f"Found old block ({len(old_block)} chars)")

NEW_BLOCK = '@main.command(name="list")\n@click.option("--category", help="Filter by category (e.g. development, security, data-ai)")\n@click.option("--tag", help="Filter by tag (e.g. react, nextjs, python, aws)")\n@click.option("--list-categories", is_flag=True, help="Show all available categories and popular tags")\ndef list_skills(category, tag, list_categories):\n    """List available skills from the catalog (625+ skills). Filter by --category or --tag."""\n\n    catalog = load_catalog()\n\n    if list_categories:\n        if catalog:\n            console.print("\\n[bold cyan]Available Categories:[/bold cyan]")\n            for cat in catalog.get("categories", []):\n                console.print(f"  - {cat}")\n\n            # Collect all unique tags from the catalog, sorted by frequency\n            tag_counts: dict = {}\n            for skill_data in catalog.get("skills", {}).values():\n                for t in skill_data.get("tags", []):\n                    tag_counts[t] = tag_counts.get(t, 0) + 1\n            top_tags = sorted(tag_counts, key=lambda t: tag_counts[t], reverse=True)[:20]\n\n            console.print("\\n[bold cyan]Popular Tags (use with --tag):[/bold cyan]")\n            for t in top_tags:\n                console.print(f"  - {t}  [dim]({tag_counts[t]} skills)[/dim]")\n\n            console.print("\\n[dim]Install by category:  skillsmith init --category <name>[/dim]")\n            console.print("[dim]Install by tag:        skillsmith init --tag <name>[/dim]\\n")\n        else:\n            console.print("[red]Catalog not found. Cannot list categories.[/red]")\n        return\n\n    # ── Main listing: iterate the catalog (625+ skills), not local template dir ──\n    catalog_skills = catalog.get("skills", {}) if catalog else {}\n\n    if not catalog_skills:\n        console.print("[red]Error: Skill catalog not found or empty.[/red]")\n        return\n\n    title = "Available Skills (catalog)"\n    if category:\n        title += f" — category: {category}"\n    if tag:\n        title += f" — tag: {tag}"\n\n    table = Table(title=title, show_header=True, header_style="bold magenta")\n    table.add_column("Skill", style="cyan", no_wrap=True)\n    table.add_column("Category", style="magenta")\n    table.add_column("Tags", style="dim")\n    table.add_column("Description", style="white")\n\n    count = 0\n    for skill_name, skill_data in sorted(catalog_skills.items()):\n        skill_category = skill_data.get("category", "")\n        skill_tags     = skill_data.get("tags", [])\n        skill_desc     = skill_data.get("description", "No description")\n\n        # Apply filters\n        if category and skill_category != category:\n            continue\n        if tag and tag.lower() not in [t.lower() for t in skill_tags]:\n            continue\n\n        tags_str = ", ".join(skill_tags[:4])\n        if len(skill_tags) > 4:\n            tags_str += f" +{len(skill_tags) - 4}"\n\n        desc_str = skill_desc[:72] + ("..." if len(skill_desc) > 72 else "")\n        table.add_row(skill_name, skill_category, tags_str, desc_str)\n        count += 1\n\n    console.print(table)\n    console.print(\n        f"\\n[dim]Showing {count} skill(s). "\n        "Install with: skillsmith init --category <name>  or  skillsmith init --tag <name>[/dim]\\n"\n    )'

new_content = content[:start_idx] + NEW_BLOCK + content[end_idx:]

cli_path.write_bytes(new_content.encode("utf-8"))
print(f"Patched successfully! New file size: {len(new_content)} chars")

# Sanity check: old iter_skill_dirs loop must be gone from list_skills
list_start = new_content.find('@main.command(name="list")')
add_start  = new_content.find(END_SENTINEL, list_start)
new_list_block = new_content[list_start:add_start]
assert "for skill_folder in iter_skill_dirs" not in new_list_block, \
    "ERROR: old iter_skill_dirs loop still present in list_skills!"
assert "catalog_skills.items()" in new_list_block, \
    "ERROR: new catalog iteration not found in list_skills!"
print("Sanity checks passed!")
