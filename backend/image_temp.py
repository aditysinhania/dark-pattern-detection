"""Decode base64 image payloads and write them to a temporary file."""

from __future__ import annotations

import base64
import binascii
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

# Upper bound to limit memory and disk use (10 MiB)
MAX_IMAGE_BYTES = 10 * 1024 * 1024


def _strip_data_url_prefix(data: str) -> str:
    s = data.strip()
    if s.startswith("data:") and "base64," in s:
        return s.split("base64,", 1)[1].strip()
    return s


def decode_base64_image(data: str) -> bytes:
    """Decode a raw base64 string or a ``data:image/...;base64,...`` data URL."""
    raw = _strip_data_url_prefix(data)
    if not raw:
        raise ValueError("Empty base64 image payload")
    try:
        out = base64.b64decode(raw, validate=False)
    except binascii.Error as exc:
        raise ValueError("Invalid base64 image data") from exc
    if len(out) > MAX_IMAGE_BYTES:
        raise ValueError(f"Image exceeds maximum size ({MAX_IMAGE_BYTES} bytes)")
    return out


def _suffix_from_magic(blob: bytes) -> str:
    if len(blob) >= 3 and blob[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if len(blob) >= 8 and blob[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if len(blob) >= 6 and blob[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if len(blob) >= 12 and blob[:4] == b"RIFF" and blob[8:12] == b"WEBP":
        return ".webp"
    return ".bin"


def write_temp_image(blob: bytes, prefix: str = "dpd_img_") -> Path:
    """Write bytes to a named temp file and return its path (caller must delete)."""
    suffix = _suffix_from_magic(blob)
    fd, path_str = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    try:
        os.write(fd, blob)
    finally:
        os.close(fd)
    return Path(path_str)


@contextmanager
def temp_image_path_from_base64(
    image_base64: str | None,
) -> Generator[tuple[Path | None, bytes | None], None, None]:
    """
    If ``image_base64`` is non-empty, decode once, write a temp file, yield
    ``(path, decoded_bytes)``, then delete the file. If empty/None, yield ``(None, None)``.
    """
    if not image_base64 or not image_base64.strip():
        yield None, None
        return
    blob = decode_base64_image(image_base64)
    path = write_temp_image(blob)
    try:
        yield path, blob
    finally:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
