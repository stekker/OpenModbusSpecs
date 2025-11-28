#!/usr/bin/env python3
"""Verify PGP signatures on vendor-maintained device profiles"""

import sys
import subprocess
import hashlib
import base64
import tempfile
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed")
    print("Install with: pip3 install pyyaml")
    sys.exit(1)


def wkd_hash(email_local):
    """Generate WKD hash from email local part (before @)"""
    sha1 = hashlib.sha1(email_local.encode('utf-8')).digest()
    return base64.b32encode(sha1).decode('ascii').lower().rstrip('=')


def fetch_pgp_key_wkd(email):
    """Fetch PGP public key via Web Key Directory (WKD)"""
    local_part, domain = email.split('@')
    wkd_url = f"https://{domain}/.well-known/openpgpkey/hu/{wkd_hash(local_part)}?l={local_part}"

    print(f"  Trying WKD: {wkd_url}")

    try:
        response = urlopen(wkd_url, timeout=10)
        return response.read()
    except Exception as e:
        print(f"  WKD lookup failed: {e}")
        return None


def fetch_pgp_key_url(url):
    """Fetch PGP public key from direct URL"""
    print(f"  Fetching key from: {url}")

    try:
        response = urlopen(url, timeout=10)
        return response.read()
    except Exception as e:
        print(f"  Failed to fetch key: {e}")
        return None


def import_pgp_key(key_data):
    """Import PGP key into temporary keyring"""
    try:
        result = subprocess.run(
            ['gpg', '--import', '--batch', '--no-default-keyring', '--keyring', 'trustedkeys.gpg'],
            input=key_data,
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        print(f"  Failed to import key: {e}")
        return False


def verify_detached_signature(yaml_file, signature_b64, signer_email):
    """Verify detached PGP signature"""

    # Decode signature
    try:
        signature_data = base64.b64decode(signature_b64)
    except Exception as e:
        print(f"  Failed to decode signature: {e}")
        return False

    # Create temporary files
    with tempfile.NamedTemporaryFile(suffix='.sig', delete=False) as sig_file:
        sig_file.write(signature_data)
        sig_path = sig_file.name

    try:
        # Remove signature from YAML for verification
        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        # Remove signature field for canonical form
        if 'device' in data and 'signature' in data['device']:
            del data['device']['signature']

        # Write canonical form
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as canonical:
            yaml.dump(data, canonical, default_flow_style=False)
            canonical_path = canonical.name

        # Verify signature
        result = subprocess.run(
            ['gpg', '--verify', '--batch', sig_path, canonical_path],
            capture_output=True,
            timeout=10
        )

        return result.returncode == 0

    except Exception as e:
        print(f"  Verification failed: {e}")
        return False
    finally:
        # Cleanup
        Path(sig_path).unlink(missing_ok=True)
        if 'canonical_path' in locals():
            Path(canonical_path).unlink(missing_ok=True)


def verify_profile(yaml_file):
    """Verify a device profile's PGP signature"""
    print(f"\nVerifying: {yaml_file}")
    print("=" * 60)

    # Load YAML
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    device_info = data.get('device', {})
    signature_info = device_info.get('signature')

    if not signature_info:
        print("  ⚠ No signature found (optional for community contributions)")
        return True  # Not required for all profiles

    # Extract signature details
    pgp_sig = signature_info.get('pgp')
    signed_by = signature_info.get('signed_by')
    signed_at = signature_info.get('signed_at')

    if not pgp_sig or not signed_by:
        print("  ✗ Invalid signature format")
        return False

    print(f"  Signed by: {signed_by}")
    print(f"  Signed at: {signed_at}")

    # Get maintainer info
    maintainers = device_info.get('maintainers', [])
    signer_maintainer = None

    for m in maintainers:
        if m.get('email') == signed_by:
            signer_maintainer = m
            break

    if not signer_maintainer:
        print(f"  ⚠ Signer {signed_by} not in maintainers list")

    # Try to fetch public key
    key_data = None

    # 1. Try WKD
    print("\n  Fetching public key...")
    key_data = fetch_pgp_key_wkd(signed_by)

    # 2. Try direct URL if provided
    if not key_data and signer_maintainer and signer_maintainer.get('pgp_key_url'):
        key_data = fetch_pgp_key_url(signer_maintainer['pgp_key_url'])

    if not key_data:
        print("  ✗ Could not fetch public key")
        return False

    # Import key
    print("  Importing public key...")
    if not import_pgp_key(key_data):
        print("  ✗ Failed to import key")
        return False

    # Verify signature
    print("  Verifying signature...")
    if verify_detached_signature(yaml_file, pgp_sig, signed_by):
        print("  ✓ Signature valid!")

        # Check fingerprint if provided
        if signer_maintainer and signer_maintainer.get('pgp_fingerprint'):
            expected_fp = signer_maintainer['pgp_fingerprint']
            print(f"  Expected fingerprint: {expected_fp}")
            # TODO: Verify actual fingerprint matches

        return True
    else:
        print("  ✗ Signature verification failed")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_signature.py <yaml_file>")
        sys.exit(1)

    yaml_file = sys.argv[1]

    if not Path(yaml_file).exists():
        print(f"Error: File not found: {yaml_file}")
        sys.exit(1)

    # Check if GPG is available
    try:
        subprocess.run(['gpg', '--version'], capture_output=True, check=True)
    except:
        print("Error: GPG not installed")
        print("Install with: apt install gnupg  # or brew install gnupg")
        sys.exit(1)

    success = verify_profile(yaml_file)

    print("\n" + "=" * 60)
    if success:
        print("✓ Verification successful")
        sys.exit(0)
    else:
        print("✗ Verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
