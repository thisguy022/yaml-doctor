from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError

yaml = YAML()

def validate_yaml_string(yaml_string: str) -> bool:
    try:
        yaml.load(yaml_string)
        return True
    except DuplicateKeyError as e:
        print(f"Duplicate key detected: {e}")
        return False
    except Exception as e:
        print(f"Invalid YAML: {e}")
        return False
