# OpenModbus Device Registry

**Status**: 🚧 Early stage - lightweight governance, PRs auto-merge if CI passes

An open, machine-readable specification for Modbus device register maps. Think of it as "OpenAPI for Modbus" - a standardized way to describe Modbus device interfaces to eliminate the need for manually interpreting PDF datasheets.

---

## 🤝 Seeking Maintainers

**This project needs active maintainers!** We welcome:

- **Device manufacturers** - Take authoritative ownership of your product profiles
- **Integration developers** - Maintain profiles for devices you regularly work with
- **Community contributors** - Submit 3+ quality device profiles and become a co-maintainer

When you contribute a device, you can claim maintainer role by adding yourself to the YAML file. Manufacturers are especially encouraged to take over profiles for their products to ensure accuracy.

**Current status**: All existing devices have emeritus maintainers (project founders who've stepped back to let the community lead).

See [docs/MAINTAINERS.md](docs/MAINTAINERS.md) to learn more.

---

## Overview

The Modbus protocol is ubiquitous in industrial automation, but device interfaces are typically documented in PDF manuals that require manual interpretation. This project provides:

1. **A formal JSON schema** for describing Modbus device register maps
2. **A growing registry** of device profiles for common Modbus devices
3. **Validation tools** to ensure conformance to the specification

## Repository Structure

```
├── schema/
│   └── v1/
│       └── openmodbus-schema-v1.json    # JSON Schema definition
├── registry/
│   ├── stable/                          # Validated device profiles
│   │   ├── <manufacturer>/
│   │   │   └── <model>.yaml
│   └── ...
├── contrib/                             # Community contributions (pending validation)
├── tools/
│   ├── validate.py                      # Python validation script
│   └── validate_all.sh                  # Bash validation script
└── docs/                                # Documentation
```

## Device Profile Format

Device profiles are written in YAML and describe:

- Device metadata (manufacturer, model, protocol)
- Register addresses and their data types
- Byte order and scaling information
- Human-readable and machine-safe identifiers
- OBIS codes (for energy meters)
- Vendor documentation references

Example:

```yaml
version: "0.1"

device:
  id: example_device
  manufacturer: Example Corp
  model: EX-1000
  description: Example three-phase energy meter
  protocol: modbus_tcp
  default_byte_order: ABCD
  default_register_type: holding

registers:
  "0":
    descriptive_name: voltage_L1
    vendor_name: "Voltage Phase 1"
    type: float
    bit_width: 32
    signed: true
    length: 2
    unit: V
    register_type: holding
```

## Using the Registry

### For Developers

Fetch device profiles programmatically:

```bash
# Download a specific device profile
curl -O https://raw.githubusercontent.com/yourorg/OpenModbusSpecs/main/registry/stable/alfen/ng9xx.yaml

# Or clone the entire registry
git clone https://github.com/yourorg/OpenModbusSpecs.git
```

### For Automation Systems

Device profiles can be parsed to automatically:
- Generate Modbus polling configurations
- Create monitoring dashboards
- Validate register addresses
- Convert raw values to engineering units

## Contributing

We welcome contributions of new device profiles! When you contribute a device, you become its maintainer.

**Quick Start:**

1. Create a YAML file following the schema (add yourself as maintainer)
2. Validate it using `tools/validate.py`
3. Submit a pull request adding your file to `registry/contrib/`
4. After review, it will be promoted to `registry/stable/`

**Maintainer System:**

Each device has designated maintainers who review changes and ensure quality. Contributors automatically become maintainers of devices they add. See [docs/MAINTAINERS.md](docs/MAINTAINERS.md) for details.

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines and [registry/contrib/README.md](registry/contrib/README.md) for the contribution workflow.

## Validation

Validate your device profile:

```bash
# Python validator (recommended - minimal dependencies)
pip3 install pyyaml jsonschema
python3 tools/validate.py

# Alternative: Shell script validator (requires Node.js)
npm install -g js-yaml ajv-cli ajv-formats
./tools/validate_all.sh
```

## Schema Version

Current schema version: **v0.1** (pre-release)

The schema uses semantic versioning. We're starting at v0.1 to gather community feedback before stabilizing to v1.0.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Vision

Our goal is to create the de facto standard for Modbus device interface descriptions, making industrial automation more accessible and reducing integration time from days to minutes.

## About Stekker

This project is maintained by [Stekker](https://stekker.com), a company on a mission to make the electrical grid more sustainable and resilient. We enable organizations to maximize their use of locally generated renewable electricity while staying within grid connection constraints.

Through intelligent load management and real-time optimization, we help our customers operate more efficiently by steering when consumption occurs—whether charging electric vehicle fleets, managing stationary battery storage, or controlling other flexible loads. This ensures they use the cleanest and most affordable electricity available at any given moment.

The OpenModbus specification emerged from our need to rapidly integrate diverse Modbus devices in industrial and commercial energy management deployments. We're sharing it with the community to accelerate the transition to smarter, cleaner energy systems.

Learn more at [stekker.com](https://stekker.com)

## Support

- **Issues**: Report bugs or request new device support via GitHub Issues
- **Discussions**: Join conversations about the specification
- **Documentation**: See the [docs/](docs/) directory for detailed guides
