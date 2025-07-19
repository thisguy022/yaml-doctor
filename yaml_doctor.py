import sys
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError

yaml = YAML()

def validate_yaml_string(yaml_string: str) -> bool:
    try:
        yaml.load(yaml_string)
        return True
    except DuplicateKeyError as e:
        print(f"❌ Duplicate key detected: {e}")
        return False
    except Exception as e:
        print(f"❌ Invalid YAML: {e}")
        return False

def validate_yaml_file(path: str) -> bool:
    try:
        with open(path, "r") as f:
            content = f.read()
        return validate_yaml_string(content)
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python yaml_doctor.py <path_to_yaml_file>")
        sys.exit(1)

    path = sys.argv[1]
    success = validate_yaml_file(path)
    sys.exit(0 if success else 1)
