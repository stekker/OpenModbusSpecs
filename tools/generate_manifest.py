#!/usr/bin/env python3
"""Generate manifest.json from device profiles in registry/"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed")
    print("Install with: pip3 install pyyaml")
    sys.exit(1)


def generate_manifest():
    """Generate manifest from all YAML files in registry/"""
    repo_root = Path(__file__).parent.parent

    devices = {}

    # Process both stable and contrib directories
    for stability in ["stable", "contrib"]:
        registry_dir = repo_root / "registry" / stability

        if not registry_dir.exists():
            continue

        # Find all YAML files
        for yaml_file in sorted(registry_dir.rglob("*.yaml")):
            if yaml_file.name == "README.md":
                continue

            # Load device data
            with open(yaml_file) as f:
                data = yaml.safe_load(f)

            device_info = data.get("device", {})
            device_id = device_info.get("id")

            if not device_id:
                print(f"Warning: No device.id found in {yaml_file}")
                continue

            # Get relative path from repo root
            rel_path = yaml_file.relative_to(repo_root)

            # Extract maintainers
            maintainers_list = device_info.get("maintainers", [])
            maintainer_info = []
            for m in maintainers_list:
                maintainer_info.append({
                    "github": m.get("github"),
                    "role": m.get("role", "contributor")
                })

            # Build version entry
            version_entry = {
                "version": "1.0.0",  # Default version for now
                "stability": stability,
                "path": str(rel_path),
                "url": f"https://raw.githubusercontent.com/stekker/OpenModbusSpecs/main/{rel_path}",
                "published_at": datetime.now(timezone.utc).isoformat(),
                "maintainers": maintainer_info,
                "has_active_maintainer": len(maintainer_info) > 0
            }

            # Add canonical source if available
            canonical = device_info.get("canonical_source")
            if canonical:
                version_entry["canonical_source"] = canonical

            # Initialize device entry if it doesn't exist
            if device_id not in devices:
                devices[device_id] = {
                    "manufacturer": device_info.get("manufacturer", ""),
                    "model": device_info.get("model", ""),
                    "description": device_info.get("description", ""),
                    "protocol": device_info.get("protocol", ""),
                    "versions": [],
                    "latest": {}
                }

            # Add version to device
            devices[device_id]["versions"].append(version_entry)

            # Update latest pointer
            devices[device_id]["latest"][stability] = "1.0.0"

    # Build manifest
    manifest = {
        "version": "0.1.0",
        "schema_version": "0.1.0",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "description": "OpenModbus Device Registry - Stable device profiles",
        "devices": devices
    }

    # Write manifest
    manifest_path = repo_root / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Generated manifest with {len(devices)} devices:")
    for device_id in sorted(devices.keys()):
        print(f"  - {device_id}")
    print(f"\nManifest written to: {manifest_path}")


if __name__ == "__main__":
    generate_manifest()
