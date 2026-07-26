"""
Tests for AI Intelligence Engine, Provider Abstraction, and Privacy Masking.
"""

from healcode.ai.provider import OfflineProvider, get_provider
from healcode.ai.privacy import mask_secrets
from healcode.ai.engine import AIEngine


def test_offline_provider_generates_summary() -> None:
    """OfflineProvider should return a deterministic heuristic summary."""
    provider = OfflineProvider()
    findings = [
        {"id": "SYS-DISK-LOW", "severity": "WARN", "message": "Low disk space"},
        {"id": "SECRET-EXPOSED", "severity": "ERROR", "message": "Exposed API key"},
        {"id": "RT-NODE-MISSING", "severity": "INFO", "message": "Node not found"},
    ]
    result = provider.generate("summarize", {"findings": findings})
    assert "3 findings" in result
    assert "Critical/Error: 1" in result


def test_privacy_masker_scrubs_secrets() -> None:
    """Privacy masker should replace secrets with ********."""
    text = "api_key=sk-abc123 password=hunter2 bearer tok3n"
    masked = mask_secrets(text)
    assert "sk-abc123" not in masked
    assert "hunter2" not in masked
    assert "********" in masked


def test_ai_engine_full_pipeline() -> None:
    """AIEngine.analyse() should return all expected keys."""
    engine = AIEngine()
    findings = [
        {"id": "DOCKER-DAEMON-OFF", "severity": "ERROR", "message": "Docker daemon not running",
         "scanner": "docker-scanner", "file": "", "line": 0, "fix_suggested": "Start Docker Desktop."},
        {"id": "COMPOSE-NO-RESTART", "severity": "WARN", "message": "Missing restart policy",
         "scanner": "compose-scanner", "file": "docker-compose.yml", "line": 3,
         "fix_suggested": "Add restart: unless-stopped."},
    ]
    result = engine.analyse(findings)

    # Check structure
    assert "provider" in result
    assert result["provider"] == "offline-heuristic"
    assert "correlation" in result
    assert "root_causes" in result
    assert "recommendations" in result
    assert "prioritized" in result
    assert "summary" in result

    # Root causes should group Docker findings
    groups = [c["group"] for c in result["root_causes"]]
    assert "Docker Issues" in groups

    # Recommendations should include the fix suggestions
    rec_ids = [r["finding_id"] for r in result["recommendations"]]
    assert "DOCKER-DAEMON-OFF" in rec_ids
    assert "COMPOSE-NO-RESTART" in rec_ids


def test_get_provider_fallback() -> None:
    """Unknown provider names should fall back to OfflineProvider."""
    provider = get_provider("nonexistent-provider")
    assert provider.name == "offline-heuristic"
