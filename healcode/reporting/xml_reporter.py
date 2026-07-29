"""
HealCode XML Reporter
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from healcode.reporting.base import BaseReporter

class XMLReporter(BaseReporter):
    def generate(self, findings: List[Dict[str, Any]], system_info: Dict[str, Any]) -> None:
        root = ET.Element("healcode-report")
        
        sys_elem = ET.SubElement(root, "system-info")
        for k, v in system_info.items():
            if isinstance(v, (str, int, float, bool)):
                elem = ET.SubElement(sys_elem, k)
                elem.text = str(v)

        findings_elem = ET.SubElement(root, "findings")
        for f in findings:
            find_elem = ET.SubElement(findings_elem, "finding")
            for k, v in f.items():
                elem = ET.SubElement(find_elem, k)
                elem.text = str(v)

        # Print XML
        print(ET.tostring(root, encoding="utf-8").decode("utf-8"))
