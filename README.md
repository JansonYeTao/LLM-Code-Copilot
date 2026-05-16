# LLM Code Copilot

A local-first starter repository for a code-copilot style workflow powered by a self-hosted LLM endpoint (no Colab required).

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── configs/
│   └── example.env
├── docs/
│   └── non-colab-setup.md
├── scripts/
│   └── run_api.sh
└── services/
    ├── api/
    │   └── main.py
    └── llm_host_colab.ipynb
```

## What Changed

This refactor introduces a non-Colab path:

- A FastAPI gateway (`/health`, `/generate`) in `services/api/main.py`.
- A local run script (`scripts/run_api.sh`).
- Example environment config (`configs/example.env`).
- Local setup guide (`docs/non-colab-setup.md`).

The notebook remains for legacy experimentation, but the default development path is now local and scriptable.

## Quick Start (Local)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure upstream LLM server:

```bash
cp configs/example.env .env
# Edit LLM_BASE_URL if needed
```

4. Run API:

```bash
./scripts/run_api.sh
```

5. Validate:

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/generate \
  -H 'content-type: application/json' \
  -d '{"prompt":"write a python hello world","max_tokens":64,"temperature":0.2}'
```

## Notes

- `/generate` proxies to `{LLM_BASE_URL}/completion` in llama.cpp-compatible servers.
- This repo is for local prototyping and integration experiments.
