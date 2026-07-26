"""
Tests for Weighted Health Scoring
"""

from healcode.core.health import HealthEngine

def test_health_scoring_calculations() -> None:
    engine = HealthEngine()
    
    # Empty findings should result in a 100% score
    empty_score = engine.calculate_score([])
    assert empty_score["overall"] == 100.0
    
    # Test deductions
    findings = [
        {"id": "SYS-MEM-HIGH", "severity": "WARN", "file": "system"},
        {"id": "SYS-NET-OFFLINE", "severity": "ERROR", "file": "network"}
    ]
    
    score = engine.calculate_score(findings)
    assert score["overall"] < 100.0
    
    # Check category deductions
    assert score["categories"]["HARDWARE"] == 90.0  # WARN deduction (-10)
    assert score["categories"]["NETWORK"] == 75.0   # ERROR deduction (-25)
