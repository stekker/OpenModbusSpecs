# Maintainer Guide

This document explains the maintainer system for OpenModbus device profiles.

## What is a Maintainer?

Maintainers are individuals or organizations responsible for the accuracy and maintenance of specific device profiles. They review contributions, test updates, and ensure profile quality.

## Maintainer Roles

- **primary**: Main point of contact, has device access for testing
- **contributor**: Contributed to the profile, reviews changes
- **emeritus**: Former maintainer, no longer active but credited

## Becoming a Maintainer

### New Device

When you contribute a new device profile, you automatically become its initial maintainer.

### Existing Device

To adopt an orphaned device or become a co-maintainer:

1. Submit a PR adding yourself to the device's `maintainers` list
2. Explain your interest and experience with the device
3. Existing maintainer (if any) or core team will review

## Maintainer Responsibilities

✅ **Review PRs** affecting your device
✅ **Test changes** against real hardware when possible
✅ **Respond to issues** about your device
✅ **Keep profile updated** as firmware/documentation changes
✅ **Mentor contributors** interested in your device

## Maintainer Benefits

- Listed in device YAML and manifest
- GitHub notifications for device-specific PRs
- Recognition in community
- Direct input on device profile direction

## Stepping Down

If you can no longer maintain a device:

1. Update your role to `emeritus` or remove yourself
2. Notify core team so device can be marked as needing maintainer
3. Help transition to new maintainer if possible

## Core Team

For devices without maintainers, the Stekker core team (@stekker/openmodbus-core) provides backup review.

## Adding Maintainer Info to YAML

```yaml
device:
  id: example_device
  manufacturer: Example Corp
  model: EX-1000
  protocol: modbus_tcp
  maintainers:
    - name: Your Name
      github: yourusername
      organization: Your Company
      email: you@example.com
      role: primary
```

Only `github` is required. Email is recommended for direct contact.

## GitHub Integration

The `.github/CODEOWNERS` file routes PRs to device maintainers automatically. When you add yourself as maintainer, update CODEOWNERS too:

```
# In .github/CODEOWNERS
/registry/stable/example/** @yourusername
/registry/contrib/example_*.yaml @yourusername
```

## Questions?

Open an issue or contact the core team at edb+openmodbus@stekker.com
