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

def fix_yaml_file(in_path, out_path):
    yaml = YAML()
    yaml.preserve_quotes = True

    with open(in_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    key_tracker = {}
    current_indent = 0

    for line in lines:
        if ':' in line and not line.strip().startswith('#'):
            leading_spaces = len(line) - len(line.lstrip())
            key_part = line.split(':', 1)[0].strip()

            # Build a context key based on indentation
            context_key = f"{leading_spaces}:{key_part}"

            if context_key in key_tracker:
                key_tracker[context_key] += 1
                new_key = f"{key_part}__dup{key_tracker[context_key]}"
                print(f"🔁 Renaming duplicate '{key_part}' → '{new_key}'")
                line = line.replace(key_part, new_key, 1)
            else:
                key_tracker[context_key] = 0

        fixed_lines.append(line)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print(f"✅ Fixed YAML written to: {out_path}")


    print(f"✅ Fixed YAML written to: {out_path}")


