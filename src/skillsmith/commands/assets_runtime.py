import os
import shutil
from pathlib import Path

import requests


TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates"
DEFAULT_RUNTIME_ASSETS = (".agent/skills.zip", ".agent/skill_catalog.json")
DEFAULT_ASSET_BASE_URL = (
    "https://raw.githubusercontent.com/ApexIQ/skillsmith/main/src/skillsmith/templates"
)


def _asset_cache_dir() -> Path:
    override = os.environ.get("SKILLSMITH_ASSET_CACHE")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".skillsmith" / "assets" / "v1"


def _asset_override_dir() -> Path | None:
    override = os.environ.get("SKILLSMITH_ASSETS_DIR", "").strip()
    if not override:
        return None
    return Path(override).expanduser()


def _asset_base_url() -> str:
    return os.environ.get("SKILLSMITH_ASSET_BASE_URL", DEFAULT_ASSET_BASE_URL).rstrip("/")


def _auto_bootstrap_enabled() -> bool:
    raw = os.environ.get("SKILLSMITH_AUTO_BOOTSTRAP_ASSETS", "1").strip().lower()
    return raw not in {"0", "false", "off", "no"}


def _candidate_paths(relative_path: str, include_packaged: bool = True) -> list[tuple[str, Path]]:
    rel = relative_path.replace("\\", "/").lstrip("/")
    paths: list[tuple[str, Path]] = []
    override_dir = _asset_override_dir()
    if override_dir is not None:
        paths.append(("override", override_dir / rel))
    paths.append(("cache", _asset_cache_dir() / rel))
    if include_packaged:
        paths.append(("packaged", TEMPLATE_DIR / rel))
    return paths


def resolve_runtime_asset(
    relative_path: str,
    *,
    required: bool = False,
    auto_bootstrap: bool = True,
    include_packaged: bool = True,
) -> Path | None:
    """Resolve an asset path from override/cache/packaged locations."""
    rel = relative_path.replace("\\", "/").lstrip("/")
    for _, candidate in _candidate_paths(rel, include_packaged=include_packaged):
        if candidate.exists():
            return candidate
    if auto_bootstrap and _auto_bootstrap_enabled():
        try:
            bootstrap_runtime_assets(relative_paths=[rel], include_packaged=include_packaged)
        except Exception:
            pass
        for _, candidate in _candidate_paths(rel, include_packaged=include_packaged):
            if candidate.exists():
                return candidate
    if required:
        raise FileNotFoundError(
            f"Missing runtime asset: {rel}. Run `skillsmith assets bootstrap` or set SKILLSMITH_ASSETS_DIR."
        )
    return None


def describe_runtime_assets(
    relative_paths: tuple[str, ...] = DEFAULT_RUNTIME_ASSETS,
    *,
    include_packaged: bool = True,
) -> list[dict]:
    rows: list[dict] = []
    for rel in relative_paths:
        rel_normalized = rel.replace("\\", "/").lstrip("/")
        source = "missing"
        path_value = None
        for candidate_source, candidate_path in _candidate_paths(
            rel_normalized, include_packaged=include_packaged
        ):
            if candidate_path.exists():
                source = candidate_source
                path_value = str(candidate_path)
                break
        rows.append(
            {
                "asset": rel_normalized,
                "status": "available" if source != "missing" else "missing",
                "source": source,
                "path": path_value,
            }
        )
    return rows


def _copy_asset_from_source(source_dir: Path, relative_path: str, *, force: bool = False) -> Path:
    rel = relative_path.replace("\\", "/").lstrip("/")
    source = source_dir / rel
    if not source.exists():
        raise FileNotFoundError(f"Missing asset in source dir: {source}")
    destination = _asset_cache_dir() / rel
    if destination.exists() and not force:
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def _download_asset(relative_path: str, *, base_url: str, force: bool = False, timeout: int = 15) -> Path:
    rel = relative_path.replace("\\", "/").lstrip("/")
    destination = _asset_cache_dir() / rel
    if destination.exists() and not force:
        return destination

    url = f"{base_url}/{rel}"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = destination.with_suffix(destination.suffix + ".tmp")
    tmp_path.write_bytes(response.content)
    tmp_path.replace(destination)
    return destination


def bootstrap_runtime_assets(
    *,
    relative_paths: list[str] | None = None,
    source_dir: Path | None = None,
    base_url: str | None = None,
    force: bool = False,
    include_packaged: bool = True,
) -> list[Path]:
    """Populate runtime assets into the user cache from local source or remote URL."""
    selected_paths = relative_paths or list(DEFAULT_RUNTIME_ASSETS)
    copied: list[Path] = []
    for rel in selected_paths:
        rel_normalized = rel.replace("\\", "/").lstrip("/")
        if source_dir is not None:
            copied.append(_copy_asset_from_source(source_dir, rel_normalized, force=force))
            continue
        packaged = resolve_runtime_asset(
            rel_normalized,
            required=False,
            auto_bootstrap=False,
            include_packaged=include_packaged,
        )
        if packaged and packaged.exists():
            copied.append(_copy_asset_from_source(TEMPLATE_DIR, rel_normalized, force=force))
            continue
        copied.append(
            _download_asset(
                rel_normalized,
                base_url=(base_url or _asset_base_url()),
                force=force,
            )
        )
    return copied

