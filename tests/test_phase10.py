"""
Tests for Phase 10 Production Readiness (Profiles, Baseline comparisons, Watch mode, and Marketplace)
"""

import os
import json
import tempfile
import argparse
from healcode.cli.commands.profile import ProfileCommand
from healcode.cli.commands.baseline import BaselineCommand
from healcode.cli.commands.marketplace import MarketplaceCommand
from healcode.config.models import ProjectConfig
from healcode.core.profiles import PROFILES

def test_profile_listing_and_set() -> None:
    config = ProjectConfig()
    cmd = ProfileCommand()
    
    # Assert profiles definition matches expectation
    assert "DevOps" in PROFILES
    assert "Security" in PROFILES
    assert "Minimal" in PROFILES

    parser = argparse.ArgumentParser()
    cmd.setup_parser(parser)
    
    args = parser.parse_args(["list"])
    rc = cmd.run(args, config)
    assert rc == 0

    args = parser.parse_args(["set", "DevOps"])
    rc = cmd.run(args, config)
    assert rc == 0
    assert config.scan.profile == "DevOps"


def test_baseline_capture_and_drift(tmp_path) -> None:
    config = ProjectConfig()
    cmd = BaselineCommand()
    
    # Change working directory so it records baseline correctly
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        parser = argparse.ArgumentParser()
        cmd.setup_parser(parser)
        
        # Create baseline
        args = parser.parse_args(["create", "base_test"])
        rc = cmd.run(args, config)
        assert rc == 0
        
        baseline_file = os.path.join(".healcode_baselines", "base_test.json")
        assert os.path.exists(baseline_file)
        
        with open(baseline_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["name"] == "base_test"
            assert "score" in data
            
        # Compare baseline
        args = parser.parse_args(["compare", "base_test"])
        rc = cmd.run(args, config)
        assert rc == 0
    finally:
        os.chdir(original_cwd)


def test_marketplace_mock_searches() -> None:
    config = ProjectConfig()
    cmd = MarketplaceCommand()
    
    parser = argparse.ArgumentParser()
    cmd.setup_parser(parser)
    
    # Search command
    args = parser.parse_args(["search", "security"])
    rc = cmd.run(args, config)
    assert rc == 0
    
    # Install command
    args = parser.parse_args(["install", "security-hardening-pack"])
    rc = cmd.run(args, config)
    assert rc == 0
