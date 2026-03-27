# patrimonio-autopilot

D1 foundation scaffold for a Python project.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template and fill values:

```bash
copy .env.example .env
```

## Run smoke checks

From project root:

```bash
python -m compileall src
python src/ops/run_healthcheck.py
```

Optional alert plumbing test:

```bash
python src/ops/run_healthcheck.py --test-alert telegram
python src/ops/run_healthcheck.py --test-alert email
```

Notes:
- Healthcheck verifies required config files and environment variables.
- Alert tests fail explicitly when required environment values are missing.
