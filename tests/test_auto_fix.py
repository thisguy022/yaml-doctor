import unittest
from deep_auto_fix import rename_duplicate_keys_preserve_structure

BROKEN = """\
light:
  brightness: 100
  brightness: 200
  brightness: 300
"""

EXPECTED = """\
light:
  brightness: 100
  brightness__dup1: 200
  brightness__dup2: 300
"""

class TestAutoFix(unittest.TestCase):
    def test_duplicate_fix(self):
        fixed = rename_duplicate_keys_preserve_structure(BROKEN.splitlines())
        self.assertEqual('\n'.join(fixed).strip(), EXPECTED.strip())

if __name__ == "__main__":
    unittest.main()
