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
version: "0.3.0"

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
    name: voltage_L1            # Machine-readable identifier (snake_case)
    type: float32               # int16, uint16, int32, uint32, int64, uint64, float32, float64, string, or bool
    length: 2                   # Number of 16-bit registers (optional for numeric types, inferred from type)
    unit: V                     # SI unit or empty string
    register_type: holding      # Can override device default
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
    display_name: "Original register name from manual"
    byte_order: BADC           # Override device default
    obis_code: "1-0:1.8.0*255" # For energy meters
    notes: "Special considerations for this register"
    scaling:
      factor: 0.01
      offset: 0
    bits:                       # For bitfield definitions
      "0":
        name: status_bit_0
        display_name: "Ready"
      "1":
        name: status_bit_1
        display_name: "Fault"
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

### name

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

All numeric types have **implied length** (number of 16-bit registers) - you don't need to specify it. Only `string` types require an explicit `length` field.

### Complete Type Reference

| Type | Bits | Registers | Signedness | Usage |
|------|------|-----------|------------|-------|
| `uint8` | 8 | 1 | Unsigned | Rare (0-255) |
| `int8` | 8 | 1 | Signed | Rare (-128 to 127) |
| `uint16` | 16 | 1 | Unsigned | Very common (baseline Modbus) |
| `int16` | 16 | 1 | Signed | Very common |
| `uint32` | 32 | 2 | Unsigned | Common |
| `int32` | 32 | 2 | Signed | Common |
| `uint64` | 64 | 4 | Unsigned | Rare |
| `int64` | 64 | 4 | Signed | Rare |
| `float32` | 32 | 2 | IEEE 754 | Very common |
| `float64` | 64 | 4 | IEEE 754 | Uncommon |
| `bool` | 1 bit | 1 | N/A | Common |
| `string` | Variable | Variable | N/A | Common |

### Examples

#### Numeric Types (length inferred)
```yaml
registers:
  "0":
    name: product_id
    type: uint16      # 1 register - NO length field needed
    unit: ""

  "10":
    name: voltage_L1
    type: float32     # 2 registers - NO length field needed
    unit: V
    scaling:
      factor: 0.01
      offset: 0

  "100":
    name: total_energy
    type: uint32      # 2 registers - NO length field needed
    unit: Wh

  "200":
    name: timestamp
    type: int64       # 4 registers - NO length field needed
    unit: s
```

#### String Type (length required)
```yaml
registers:
  "1000":
    name: device_name
    type: string
    length: 16        # REQUIRED: 16 registers = 32 bytes capacity
    unit: ""
```

### Common Mistakes

**❌ Don't use programming language aliases** - they're not accepted:
```yaml
type: int            # ❌ Error - use int32
type: short          # ❌ Error - use int16
type: double         # ❌ Error - use float64
type: float          # ❌ Error - use float32
```

**✅ Use explicit numeric type names:**
```yaml
type: int32          # ✓ Correct
type: int16          # ✓ Correct
type: float64        # ✓ Correct
type: float32        # ✓ Correct
```

The validator will suggest corrections if you use common aliases.

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
