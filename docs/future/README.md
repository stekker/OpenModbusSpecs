# Future Enhancements

This directory contains documentation for features that are **not yet implemented** but may be added later as the project matures.

## Why "future"?

These features add complexity that's not justified at the current early stage. We're keeping the documentation so they can be implemented when there's clear demand.

## Current Future Features

### PGP Signature Verification (`PGP_SIGNING.md`)

**Status**: Schema supports it, but not enforced in CI
**Why postponed**: Adds friction for contributors at early stage
**When to implement**: When multiple vendors actively maintain profiles and authenticity becomes a concern

The groundwork is done:
- Schema has `signature`, `pgp_fingerprint`, `pgp_key_url` fields
- `tools/verify_signature.py` is functional
- Just needs to be uncommented in CI workflow

**To enable**: See PGP_SIGNING.md for complete vendor guide

---

## Proposing New Features

Before implementing complex features:
1. Open an issue with use case
2. Get feedback from 2+ active maintainers
3. Consider: Does this help or hinder adoption?
