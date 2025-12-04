#!/bin/bash
# Validate YAML files against OpenModbus schema

set -e

echo "OpenModbus Schema Validation"
echo "============================="
echo ""

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Install from: https://nodejs.org/"
    exit 1
fi

# Check if required npm packages are available
if ! command -v js-yaml &> /dev/null && ! npx -q js-yaml --version &> /dev/null; then
    echo "Error: js-yaml is not installed"
    echo "Install with: npm install -g js-yaml"
    echo "Or use npx (no install needed): npx will download automatically"
    exit 1
fi

# Check if ajv-cli is installed
if ! command -v ajv &> /dev/null && ! npx -q ajv --help &> /dev/null; then
    echo "Error: ajv-cli is not installed"
    echo "Install with: npm install -g ajv-cli ajv-formats"
    echo "Or use npx (no install needed): npx will download automatically"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SCHEMA="$REPO_ROOT/schema/openmodbus-schema-v0.3.0.json"
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
    node -e "console.log(JSON.stringify(require('js-yaml').load(require('fs').readFileSync('$yaml_file', 'utf8'))))" > "$JSON_FILE" 2>/dev/null || {
        echo "  ✗ FAIL (YAML parse error)"
        ((FAILED++))
        continue
    }

    # Validate against schema
    if ajv validate -s "$SCHEMA" -d "$JSON_FILE" --strict=false 2>&1 || npx -q ajv-cli validate -s "$SCHEMA" -d "$JSON_FILE" --strict=false 2>&1; then
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
