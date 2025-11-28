# Maintainer Guide

This document explains the maintainer system for OpenModbus device profiles.

## What is a Maintainer?

Maintainers are individuals or organizations responsible for the accuracy and maintenance of specific device profiles. They review contributions, test updates, and ensure profile quality.

**Note**: At this early stage, governance is intentionally lightweight. The goal is to lower barriers to contribution while building quality through community ownership.

## Maintainer Roles

- **primary**: Main point of contact, has device access for testing, authoritative source
- **contributor**: Contributed to the profile, reviews changes
- **emeritus**: Former maintainer, no longer active but credited for past work

## Becoming a Maintainer

### Contributing a New Device

When you contribute a new device profile, **you become its maintainer by default**. Simply add yourself to the YAML:

```yaml
maintainers:
  - name: Your Name
    github: yourusername
    email: you@example.com
    role: primary
```

### Claiming an Existing Device

**For Manufacturers** (⭐ Strongly Encouraged):

If you're the device manufacturer, you're the authoritative source! To claim your product's profile:

1. Fork the repository
2. Update the device YAML, adding yourself as `role: primary`
3. Submit a PR with title: `[CLAIM] Manufacturer takeover: <device_name>`
4. If CI passes, it will be merged (manufacturers get priority)

**For Community Contributors**:

To adopt a device with only emeritus maintainers:

1. Submit a PR adding yourself to `maintainers` list
2. Explain your experience with the device (have hardware, use it regularly, etc.)
3. If CI passes and explanation is reasonable, it will be merged

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

1. Update your role to `emeritus` in the device YAML
2. Open an issue titled `[SEEKING MAINTAINER] <device_name>` to find a replacement
3. Help transition to new maintainer if possible

**Note**: Devices with only emeritus maintainers are available for community adoption!

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

## GitHub Integration (Optional)

The `.github/CODEOWNERS` file can route PRs to device maintainers automatically, but **it's optional** at this early stage.

If you want GitHub notifications for your devices:
1. Add yourself to `.github/CODEOWNERS`
2. GitHub will automatically request your review on relevant PRs

Example:
```
# In .github/CODEOWNERS
/registry/stable/example/** @yourusername
```

## Questions?

Open an issue or start a discussion. This is a community-run project!
