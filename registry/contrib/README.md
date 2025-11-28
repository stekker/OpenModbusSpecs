# Community Contributions

This directory contains device profiles submitted by the community that are awaiting validation and promotion to `registry/stable/`.

## Submitting a Device Profile

1. Create your device YAML file following the [schema](../../schema/v0.1/openmodbus-schema-v0.1.json)
2. Validate it locally: `python3 tools/validate.py`
3. Submit a PR adding your file to this directory: `registry/contrib/<manufacturer>_<model>.yaml`
4. Our team will review and test the profile
5. Once validated, it will be moved to `registry/stable/<manufacturer>/<model>.yaml`

## Naming Convention

Use the format: `<manufacturer>_<model>.yaml`

Examples:
- `siemens_pac2200.yaml`
- `schneider_pm5560.yaml`
- `abb_b23.yaml`

## What Happens Next?

After you submit your PR:
1. **Automated validation** - CI checks schema conformance
2. **Manual review** - We verify against datasheets
3. **Testing** - Ideally tested with real hardware
4. **Promotion** - Moved to stable and added to manifest.json

Thank you for contributing to the OpenModbus ecosystem!
