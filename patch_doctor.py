"""
Patch script: adds PATH detection to the doctor command in src/skillsmith/cli.py
"""
import sys
from pathlib import Path

cli_path = Path(__file__).parent / "src" / "skillsmith" / "cli.py"
content = cli_path.read_bytes().decode("utf-8")

# ── 1. Locate the doctor function ───────────────────────────────────────────
DOCTOR_START = '@main.command()\r\n@click.option("--fix", is_flag=True, help="Auto-fix missing platform files by running init")\r\ndef doctor(fix):'

if DOCTOR_START not in content:
    # Try with \n if \r\n not found
    DOCTOR_START = DOCTOR_START.replace("\r\n", "\n")
    if DOCTOR_START not in content:
        print("ERROR: Could not find doctor function start")
        exit(1)

# ── 2. Define the new section for PATH detection ──────────────────────────────
PATH_DETECTION_CODE = """
    # ── 0. PATH Detection ─────────────────────────────────────────────────────
    console.print("[bold]Executable PATH[/bold]")
    is_on_path = shutil.which("skillsmith") is not None
    if is_on_path:
        console.print("  [green][OK][/green] 'skillsmith' command is on your PATH")
    else:
        all_ok = False
        console.print("  [red][!!][/red] 'skillsmith' is NOT on your PATH")
        
        # Try to find where it is
        import sysconfig
        scripts_dir = sysconfig.get_path("scripts")
        if not scripts_dir:
            # Fallback for some systems
            scripts_dir = str(Path(sys.executable).parent / "Scripts")
            
        console.print(f"  [dim]Expected location: {scripts_dir}[/dim]")
        
        if sys.platform == "win32":
            console.print(f"  [yellow]Tip:[/yellow] Run this to fix permanently: [bold]setx PATH \\\"%PATH%;{scripts_dir}\\\"[/bold]")
        else:
            console.print(f"  [yellow]Tip:[/yellow] Add this to your shell profile: [bold]export PATH=\\\"$PATH:{scripts_dir}\\\"[/bold]")
            
        console.print("  [blue][INFO][/blue] [bold]Alternative:[/bold] You can always use [bold]python -m skillsmith[/bold] to run the tool.")
"""

# Insert it right after `all_ok = True`
INSERT_POINT = "all_ok = True"
idx = content.find(INSERT_POINT, content.find(DOCTOR_START))
if idx == -1:
    print("ERROR: Could not find insertion point")
    exit(1)

insertion_idx = idx + len(INSERT_POINT)
new_content = content[:insertion_idx] + PATH_DETECTION_CODE + content[insertion_idx:]

cli_path.write_bytes(new_content.encode("utf-8"))
print("Doctor command patched successfully with PATH detection!")
