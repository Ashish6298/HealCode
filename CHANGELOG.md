# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-07-30

### Added
- **Diagnostic Scanning Profiles**: Targeted scans using DevOps, Security, Minimal, Full config profiles.
- **Baseline & Drift Detection**: Save snapshots and compare regressions or resolved issues.
- **Directory Watch Mode**: Automated polling based incremental rescans.
- **Mock Plugin Marketplace**: Search, install, update, and validate custom plugins offline.
- **Reporting Extensions**: CSV and XML format generation.
- **Safe Scanner Concurrency**: Parallelized execution in Core ScanEngine.

## [0.9.0] - 2026-07-27

### Added
- **AI Intelligence Engine**: Modular AI analysis layer (root cause, correlation, recommendation, prioritization, executive summary).
- **AI Provider Abstraction**: Pluggable provider interface supporting Offline, OpenAI, Anthropic, Gemini, Ollama, and OpenAI-compatible endpoints.
- **Offline-First AI**: Built-in heuristic provider requires no external API calls.
- **Privacy Masking Layer**: Automatically scrubs secrets, API keys, tokens, and passwords before any data leaves the machine.
- **`healcode ai` CLI Command**: Runs AI-powered analysis on scan findings with `--offline` flag.
- **AIConfig**: New configuration dataclass for provider, model, temperature, masking, timeout, and retry settings.
- **Expanded Health Score categories**: AI_READINESS, ROOT_CAUSE_COVERAGE, RECOMMENDATION_QUALITY.

## [0.8.0] - 2026-07-26

### Added
- **Universal Code Analyzer**: Parses code nesting and estimates complexity metrics.
- **Performance anti-patterns detector**: Flags nested loop structures offline.
- **Expanded Health Score categories**: CODE_QUALITY, MAINTAINABILITY, ARCHITECTURE_QUALITY, COMPLEXITY_HEALTH, SECURITY_ANALYSIS, PERFORMANCE_HEALTH, DOCUMENTATION_COMPLETENESS, TEST_QUALITY, TECHNICAL_DEBT, CODE_READINESS, STATIC_ANALYSIS_HEALTH, DEPENDENCY_GRAPH_HEALTH.

## [0.7.0] - 2026-07-26

### Added
- **Cloud Tooling Scanner**: Discovers AWS, Azure, Google Cloud CLI tools locally configured setups.
- **Kubernetes contexts checker**: Verifies kubeconfig config file path and active context definitions.
- **Helm chart quality scans**: Evaluates values.yaml setups and Chart templates.
- **Infrastructure-as-Code (IaC) Scanner**: Identifies local Terraform provider variables files.
- **Expanded Health Score categories**: CLOUD_CLI_HEALTH, CLOUD_AUTHENTICATION_HEALTH, CLOUD_CONFIGURATION_HEALTH, KUBERNETES_HEALTH, MANIFEST_QUALITY, HELM_HEALTH, IAC_HEALTH, CLUSTER_READINESS, DEPLOYMENT_READINESS, INFRASTRUCTURE_SECURITY, CREDENTIAL_HYGIENE, CLOUD_PROJECT_READINESS.

## [0.6.0] - 2026-07-26

### Added
- **Project Structure Analyzer**: Audits repository workspace rules, directories configurations, and standards checklists.
- **Dependency Manifest Auditor**: Compares dependency declaration maps and identifies missing lockfiles.
- **CI/CD Intelligence**: Identifies GitHub Actions workflow config files.
- **Ignore File Intelligence**: Audits `.gitignore` layout availability.
- **Expanded Health Score categories**: PROJECT_STRUCTURE_HEALTH, DEPENDENCY_HEALTH, REPOSITORY_QUALITY, DOCUMENTATION_QUALITY, BUILD_HEALTH, TESTING_HEALTH, CICD_HEALTH, WORKSPACE_HEALTH, CONFIGURATION_HEALTH, IGNORE_FILE_HEALTH, PROJECT_MAINTAINABILITY, PROJECT_READINESS.

## [0.5.0] - 2026-07-26

### Added
- **Docker System Scanner**: Verifies daemon availability, client/server version info, and context setups.
- **Dockerfile Best Practices Validator**: Analyzes Dockerfiles to flag latest tags, missing healthchecks, and root executions.
- **Docker Compose Scanner**: Validates compose configuration properties such as restart policies.
- **Expanded Health Score categories**: DOCKER_HEALTH, CONTAINER_HEALTH, IMAGE_HEALTH, DOCKERFILE_QUALITY, COMPOSE_QUALITY, NETWORK_HEALTH, VOLUME_HEALTH, CONTAINER_SECURITY_READINESS, DOCKER_ENVIRONMENT_READINESS.

## [0.4.0] - 2026-07-26

### Added
- **Git Scanner**: Resolves Git installations, local branch state, configurations, cleanliness status, and untracked files.
- **SSH/HTTPS Authentication Checker**: Verifies SSH keypair presence (e.g. `~/.ssh`) and HTTPS credential helpers, masking sensitive outputs.
- **Environment Scanner**: Flags missing `.env` files and tracks environment variable key drift against `.env.example`.
- **Exposed Secret Scanning**: Searches files for raw API keys or PEM private keys and masks matches safely in output logs.
- **Framework Detection**: Scans dependency declarations to identify React, Vue, FastAPI, Django, Flutter, etc.
- **Expanded Health Score categories**: GIT_HEALTH, AUTHENTICATION_HEALTH, ENVIRONMENT_HEALTH, REPOSITORY_HEALTH, FRAMEWORK_READINESS, CONFIGURATION_QUALITY, SECRET_HYGIENE.

## [0.3.0] - 2026-07-26

### Added
- **Runtime intelligence**: Identifies installed compilers and interpreters (Node.js, Python, Java, Go, Rust, Dart, Flutter).
- **Toolchain compatibility**: Compares engine constraints inside package.json or pyproject.toml and flags mismatches.
- **Reports archiving**: Archives all test reports directly under reports/ folder.

## [0.2.0] - 2026-07-26

### Added
- **System Scanner**: Collects hostname, OS information, CPU cores, memory metrics, swap stats, disk usage, active shell, and internet connectivity.
- **PATH Analyzer**: Detects duplicates, nonexistent folders, inaccessible directories, and missing system folders in `PATH`.
- **Port Scanner**: Detects local listening ports for conflicts in standard dev ranges (e.g. 3000, 5000, 8080, etc.).
- **Weighted Health Scoring**: Calculates health scores per category (SYSTEM, HARDWARE, STORAGE, NETWORK, ENVIRONMENT) and provides visual meters.
- **In-Memory and Target Path Caching**: Optimizes repeated scans by validating target folder modification times.
- **Encoding Safety Fallbacks**: Prevents terminal crashes on Windows consoles utilizing CP1252.

## [0.1.0] - 2026-07-26

### Added
- Initial project layout and structure for **HealCode**.
- Professional CLI entry point using custom argparse routing.
- Custom Logging Framework with TRACE level support and Rich styling.
- OS Detector identifying Windows, macOS, Linux, and WSL environments.
- Core Scanning Engine supporting exclusions and directory depth rules.
- Built-in default scanner checking for TODOs and large files.
- SQLite-backed Cache Manager with TTL expiration support.
- Reporting interface with Console (table representation) and JSON reporters.
- Type-safe Config Management merging global/project JSON configs.
- Health engine verifying runtime environment status.
- Type checks under mypy and pytest suites covering all modules.
