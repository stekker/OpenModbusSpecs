# Architecture Decisions

This document explains key design decisions for OpenModbusSpecs.

## Manifest Format: JSON vs YAML

**Decision: Use JSON for manifest.json**

**Rationale:**

✅ **Machine-first format**: The manifest is primarily consumed by programs, not humans
✅ **Standard for package registries**: npm (package.json), Composer (composer.json), Cargo (Cargo.lock), pip (all use JSON)
✅ **Broader language support**: Every language has JSON parsers, YAML support varies
✅ **No ambiguity**: JSON has one way to represent data, YAML has many
✅ **API-friendly**: Direct JSON responses from GitHub raw files

**Device profiles use YAML because:**
- Human-authored and reviewed
- More readable for technical documentation
- Comments support (for notes, TODOs)
- Less verbose for nested structures

**Example usage:**
```bash
# Fetch manifest (JSON)
curl https://raw.githubusercontent.com/stekker/OpenModbusSpecs/main/manifest.json

# Fetch device profile (YAML)
curl https://raw.githubusercontent.com/stekker/OpenModbusSpecs/main/registry/stable/alfen/ng9xx.yaml
```

## Version Locking for Production

**Critical for stability:** Edge devices must pin specific versions.

### Anti-Pattern: Auto-Update
```go
// ❌ DON'T DO THIS IN PRODUCTION
profile := fetchLatestDeviceProfile("alfen_ng9xx")
// Behavior could change between daemon restarts!
```

### Best Practice: Version Pinning
```yaml
# edge-config.yaml
device_profiles:
  alfen_ng9xx:
    version: "1.0.0"          # Locked version
    stability: "stable"        # Never use contrib in prod
    source: "registry"         # or "canonical" for vendor-hosted
    checksum: "sha256:abc..."  # Integrity check

  # Can test new versions in development
  peblar_home:
    version: "1.1.0-beta"
    stability: "contrib"
    source: "canonical"
```

### Version Strategy Options

**1. Strict Pinning (Recommended for Production)**
```go
config := DeviceConfig{
    DeviceID: "alfen_ng9xx",
    Version:  "1.0.0",        // Exact version
    Source:   "canonical",     // Prefer vendor source
}
```

**2. Stability-Based (For Development)**
```go
config := DeviceConfig{
    DeviceID:  "alfen_ng9xx",
    Version:   "latest",
    Stability: "stable",       // Latest stable only
}
```

**3. Automatic Updates (CI/Testing Only)**
```go
// Only for automated testing environments
config := DeviceConfig{
    DeviceID:  "alfen_ng9xx",
    Version:   "latest",
    Stability: "contrib",      // Bleeding edge
    AutoUpdate: true,          // Dangerous!
}
```

### Edge Device Implementation Example

```go
type DeviceProfileManager struct {
    cache     map[string]DeviceProfile
    lockFile  string  // versions.lock - like package-lock.json
}

func (m *DeviceProfileManager) LoadProfile(deviceID string) (*DeviceProfile, error) {
    // 1. Check lock file for pinned version
    locked := m.readLockFile()
    if version, ok := locked[deviceID]; ok {
        return m.fetchVersion(deviceID, version)
    }

    // 2. Check manifest for latest stable
    manifest := m.fetchManifest()
    version := manifest.Devices[deviceID].Latest.Stable

    // 3. Download and verify
    profile := m.fetchVersion(deviceID, version)

    // 4. Update lock file
    m.updateLockFile(deviceID, version)

    return profile, nil
}
```

### Lock File Format

```json
{
  "generated_at": "2025-11-28T15:30:00Z",
  "schema_version": "0.3.0",
  "locked_profiles": {
    "alfen_ng9xx": {
      "version": "1.0.0",
      "stability": "stable",
      "url": "https://raw.githubusercontent.com/stekker/OpenModbusSpecs/main/registry/stable/alfen/ng9xx.yaml",
      "canonical_source": null,
      "sha256": "abc123...",
      "locked_at": "2025-11-28T10:00:00Z"
    },
    "janitza_umg604": {
      "version": "1.0.0",
      "stability": "stable",
      "url": "https://raw.githubusercontent.com/stekker/OpenModbusSpecs/main/registry/stable/janitza/umg604.yaml",
      "sha256": "def456...",
      "locked_at": "2025-11-27T14:00:00Z"
    }
  }
}
```

## CODEOWNERS

**What it is:** GitHub-specific feature for automated PR review requests

**What it does:**
- ✅ Automatically requests review from specified users/teams
- ✅ Sends email notifications to maintainers
- ✅ Shows in PR interface as "Requested reviewers"
- ✅ Can enforce required reviews before merge

**Limitations:**
- ❌ GitHub-specific (doesn't work on GitLab, Gitea, etc.)
- ❌ Requires users to have GitHub accounts
- ❌ Doesn't work for vendor-hosted profiles

**Our approach:**

1. **Use CODEOWNERS for GitHub workflow**
   - Works great for contributors with GitHub accounts
   - Automatic notifications

2. **Also maintain metadata in YAML**
   - Vendor-neutral
   - Portable across platforms
   - Part of the spec itself

3. **Platform-agnostic alternative**
   - Maintainers are in the YAML `device.maintainers`
   - Tools can parse this for any platform
   - Email notifications can be custom-built

**Example alternatives:**

GitLab uses `.gitlab/CODEOWNERS`, Gitea has similar features. By keeping maintainer info in the YAML files themselves, we remain platform-independent.

## Vendor-Hosted Profiles

**Workflow:**

```
┌─────────────────┐
│ Vendor Website  │
│ acme.com        │
│ /modbus/*.yaml  │ ← Canonical source (controlled by vendor)
└────────┬────────┘
         │ Referenced by
         │
┌────────▼────────────────┐
│ OpenModbusSpecs         │
│ (GitHub Registry)       │
│ - Validation            │
│ - Discovery             │ ← Mirror + metadata
│ - Community additions   │
└────────┬────────────────┘
         │ Used by
         │
┌────────▼────────┐
│ Edge Device     │
│ 1. Check vendor │ ← Prefers canonical_source
│ 2. Fallback     │ ← Uses registry mirror
│ 3. Cache        │ ← Local cache
└─────────────────┘
```

**Benefits:**
- Vendors maintain control
- We provide discovery + validation
- Users get reliability (fallback mirror)

## Summary

| Aspect | Decision | Reason |
|--------|----------|--------|
| **Manifest format** | JSON | Machine-first, standard for registries |
| **Device profiles** | YAML | Human-readable, comments, less verbose |
| **Version strategy** | Lock in production | Prevent surprise behavior changes |
| **CODEOWNERS** | Use but don't depend on it | GitHub convenience, not core to spec |
| **Vendor hosting** | Support canonical_source | Vendors control authoritative source |
| **Stability levels** | stable/contrib/beta | Clear quality signaling |

These decisions prioritize **stability for production**, **openness for community**, and **flexibility for vendors**.
