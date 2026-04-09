from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, model_validator

from detector import analyze_text
from image_temp import temp_image_path_from_base64

app = FastAPI(
    title="Dark pattern detector",
    description="Analyze text for common dark-pattern signals and an aggregate score.",
    version="0.1.0",
)


class AnalyzeRequest(BaseModel):
    text: str = Field(
        default="",
        description="Plain text to analyze (e.g. UI copy). Can be empty if `html` is provided.",
    )
    html: str | None = Field(
        default=None,
        description="Optional HTML fragment; scanned for pre-checked checkbox inputs.",
    )
    image_base64: str | None = Field(
        default=None,
        description="Optional image as base64 (raw or data URL); decoded and stored in a temp file during the request.",
    )

    @model_validator(mode="after")
    def require_at_least_one_input(self) -> "AnalyzeRequest":
        has_text = bool(self.text and self.text.strip())
        has_html = bool(self.html and self.html.strip())
        has_image = bool(self.image_base64 and self.image_base64.strip())
        if not has_text and not has_html and not has_image:
            raise ValueError('Provide non-empty "text", "html", and/or "image_base64".')
        return self


class DarkPatternHit(BaseModel):
    id: str
    name: str
    description: str
    matched_phrases: list[str]
    confidence: float = Field(..., ge=0.0, le=1.0)


class AnalyzeResponse(BaseModel):
    dark_patterns: list[DarkPatternHit]
    score: int = Field(..., ge=0, le=100, description="0 = none detected, 100 = high concern.")


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(body: AnalyzeRequest) -> AnalyzeResponse:
    try:
        with temp_image_path_from_base64(body.image_base64) as result:
            _, image_blob = result
            raw, score = analyze_text(body.text, html=body.html, image_bytes=image_blob)
    except ValueError as exc:
        detail = str(exc)
        status = 413 if "maximum size" in detail else 400
        raise HTTPException(status_code=status, detail=detail) from exc

    patterns = [DarkPatternHit(**item) for item in raw]
    return AnalyzeResponse(dark_patterns=patterns, score=score)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
