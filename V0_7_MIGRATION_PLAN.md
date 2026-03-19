# skillsmith v0.7 Migration Plan

## Goal
Ship a smaller package and decouple heavyweight runtime assets from the default wheel, without breaking existing user flows.

## Scope
- Packaging layout and artifact boundaries
- Runtime asset resolution and bootstrap behavior
- CLI command surface additions for assets
- Backward compatibility guarantees and deprecation path

## File Moves and Ownership
1. Runtime asset resolution moved into:
   - `src/skillsmith/commands/assets_runtime.py`
2. Runtime asset command group added in:
   - `src/skillsmith/commands/assets.py`
3. CLI wiring updated in:
   - `src/skillsmith/cli.py`
   - `src/skillsmith/commands/__init__.py`
4. Init/list flows switched to runtime-asset resolver:
   - `src/skillsmith/commands/init.py`
   - `src/skillsmith/commands/list_cmd.py`
5. Packaging boundary tightened in:
   - `pyproject.toml`

## New Commands (v0.7 Track)
1. `skillsmith assets status`
   - Reports whether required runtime assets are available.
   - Supports human output and JSON output (`--json-output`).
2. `skillsmith assets bootstrap`
   - Populates runtime asset cache.
   - Supports:
     - `--from-dir <dir>` for local/offline copy
     - `--base-url <url>` for remote bootstrap source
     - `--force` overwrite

## Runtime Asset Strategy
- Default runtime assets:
  - `.agent/skills.zip`
  - `.agent/skill_catalog.json`
- Resolver order:
  1. `SKILLSMITH_ASSETS_DIR` override
  2. Local cache (`~/.skillsmith/assets/v1` by default or `SKILLSMITH_ASSET_CACHE`)
  3. Packaged fallback (when present)
- Auto-bootstrap:
  - Enabled by default (`SKILLSMITH_AUTO_BOOTSTRAP_ASSETS=1`)
  - Can be disabled for strict/offline environments

## Packaging Changes
1. Wheel:
   - Keep `src/skillsmith` package only.
   - Exclude `src/skillsmith/templates/.agent/skills.zip`.
2. Source distribution:
   - Explicit allowlist to avoid shipping repo-local runtime/test/docs artifacts.
   - Include only:
     - `src/skillsmith/**`
     - `README.md`
     - `LICENSE`
     - `pyproject.toml`

## Backward Compatibility Strategy
1. Existing workflows remain valid:
   - `skillsmith init`
   - `skillsmith list`
   - `skillsmith add`
2. If runtime assets are missing:
   - Commands provide actionable guidance to run `skillsmith assets bootstrap`.
3. Existing local/dev behavior:
   - If packaged assets exist (editable/dev installs), resolver still uses them.
4. Existing users do not need migration flags:
   - Bootstrap is additive and only required when assets are not already available.

## Rollout Plan
1. Release candidate:
   - Build wheel/sdist and enforce size budgets in CI.
2. Migration verification:
   - Run unit tests including runtime asset tests.
   - Validate `init`, `list`, and `assets` command behavior in clean environment.
3. Final release:
   - Publish v0.7 with release notes focused on smaller installs and asset bootstrap flow.

## Risks and Mitigations
1. Network-restricted environments may fail auto-bootstrap.
   - Mitigation: `assets bootstrap --from-dir` and asset override env vars.
2. Older workflows expecting embedded zip in wheel.
   - Mitigation: compatibility messaging and explicit status/bootstrap commands.
3. Cache path/permission differences across systems.
   - Mitigation: `SKILLSMITH_ASSET_CACHE` override.
