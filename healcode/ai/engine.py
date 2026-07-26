"""
HealCode AI Intelligence Engine
Orchestrates root-cause analysis, correlation, recommendation, prioritization,
and executive summary generation on top of scanner findings.

This engine is entirely optional — the scanning pipeline is unaffected
when AI is disabled or no provider is configured.
"""

from typing import List, Dict, Any, Optional
from collections import defaultdict

from healcode.ai.provider import AIProvider, OfflineProvider, get_provider


class AIEngine:
    """Central orchestrator for all AI-powered analysis.

    Architecture::

        Scanner Engine → Findings → AIEngine
                                        ├── correlate()
                                        ├── root_cause()
                                        ├── recommend()
                                        ├── prioritize()
                                        └── summarize()
    """

    def __init__(self, provider: Optional[AIProvider] = None) -> None:
        self.provider: AIProvider = provider or get_provider("offline")

    # ------------------------------------------------------------------
    # Correlation Engine
    # ------------------------------------------------------------------

    def correlate(self, findings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group related findings by logical category."""

        groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        prefix_map: Dict[str, str] = {
            "SYS-": "System Issues",
            "PATH": "Environment Issues",
            "PORT": "Networking Issues",
            "RT-": "Runtime Issues",
            "COMPAT-": "Dependency Issues",
            "GIT-": "Git Issues",
            "ENV-": "Environment Issues",
            "SECRET-": "Security Issues",
            "FW-": "Framework Issues",
            "DOCKER-": "Docker Issues",
            "DOCKERFILE-": "Docker Issues",
            "COMPOSE-": "Docker Issues",
            "PROJ-": "Project Structure Issues",
            "CLOUD-": "Cloud / Kubernetes Issues",
            "CODE-": "Code Quality Issues",
        }

        for f in findings:
            fid = f.get("id", "")
            matched = False
            for prefix, group in prefix_map.items():
                if fid.startswith(prefix):
                    groups[group].append(f)
                    matched = True
                    break
            if not matched:
                groups["Other"].append(f)

        return dict(groups)

    # ------------------------------------------------------------------
    # Root Cause Analysis Engine
    # ------------------------------------------------------------------

    def root_cause(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Infer probable root causes from correlated findings."""

        groups = self.correlate(findings)
        causes: List[Dict[str, Any]] = []

        for group_name, group_findings in groups.items():
            if not group_findings:
                continue

            severities = [f.get("severity", "INFO").upper() for f in group_findings]
            has_critical = "CRITICAL" in severities or "ERROR" in severities
            count = len(group_findings)

            confidence = min(99, 50 + count * 5 + (20 if has_critical else 0))

            causes.append({
                "group": group_name,
                "finding_count": count,
                "has_critical": has_critical,
                "confidence": confidence,
                "summary": (
                    f"{group_name}: {count} finding(s) detected"
                    f"{' — includes critical issues' if has_critical else ''}."
                ),
            })

        causes.sort(key=lambda c: (-c["confidence"], -c["finding_count"]))
        return causes

    # ------------------------------------------------------------------
    # Recommendation Engine
    # ------------------------------------------------------------------

    def recommend(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable repair recommendations."""

        recs: List[Dict[str, Any]] = []

        for f in findings:
            fix = f.get("fix_suggested", "")
            if not fix:
                continue
            severity = f.get("severity", "INFO").upper()
            risk = "High" if severity in ("CRITICAL", "ERROR") else (
                "Medium" if severity in ("WARN", "WARNING") else "Low"
            )
            recs.append({
                "finding_id": f.get("id", ""),
                "file": f.get("file", ""),
                "description": fix,
                "risk": risk,
                "difficulty": "Easy" if risk == "Low" else "Moderate",
                "estimated_minutes": 5 if risk == "Low" else (15 if risk == "Medium" else 30),
            })

        recs.sort(key=lambda r: {"High": 0, "Medium": 1, "Low": 2}.get(r["risk"], 3))
        return recs

    # ------------------------------------------------------------------
    # Prioritization Engine
    # ------------------------------------------------------------------

    def prioritize(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank findings by impact and urgency."""

        priority_map = {
            "CRITICAL": "Critical",
            "ERROR": "High",
            "WARN": "Medium",
            "WARNING": "Medium",
            "INFO": "Low",
        }

        prioritized = []
        for f in findings:
            sev = f.get("severity", "INFO").upper()
            priority = priority_map.get(sev, "Informational")
            prioritized.append({
                **f,
                "priority": priority,
            })

        order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4}
        prioritized.sort(key=lambda p: order.get(p["priority"], 5))
        return prioritized

    # ------------------------------------------------------------------
    # Executive Summary Engine
    # ------------------------------------------------------------------

    def summarize(self, findings: List[Dict[str, Any]]) -> str:
        """Produce a human-friendly executive summary."""

        response = self.provider.generate(
            "Summarize the developer environment health.",
            {"findings": findings},
        )
        return response

    # ------------------------------------------------------------------
    # Full Analysis Pipeline
    # ------------------------------------------------------------------

    def analyse(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run the complete AI analysis pipeline and return enriched results."""

        return {
            "provider": self.provider.name,
            "correlation": self.correlate(findings),
            "root_causes": self.root_cause(findings),
            "recommendations": self.recommend(findings),
            "prioritized": self.prioritize(findings),
            "summary": self.summarize(findings),
        }
