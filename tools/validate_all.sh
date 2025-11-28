#!/bin/bash
# Validate YAML files against OpenModbus schema

set -e

echo "OpenModbus Schema Validation"
echo "============================="
echo ""

# Check if yq is installed
if ! command -v yq &> /dev/null; then
    echo "Error: yq is not installed"
    echo "Install with: brew install yq"
    exit 1
fi

# Check if ajv-cli is installed
if ! command -v ajv &> /dev/null; then
    echo "Error: ajv-cli is not installed"
    echo "Install with: npm install -g ajv-cli ajv-formats"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SCHEMA="$REPO_ROOT/schema/v1/openmodbus-schema-v1.json"
REGISTRY_DIR="$REPO_ROOT/registry"
PASSED=0
FAILED=0

echo "Schema: $SCHEMA"
echo ""

# Find all YAML files in registry directory (recursively)
while IFS= read -r yaml_file; do
    echo "Validating: $(basename "$yaml_file")"

    # Convert YAML to JSON for validation
    JSON_FILE="/tmp/$(basename "$yaml_file" .yaml).json"
    yq eval -o=json "$yaml_file" > "$JSON_FILE"

    # Validate against schema
    if ajv validate -s "$SCHEMA" -d "$JSON_FILE" --strict=false 2>&1; then
        echo "  ✓ PASS"
        ((PASSED++))
    else
        echo "  ✗ FAIL"
        ((FAILED++))
    fi

    rm "$JSON_FILE"
    echo ""
done < <(find "$REGISTRY_DIR" -name "*.yaml" -type f)

echo "============================="
echo "Results: $PASSED passed, $FAILED failed"
echo ""

if [ $FAILED -gt 0 ]; then
    exit 1
fi
