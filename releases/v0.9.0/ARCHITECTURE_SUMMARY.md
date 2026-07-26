# Architecture Summary - v0.9.0

Phase 9 introduces the `healcode/ai/` subsystem as a post-scan enhancement layer:

```
Scanner Engine → Findings → AI Engine
                                ├── Correlation Engine
                                ├── Root Cause Engine
                                ├── Recommendation Engine
                                ├── Prioritization Engine
                                └── Summary Engine
```

Key design principles:
- AI never modifies scanner output.
- AI is entirely optional (offline-first).
- Privacy masking applied before any external transmission.
- Provider interface supports future LLM plugins without core changes.
