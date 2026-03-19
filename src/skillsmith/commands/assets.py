import json
from pathlib import Path

import click
from rich.table import Table

from . import console
from .assets_runtime import (
    DEFAULT_RUNTIME_ASSETS,
    bootstrap_runtime_assets,
    describe_runtime_assets,
)


@click.group(name="assets")
def assets_command():
    """Manage optional runtime assets."""


@assets_command.command("status")
@click.option("--json-output", "json_output", is_flag=True, help="Print machine-readable JSON output")
def assets_status_command(json_output: bool):
    rows = describe_runtime_assets(DEFAULT_RUNTIME_ASSETS)
    if json_output:
        click.echo(json.dumps(rows, indent=2))
        return

    table = Table(title="Runtime Assets")
    table.add_column("Asset", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Source", style="green")
    table.add_column("Path", style="dim")
    for row in rows:
        table.add_row(row["asset"], row["status"], row["source"], row["path"] or "-")
    console.print(table)


@assets_command.command("bootstrap")
@click.option("--force", is_flag=True, help="Overwrite cached assets")
@click.option(
    "--base-url",
    default=None,
    help="Remote base URL for asset files (defaults to SKILLSMITH_ASSET_BASE_URL or built-in URL)",
)
@click.option(
    "--from-dir",
    "from_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Local source directory containing templates/.agent assets",
)
def assets_bootstrap_command(force: bool, base_url: str | None, from_dir: Path | None):
    copied = bootstrap_runtime_assets(
        relative_paths=list(DEFAULT_RUNTIME_ASSETS),
        source_dir=from_dir,
        base_url=base_url,
        force=force,
    )
    console.print("[green][OK][/green] Runtime assets ready:")
    for asset_path in copied:
        console.print(f"  - {asset_path}")

