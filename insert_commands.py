"""Insert snapshot and watch commands into cli.py before the __main__ block."""
from pathlib import Path

cli_path = Path(__file__).parent / "src" / "skillsmith" / "cli.py"
content = cli_path.read_bytes()

MARKER = b'if __name__ == "__main__":'
idx = content.rfind(MARKER)
if idx == -1:
    print("ERROR: marker not found")
    exit(1)

print(f"Found marker at byte {idx} of {len(content)}")

NEW_COMMANDS = b'''
@main.command()
@click.option("--note", "-n", default="", help="Optional note to embed in the snapshot")
@click.option("--list", "list_snapshots", is_flag=True, help="List existing snapshots")
@click.option("--restore", default="", help="Restore a snapshot by filename")
def snapshot(note, list_snapshots, restore):
    """Save or restore a snapshot of your .agent/ context.

    Snapshots are timestamped zips of your entire .agent/ directory stored in
    .agent/snapshots/. Use them to checkpoint context before big changes or
    restore after a long break.

    \\b
    Examples:
      skillsmith snapshot                          # save current state
      skillsmith snapshot -n "before refactor"    # save with a note
      skillsmith snapshot --list                   # list all snapshots
      skillsmith snapshot --restore 2026-02-19_10-30-00.zip
    """
    import datetime

    agent_dir = Path.cwd() / ".agent"
    snapshots_dir = agent_dir / "snapshots"

    if not agent_dir.exists():
        console.print("[red]Error: .agent/ not found. Run: skillsmith init[/red]")
        return

    if list_snapshots:
        if not snapshots_dir.exists() or not any(snapshots_dir.glob("*.zip")):
            console.print("[dim]No snapshots found.[/dim]")
            return
        table = Table(title=f"Snapshots: {snapshots_dir}")
        table.add_column("File", style="cyan")
        table.add_column("Size", style="white")
        table.add_column("Note", style="dim")
        for snap in sorted(snapshots_dir.glob("*.zip"), reverse=True):
            size_kb = snap.stat().st_size / 1024
            snap_note = ""
            try:
                with zipfile.ZipFile(snap) as z:
                    snap_note = z.comment.decode("utf-8", errors="ignore")
            except Exception:
                pass
            table.add_row(snap.name, f"{size_kb:.1f} KB", snap_note)
        console.print(table)
        return

    if restore:
        snap_file = snapshots_dir / restore if not Path(restore).is_absolute() else Path(restore)
        if not snap_file.exists():
            console.print(f"[red]Snapshot not found: {snap_file}[/red]")
            return
        console.print(f"[yellow]Restoring {snap_file.name} ...[/yellow]")
        with zipfile.ZipFile(snap_file) as z:
            z.extractall(agent_dir.parent)
        console.print(f"[green][OK][/green] Restored {snap_file.name}")
        return

    snapshots_dir.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snap_path = snapshots_dir / f"{timestamp}.zip"

    file_count = 0
    with zipfile.ZipFile(snap_path, "w", zipfile.ZIP_DEFLATED) as zf:
        if note:
            zf.comment = note.encode("utf-8")
        for file in sorted(agent_dir.rglob("*")):
            if "snapshots" in file.parts:
                continue
            if file.is_file():
                arcname = file.relative_to(agent_dir.parent)
                zf.write(file, arcname)
                file_count += 1

    size_kb = snap_path.stat().st_size / 1024
    console.print(f"[green][OK][/green] Snapshot saved: [bold]{snap_path.name}[/bold]")
    console.print(f"     Files: {file_count}  |  Size: {size_kb:.1f} KB")
    if note:
        console.print(f"     Note:  {note}")
    console.print(f"     Path:  [dim]{snap_path}[/dim]")


@main.command()
@click.option("--interval", default=30, show_default=True, help="Poll interval in seconds")
@click.option("--state-file", default=".agent/STATE.md", show_default=True,
              help="Path to STATE.md to monitor")
@click.option("--stale-hours", default=24, show_default=True,
              help="Hours before STATE.md is considered stale")
def watch(interval, state_file, stale_hours):
    """Watch for context drift and keep your agent state fresh.

    Monitors your project for:
      - Git branch switches (prompts you to update STATE.md)
      - STATE.md staleness (warns when context is older than N hours)
      - New/deleted skills in .agent/skills/

    \\b
    Examples:
      skillsmith watch                  # poll every 30s
      skillsmith watch --interval 60    # poll every 60s
      skillsmith watch --stale-hours 8  # warn after 8h
    """
    import time
    import datetime
    import subprocess as sp

    state_path = Path.cwd() / state_file
    skills_dir = Path.cwd() / ".agent" / "skills"

    def get_branch():
        try:
            result = sp.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, cwd=str(Path.cwd())
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None

    def get_skill_set():
        if not skills_dir.exists():
            return set()
        return {f.parent.name for f in skills_dir.rglob("SKILL.md")}

    def state_age_hours():
        if not state_path.exists():
            return None
        mtime = datetime.datetime.fromtimestamp(state_path.stat().st_mtime)
        return (datetime.datetime.now() - mtime).total_seconds() / 3600

    console.print(f"\\n[bold cyan]skillsmith watch[/bold cyan] - monitoring context drift")
    console.print(f"  STATE.md:    [dim]{state_path}[/dim]")
    console.print(f"  Poll:        every {interval}s")
    console.print(f"  Stale after: {stale_hours}h")
    console.print(f"  Press [bold]Ctrl+C[/bold] to stop.\\n")

    last_branch = get_branch()
    last_skills = get_skill_set()
    warned_stale = False

    if last_branch:
        console.print(f"[dim]Branch: {last_branch}[/dim]")

    try:
        while True:
            time.sleep(interval)
            now_str = datetime.datetime.now().strftime("%H:%M:%S")

            current_branch = get_branch()
            if current_branch and current_branch != last_branch:
                console.print(
                    f"[{now_str}] [yellow][!!] Branch changed:[/yellow] "
                    f"[dim]{last_branch}[/dim] -> [bold]{current_branch}[/bold]"
                )
                console.print(f"          Update STATE.md with your current task context.")
                last_branch = current_branch
                warned_stale = False

            age = state_age_hours()
            if age is not None and age > stale_hours and not warned_stale:
                console.print(
                    f"[{now_str}] [yellow][!!] STATE.md is stale[/yellow] "
                    f"({age:.1f}h old > {stale_hours}h limit)"
                )
                console.print(
                    f"          Run: [bold]skillsmith snapshot -n 'checkpoint'[/bold] "
                    f"then update STATE.md"
                )
                warned_stale = True
            elif age is not None and age <= stale_hours:
                warned_stale = False

            current_skills = get_skill_set()
            added = current_skills - last_skills
            removed = last_skills - current_skills
            if added:
                console.print(
                    f"[{now_str}] [green][+][/green] New skills: {', '.join(sorted(added))}"
                )
            if removed:
                console.print(
                    f"[{now_str}] [red][-][/red] Removed skills: {', '.join(sorted(removed))}"
                )
            last_skills = current_skills

    except KeyboardInterrupt:
        console.print("\\n[dim]Watch stopped.[/dim]")


'''

new_content = content[:idx] + NEW_COMMANDS + content[idx:]
cli_path.write_bytes(new_content)
print(f"Done. New file size: {len(new_content)} bytes")
