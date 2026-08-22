import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "package.json"


class OpenCodePluginTest(unittest.TestCase):
    def opencode(self, *args):
        config = json.dumps({"plugin": [ROOT.as_uri()]})
        env = {
            **os.environ,
            "OPENCODE_CONFIG_CONTENT": config,
            "OPENCODE_DISABLE_EXTERNAL_SKILLS": "1",
            "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS": "1",
        }
        return subprocess.run(
            ["opencode", *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_package_exposes_the_opencode_plugin(self):
        package = json.loads(PACKAGE.read_text(encoding="utf-8"))
        self.assertEqual("@alvadorncorp/gopher", package["name"])
        self.assertEqual("plugins/gopher/opencode/plugin.js", package["main"])
        self.assertEqual(">=1.18.15", package["engines"]["opencode"])
        self.assertEqual("public", package["publishConfig"]["access"])

    def test_plugin_registers_the_shared_skill_path_and_role_agents(self):
        source = (ROOT / "plugins/gopher/opencode/plugin.js").read_text(encoding="utf-8")
        self.assertIn('"skills"', source)
        self.assertIn('"gopher-architect"', source)
        self.assertIn('"gopher-developer"', source)
        self.assertIn('"gopher-reviewer"', source)


if __name__ == "__main__":
    unittest.main()
