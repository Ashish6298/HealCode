"""
HealCode Reporting Base
"""

from typing import List, Dict, Any
from healcode.core.interfaces import IReporter

class BaseReporter(IReporter):
    def get_summary(self, findings: List[Dict[str, Any]]) -> Dict[str, int]:
        summary = {"TOTAL": len(findings), "ERROR": 0, "WARN": 0, "INFO": 0}
        for finding in findings:
            severity = finding.get("severity", "WARN").upper()
            if severity in summary:
                summary[severity] += 1
            else:
                summary[severity] = 1
        return summary
