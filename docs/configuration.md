# Configuration Reference

HealCode behavior is configured through a `healcode.json` file in the root of your project.

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `logging.level` | string | `"INFO"` | Log output detail level (`TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`). |
| `logging.json_format` | boolean | `false` | Enable structured JSON logging. |
| `cache.enabled` | boolean | `true` | Enable scan caching. |
| `scan.max_depth` | integer | `5` | Maximum recursive folder depth. |
| `scan.profile` | string | `"Full"` | Active scan profile (`DevOps`, `Security`, `Minimal`, `Full`). |
| `ai.enabled` | boolean | `false` | Enable AI Intelligence features. |
| `ai.offline_mode` | boolean | `true` | Execute local AI heuristics instead of calling remote APIs. |
