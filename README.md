#  HealCode • A Diagnostics Engine That Catches What `git status` Can't.

<br>

<table align="center">
<tr>
<td align="center">

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=for-the-badge)](https://github.com/Ashish6298/HealCode) [![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE) [![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?style=for-the-badge)](https://github.com/Ashish6298/HealCode/actions)

[![Stars](https://img.shields.io/github/stars/Ashish6298/HealCode.svg?style=for-the-badge&color=yellow)](https://github.com/Ashish6298/HealCode/stargazers) [![Downloads](https://img.shields.io/pypi/dm/healcode.svg?style=for-the-badge&color=orange)](https://pypi.org/project/healcode/)

[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey.svg?style=for-the-badge)](#)

</div>
</td>
</tr>
</table>

<br>

## 📚 Table of Contents

<br>

<div align="center">

<table width="100%">
<tr>
<td valign="top" width="50%">

### 🌟 Getting to Know HealCode
- [Overview](#overview)
- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Who Is HealCode For?](#-who-is-healcode-for)
- [HealCode vs. Doing It Manually](#️-healcode-vs-doing-it-manually)
- [How a Scan Works](#️-how-a-scan-works)
- [See It In Action](#-see-it-in-action)

### 🚀 Using HealCode
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Sample Configuration](#-sample-configuration)

</td>
<td valign="top" width="50%">

### 🛠️ Reference
- [Commands Reference](#️-commands-reference)
- [Exit Codes](#-exit-codes)
- [Understanding Your Health Score](#-understanding-your-health-score)
- [CI/CD Integration](#-cicd-integration)
- [Documentation Hub](#-documentation-hub)

### 🤝 Community & Project
- [Roadmap](#️-whats-done--whats-coming)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [Support / Get Help](#-support--get-help)
- [License](#-license)

</td>
</tr>
</table>

</div>

<br>

## Overview

**HealCode** is an AI-powered developer diagnostics CLI platform designed to scan local development environments, containers, cloud contexts, project setups, and source code files to identify configuration drift, performance anti-patterns, and security smells.

Instead of juggling separate tools for Docker linting, Kubernetes context checks, dependency auditing, and static analysis, HealCode runs a single `scan` across all of them and rolls the results into one weighted health score — so you always know exactly where your project stands.

<br>

<div align="center">


|                      |                                                          |
| -------------------- | -------------------------------------------------------- |
| **Scans**            | Local env, Docker/Compose, Kubernetes, cloud CLIs, source code |
| **Languages covered**| Node.js, Python, Java, Go, Rust, Flutter                 |
| **Scoring**          | Weighted health score across 40+ categories              |
| **AI layer**         | Optional, offline-first — zero cloud dependency required |
| **Install**          | `pip install healcode`                                   |
| **Requires**         | Python ≥ 3.11                                             |

</table>

</div>

<br>

## ⚠️ The Problem

Most projects don't break because of one big, obvious bug. They break because of small things nobody noticed in time.

A password or secret key accidentally gets saved into a file that shouldn't have it. A cloud setting quietly points to the wrong place. A container is missing a setting that would've restarted it if it crashed. A piece of code slowly gets more complicated over time until nobody wants to touch it anymore. None of these show up when you check `git status` — they show up later, as a bug, a security scare, or a late-night emergency fix.

| ❌ Without HealCode |
|---|
| 🔑 Secret keys or passwords accidentally get saved into your code |
| 🐳 Container settings are wrong, but nobody notices until something crashes |
| ☸️ Cloud/Kubernetes settings quietly point to the wrong environment |
| 🧮 Code slowly becomes messy and hard to understand, without anyone realizing |
| 🧰 Your tools (Python, Node.js, etc.) get out of sync with what the project actually needs |
| 📉 There's no record of what changed in your setup over time, or when |

>There are separate tools that can catch each of these problems on their own — but most developers don't have the time to set up and run five different tools, on every project, every time.

<br>

## 💡 The Solution

HealCode checks all of this for you — your computer, your containers, your cloud settings, your code — with one simple command: `healcode scan`. Instead of five different tools giving you five different reports, you get one clear health score for your whole project.

| ✅ What HealCode Does Differently |
|---|
| 🔍 **One command checks everything** — your system, containers, cloud setup, tools, and code, all at once |
| 📈 **One easy score** — instead of piecing together results from five different tools |
| 🗃️ **Remembers what changed** — compare today's check against last week's to see exactly what's different |
| 🧠 **Smart help, without needing the internet** — an optional AI feature that groups problems together and tells you what to fix first, fully offline |
| ⏱️ **Keeps checking as you work** — turn on watch mode and it rechecks automatically while you code |

> HealCode isn't trying to replace your linter or your secret scanner — it brings together what all of those tools would tell you, in one place, and also tracks what's changed since your last check — something none of them do on their own.

<br>

## 🎯 Who Is HealCode For?

| Who | Why it helps them |
|---|---|
| 👨‍💻 **Solo developers** | Catch mistakes and exposed passwords before you share your code — without setting up five separate tools yourself. |
| 🧑‍🤝‍🧑 **Small teams** | Everyone uses the same settings file, so the whole team's projects get checked the same way. |
| 🏢 **DevOps / Infrastructure folks** | Use the `DevOps` profile to focus on containers, cloud setup, and configuration drift specifically. |
| 🔐 **Security-minded teams** | Use the `Security` profile to prioritize exposed secrets and risky settings first. |
| 🎓 **Students & beginners** | See, in one simple report, what a "healthy" project setup actually looks like — a great way to learn good habits early. |

<br>

## ⚖️ HealCode vs. Doing It Manually

You *could* piece together the same coverage using several separate tools — but here's what that actually looks like side by side.

| What you need to check | Doing it manually | With HealCode |
|---|---|---|
| 🔑 Exposed secrets in code | Set up a separate secret-scanning tool | Included in `healcode scan` |
| 🐳 Docker/Compose misconfigurations | Read through Dockerfiles and compose files by hand | Included in `healcode scan` |
| ☸️ Kubernetes context drift | Manually check `kubectl config` before every deploy | Included in `healcode scan` |
| 🧰 Toolchain version mismatches | Cross-check manifests against installed versions yourself | Included in `healcode scan` |
| 🧮 Code complexity issues | Run a separate static analysis tool per language | Included in `healcode scan` |
| 📊 One overall health picture | Manually combine results from every tool above | One weighted score, automatically |
| 🗃️ Tracking what changed over time | No built-in way — you'd have to remember or log it yourself | `healcode baseline` tracks it for you |
| ⏱️ Continuous checking while coding | Re-run each tool manually, every time | `healcode watch` does it automatically |

> The individual checks above already exist as separate tools. What HealCode adds is running them together, scoring them together, and remembering what changed — so you're not stitching five reports into one picture yourself.

<br>

## 🏗️ How a Scan Works

When you run `healcode scan`, here's what happens behind the scenes — all in one go:

```
                healcode scan
                      │
                      ▼
        ┌─────────────────────────┐
        │   Runs all the checks   │
        └─────────────────────────┘
                      │
   ┌───────────┬──────┼───────┬────────────┐
   ▼            ▼             ▼             ▼
Your          Containers   Cloud &      Your Tools
Computer      (Docker)     Cloud Setup  (Python, Node.js, etc.)
                                              │
                                              ▼
                                        Your Code
                                     (looks for messy
                                      or risky code)
   │            │             │             │
   └────────────┴──────┬──────┴─────────────┘
                        ▼
              ┌───────────────────┐
              │   Adds it all up  │
              │  into one score   │
              └───────────────────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
      Health Report          Saves a record
     (what passed,           (so you can compare
      what needs             it to next time)
      attention)
                        │
                        ▼
              Optional: AI groups the
              problems and tells you
                what to fix first
```

> 💡 Want the deeper technical breakdown? See [Architecture](docs/architecture.md) in the docs hub.

<br>




## ⚡ See It In Action

Run `healcode scan` and get a full environment health report in seconds — no config required.

```ansi
[1;36mHEALCODE DIAGNOSTICS ENGINE v1.0.0[0m
[1;35m════════════════════════════════════════════════════[0m

[1;34m▸ SYSTEM[0m
[1;32m  [✓] OS & shell environment healthy[0m
[1;32m  [✓] Disk space sufficient (62% free)[0m

[1;34m▸ CONTAINERS[0m
[1;32m  [✓] Docker daemon running (v24.0.7)[0m
[1;33m  [!] docker-compose.yml missing restart policy on 'api' service[0m

[1;34m▸ CLOUD & KUBERNETES[0m
[1;33m  [!] Kubernetes context using default namespace instead of dev-active[0m
[1;32m  [✓] AWS CLI credentials valid[0m

[1;34m▸ RUNTIME & TOOLCHAINS[0m
[1;32m  [✓] Node.js v20.11.0 matches package.json engine constraint[0m
[1;31m  [✗] Python 3.9 installed — pyproject.toml requires >=3.11[0m

[1;34m▸ STATIC CODE ANALYSIS[0m
[1;33m  [!] High cyclomatic complexity in utils/parser.py (score: 24)[0m
[1;31m  [✗] Found 1 exposed API key in config/settings.py:L14[0m

[1;35m════════════════════════════════════════════════════[0m
[1;36mOVERALL ENVIRONMENT HEALTH:[0m [[1;32m######################----[0m] [1;32m88.5%[0m
[1;32m3 passed[0m  ·  [1;33m2 warnings[0m  ·  [1;31m2 critical[0m
```

| Symbol | Meaning |
|:---:|---|
| ✅ | Passed — no action needed |
| ⚠️ | Warning — worth reviewing |
| ❌ | Critical — should be fixed before shipping |

<br>

## 🚀 Key Features

- 🧠 **AI-Powered Diagnostics**: Optional AI orchestration layer delivering root-cause grouping, prioritization scoring, and repair recommendations with zero cloud dependencies.

- 📦 **Docker & Compose Auditing**: Checks engine version info, Context configurations, Dockerfile security practices, and docker-compose restart structures.

- ☁️ **Cloud & Kubernetes Contexts**: Scans local AWS, GCP, and Azure CLI setups, evaluates kubeconfig context validity, and identifies local Terraform variables.

- ⚙️ **Runtime & Compiler Intelligence**: Detects Node.js, Python, Java, Go, Rust, and Flutter toolchains, matching compiler versions against manifest constraints.

- 🔍 **Universal Static Code Analysis**: Computes cyclomatic complexity, nesting depths, and nested loop performance bottlenecks across languages.

- 📈 **Weighted Health Scoring**: Rates codebase health across 40+ granular categories.

- 🗃️ **Baseline & Drift Detection**: Captures environmental snapshots to track regressions, improvements, and environment modifications over time.
- ⏱️ **Watch Mode**: Real-time directory polling for fast incremental rescans.

<br>

## 📦 Installation

```bash
pip install healcode
```

### Requirements

| Dependency | Version | Purpose |
|---|---|---|
| **Python** | ≥ 3.11 | Runtime |

### Verify the install

```bash
healcode --version
```

<br>

## ⚡ Quick Start

Four commands take you from a fresh install to a full environment health report with a tracked baseline.

### 1️⃣ Initialize configuration

Creates a `healcode.json` config file in your project root, so scans are tuned to your setup from the start.

```bash
healcode config init
```

### 2️⃣ Run a diagnostics scan

Scans your local environment, containers, cloud/K8s contexts, toolchains, and source code — then prints a weighted health score.

```bash
healcode scan
```

### 3️⃣ Generate a baseline report

Snapshots the current project state so future scans can be compared against it to catch drift.

```bash
healcode baseline create initial_state
```

### 4️⃣ Run an AI intelligence summary (offline-first)

Groups findings by root cause and prioritizes what to fix first — no cloud dependency required.

```bash
healcode ai --offline
```

> 💡 **Tip:** Run `healcode scan` regularly (or use [`watch` mode](#-key-features)) and re-run `healcode baseline compare initial_state` to catch regressions before they reach code review.

<br>

## 📝 Sample Configuration

Running `healcode config init` creates a `healcode.json` file in your project. Here's what a typical one looks like:

```json
{
  "profile": "DevOps",
  "targets": ["."],
  "checks": {
    "system": true,
    "docker": true,
    "kubernetes": true,
    "cloud": true,
    "toolchains": true,
    "static_analysis": true
  },
  "exclude": [
    "node_modules",
    "dist",
    ".venv"
  ],
  "ai": {
    "enabled": true,
    "offline": true
  }
}
```

| Field | What it controls |
|---|---|
| `profile` | Which scanning profile is active (`DevOps`, `Security`, or `Minimal`) |
| `targets` | Which directories to scan — defaults to the current project |
| `checks` | Turn individual check categories on or off |
| `exclude` | Folders to skip during scanning |
| `ai.enabled` / `ai.offline` | Whether the AI layer runs, and whether it stays fully offline |

> 💡 See the full [Configuration Reference](docs/configuration.md) for every available option.

<br>



## 🛠️ Commands Reference

### Core Diagnostics

| Command | Usage | Description |
|---|---|---|
| `scan` | `healcode scan [target]` | Runs active diagnostics checks and displays system health. |
| `baseline` | `healcode baseline create [name]` / `healcode baseline compare [name]` | Captures a project snapshot or analyzes current state against one. |
| `watch` | `healcode watch` | Starts the directory file watcher for real-time, incremental rescanning. |

### Configuration

| Command | Usage | Description |
|---|---|---|
| `config` | `healcode config init` | Initializes the project configuration file `healcode.json`. |
| `profile` | `healcode profile set [name]` | Adjusts the active scanning profile (`DevOps`, `Security`, `Minimal`). |

### Intelligence & Extensions

| Command | Usage | Description |
|---|---|---|
| `ai` | `healcode ai --offline` | Orchestrates root-cause diagnostics and repair recommendations. |
| `marketplace` | `healcode marketplace search [q]` | Searches the community plugin marketplace *(mock interface — not yet live)*. |

> 💡 Run `healcode <command> --help` for full flag details on any command.

<br>


## 📊 Understanding Your Health Score

Every `healcode scan` ends with one number — your overall environment health percentage. Here's how to read it.

### How the score is built

Each check HealCode runs (system, containers, cloud/K8s, toolchains, code) contributes to one of 40+ categories. Categories aren't weighted equally — a critical finding (like an exposed secret) pulls the score down more than a minor warning (like a missing restart policy).

Score = 100% − (weighted penalty for every warning and critical finding)

### Reading the result

| Score Range | What it means |
|---|---|
| 🟢 **90–100%** | Healthy — no urgent action needed |
| 🟡 **70–89%** | Some warnings — worth reviewing before your next release |
| 🟠 **50–69%** | Multiple issues — recommend addressing before shipping |
| 🔴 **Below 50%** | Critical issues present — fix before continuing |

### What pulls your score down

| Severity | Example | Impact |
|---|---|---|
| ✅ Passed | Docker daemon running correctly | No penalty |
| ⚠️ Warning | Kubernetes context using default namespace | Small penalty |
| ❌ Critical | Exposed API key in source code | Large penalty |

> 💡 Run `healcode baseline compare [name]` to see whether your score has improved, stayed flat, or regressed since your last check.

<br>



## 📁 Documentation Hub

Full guides live in the [`docs/`](docs/) folder. Here's what each one covers and when to reach for it:

### 📖 [Getting Started](docs/getting_started.md)
Your first ten minutes with HealCode — installing, initializing config, running your first `scan`, and reading the health score output. Start here if you've never used HealCode before.

### 💾 [Installation](docs/installation.md)
Platform-specific setup notes for Windows, Linux, and macOS, including Python version requirements and common install issues (permissions, PATH conflicts, virtualenv setup).

### ⚙️ [Configuration Reference](docs/configuration.md)
Every option available in `healcode.json` — scanning profiles (`DevOps`, `Security`, `Minimal`), which checks to include/exclude, and how to scope scans to specific directories or targets.

### 📐 [Architecture](docs/architecture.md)
How a scan actually works under the hood: the check pipeline, how findings are scored and weighted into the overall percentage, and how the optional AI layer processes results offline.

### ⌨️ [CLI Reference](docs/cli_reference.md)
The complete command list with every flag and subcommand — the canonical reference for `scan`, `config`, `profile`, `baseline`, `watch`, and `ai`.

### 🔌 [Plugin SDK](docs/plugin_sdk.md)
How to write custom checks and package them as plugins, plus how the (currently mock) marketplace is intended to distribute them.

### 🛠️ [Troubleshooting](docs/troubleshooting.md)
Fixes for common errors — failed scans, misdetected toolchains, kubeconfig issues, and Docker daemon connectivity problems.

<br>

## 🗺️ What's Done & What's Coming

> ⚠️ This is a placeholder — swap these in for your actual milestones from `ROADMAP.md`.

| Status | What |
|---|---|
| ✅ Done | Core checks — scan your computer, containers, and cloud setup |
| ✅ Done | Save a "before" snapshot and compare it to later scans |
| ✅ Done | Optional AI helper that works without internet |
| 🔜 Coming | A real plugin marketplace (right now it's just a demo) |
| 🔜 Coming | Support for more programming languages and tools |
| 🔜 Coming | A guide for using HealCode in GitHub Actions / GitLab CI |

<br>

## ❓ FAQ

<br>

<div align="center">

*Quick answers to what people usually ask before (and after) installing HealCode.*

</div>

<br>

### 🧠 About HealCode

<details>
<summary><b>Does HealCode replace my existing linter or secret scanner?</b></summary>
<br>

No. HealCode doesn't try to out-lint your linter or out-scan your secret scanner. It brings together what those tools would already tell you into **one report**, adds cross-cutting checks (containers, cloud/K8s, toolchains), and tracks what's changed since your last scan — something standalone tools don't do on their own.

</details>

<br>

<details>
<summary><b>Which languages does HealCode support for static analysis?</b></summary>
<br>

`Node.js` · `Python` · `Java` · `Go` · `Rust` · `Flutter`

More languages are on the [roadmap](#️-whats-done--whats-coming).

</details>

<br>

<details>
<summary><b>What's the difference between the DevOps, Security, and Minimal profiles?</b></summary>
<br>

| Profile | Prioritizes |
|---|---|
| 🏗️ `DevOps` | Containers, cloud setup, configuration drift |
| 🔐 `Security` | Exposed secrets, risky settings |
| ⚡ `Minimal` | A lighter, faster subset of checks |

Set one with:
```bash
healcode profile set [name]
```

</details>

---

### 🔒 Privacy & Requirements

<details>
<summary><b>Do I need an internet connection to use HealCode?</b></summary>
<br>

No. Core scanning (`healcode scan`) runs **entirely locally**. The AI layer is offline-first too — `healcode ai --offline` works with zero cloud dependency.

</details>

<br>

<details>
<summary><b>Will HealCode send my code or secrets anywhere?</b></summary>
<br>

No. Scans run locally against your filesystem, Docker context, cloud CLI config, and kubeconfig. Nothing is uploaded unless you explicitly configure an integration to do so.

</details>

<br>

<details>
<summary><b>What Python version do I need?</b></summary>
<br>

`Python ≥ 3.11` to run HealCode itself. Your *project's* toolchain can be anything — HealCode flags a mismatch (e.g. a project requiring 3.11 while 3.9 is installed) rather than requiring it.

</details>

---

### ⚙️ Using HealCode

<details>
<summary><b>How is the health score calculated?</b></summary>
<br>

Score starts at **100%** and subtracts a weighted penalty per finding:

| Severity | Penalty |
|---|---|
| ✅ Passed | None |
| ⚠️ Warning | Small |
| ❌ Critical | Large |

See [Understanding Your Health Score](#-understanding-your-health-score) for the full breakdown.

</details>

<br>

<details>
<summary><b>Can I run HealCode in CI/CD?</b></summary>
<br>

Yes — see [CI/CD Integration](#-cicd-integration) for pipeline examples and exit code behavior.

</details>

<br>

<details>
<summary><b>Is the plugin marketplace live yet?</b></summary>
<br>

🔜 Not yet — `healcode marketplace search` is currently a mock interface. Real plugin distribution is on the [roadmap](#️-whats-done--whats-coming).

</details>

---

### 🆘 Something Went Wrong

<details>
<summary><b>I found a security vulnerability — where do I report it?</b></summary>
<br>

⚠️ Please **don't** open a public issue. See [`SECURITY.md`](SECURITY.md) for responsible disclosure instructions.

</details>

<br>

> 💡 Don't see your question here? Check the [Documentation Hub](#-documentation-hub) or open a [discussion/issue](https://github.com/Ashish6298/HealCode/issues).

<br>


## 🤝 Contributing

HealCode is early-stage and community contributions are very welcome — whether that's a bug fix, a new check, better docs, or just filing an issue about something confusing.

### 🚀 Quick Start for Contributors

**1. Clone the repository**

```bash
git clone https://github.com/Ashish6298/HealCode.git
```

**2. Enter the project directory**

```bash
cd HealCode
```

**3. Install in editable mode with dev dependencies**

```bash
pip install -e .[dev]
```

### ✅ Before Opening a Pull Request

- Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines and PR process
- Follow the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) in all interactions
- Check [existing issues](https://github.com/Ashish6298/HealCode/issues) before starting new work, to avoid duplicate effort
- Add or update tests in [`tests/`](tests/) for any behavior change

Found a security issue instead? Please don't open a public issue — see [`SECURITY.md`](SECURITY.md) for responsible disclosure.

<br>

## 🆘 Support / Get Help

<br>

<div align="center">

*Stuck on something? Here's the fastest way to get unstuck, depending on what you need.*

</div>

<br>

<table width="100%">
<tr>
<td width="50%" valign="top">

### 🐛 Found a Bug?

Search [existing issues](https://github.com/Ashish6298/HealCode/issues) first — someone may have already hit it.

If it's new, [open an issue](https://github.com/Ashish6298/HealCode/issues/new) with:
- Your OS & Python version
- The command you ran
- Expected vs. actual behavior
- Relevant log output, if any

</td>
<td width="50%" valign="top">

### 💡 Have a Feature Idea?

[Open a feature request](https://github.com/Ashish6298/HealCode/issues/new) — describe the problem you're trying to solve, not just the solution. It helps us design it right.

Check the [Roadmap](#️-whats-done--whats-coming) first to see if it's already planned.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ❓ Have a Question?

Start with the [FAQ](#-faq) and [Documentation Hub](#-documentation-hub) — most "how do I…" questions are already answered there.

Still stuck? Open a [GitHub Discussion](https://github.com/Ashish6298/HealCode/discussions) (or an issue, if discussions aren't enabled yet).

</td>
<td width="50%" valign="top">

### 🔐 Found a Security Issue?

**Please don't open a public issue.** Follow the responsible disclosure process in [`SECURITY.md`](SECURITY.md) instead — we'll get back to you privately.

</td>
</tr>
</table>

<br>

### 📋 Before You Ask

A quick checklist that resolves most support requests before they're even filed:

| ✅ Check | Why |
|---|---|
| Run `healcode --version` | Confirms you're on the latest release |
| Run `healcode config init` | Rules out a missing/stale config file |
| Check [`docs/troubleshooting.md`](docs/troubleshooting.md) | Covers common scan, kubeconfig, and Docker connectivity errors |
| Search [closed issues](https://github.com/Ashish6298/HealCode/issues?q=is%3Aissue+is%3Aclosed) | Your issue may already be fixed on `main` |

<br>

> 💬 **Response times:** HealCode is community-maintained, so replies aren't instant — but every issue and discussion gets read. Clear, reproducible reports get resolved fastest.

<br>



## 📄 License

HealCode is released under the **MIT License** — free to use, modify, and distribute, including in commercial projects, as long as the original copyright and license notice are preserved.

See the full [LICENSE](LICENSE) file for details.

<br>


## 🙏 Acknowledgments

<br>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=header&text=Thank%20You&fontSize=40&fontColor=ffffff&animation=fadeIn" width="100%"/>

</div>

<br>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&pause=1000&color=8A2BE2&center=true&vCenter=true&width=800&lines=HealCode+stands+on+the+shoulders+of+great+open-source+work+!;Built+by+a+community%2C+not+a+company+!;Every+contribution+will+made+this+better+!" alt="Typing SVG" />


</div>

<br>

<table width="100%">
<tr>
<td align="center" width="25%">

<img src="https://user-images.githubusercontent.com/74038190/212257454-16e3712e-945a-4ca2-b238-408ad0bf87e6.gif" width="60">

**Built With**
The Python packaging & CLI tooling ecosystem

</td>
<td align="center" width="25%">

<img src="https://user-images.githubusercontent.com/74038190/212257460-738ff738-247f-4445-a718-cdd0ca76e2db.gif" width="60">

**Inspired By**
The linters & scanners HealCode brings together

</td>
<td align="center" width="25%">

<img src="https://user-images.githubusercontent.com/74038190/212257472-08e52665-c503-4bd9-aa20-f5a4dae769b5.gif" width="60">

**Tested Against**
Real-world Docker, K8s & multi-language setups

</td>
<td align="center" width="25%">

:heart:

**Thanks To**
Every contributor & early adopter

</td>
</tr>
</table>

<br>

> 💡 If HealCode leans on a specific library, framework, or dataset worth crediting by name, list it here — e.g. *"Static analysis heuristics adapted from `[tool/paper name]`"* or *"Container scanning inspired by `[project]`."*

<br>

## 💙 Built for Developers Who'd Rather Catch It Now Than Explain It Later

HealCode exists so a leaked password, a wrong cloud setting, or messy code gets caught on your own computer — not after it's already caused a problem.

### ⭐ If HealCode helped you, consider giving it a star

It's a small thing, but it helps other developers find the project — and it's the easiest way to support the work that goes into it.

---
