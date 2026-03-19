import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from click.testing import CliRunner

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in os.sys.path:
    os.sys.path.insert(0, str(SRC))

from skillsmith.cli import main
from skillsmith.commands.assets_runtime import (
    bootstrap_runtime_assets,
    resolve_runtime_asset,
)


class _MockResponse:
    def __init__(self, content: bytes):
        self.content = content

    def raise_for_status(self):
        return None


class AssetsRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_bootstrap_runtime_assets_from_local_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_dir = root / "source"
            cache_dir = root / "cache"
            source_asset = source_dir / ".agent" / "skills.zip"
            source_asset.parent.mkdir(parents=True, exist_ok=True)
            source_asset.write_bytes(b"zip-data")

            with mock.patch.dict(
                os.environ,
                {
                    "SKILLSMITH_ASSET_CACHE": str(cache_dir),
                    "SKILLSMITH_AUTO_BOOTSTRAP_ASSETS": "0",
                },
                clear=False,
            ):
                copied = bootstrap_runtime_assets(
                    relative_paths=[".agent/skills.zip"],
                    source_dir=source_dir,
                    force=True,
                )
                resolved = resolve_runtime_asset(
                    ".agent/skills.zip",
                    auto_bootstrap=False,
                    include_packaged=False,
                )

            self.assertEqual(len(copied), 1)
            self.assertTrue(copied[0].exists())
            self.assertEqual(copied[0].read_bytes(), b"zip-data")
            self.assertIsNotNone(resolved)
            self.assertEqual(resolved.read_bytes(), b"zip-data")

    def test_resolve_runtime_asset_auto_bootstraps_from_remote(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = Path(temp_dir) / "cache"
            with mock.patch.dict(
                os.environ,
                {
                    "SKILLSMITH_ASSET_CACHE": str(cache_dir),
                    "SKILLSMITH_AUTO_BOOTSTRAP_ASSETS": "1",
                    "SKILLSMITH_ASSET_BASE_URL": "https://example.invalid/assets",
                },
                clear=False,
            ), mock.patch(
                "skillsmith.commands.assets_runtime.requests.get",
                return_value=_MockResponse(b"catalog-data"),
            ) as mock_get:
                resolved = resolve_runtime_asset(
                    ".agent/skill_catalog.json",
                    auto_bootstrap=True,
                    include_packaged=False,
                    required=True,
                )

            self.assertIsNotNone(resolved)
            self.assertTrue(resolved.exists())
            self.assertEqual(resolved.read_bytes(), b"catalog-data")
            self.assertIn(
                "/.agent/skill_catalog.json",
                mock_get.call_args.args[0],
            )

    def test_assets_command_status_and_bootstrap_from_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source_dir = root / "source"
            cache_dir = root / "cache"
            (source_dir / ".agent").mkdir(parents=True, exist_ok=True)
            (source_dir / ".agent" / "skills.zip").write_bytes(b"z")
            (source_dir / ".agent" / "skill_catalog.json").write_text("[]", encoding="utf-8")

            with mock.patch.dict(
                os.environ,
                {
                    "SKILLSMITH_ASSET_CACHE": str(cache_dir),
                    "SKILLSMITH_AUTO_BOOTSTRAP_ASSETS": "0",
                },
                clear=False,
            ):
                bootstrap_result = self.runner.invoke(
                    main, ["assets", "bootstrap", "--from-dir", str(source_dir), "--force"]
                )
                status_result = self.runner.invoke(main, ["assets", "status"])

            self.assertEqual(bootstrap_result.exit_code, 0, bootstrap_result.output)
            self.assertIn("Runtime assets ready", bootstrap_result.output)
            self.assertEqual(status_result.exit_code, 0, status_result.output)
            self.assertIn("skills.zip", status_result.output)


if __name__ == "__main__":
    unittest.main()

