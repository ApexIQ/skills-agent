"""Debug: find the exact bytes around the add command decorator."""
from pathlib import Path

cli_path = Path(__file__).parent / "src" / "skillsmith" / "cli.py"
content = cli_path.read_bytes().decode("utf-8")

# Find the list command start
start_idx = content.find('@main.command(name="list")')
print(f"list command starts at: {start_idx}")

# Find the add command - search for it after the list command
add_idx = content.find("@main.command()", start_idx + 100)
print(f"next @main.command() at: {add_idx}")

# Show what's around add_idx
print("Context around add command:")
print(repr(content[add_idx-50:add_idx+80]))

# Also show the end of the list command block
print("\nEnd of list block (chars before add):")
print(repr(content[add_idx-100:add_idx]))
