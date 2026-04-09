"""
Smoke-test POST /analyze.

By default uses FastAPI TestClient (no server on port 8000 required).

To hit a running API instead, set LIVE_API_URL, e.g.:
  set LIVE_API_URL=http://127.0.0.1:8000
  python test.py
"""

from __future__ import annotations

import base64
import os
from pathlib import Path

import requests
from fastapi.testclient import TestClient

from main import app

_MINIMAL_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)
_img_path = Path(__file__).resolve().parent / "test.png"
if _img_path.is_file():
    image_base64 = base64.b64encode(_img_path.read_bytes()).decode()
else:
    image_base64 = _MINIMAL_PNG_B64

data = {
    "text": "Hurry! Only 2 left!",
    "html": "<input type='checkbox' checked>",
    "image_base64": image_base64,
}

live = os.environ.get("LIVE_API_URL", "").strip()
if live:
    url = live.rstrip("/") + "/analyze"
    response = requests.post(url, json=data, timeout=30)
else:
    with TestClient(app) as client:
        response = client.post("/analyze", json=data)

response.raise_for_status()
print(response.json())
