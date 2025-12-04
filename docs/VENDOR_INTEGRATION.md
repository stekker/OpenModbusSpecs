# Vendor Integration Guide

This guide explains how device manufacturers can provide authoritative OpenModbus device profiles.

## Why Vendors Should Participate

**Benefits for vendors:**
- ✅ Customers can integrate your devices faster (minutes vs days)
- ✅ Reduce support burden from integration questions
- ✅ Ensure accurate representation of your device capabilities
- ✅ Join the growing OpenModbus ecosystem
- ✅ Free marketing to integrators and automation engineers

**Benefits for users:**
- ✅ Authoritative source directly from manufacturer
- ✅ Always up-to-date with latest firmware
- ✅ Official support and validation

## Hosting Your Device Profile

### Option 1: Host on Your Website (Recommended)

Host the YAML file on your website and mark it as canonical:

```yaml
version: "0.3.0"

device:
  id: acme_meter_pro
  manufacturer: ACME Corp
  model: Meter Pro 3000
  protocol: modbus_tcp
  canonical_source: "https://acme.com/downloads/modbus/meter-pro-3000.yaml"
  sources:
    - url: "https://acme.com/docs/meter-pro-3000-modbus.pdf"
      type: "manual"
      description: "Official Modbus Integration Manual"
  maintainers:
    - name: "ACME Support Team"
      github: "acmecorp"
      organization: "ACME Corp"
      email: "support@acme.com"
      role: "primary"

registers:
  # Your device registers...
```

**Benefits:**
- You control updates
- No dependency on third parties
- Can version alongside firmware releases

**Best practices:**
- Use stable URL that won't break
- Enable CORS headers for browser-based tools
- Consider versioning: `meter-pro-3000-v1.2.yaml`

### Option 2: Contribute to OpenModbusSpecs

Submit your profile to our registry:

1. Create YAML following our schema
2. Submit PR to `registry/contrib/`
3. After validation, promoted to `registry/stable/`
4. We mirror and distribute

**Benefits:**
- Community validation
- GitHub-based version control
- Discoverable in central registry

## Integration with Edge Devices

Users can configure their systems to prefer vendor sources:

```yaml
# Edge device config
device_profiles:
  sources:
    - type: "vendor_canonical"    # Try vendor's official URL first
      priority: 1
    - type: "openmodbus_registry"  # Fallback to our mirror
      priority: 2

  version_strategy: "locked"       # Don't auto-update in production
```

## Example: Vendor-Hosted Profile

```yaml
# https://victronenergy.com/modbus/vm-3p75ct.yaml
version: "0.3.0"

device:
  id: victron_vm3p75ct
  manufacturer: Victron Energy
  model: VM-3P75CT
  description: Three-phase energy meter
  protocol: modbus_udp
  canonical_source: "https://victronenergy.com/modbus/vm-3p75ct.yaml"

  sources:
    - url: "https://www.victronenergy.com/live/energy:vm-3p75ct"
      type: "website"
      description: "Product page"
    - url: "https://www.victronenergy.com/upload/documents/Datasheet-VM-3P75CT-energy-meter-EN.pdf"
      type: "datasheet"

  maintainers:
    - name: "Victron Energy"
      github: "victronenergy"
      organization: "Victron Energy B.V."
      email: "support@victronenergy.com"
      role: "primary"

registers:
  "4096":
    name: product_id
    display_name: "Product ID"
    type: uint16
    length: 1
    unit: ""
    register_type: holding
  # ... more registers
```

## Versioning Strategy

### For Production Edge Devices

**Recommended: Version Locking**

```go
// Edge device downloads specific version
profile := fetchDeviceProfile(
    deviceID: "victron_vm3p75ct",
    version: "1.0.0",        // Locked version
    stability: "stable"       // Only stable releases
)
```

**Never auto-update in production!** Pin to tested versions.

### For Development/Testing

```go
// Development: Use latest
profile := fetchDeviceProfile(
    deviceID: "victron_vm3p75ct",
    version: "latest",
    stability: "contrib"      // Test bleeding edge
)
```

## Manifest Structure

The manifest supports vendor-hosted profiles:

```json
{
  "devices": {
    "victron_vm3p75ct": {
      "versions": [
        {
          "version": "1.0.0",
          "stability": "stable",
          "url": "https://raw.githubusercontent.com/stekker/OpenModbusSpecs/main/...",
          "canonical_source": "https://victronenergy.com/modbus/vm-3p75ct.yaml",
          "maintainers": [{"github": "victronenergy", "role": "primary"}]
        }
      ],
      "latest": {"stable": "1.0.0"}
    }
  }
}
```

Edge devices check `canonical_source` first, fall back to our mirror.

## Submitting Your Profile

1. **Create** device profile following [schema](../schema/openmodbus-schema-v0.3.0.json)
2. **Validate** using `python3 tools/validate.py`
3. **Test** with real hardware
4. **Submit** via:
   - Option A: Host on your site, submit PR with canonical_source link
   - Option B: Submit full YAML to our registry
5. **Maintain** - you're notified of community changes via GitHub

## Questions?

Contact: edb+openmodbus@stekker.com

We're happy to help vendors integrate!
