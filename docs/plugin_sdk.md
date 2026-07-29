# Plugin SDK Guide

Third-party developers can write custom scanners for HealCode by adhering to the `IScanner` contract interface.

## Writing a Custom Scanner

Create a Python class inheriting from `IScanner`:

```python
from healcode.core.interfaces import IScanner
from healcode.config.models import ProjectConfig
from typing import List, Dict, Any

class CustomScanner(IScanner):
    @property
    def name(self) -> str:
        return "custom-scanner"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Performs checks against custom company rules."

    def initialize(self, config: ProjectConfig) -> None:
        pass

    def scan(self, target_path: str) -> List[Dict[str, Any]]:
        # custom checks logic
        return []
```
