# HealCode v0.9.0 Implementation Summary

## New Subsystem: `healcode/ai/`
- **provider.py** — `AIProvider` ABC, `OfflineProvider`, provider registry.
- **engine.py** — `AIEngine` orchestrating correlation, root-cause, recommendation, prioritization, and summary.
- **privacy.py** — `PrivacyMasker` with regex-based secret scrubbing.

## Configuration Extension
- `AIConfig` dataclass added to `ProjectConfig` (enabled, provider, model, offline_mode, mask_secrets, temperature, max_tokens, timeout, retry_count, local_endpoint).

## CLI Extension
- `AICommand` registered in entrypoint as `healcode ai`.

## Health Engine Extension
- 3 new categories: AI_READINESS, ROOT_CAUSE_COVERAGE, RECOMMENDATION_QUALITY.
