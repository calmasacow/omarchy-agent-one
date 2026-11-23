"""Launcher checks: a chosen agent goes through the stock omarchy-agent."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / 'scripts/omarchy-agent-one-launch'
SHIM = ROOT / 'scripts/default-agent/omarchy-default-agent'

# Stand-ins for the Omarchy commands the launcher reaches. The fake
# omarchy-agent asks omarchy-default-agent and hands off to omarchy-launch-tui,
# as the real one does; the fake terminal launcher records the environment the
# agent session would inherit instead of opening a terminal.
FAKES = {
  'omarchy-agent': 'omarchy-default-agent > "$FAKE_DIR/launched"\nexec omarchy-launch-tui --app-id=org.omarchy.agent agent\n',
  'omarchy-launch-tui': 'printf "%s\\n" "$*" > "$FAKE_DIR/terminal"\nenv > "$FAKE_DIR/session-env"\n',
  'omarchy-cmd-missing': 'exit "${FAKE_MISSING:-1}"\n',
  'omarchy-notification-send': 'printf "%s" "$*" > "$FAKE_DIR/notified"\n',
}


class LaunchTests(unittest.TestCase):
  def setUp(self):
    self.tmp = tempfile.TemporaryDirectory()
    self.dir = Path(self.tmp.name)
    bin_dir = self.dir / 'bin'
    bin_dir.mkdir()
    for name, body in FAKES.items():
      path = bin_dir / name
      path.write_text('#!/bin/bash\n' + body)
      path.chmod(0o755)
    self.env = dict(os.environ, PATH=str(bin_dir) + ':' + os.environ['PATH'], FAKE_DIR=str(self.dir))

  def tearDown(self):
    self.tmp.cleanup()

  def launch(self, *args, **env):
    return subprocess.run([str(LAUNCHER), *args], env=dict(self.env, **env),
                          capture_output=True, text=True)

  def test_launches_requested_agent(self):
    result = self.launch('agy')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual((self.dir / 'launched').read_text(), 'agy\n')

  def test_agent_session_gets_clean_environment(self):
    # uwsm-app evals the terminal command in its own process, so anything the
    # launcher sets would reach the agent's session.
    result = self.launch('claude')
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual((self.dir / 'terminal').read_text(), '--app-id=org.omarchy.agent agent\n')
    env = dict(line.split('=', 1) for line in (self.dir / 'session-env').read_text().splitlines() if '=' in line)
    self.assertFalse('AGENT_ONE_LAUNCH_AGENT' in env, 'chosen agent leaked into the session')
    self.assertEqual(env['PATH'], self.env['PATH'])

  def test_rejects_unsafe_names(self):
    for args in [[], [''], ['--pick'], ['../x'], ['a b'], ['claude', 'codex'], ['a' * 65]]:
      with self.subTest(args=args):
        result = self.launch(*args)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.dir / 'launched').exists())

  def test_missing_agent_notifies(self):
    result = self.launch('agy', FAKE_MISSING='0')
    self.assertEqual(result.returncode, 1)
    self.assertFalse((self.dir / 'launched').exists())
    self.assertIn('agy is not installed', (self.dir / 'notified').read_text())

  def test_shim_prints_requested_agent(self):
    result = subprocess.run([str(SHIM)], env=dict(self.env, AGENT_ONE_LAUNCH_AGENT='codex'),
                            capture_output=True, text=True)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout, 'codex\n')


if __name__ == '__main__':
  unittest.main()
