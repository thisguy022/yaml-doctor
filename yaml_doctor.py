import sys
import argparse
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError

# import the fixer you already wrote
from deep_auto_fix import fix_yaml_file

yaml = YAML()

# ──────────────────────────── core validation helpers ────────────────────────────
def validate_yaml_string(yaml_string: str) -> bool:
    """Return True if YAML parses with no duplicate keys or syntax errors."""
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
    """Read a file from disk and run validate_yaml_string()."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return validate_yaml_string(content)
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        return False


# ──────────────────────────── CLI entry point ────────────────────────────────────
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="YAML-Doctor — validate Home-Assistant-style YAML and optionally auto-fix duplicate keys."
    )
    parser.add_argument("file", help="Path to the YAML file you want to check")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rename duplicate keys in-place (over-writes the original file)",
    )
    args = parser.parse_args()

    # 1️⃣ Just validate
    if not args.fix:
        ok = validate_yaml_file(args.file)
        sys.exit(0 if ok else 1)

    # 2️⃣ Validate first, then auto-fix if problems
    print("🔍 Running validation before fix…")
    ok_before = validate_yaml_file(args.file)
    if ok_before:
        print("✅ No issues detected — nothing to fix.")
        sys.exit(0)

    print("🛠  Attempting auto-fix (duplicates will be renamed)…")
    try:
        fix_yaml_file(args.file, args.file)  # in-place overwrite
        print("🔁 Re-validating after fix…")
        ok_after = validate_yaml_file(args.file)
        if ok_after:
            print("🎉 File fixed successfully.")
            sys.exit(0)
        else:
            print("⚠️  Fix attempted but file still invalid.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Auto-fix failed: {e}")
        sys.exit(1)
