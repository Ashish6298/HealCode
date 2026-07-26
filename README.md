# HealCode

HealCode is an AI-powered developer diagnostics CLI tool designed to identify, analyze, and diagnose codebase issues.

## Version
v0.9.0 (Phase 9 AI Intelligence & Smart Remediation)

## Features
- **AI Intelligence Engine**: Optional AI-powered root cause analysis, repair recommendations, and executive summaries (offline-first).
- **Code Static Analysis**: Computes cyclomatic complexity estimations, indentation depths, and performance loop bottlenecks.
- **Cloud & Kubernetes Intelligence**: Scans host cloud toolings (AWS, Azure, GCP CLI), Kubernetes contexts, and Terraform deployments.
- **Project Intelligence**: Discovers project structures, workspaces, manifests configuration, CI pipelines, and testing suites.
- **Runtime Intelligence**: Automatically detects Node.js, Python, Go, Rust, Java, Dart, and Flutter versions and installations.
- **Polished CLI Interface**: Interactive command router using `argparse` with CP1252/Unicode safety.
- **Diagnostics Scanning**: Optimized scanner engines that run global checks once.
- **SQLite Cache**: Speeds up consecutive scans utilizing target directory timestamp modifications.
- **Unified Reporting**: Renders findings to Console Tables, visual Health score gauges, and deep JSON reports.
- **Unified Reports Archiving**: Consolidates all phase logs directly inside the `reports/` folder.

## Installation

To install and run HealCode locally:

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e .[dev]
```

## Usage

```bash
# Print version
healcode version

# Initialize config
healcode config init

# Run scan
healcode scan
```

## Running Tests
To run tests and verify type checks:
```bash
pytest tests/
mypy healcode/
```
