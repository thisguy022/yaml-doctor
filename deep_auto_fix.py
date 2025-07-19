print(">>> running NEW deep_auto_fix.py from", __file__)
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from collections import defaultdict
import sys

def rename_duplicate_keys_preserve_structure(yaml_lines):
    new_lines = []
    context_stack = []
    indent_levels = []
    key_count = defaultdict(int)

    for line in yaml_lines:
        if ':' not in line or line.strip().startswith('#') or line.strip() == '':
            new_lines.append(line)
            continue

        indent = len(line) - len(line.lstrip())
        key = line.strip().split(':')[0]

        # Adjust stack if indentation decreased
        while indent_levels and indent < indent_levels[-1]:
            indent_levels.pop()
            context_stack.pop()

        # Build full key path
        full_path = '.'.join(context_stack + [key])
        key_count[full_path] += 1

        if key_count[full_path] > 1:
            new_key = f"{key}__dup{key_count[full_path]-1}"
            print(f"🔁 Renaming '{key}' → '{new_key}'")
            new_line = line.replace(key, new_key, 1)
        else:
            new_key = key
            new_line = line

        # If this is a mapping that opens a new block
        if line.rstrip().endswith(':') or line.strip().endswith(': |') or line.strip().endswith(': >'):
            indent_levels.append(indent)
            context_stack.append(new_key)

        new_lines.append(new_line)

    return new_lines

def fix_yaml_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = rename_duplicate_keys_preserve_structure(lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print(f"✅ Fixed YAML written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python deep_auto_fix.py input.yaml output.yaml")
        sys.exit(1)

    fix_yaml_file(sys.argv[1], sys.argv[2])



