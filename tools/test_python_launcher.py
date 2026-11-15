import json
from pathlib import Path
import subprocess
import unittest


LAUNCHER = (Path(__file__).parent / "python.mjs").resolve().as_uri()


class PythonLauncherTests(unittest.TestCase):
    def launch(self, available, platform="win32", exit_code=0):
        script = """
import childProcess from 'node:child_process'
import { syncBuiltinESMExports } from 'node:module'
const [available, platform, exitCode, launcher] = JSON.parse(process.argv[1])
Object.defineProperty(process, 'platform', { value: platform })
childProcess.spawnSync = (command, args, options) => {
  if (options.stdio === 'inherit') {
    console.log(JSON.stringify({ command, args }))
    return { status: exitCode }
  }
  const output = available[command]
  return output === undefined
    ? { status: null, error: { code: 'ENOENT' } }
    : { status: 0, stdout: output }
}
syncBuiltinESMExports()
process.argv = ['node', launcher, '-c', 'print("中文 path with spaces")']
await import(launcher)
"""
        return subprocess.run(
            ["node", "--input-type=module", "-e", script,
             json.dumps([available, platform, exit_code, LAUNCHER])],
            capture_output=True, text=True, encoding="utf-8",
        )

    def test_falls_back_to_uv(self):
        result = self.launch({"python": "", "python3": "", "uv": "C:/Python 3.12/python.exe\r\n"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {
            "command": "C:/Python 3.12/python.exe",
            "args": ["-c", 'print("中文 path with spaces")'],
        })

    def test_uses_standard_python_commands_without_uv(self):
        for platform, command in [("win32", "py"), ("win32", "python"), ("linux", "python3")]:
            with self.subTest(platform=platform, command=command):
                result = self.launch({command: "/installed/python\n"}, platform=platform)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["command"], "/installed/python")

    def test_preserves_script_failure_exit_code(self):
        result = self.launch({"py": "/installed/python\n"}, exit_code=7)
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 1)

    def test_reports_missing_python(self):
        result = self.launch({})
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("Python 3.12+", result.stderr)


if __name__ == "__main__":
    unittest.main()
