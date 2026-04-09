"""OpenCV: decode image bytes, grayscale, detect bright regions (attention cues)."""

from __future__ import annotations

import cv2
import numpy as np

# Pixels at or above this grayscale level count as "bright"
BRIGHT_THRESHOLD = 200
# Ignore tiny noise blobs; region must be at least this area (px) or fraction of image
MIN_REGION_AREA_RATIO = 0.0005
MIN_REGION_AREA_ABS = 40
# Minimum share of image that is bright before we flag on coverage alone (no big contour)
MIN_BRIGHT_COVERAGE = 0.025


def analyze_brightness_attention(image_bytes: bytes) -> tuple[bool, float, list[str]]:
    """
    Decode image from bytes, convert to grayscale, find bright regions.

    Returns ``(should_flag, confidence, matched_phrases)``. If decoding fails, returns
    ``(False, 0.0, [])`` (invalid image bytes are ignored for this signal).
    """
    if not image_bytes:
        return False, 0.0, []

    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        return False, 0.0, []

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape[:2]
    area = h * w
    if area == 0:
        return False, 0.0, []

    _, binary = cv2.threshold(gray, BRIGHT_THRESHOLD, 255, cv2.THRESH_BINARY)
    bright_ratio = float(np.count_nonzero(binary)) / float(area)

    min_region = max(MIN_REGION_AREA_ABS, int(area * MIN_REGION_AREA_RATIO))
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    significant = [c for c in contours if cv2.contourArea(c) >= min_region]

    has_regions = len(significant) > 0
    high_coverage = bright_ratio >= MIN_BRIGHT_COVERAGE

    if not has_regions and not high_coverage:
        return False, 0.0, []

    phrases: list[str] = []
    if has_regions:
        phrases.append(f"{len(significant)} bright region(s) (threshold {BRIGHT_THRESHOLD}, min area {min_region}px)")
    if high_coverage:
        phrases.append(f"bright coverage ~{bright_ratio:.1%}")

    n_regions = len(significant)
    conf = min(
        0.92,
        0.42 + 0.11 * min(n_regions, 6) + min(0.38, bright_ratio * 5.0),
    )
    return True, round(conf, 3), phrases if phrases else ["bright regions detected"]
