# Getting Started with HealCode

Welcome to HealCode! This guide will help you install and run your first diagnostics scan.

## Quick Start in 3 Steps

### 1. Installation
Install HealCode using `pip`:
```bash
pip install healcode
```

### 2. Initialization
Create a new configuration file in your project directory:
```bash
healcode config init
```
This generates a `healcode.json` file in the current directory.

### 3. Run a Scan
Start the diagnostic scan:
```bash
healcode scan
```
HealCode will execute active scanners (such as system diagnostics, runtime dependencies check, Docker contexts, project configs) and print a consolidated health score report.
