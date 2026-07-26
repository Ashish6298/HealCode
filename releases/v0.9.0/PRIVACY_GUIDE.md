# Privacy Guide - v0.9.0

HealCode masks the following before transmitting data to external AI providers:

- API keys (`api_key`, `apikey`, `secret_key`)
- Access tokens (`access_token`, `bearer`)
- Passwords (`password`, `passwd`, `pwd`)
- Connection strings (`connection_string`, `database_url`, `db_url`)
- SSH / private keys (PEM blocks)
- AWS credentials (`aws_access_key_id`, `aws_secret_access_key`)

The `OfflineProvider` never transmits data externally. Use `healcode ai --offline` to guarantee no network calls.
