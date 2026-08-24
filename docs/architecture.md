# Architecture

`container-pulse` uses a small `src/` package with two layers:

1. `core.py` contains deterministic functions that can be tested without the CLI.
2. `cli.py` handles arguments, formatting, and process exit codes.

Runtime dependencies are intentionally limited to the Python standard library. Tests use pytest through the optional `dev` dependency. CI compiles the package and runs the test suite on every push and pull request.

The source reference `dani3l0/Status` influenced only the problem-space research. Implementation details are intentionally independent.
