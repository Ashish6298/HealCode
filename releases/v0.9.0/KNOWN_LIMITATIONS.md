# Known Limitations - v0.9.0

- Only the `OfflineProvider` ships with HealCode core; cloud providers require separate plugin packages.
- Privacy masker uses regex patterns; custom secret formats may need configuration overrides.
- AI analysis is heuristic-based in offline mode — LLM-powered analysis requires an external provider plugin.
