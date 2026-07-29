# HealCode 🛡️

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=for-the-badge)](https://github.com/Ashish6298/HealCode)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?style=for-the-badge)](https://github.com/Ashish6298/HealCode/actions)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey.svg?style=for-the-badge)](#)

> **HealCode** is an AI-powered developer diagnostics CLI platform designed to scan local development environments, containers, cloud contexts, project setups, and source code files to identify configuration drift, performance anti-patterns, and security smells.

---

## ⚡ Interactive CLI Dashboard Mockup

```ansi
[1;36mHEALCODE DIAGNOSTICS ENGINE v1.0.0[0m
[1;35m====================================[0m

[1;32m[✓] System diagnostics healthy[0m
[1;32m[✓] Docker daemon running[0m
[1;33m[!] Kubernetes context using default namespace instead of dev-active[0m
[1;31m[✗] Found 1 exposed API Key in config/settings.py:L14[0m

[1;36mOVERALL ENVIRONMENT HEALTH:[0m [[1;32m######################----[0m] [1;32m88.5%[0m
```

---

## 🚀 Key Features

- 🧠 **AI-Powered Diagnostics**: Optional AI orchestration layer delivering root-cause grouping, prioritization scoring, and repair recommendations with zero cloud dependencies.
- 📦 **Docker & Compose Auditing**: Checks engine version info, Context configurations, Dockerfile security practices, and docker-compose restart structures.
- ☁️ **Cloud & Kubernetes Contexts**: Scans local AWS, GCP, and Azure CLI setups, evaluates kubeconfig context validity, and identifies local Terraform variables.
- ⚙️ **Runtime & Compiler Intelligence**: Detects Node.js, Python, Java, Go, Rust, and Flutter toolchains, matching compiler versions against manifest constraints.
- 🔍 **Universal Static Code Analysis**: Computes cyclomatic complexity, nesting depths, and nested loop performance bottlenecks across languages.
- 📈 **Weighted Health Scoring**: Rates codebase health across 40+ granular categories.
- 🗃️ **Baseline & Drift Detection**: Captures environmental snapshots to track regressions, improvements, and environment modifications over time.
- ⏱️ **Watch Mode**: Real-time directory polling for fast incremental rescans.

---

## 📦 Installation

```bash
pip install healcode
```

*Requires Python >= 3.11*

---

## ⚡ Quick Start

### 1. Initialize configuration
```bash
healcode config init
```

### 2. Run diagnostics scan
```bash
healcode scan
```

### 3. Generate baseline report
```bash
healcode baseline create initial_state
```

### 4. Run AI Intelligence summary (offline-first)
```bash
healcode ai --offline
```

---

## 🛠️ Commands Reference

| Command | Action | Description |
|---------|--------|-------------|
| `scan` | `healcode scan [target]` | Runs active diagnostics checks and displays system health. |
| `config` | `healcode config init` | Initializes project configuration file `healcode.json`. |
| `profile` | `healcode profile set [name]` | Adjusts active scanning profile (DevOps, Security, Minimal). |
| `baseline` | `healcode baseline compare [name]` | Analyzes current project state against a captured baseline. |
| `watch` | `healcode watch` | Starts the directory file watcher for real-time rescanning. |
| `marketplace`| `healcode marketplace search [q]` | Searches community plugin marketplace (mock interface). |
| `ai` | `healcode ai --offline` | Orchestrates root-cause diagnostics and recommendations. |

---

## 📁 Documentation Hub

For detailed guides, explore our complete [docs/](docs/) ecosystem:
- 📖 [Getting Started Guide](docs/getting_started.md)
- 💾 [Installation Guide](docs/installation.md)
- ⚙️ [Configuration Reference](docs/configuration.md)
- 📐 [Architecture Details](docs/architecture.md)
- 🔌 [Plugin SDK Reference](docs/plugin_sdk.md)
- ⌨️ [CLI Reference Manual](docs/cli_reference.md)
- 🛠️ [Troubleshooting Guide](docs/troubleshooting.md)

---

## 🤝 Contributing

We welcome community contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 📄 License

This project is licensed under the [MIT License](LICENSE).
