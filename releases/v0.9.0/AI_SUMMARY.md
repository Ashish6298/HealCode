# AI Summary - v0.9.0

The AI Intelligence Engine is an optional, modular layer that consumes scanner findings to produce:

1. **Correlated Issue Groups** — Related findings clustered by domain (Docker, Git, Security, etc.).
2. **Root Cause Analysis** — Inferred causal relationships with confidence scores.
3. **Prioritized Recommendations** — Repair actions ranked by risk, difficulty, and estimated time.
4. **Executive Summaries** — Human-friendly environment health narratives.

The engine ships with an offline heuristic provider and supports pluggable cloud/local LLM providers.
