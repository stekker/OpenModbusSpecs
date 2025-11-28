# PGP Signature Verification Guide

This guide explains how vendors can digitally sign their device profiles for authenticity.

## Why Sign Device Profiles?

✅ **Authenticity**: Prove the profile comes from the official vendor
✅ **Integrity**: Detect tampering or unauthorized modifications
✅ **Trust**: Build confidence in vendor-maintained profiles
✅ **Security**: Prevent supply-chain attacks

## For Vendors: How to Sign Your Profiles

### Step 1: Generate PGP Key (if needed)

```bash
# Generate new key
gpg --full-generate-key

# Choose:
# - RSA and RSA (default)
# - 4096 bits
# - Key does not expire (or set expiry)
# - Real name: Your Company
# - Email: support@yourcompany.com
```

### Step 2: Set Up Web Key Directory (WKD)

**Recommended:** Host your public key using the WKD standard.

```bash
# Export your public key
gpg --export support@yourcompany.com > pubkey.asc

# Generate WKD hash
echo -n "support" | sha1sum | xxd -r -p | base32 | tr 'A-Z' 'a-z' | tr -d '='
# Output: 8fh4si4oend9km1d85ckm45o7h3bjpu4 (example)

# Host at:
# https://yourcompany.com/.well-known/openpgpkey/hu/8fh4si4oend9km1d85ckm45o7h3bjpu4

# Enable CORS headers in your web server:
Access-Control-Allow-Origin: *
```

**Directory structure:**
```
yourcompany.com/
└── .well-known/
    └── openpgpkey/
        ├── policy         # Optional: contains allowed domains
        └── hu/
            └── 8fh4si4... # Your key file (binary format)
```

### Step 3: Add PGP Info to Device Profile

```yaml
version: "0.1.0"

device:
  id: acme_meter_pro
  manufacturer: ACME Corp
  model: Meter Pro 3000
  protocol: modbus_tcp

  maintainers:
    - name: "ACME Support Team"
      github: "acmecorp"
      email: "support@acme.com"
      role: "primary"
      pgp_fingerprint: "1234567890ABCDEF1234567890ABCDEF12345678"
      pgp_key_url: "https://acme.com/pgp/support.asc"  # Fallback

registers:
  # ... your registers
```

### Step 4: Sign the Profile

```bash
# Create canonical version (without signature field)
# Sign it
gpg --detach-sign --armor --local-user support@acme.com acme_meter_pro.yaml

# This creates acme_meter_pro.yaml.asc

# Convert to base64 for embedding
base64 acme_meter_pro.yaml.asc > signature.b64
```

### Step 5: Embed Signature in YAML

```yaml
version: "0.1.0"

device:
  id: acme_meter_pro
  # ... other fields ...

  signature:
    pgp: |
      LS0tLS1CRUdJTiBQR1AgU0lHTkFUVVJFLS0tLS0KCmlRSXpCQUFCQ2dBZEZpRUVBQUFB
      QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB
      ... (base64-encoded signature)
    signed_by: "support@acme.com"
    signed_at: "2025-11-28T16:00:00Z"

registers:
  # ... your registers
```

## For Users: How to Verify Signatures

### Automatic Verification (CI)

Our CI automatically verifies vendor signatures:

```yaml
# .github/workflows/validate-devices.yml
- name: Verify PGP signatures
  run: |
    python3 tools/verify_signature.py registry/stable/**/*.yaml
```

### Manual Verification

```bash
# Verify a vendor profile
python3 tools/verify_signature.py registry/stable/acme/meter_pro.yaml

# Output:
# Verifying: registry/stable/acme/meter_pro.yaml
# ============================================================
#   Signed by: support@acme.com
#   Signed at: 2025-11-28T16:00:00Z
#   Fetching public key...
#   Trying WKD: https://acme.com/.well-known/openpgpkey/hu/...
#   Importing public key...
#   Verifying signature...
#   ✓ Signature valid!
# ============================================================
# ✓ Verification successful
```

## Security Model

### Trust Hierarchy

```
┌─────────────────────┐
│ Vendor's WKD Server │ ← Vendor controls (HTTPS secured)
└──────────┬──────────┘
           │ Publishes
           ▼
    ┌─────────────┐
    │ PGP Public  │
    │    Key      │
    └──────┬──────┘
           │ Signs
           ▼
┌──────────────────────┐
│ Device Profile YAML  │ ← Signature embedded
└──────────┬───────────┘
           │ Verified by
           ▼
    ┌─────────────┐
    │ CI Pipeline │ ← Automated check
    │ + Reviewers │
    └─────────────┘
```

### Signature Levels

**Required:**
- Vendor-hosted canonical sources
- Profiles with `canonical_source` field

**Recommended:**
- All vendor-maintained profiles in our registry

**Optional:**
- Community contributions (can be unsigned)

## Alternative: Separate Signature Files

If you prefer not to embed signatures:

```bash
# Directory structure:
registry/stable/acme/
├── meter_pro.yaml
└── meter_pro.yaml.asc  # Detached signature

# Verification:
gpg --verify meter_pro.yaml.asc meter_pro.yaml
```

## Key Management Best Practices

✅ **Use dedicated signing key** (not personal key)
✅ **Set expiration** (1-2 years, then renew)
✅ **Publish revocation certificate** (if key compromised)
✅ **Document key rotation** process
✅ **Use hardware security module** (HSM) for production

## WKD Setup Examples

### Nginx

```nginx
location /.well-known/openpgpkey/ {
    add_header Access-Control-Allow-Origin *;
    add_header Content-Type application/octet-stream;
}
```

### Apache

```apache
<Directory "/var/www/html/.well-known/openpgpkey">
    Header set Access-Control-Allow-Origin "*"
    Header set Content-Type "application/octet-stream"
</Directory>
```

### Python (for dynamic generation)

```python
import hashlib
import base64

def wkd_hash(local_part):
    sha1 = hashlib.sha1(local_part.encode()).digest()
    return base64.b32encode(sha1).decode().lower().rstrip('=')

# Generate path
local = "support"
hash_dir = wkd_hash(local)
print(f"/.well-known/openpgpkey/hu/{hash_dir}")
```

## Testing Your WKD Setup

```bash
# Test WKD discovery
gpg --locate-keys --auto-key-locate clear,wkd support@yourcompany.com

# Should output:
# gpg: key XXXXXXXX: public key "Support <support@yourcompany.com>" imported
```

## FAQ

**Q: Is signing required?**
A: No, but strongly recommended for vendor-maintained profiles.

**Q: Can I use a different email than maintainer email?**
A: Yes, but it should be listed in maintainers with that email.

**Q: What if my WKD setup doesn't work?**
A: Provide `pgp_key_url` as fallback direct link.

**Q: Can I sign with subkey?**
A: Yes, as long as the primary key is published via WKD.

**Q: How often should I re-sign?**
A: Re-sign whenever the profile content changes.

## Resources

- [WKD Specification](https://datatracker.ietf.org/doc/html/draft-koch-openpgp-webkey-service)
- [GPG Documentation](https://gnupg.org/documentation/)
- [Security.txt RFC 9116](https://www.rfc-editor.org/rfc/rfc9116.html)

## Contact

Questions about PGP signing? Contact: edb+openmodbus@stekker.com
