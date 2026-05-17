# Non-Colab Local Setup

## 1) Start your local LLM server

Run your llama.cpp-compatible server locally and expose a `/completion` endpoint.

## 2) Run API gateway

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/run_api.sh
```

## 3) Test endpoint

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/generate \
  -H 'content-type: application/json' \
  -d '{"prompt":"write a python hello world","max_tokens":64,"temperature":0.2}'
```


## 4) Test streaming

```bash
curl -N http://127.0.0.1:8000/generate \
  -H 'content-type: application/json' \
  -d '{"prompt":"stream me a short poem","max_tokens":64,"temperature":0.7,"stream":true}'
```

Expected response type is `text/event-stream` with `event: token` chunks and a final `event: done`.
