"""
HealCode Scan Profiles Definition
"""

from typing import Dict, List, Optional

PROFILES: Dict[str, Optional[List[str]]] = {
    "Minimal": ["default-scanner", "system-scanner"],
    "DevOps": ["default-scanner", "system-scanner", "docker-scanner", "dockerfile-scanner", "compose-scanner", "git-scanner", "cloud-scanner"],
    "Security": ["default-scanner", "system-scanner", "secret-scanner", "git-scanner", "dockerfile-scanner"],
    "Cloud": ["default-scanner", "system-scanner", "cloud-scanner", "docker-scanner", "compose-scanner"],
    "Full": None,
    "Backend": ["default-scanner", "system-scanner", "runtime-scanner", "compatibility-scanner", "port-scanner", "env-scanner"],
    "Frontend": ["default-scanner", "system-scanner", "runtime-scanner", "compatibility-scanner", "port-scanner", "env-scanner"],
    "AI/ML": ["default-scanner", "system-scanner", "runtime-scanner", "code-scanner"],
    "Enterprise": None,
    "Custom": None
}
