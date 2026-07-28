import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX_MARKET = ROOT / ".agents/plugins/marketplace.json"
CLAUDE_MARKET = ROOT / ".claude-plugin/marketplace.json"
GROK_MARKET = ROOT / ".grok-plugin/marketplace.json"
KIMI_MARKET = ROOT / ".kimi-plugin/marketplace.json"
PLUGIN = ROOT / "plugins/gopher"
CODEX_PLUGIN = PLUGIN / ".codex-plugin/plugin.json"
CLAUDE_PLUGIN = PLUGIN / ".claude-plugin/plugin.json"
GROK_PLUGIN = PLUGIN / ".grok-plugin/plugin.json"
KIMI_PLUGIN = PLUGIN / ".kimi-plugin/plugin.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class BootstrapPackageTest(unittest.TestCase):
    def test_quad_harness_identity_and_sources_match(self):
        codex_market = load(CODEX_MARKET)
        claude_market = load(CLAUDE_MARKET)
        grok_market = load(GROK_MARKET)
        kimi_market = load(KIMI_MARKET)
        codex_plugin = load(CODEX_PLUGIN)
        claude_plugin = load(CLAUDE_PLUGIN)
        grok_plugin = load(GROK_PLUGIN)
        kimi_plugin = load(KIMI_PLUGIN)

        self.assertEqual("alvadorncorp", codex_market["name"])
        self.assertEqual("alvadorncorp", claude_market["name"])
        self.assertEqual("alvadorncorp", grok_market["name"])
        self.assertEqual("alvadorncorp", kimi_market["name"])
        self.assertEqual("./plugins/gopher", codex_market["plugins"][0]["source"]["path"])
        self.assertEqual("./plugins/gopher", claude_market["plugins"][0]["source"])
        self.assertEqual("./plugins/gopher", grok_market["plugins"][0]["source"]["path"])
        self.assertEqual("./plugins/gopher", kimi_market["plugins"][0]["source"])

        for key in ("name", "version", "description", "author"):
            self.assertEqual(codex_plugin[key], claude_plugin[key])
            self.assertEqual(codex_plugin[key], grok_plugin[key])
            self.assertEqual(codex_plugin[key], kimi_plugin[key])
        self.assertEqual("gopher", codex_plugin["name"])
        self.assertEqual("0.2.3", codex_plugin["version"])
        self.assertTrue((PLUGIN / "skills").is_dir())

    def test_v1_declares_no_optional_runtime_components(self):
        manifest = load(CODEX_PLUGIN)
        for forbidden in ("apps", "mcpServers", "hooks"):
            self.assertNotIn(forbidden, manifest)
        for forbidden_path in (".app.json", ".mcp.json", ".lsp.json", "hooks", "assets"):
            self.assertFalse((PLUGIN / forbidden_path).exists())


if __name__ == "__main__":
    unittest.main()
