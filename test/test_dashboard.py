"""OpenRouter integration and selector regression checks; no account access."""
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader('openrouter', str(ROOT / 'scripts/omarchy-agent-one-openrouter'))
spec = importlib.util.spec_from_loader(loader.name, loader)
collector = importlib.util.module_from_spec(spec)
loader.exec_module(collector)


def js_function(file, name):
  source = (ROOT / file).read_text()
  start = source.index('  function ' + name + '(')
  end = source.index('\n  }', start) + len('\n  }')
  return source[start:end]


class DashboardTests(unittest.TestCase):
  def test_empty_refresh_preserves_previous(self):
    old = {'balance': {'remaining': 12}, 'limits': [{'percent': .2}],
           'tierLabel': 'Prepaid', 'totalPrompts': 3, 'todayTotalTokens': 42}
    fresh = {'totalPrompts': 0, 'limits': []}
    result = collector.preserve_previous(fresh, old)
    self.assertEqual(result['balance'], old['balance'])
    self.assertEqual(result['todayTotalTokens'], 42)
    self.assertTrue(result['ready'])

  def test_successful_refresh_replaces_previous(self):
    result = collector.preserve_previous({'balance': {'remaining': 0}, 'totalPrompts': 4},
                                         {'balance': {'remaining': 12}, 'totalPrompts': 3})
    self.assertEqual(result['balance']['remaining'], 0)
    self.assertEqual(result['totalPrompts'], 4)

  def test_local_activity_identifies_actual_window(self):
    activity = collector.local_activity({'recentDays': [{'cost': 2, 'messageCount': 40, 'prompts': 3}]}, '1mo')
    self.assertEqual(activity['source'], 'local')
    self.assertEqual(activity['period'], '7d')
    self.assertEqual(activity['spend'], 2)

  def test_selector_and_account_scope(self):
    main = (ROOT / 'Main.qml').read_text()
    panel = (ROOT / 'Panel.qml').read_text()
    script = '''const assert = require('node:assert/strict');
const root = {settings: {providers: {grok: {enabled: false}}}};
const settings = root.settings;
''' + js_function('Main.qml', 'providerEnabled') + '''
assert.equal(providerEnabled('openrouter'), true);
assert.equal(providerEnabled('grokbot'), false);
settings.providers.grok.enabled = true;
assert.equal(providerEnabled('grokbot'), true);
assert.equal(providerEnabled('unrelated'), false);
''' + js_function('Panel.qml', 'selectProvider') + '''
let providers = [{providerId:'overview'}, {providerId:'grok'}, {providerId:'openrouter'}];
let selectedProviderId = '';
selectProvider(0); assert.equal(selectedProviderId, 'overview');
selectProvider(-1); assert.equal(selectedProviderId, 'openrouter');
selectProvider(3); assert.equal(selectedProviderId, 'overview');
'''
    subprocess.run(['node', '-e', script], check=True)
    self.assertIn('providerId: "overview", providerName: "Overview"', panel)
    self.assertIn('selectedProviderId = "overview"', panel)
    self.assertIn('p.providerId !== "grokbot"', main)
    snapshot = js_function('Main.qml', 'providerSnapshot')
    for private_account_field in ['balance:', 'limits:', 'activity:']:
      self.assertNotIn(private_account_field, snapshot)


if __name__ == '__main__':
  unittest.main()
