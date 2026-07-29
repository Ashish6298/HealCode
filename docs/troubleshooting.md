# Troubleshooting Guide

This guide describes resolutions for common issues when using HealCode.

## Missing Toolchains

If a scan reports warnings about Node.js or Python mismatch:
- Ensure the respective binary directories are in your system PATH variable.
- Re-run with `healcode scan --no-cache` to bypass cached configurations.

## Cache Out-of-sync

If results match previous scans despite modifying target files:
- Run with the `--no-cache` flag.
- Manually remove `.healcode_cache.db` from your project root.
