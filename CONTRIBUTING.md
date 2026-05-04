# Contributing

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements-dev.txt
pip install -e .
pytest
```

## Expectations

- Keep retriever/generator interfaces stable.
- Add tests for every behavior change.
- Keep Terraform module environment-agnostic.
- Update docs when endpoint/infra behavior changes.

## Pull Requests

- one coherent change per PR
- include test evidence
- keep lint and tests green
