# Contributing to OpenModbus Device Registry

Thank you for your interest in contributing! This guide will help you add new device profiles to the registry.

## Before You Start

1. **Check existing profiles**: Search the `registry/` directory to ensure the device isn't already documented
2. **Gather documentation**: Obtain the official Modbus register map from the device manufacturer
3. **Have access to hardware** (recommended): Testing against real hardware ensures accuracy

## Creating a Device Profile

### 1. File Location and Naming

Create a new YAML file in `registry/contrib/`:

```bash
registry/contrib/<manufacturer>_<model>.yaml
```

Use lowercase with underscores. For example:
- `alfen_ng9xx.yaml`
- `janitza_umg604.yaml`
- `landis_gyr_e450.yaml`

### 2. Required Fields

Every device profile must include:

```yaml
version: "0.2.0"

device:
  id: unique_device_id          # Snake_case identifier
  manufacturer: Manufacturer     # Official manufacturer name
  model: Model Number           # Official model designation
  protocol: modbus_tcp          # or modbus_rtu, modbus_udp
  default_byte_order: ABCD      # ABCD, BADC, CDAB, DCBA, etc.
  default_register_type: holding # holding, input, coil, or discrete_input
  maintainers:                  # You become the maintainer!
    - name: Your Name
      github: yourusername
      organization: Your Company (optional)
      email: you@example.com (optional)
      role: primary

registers:
  "0":                          # Register address (as string)
    descriptive_name: voltage_L1  # Machine-readable name (snake_case)
    type: float                 # integer, float, string, or bool
    bit_width: 32              # 16, 32, or 64 (for integer/float)
    signed: true               # true or false (for integer/float)
    length: 2                  # Number of 16-bit registers
    unit: V                    # SI unit or empty string
    register_type: holding     # Can override device default
```

### 3. Optional Fields

Enhance your profile with:

```yaml
device:
  description: Human-readable description
  tags:
    category: energy_meter
    protocol_version: "1.0"
  sources:
    - url: https://example.com/manual.pdf
      type: datasheet
      description: Official Modbus manual

registers:
  "0":
    vendor_name: "Original register name from manual"
    byte_order: BADC           # Override device default
    obis_code: "1-0:1.8.0*255" # For energy meters
    notes: "Special considerations for this register"
    scaling:
      factor: 0.01
      offset: 0
    bits:                       # For bitfield definitions
      "0":
        descriptive_name: status_bit_0
        vendor_name: "Ready"
      "1":
        descriptive_name: status_bit_1
        vendor_name: "Fault"
```

### 4. Validation

Before submitting, validate your YAML file:

```bash
# Using Python validator
python3 tools/validate.py

# Or using shell script
./tools/validate_all.sh
```

Fix any validation errors before submitting.

### 5. Submit a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b add-device-<manufacturer>-<model>`
3. Add your YAML file to `contrib/`
4. Commit: `git commit -m "feat: add <manufacturer> <model> device profile"`
5. Push and create a pull request

## Register Naming Guidelines

### descriptive_name

Use snake_case with descriptive, consistent names:

**Good:**
- `voltage_L1`, `voltage_L2`, `voltage_L3`
- `active_energy_import`, `active_energy_export`
- `current_limit_actual`

**Bad:**
- `V1`, `V2`, `V3` (too cryptic)
- `voltagePhaseOne` (use snake_case, not camelCase)
- `Voltage_L1` (don't capitalize)

### Units

Use SI units without prefixes when possible:
- `W` not `kW` (use scaling factor if needed)
- `V` not `mV`
- `A` not `mA`
- `Hz` for frequency
- `Wh` for energy
- Empty string `""` for dimensionless values

## Data Types

### Integer

```yaml
type: integer
bit_width: 32        # 16, 32, or 64
signed: true         # true or false
```

### Float

```yaml
type: float
bit_width: 32        # 32 or 64 (IEEE 754)
```

### String

```yaml
type: string
length: 32           # Number of 16-bit registers
# No bit_width or signed fields for strings
```

### Boolean

```yaml
type: bool
length: 1            # Always 1 register
# No bit_width or signed fields for booleans
```

## Byte Order

Common byte orders:
- `ABCD` - Big-endian (most common)
- `BADC` - Mid-big-endian / Byte-swapped
- `DCBA` - Little-endian
- `CDAB` - Mid-little-endian / Word-swapped

Aliases:
- `WORD_SWAP` = `CDAB`
- `BYTE_SWAP` = `BADC`
- `FULL_SWAP` = `DCBA`

## Review Process

1. **Automatic validation**: CI checks schema conformance
2. **Manual review**: We verify accuracy against datasheets
3. **Field testing**: Ideally tested with real hardware
4. **Promotion**: Once validated, moved to `registry/stable/`

## Becoming a Maintainer

When you contribute a device profile, you automatically become its maintainer! This means:

- You'll be notified of PRs affecting your device (via GitHub CODEOWNERS)
- You can review and approve changes to your device
- Your name appears in the device profile and manifest
- You help ensure quality for devices you know well

See [MAINTAINERS.md](MAINTAINERS.md) for full details on the maintainer system.

## Questions?

- Open an issue for questions about the schema
- Join discussions for general questions
- Check existing device profiles for examples
- Contact maintainers: edb+openmodbus@stekker.com

Thank you for contributing to the OpenModbus ecosystem!
