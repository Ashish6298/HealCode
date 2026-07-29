"""
HealCode CSV Reporter
"""

import csv
import io
from typing import List, Dict, Any
from healcode.reporting.base import BaseReporter

class CSVReporter(BaseReporter):
    def generate(self, findings: List[Dict[str, Any]], system_info: Dict[str, Any]) -> None:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow(["id", "scanner", "file", "line", "severity", "message", "fix_suggested"])
        
        for f in findings:
            writer.writerow([
                f.get("id", ""),
                f.get("scanner", ""),
                f.get("file", ""),
                f.get("line", 0),
                f.get("severity", ""),
                f.get("message", ""),
                f.get("fix_suggested", "")
            ])
            
        print(output.getvalue())
