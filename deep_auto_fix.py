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
        content = f.read()

    # Try to load safely first
    try:
        yaml.load(content)
        print("✅ No duplicates detected.")
        return
    except Exception as e:
        print(f"⚠️ YAML issue detected: {e}")
        print("🔁 Attempting to auto-fix...")

    from collections import defaultdict
    import re

    lines = content.split('\n')
    key_counts = defaultdict(int)
    indent_stack = []
    context_keys = []

    new_lines = []

    for line in lines:
        match = re.match(r'^(\s*)([^\s:#]+):(.*)', line)
        if match:
            indent, key, rest = match.groups()
            current_indent = len(indent)

            # Adjust context based on indentation
            while indent_stack and indent_stack[-1] >= current_indent:
                indent_stack.pop()
                context_keys.pop()

            full_key = '.'.join(context_keys + [key.strip()])
            key_counts[full_key] += 1

            if key_counts[full_key] > 1:
                key = f"{key.strip()}__dup{key_counts[full_key] - 1}"
                print(f"🔁 Renamed duplicate key at indent {current_indent}: → {key}")

            new_lines.append(f"{indent}{key}:{rest}")

            # Only push to context if this key starts a new nested block
            if rest.strip() == "":
                indent_stack.append(current_indent)
                context_keys.append(key.strip())
        else:
            new_lines.append(line)

    # Re-parse fixed YAML to ensure it’s valid
    try:
        data = yaml.load('\n'.join(new_lines))
    except Exception as e:
        print("❌ Could not fix YAML:", e)
        return

    with open(out_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)

    print(f"✅ Fixed YAML written to: {out_path}")


