# Architecture Overview

HealCode is designed with a frozen core scanner pipeline that prioritizes performance, deterministic execution, and decoupling.

## Subsystems

```mermaid
graph TD
    CLI[CLI entrypoint.py] --> Engine[ScanEngine]
    Engine --> Cache[CacheManager]
    Engine --> Scanners[Registered Scanners]
    Scanners --> Findings[List of Findings]
    Findings --> Health[Health Engine]
    Findings --> AI[AI Engine]
    Health --> Reporter[Reporter Console/JSON/CSV/XML]
    AI --> Reporter
```

## Scanner Registry
All diagnostic scanners inherit from `IScanner` and are registered dynamically in `ScanCommand.run()`. Global scanners run once per scan target, while path-specific scanners evaluate matching repository files.
