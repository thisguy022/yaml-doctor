from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.constructor import DuplicateKeyError
import sys
import os

yaml = YAML()
yaml.preserve_quotes = True
yaml.allow_duplicate_keys = True  # We'll fix them, not reject them

def rename_duplicate_keys(data: CommentedMap) -> CommentedMap:
    seen = {}
    fixed = CommentedMap()
    
    for key, value in data.items():
        if key in seen:
            seen[key] += 1
            new_key = f"{key}__dup{seen[key]}"
            print(f"🔁 Renamed duplicate key '{key}' → '{new_key}'")
        else:
            seen[key] = 0
            new_key = key

        fixed[new_key] = value

    return fixed

def fix_yaml_file(path: str, output_path: str = None):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return

    with open(path, 'r') as f:
        original = yaml.load(f)

    fixed = rename_duplicate_keys(original)

    out_file = output_path or path
    with open(out_file, 'w') as f:
        yaml.dump(fixed, f)

    print(f"✅ Fixed YAML written to: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deep_auto_fix.py <file.yaml> [output.yaml]")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None

    fix_yaml_file(in_path, out_path)
