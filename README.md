# LLM Code Copilot

A lightweight starter repository for experimenting with a code-copilot style workflow powered by a self-hosted LLM endpoint.

Today this repo is centered on a Colab notebook (`services/llm_host_colab.ipynb`) that launches an inference endpoint using `llama.cpp`, then exposes it through `ngrok` for remote access.

---

## Why this refactor?

The original repository had useful intent but minimal project structure. This refactor adds:

- clearer documentation,
- basic dependency and environment setup,
- standard ignore rules for notebook/Python work.

This keeps the repository beginner-friendly while making it easier to evolve into a more maintainable project.

---

## Current Project Structure

```text
.
├── README.md
├── requirements.txt
├── .gitignore
└── services/
    └── llm_host_colab.ipynb
```

---

## What this project does

- Spins up an LLM inference process from a notebook environment.
- Exposes an HTTP endpoint through a secure tunnel.
- Enables editor-side integrations (for example, a VS Code extension) to call that endpoint.

> Note: This is intended for learning and prototyping. Notebook + tunnel deployments are not production-grade serving infrastructure.

---

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-fork-or-repo-url>
   cd LLM-Code-Copilot
   ```

2. **Create a Python environment (optional but recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Open and run notebook**
   - Launch `services/llm_host_colab.ipynb` in Colab (or compatible Jupyter environment).
   - Follow notebook cells to:
     - fetch / load model artifacts,
     - start inference endpoint,
     - expose endpoint through ngrok,
     - copy endpoint URL for client integrations.

---

## Model Notes

The notebook flow is compatible with llama.cpp-backed models and can be adapted to different model families/quantizations (the earlier version referenced Zephyr-7B via TheBloke).

When changing models, verify:

- prompt formatting,
- context window,
- tokenizer compatibility,
- memory and latency constraints of the runtime.

---

## Recommended Next Refactors

If you continue evolving this project, a good next step is to split responsibilities:

- `services/` for serving/runtime code,
- `clients/` for editor or extension clients,
- `configs/` for model/runtime presets,
- `docs/` for architecture and troubleshooting.

Then move notebook logic into scriptable modules so the same flow can run outside Colab.

---

## Disclaimer

Use this repository for educational and prototyping purposes. For production systems, prefer managed infrastructure with proper auth, rate limits, observability, deployment automation, and secret management.
