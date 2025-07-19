import unittest
from yaml_doctor import greet

class TestYamlDoctor(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet(), "Hello from YAML Doctor")

if __name__ == "__main__":
    unittest.main()
