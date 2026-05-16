from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import httpx

app = FastAPI(title="LLM Code Copilot API", version="0.1.0")


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_tokens: int = Field(256, ge=1, le=4096)
    temperature: float = Field(0.2, ge=0.0, le=2.0)


class GenerateResponse(BaseModel):
    output: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest) -> GenerateResponse:
    """Proxy generation requests to a local llama.cpp-compatible server.

    Expected upstream:
      POST {LLM_BASE_URL}/completion
    """
    base_url = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8080")
    payload = {
        "prompt": req.prompt,
        "n_predict": req.max_tokens,
        "temperature": req.temperature,
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(f"{base_url}/completion", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream LLM error: {exc}") from exc

    text = data.get("content") or data.get("output") or ""
    return GenerateResponse(output=text)
