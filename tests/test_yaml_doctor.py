import unittest
from yaml_doctor import validate_yaml_string

class TestYamlValidation(unittest.TestCase):
    def test_valid_yaml(self):
        good_yaml = """
        light:
          brightness: 100
          color: red
        """
        self.assertTrue(validate_yaml_string(good_yaml))

    def test_duplicate_keys(self):
        bad_yaml = """
        light:
          brightness: 100
          brightness: 200
        """
        self.assertFalse(validate_yaml_string(bad_yaml))

if __name__ == "__main__":
    unittest.main()
