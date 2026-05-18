import json
import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(title="LLM Code Copilot API", version="0.2.0")


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_tokens: int = Field(256, ge=1, le=4096)
    temperature: float = Field(0.2, ge=0.0, le=2.0)
    stream: bool = False


class GenerateResponse(BaseModel):
    output: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _build_payload(req: GenerateRequest) -> dict[str, Any]:
    return {
        "prompt": req.prompt,
        "n_predict": req.max_tokens,
        "temperature": req.temperature,
        "stream": req.stream,
    }


def _extract_text(data: dict[str, Any]) -> str:
    return data.get("content") or data.get("output") or ""


def _sse(event: str, data: str) -> str:
    return f"event: {event}\ndata: {data}\n\n"


async def _stream_upstream(base_url: str, payload: dict[str, Any]):
    timeout = httpx.Timeout(connect=10.0, read=120.0, write=30.0, pool=30.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", f"{base_url}/completion", json=payload) as resp:
                resp.raise_for_status()

                saw_any = False
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    saw_any = True
                    yield _sse("token", line)

                if not saw_any:
                    yield _sse("token", "")

        yield _sse("done", "[DONE]")
    except httpx.HTTPError as exc:
        yield _sse("error", f"Upstream LLM error: {exc}")


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    """Proxy generation requests to a local llama.cpp-compatible server.

    Non-stream: returns JSON body with final output.
    Stream: returns SSE (`text/event-stream`) with token/error/done events.
    """
    base_url = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8080")
    payload = _build_payload(req)

    if req.stream:
        return StreamingResponse(
            _stream_upstream(base_url=base_url, payload=payload),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    try:
        timeout = httpx.Timeout(connect=10.0, read=120.0, write=30.0, pool=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(f"{base_url}/completion", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream LLM error: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="Upstream LLM returned invalid JSON") from exc

    return GenerateResponse(output=_extract_text(data))
