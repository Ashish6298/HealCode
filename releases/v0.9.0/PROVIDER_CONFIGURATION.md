# Provider Configuration Reference - v0.9.0

## AIConfig Fields
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| enabled | bool | False | Enable AI analysis |
| provider | str | "offline" | Provider name |
| model | str | "" | Model identifier |
| offline_mode | bool | True | Force offline heuristic |
| mask_secrets | bool | True | Scrub secrets before external calls |
| temperature | float | 0.2 | LLM temperature |
| max_tokens | int | 2048 | Max response tokens |
| timeout | int | 30 | Request timeout (seconds) |
| retry_count | int | 2 | Retry attempts |
| local_endpoint | str | "" | Local LLM endpoint URL |
