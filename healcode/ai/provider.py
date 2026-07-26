"""
HealCode AI Provider Abstraction
Defines the base interface for AI providers and a built-in offline heuristic provider.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class AIProvider(ABC):
    """Abstract base class for all AI providers.

    Implementations may connect to OpenAI, Anthropic, Gemini, Ollama,
    LM Studio, or any OpenAI-compatible endpoint.  The ``OfflineProvider``
    ships with HealCode and requires no external service.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name."""

    @abstractmethod
    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate an AI response for the given prompt and optional context.

        Args:
            prompt: The instruction / question.
            context: Additional structured data (e.g. findings list).

        Returns:
            A plain-text response string.
        """


class OfflineProvider(AIProvider):
    """Rule-based heuristic provider that runs entirely offline.

    This is the default provider when no cloud/local LLM is configured.
    It analyses findings deterministically without any network calls.
    """

    @property
    def name(self) -> str:
        return "offline-heuristic"

    def generate(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Return a deterministic heuristic response based on findings context."""

        findings: List[Dict[str, Any]] = []
        if context and "findings" in context:
            findings = context["findings"]

        severity_counts: Dict[str, int] = {}
        for f in findings:
            sev = f.get("severity", "INFO").upper()
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        total = len(findings)
        critical = severity_counts.get("CRITICAL", 0) + severity_counts.get("ERROR", 0)
        warnings = severity_counts.get("WARN", 0) + severity_counts.get("WARNING", 0)
        info = severity_counts.get("INFO", 0)

        lines = [
            f"HealCode Offline Analysis ({total} findings)",
            f"  Critical/Error: {critical}",
            f"  Warnings: {warnings}",
            f"  Informational: {info}",
        ]

        if critical > 0:
            lines.append(
                "  Recommendation: Address critical issues immediately — they may block builds or deployments."
            )
        elif warnings > 5:
            lines.append(
                "  Recommendation: Several warnings detected. Review configuration and environment hygiene."
            )
        else:
            lines.append(
                "  Recommendation: Environment is generally healthy. Review informational items at your convenience."
            )

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Provider registry — future providers register themselves here.
# ---------------------------------------------------------------------------

_PROVIDER_REGISTRY: Dict[str, type] = {
    "offline": OfflineProvider,
}


def get_provider(provider_name: str = "offline") -> AIProvider:
    """Instantiate and return a provider by name.

    Falls back to ``OfflineProvider`` for unknown names.
    """
    cls = _PROVIDER_REGISTRY.get(provider_name, OfflineProvider)
    return cls()


def register_provider(name: str, cls: type) -> None:
    """Register a custom AI provider class."""
    _PROVIDER_REGISTRY[name] = cls
