#!/usr/bin/env python3
"""Validate YAML files against OpenModbus schema"""

import json
import sys
from pathlib import Path

try:
    import yaml
    import jsonschema
except ImportError:
    print("Error: Required Python packages not installed")
    print("Install with: pip3 install pyyaml jsonschema")
    sys.exit(1)

def validate_file(yaml_path, schema):
    """Validate a single YAML file against the schema"""
    print(f"Validating: {yaml_path.name}")

    # Load YAML
    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    # Validate
    try:
        jsonschema.validate(instance=data, schema=schema)
        print(f"  ✓ PASS")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"  ✗ FAIL")
        print(f"    {e.message}")
        if e.path:
            print(f"    Path: {' -> '.join(str(p) for p in e.path)}")
        return False

def main():
    print("OpenModbus Schema Validation")
    print("=" * 50)
    print()

    # Load schema
    repo_root = Path(__file__).parent.parent
    schema_path = repo_root / "schema" / "v1" / "openmodbus-schema-v1.json"
    with open(schema_path) as f:
        schema = json.load(f)

    print(f"Schema: {schema_path}")
    print()

    # Find all YAML files in registry directory
    registry_dir = repo_root / "registry"
    yaml_files = list(registry_dir.rglob("*.yaml"))

    passed = 0
    failed = 0

    for yaml_file in sorted(yaml_files):
        if validate_file(yaml_file, schema):
            passed += 1
        else:
            failed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print()

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
