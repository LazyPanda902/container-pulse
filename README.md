# container-pulse

[![CI](https://github.com/LazyPanda902/container-pulse/actions/workflows/ci.yml/badge.svg)](https://github.com/LazyPanda902/container-pulse/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Read-only Linux host and Docker health snapshots for small self-hosted environments.

## Why this project exists

container-pulse is a small portfolio-grade operations tool designed around a concrete troubleshooting workflow rather than a demo-only code sample. It favors deterministic behavior, readable output, explicit failure states, and tests that exercise the core logic. The implementation intentionally stays narrow enough to understand quickly while still doing real work an IT support, systems, or homelab operator could use.

## What it demonstrates

- Python CLI design with no runtime third-party dependencies.
- Defensive input parsing and explicit exit behavior.
- Testable core logic separated from command-line presentation.
- GitHub Actions CI across supported Python versions.
- Privacy-conscious, read-only behavior appropriate for support tooling.
- Source-inspiration documentation that separates problem-space research from implementation.

## Quick start

```bash
git clone https://github.com/LazyPanda902/container-pulse.git
cd container-pulse
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
container-pulse --help
```

## Safety and data handling

This project is intentionally defensive and read-only. It does not exploit hosts, change remote configuration, collect credentials, or transmit collected data to a hosted service. Inputs and output stay local unless the operator explicitly redirects or shares them.

## Originality and source inspiration

Problem-space inspiration: [dani3l0/Status](https://github.com/dani3l0/Status). The reference repository was used only to understand an operational problem area and useful product ergonomics. **No source code from the reference repository is copied, vendored, or translated into this project.** The implementation, tests, CLI behavior, documentation, and project structure here are original Career Lab work.

See [`docs/source-inspiration.json`](docs/source-inspiration.json) for the machine-readable provenance note and [`docs/architecture.md`](docs/architecture.md) for the local design.

## Development

```bash
python -m pip install -e '.[dev]'
python -m compileall -q src
pytest -q
```

Pull requests should keep the project deterministic, local-first, and easy to audit. Do not add credential collection, remote exploitation, destructive actions, or mandatory cloud dependencies.

## License

MIT. See `LICENSE`.
