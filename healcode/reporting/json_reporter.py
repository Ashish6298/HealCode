"""
HealCode JSON Reporter
"""

import json
from typing import List, Dict, Any
from healcode.reporting.base import BaseReporter

class JSONReporter(BaseReporter):
    def generate(self, findings: List[Dict[str, Any]], system_info: Dict[str, Any]) -> None:
        summary = self.get_summary(findings)
        
        # Pull out extra metadata passed in system_info
        scan_duration = system_info.pop("scan_duration_seconds", 0.0)
        health_score = system_info.pop("health_score", {"overall": 100.0, "categories": {}})
        
        report = {
            "version": "0.2.0",
            "timestamp": system_info.get("timestamp", ""),
            "scan_duration_seconds": scan_duration,
            "system_info": system_info,
            "health_score": health_score,
            "summary": summary,
            "findings": findings,
            "future_compatibility": {}
        }
        # Print pure JSON output directly to stdout for parsing
        print(json.dumps(report, indent=4))
