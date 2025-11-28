#!/usr/bin/env python3
"""Check that all device profiles have maintainers"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed")
    print("Install with: pip3 install pyyaml")
    sys.exit(1)


def check_maintainers():
    """Check all device profiles for maintainer information"""
    repo_root = Path(__file__).parent.parent

    orphaned = []
    with_maintainers = []

    # Check both stable and contrib
    for stability in ["stable", "contrib"]:
        registry_dir = repo_root / "registry" / stability

        if not registry_dir.exists():
            continue

        for yaml_file in sorted(registry_dir.rglob("*.yaml")):
            if yaml_file.name == "README.md":
                continue

            # Load device data
            with open(yaml_file) as f:
                data = yaml.safe_load(f)

            device_info = data.get("device", {})
            device_id = device_info.get("id", yaml_file.stem)
            maintainers = device_info.get("maintainers", [])

            rel_path = yaml_file.relative_to(repo_root)

            if not maintainers or len(maintainers) == 0:
                orphaned.append({
                    "id": device_id,
                    "path": str(rel_path),
                    "stability": stability
                })
            else:
                # Check that maintainers have required fields
                for m in maintainers:
                    if not m.get("github"):
                        print(f"Warning: Maintainer without github username in {rel_path}")

                with_maintainers.append({
                    "id": device_id,
                    "maintainers": [m.get("github") for m in maintainers],
                    "stability": stability
                })

    # Print summary
    print("Maintainer Status")
    print("=" * 60)
    print()

    print(f"✓ Devices with maintainers: {len(with_maintainers)}")
    for device in with_maintainers:
        maintainer_str = ", ".join(f"@{m}" for m in device["maintainers"])
        print(f"  - {device['id']} [{device['stability']}]: {maintainer_str}")

    print()

    if orphaned:
        print(f"⚠ Orphaned devices (no maintainer): {len(orphaned)}")
        for device in orphaned:
            print(f"  - {device['id']} [{device['stability']}]: {device['path']}")
        print()
        print("These devices need maintainers! See docs/CONTRIBUTING.md")
        print()

    print("=" * 60)

    # Return exit code (0 = success, orphaned devices are warning not error)
    return 0


if __name__ == "__main__":
    sys.exit(check_maintainers())
