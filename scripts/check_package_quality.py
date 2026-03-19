#!/usr/bin/env python
"""Build/package quality gate: build artifacts, twine validation, size budgets."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}")


def _mb_to_bytes(value: float) -> int:
    return int(value * 1024 * 1024)


def _format_bytes(size: int) -> str:
    return f"{size / (1024 * 1024):.2f} MB"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run package quality checks (build, twine check, size budgets)."
    )
    parser.add_argument("--dist-dir", default="dist", help="Artifacts directory (default: dist)")
    parser.add_argument(
        "--max-wheel-mb",
        type=float,
        default=2.0,
        help="Maximum wheel size in MB (default: 2.0)",
    )
    parser.add_argument(
        "--max-sdist-mb",
        type=float,
        default=2.5,
        help="Maximum sdist size in MB (default: 2.5)",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip build step and validate existing files in dist-dir",
    )
    args = parser.parse_args()

    dist_dir = Path(args.dist_dir)

    try:
        if not args.skip_build:
            if dist_dir.exists():
                shutil.rmtree(dist_dir)
            _run([sys.executable, "-m", "build", "--sdist", "--wheel", "--outdir", str(dist_dir)])

        artifacts = sorted(p for p in dist_dir.glob("*") if p.is_file())
        wheels = [p for p in artifacts if p.suffix == ".whl"]
        sdists = [p for p in artifacts if p.name.endswith(".tar.gz")]

        if not wheels or not sdists:
            raise RuntimeError(
                f"Expected both wheel and sdist in {dist_dir}, found: {[p.name for p in artifacts]}"
            )

        _run([sys.executable, "-m", "twine", "check", *[str(p) for p in artifacts]])

        wheel_budget = _mb_to_bytes(args.max_wheel_mb)
        sdist_budget = _mb_to_bytes(args.max_sdist_mb)

        size_failures: list[str] = []
        for artifact in wheels:
            size = artifact.stat().st_size
            if size > wheel_budget:
                size_failures.append(
                    f"{artifact.name}: {_format_bytes(size)} > {_format_bytes(wheel_budget)} wheel budget"
                )
        for artifact in sdists:
            size = artifact.stat().st_size
            if size > sdist_budget:
                size_failures.append(
                    f"{artifact.name}: {_format_bytes(size)} > {_format_bytes(sdist_budget)} sdist budget"
                )

        if size_failures:
            raise RuntimeError("Size budget failures:\n- " + "\n- ".join(size_failures))

        print("Package quality checks passed:")
        for artifact in artifacts:
            print(f"- {artifact.name}: {_format_bytes(artifact.stat().st_size)}")
        return 0
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
