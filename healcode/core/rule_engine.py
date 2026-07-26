"""
HealCode Rule Engine Foundation
Supports isolated rules, platform eligibility, and custom thresholds.
"""

import sys
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class Rule(ABC):
    def __init__(self, id: str, description: str, severity: str = "WARN", platforms: Optional[List[str]] = None) -> None:
        self.id = id
        self.description = description
        self.severity = severity
        self.platforms = platforms  # If set, list of compatible platforms (e.g. ['win32', 'linux'])

    def is_eligible(self) -> bool:
        if self.platforms is None:
            return True
        return sys.platform in self.platforms

    @abstractmethod
    def evaluate(self, data: Dict[str, Any]) -> bool:
        """Returns True if the rule is violated/triggered."""
        pass


class RuleEngine:
    def __init__(self) -> None:
        self.rules: List[Rule] = []

    def register_rule(self, rule: Rule) -> None:
        self.rules.append(rule)

    def evaluate_all(self, target_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        for rule in self.rules:
            if not rule.is_eligible():
                continue
            try:
                if rule.evaluate(target_data):
                    findings.append({
                        "id": rule.id,
                        "scanner": "rule-engine",
                        "file": target_data.get("file", "unknown"),
                        "line": target_data.get("line", 0),
                        "severity": rule.severity,
                        "message": f"Rule {rule.id} triggered: {rule.description}",
                        "fix_suggested": "Review the rule violations and remediate."
                    })
            except Exception:
                pass
        return findings
