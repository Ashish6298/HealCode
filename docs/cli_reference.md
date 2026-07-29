# CLI Reference Manual

HealCode provides a unified CLI utility matching the following commands.

## Subcommands

### `scan`
Runs active diagnostic checks on a directory path.
```bash
healcode scan [target] [--no-cache] [--format console|json|csv|xml] [--profile PROFILE]
```

### `config`
Configures settings and initializes local configuration profiles.
```bash
healcode config init
healcode config show
```

### `profile`
Lists and manages scan profiles.
```bash
healcode profile list
healcode profile show
healcode profile set [name]
```

### `baseline`
Save current scan baseline or compare configuration drift against a baseline.
```bash
healcode baseline create [name]
healcode baseline compare [name]
```

### `watch`
Monitor directory changes and trigger incremental rescans.
```bash
healcode watch [target]
```

### `marketplace`
Offline command to search, install, update, and manage plugins.
```bash
healcode marketplace search [query]
healcode marketplace install [plugin_name]
```

### `ai`
Run AI root-cause analysis on findings.
```bash
healcode ai [--offline]
```
