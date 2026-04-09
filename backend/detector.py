"""Heuristic dark-pattern detection from plain text."""

from __future__ import annotations

import re
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass(frozen=True)
class PatternRule:
    """A detectable dark-pattern category with weighted phrases."""

    id: str
    name: str
    description: str
    weight: int  # contribution toward aggregate score (capped when summed)
    phrases: tuple[str, ...]


_RULES: tuple[PatternRule, ...] = (
    PatternRule(
        id="false_urgency",
        name="False urgency",
        description="Language that pressures users to act immediately.",
        weight=18,
        phrases=(
            "limited time",
            "limited-time",
            "act now",
            "order now",
            "buy now",
            "shop now",
            "expires soon",
            "expires today",
            "expires at midnight",
            "ends tonight",
            "ends today",
            "ends in",
            "ending soon",
            "sale ends",
            "offer ends",
            "offer expires",
            "only a few left",
            "hurry",
            "don't wait",
            "don't miss out",
            "don't miss this",
            "last chance",
            "final chance",
            "final hours",
            "final day",
            "while supplies last",
            "today only",
            "one day only",
            "flash sale",
            "lightning deal",
            "clock is ticking",
            "time is running out",
            "running out of time",
            "deadline",
            "closing soon",
            "last minute",
            "before it's gone",
            "before it sells out",
            "selling out fast",
            "almost sold out",
            "instant savings",
            "claim now",
            "grab it now",
            "while you can",
        ),
    ),
    PatternRule(
        id="false_scarcity",
        name="False scarcity",
        description="Claims about low stock or high demand that may be misleading.",
        weight=16,
        phrases=(
            "only 2 left",
            "only 3 left",
            "selling fast",
            "almost gone",
            "in high demand",
            "people are viewing",
            "just sold",
        ),
    ),
    PatternRule(
        id="confirmshaming",
        name="Confirmshaming",
        description="Guilt or social pressure to avoid opting out.",
        weight=20,
        phrases=(
            "no thanks, i hate",
            "no thanks i hate",
            "no, thanks i hate",
            "i don't want to save",
            "i do not want to save",
            "i don't want free",
            "i don't need a discount",
            "i don't want a discount",
            "i don't want savings",
            "i'll pay full price",
            "i will pay full price",
            "i prefer to pay full price",
            "no, i like paying more",
            "i enjoy paying full price",
            "i don't care about saving",
            "i don't care about deals",
            "i don't care about",
            "i'm not interested in saving",
            "i am not interested in saving",
            "no, i'd rather pay",
            "i'd rather pay full price",
            "i reject this offer",
            "decline savings",
            "skip this deal",
            "continue without saving",
            "no thanks i'd rather",
            "no thanks, i'd rather",
            "i'll pass on this deal",
            "i'll pass on saving",
            "maybe i don't like saving",
            "no i love paying more",
            "i don't like free stuff",
            "turn down savings",
        ),
    ),
    PatternRule(
        id="trick_wording",
        name="Trick wording",
        description="Ambiguous or misleading labels on actions.",
        weight=15,
        phrases=(
            "subscribe to continue",
            "agree and pay",
            "unlock offer",
            "free trial, then",
            "start trial then",
        ),
    ),
    PatternRule(
        id="hidden_costs",
        name="Hidden costs / drip pricing",
        description="Fees or charges surfaced late in the flow.",
        weight=17,
        phrases=(
            "plus taxes and fees",
            "additional fees apply",
            "service fee",
            "processing fee",
            "small order fee",
            "convenience fee",
        ),
    ),
    PatternRule(
        id="forced_action",
        name="Forced action / nagging",
        description="Blocking progress until the user accepts something.",
        weight=14,
        phrases=(
            "you must accept",
            "required to continue",
            "enable notifications to",
            "turn on notifications",
            "create an account to",
        ),
    ),
    PatternRule(
        id="subscription_trap",
        name="Subscription / continuity pressure",
        description="Language about recurring billing or cancellation.",
        weight=16,
        phrases=(
            "auto-renew",
            "automatically renew",
            "recurring charge",
            "renews automatically",
            "billed annually",
            "cancel before",
        ),
    ),
)

# Extra regex-only signals (category id, name, description, weight, pattern)
_REGEX_RULES: tuple[tuple[str, str, str, int, re.Pattern[str]], ...] = (
    (
        "countdown_pressure",
        "Countdown pressure",
        "Timer or countdown language tied to an offer.",
        12,
        re.compile(r"\b\d{1,2}:\d{2}\s*(left|remaining)\b", re.IGNORECASE),
    ),
    (
        "social_proof_spam",
        "Social proof spam",
        "Numeric social proof claims (e.g. viewers in cart).",
        10,
        re.compile(r"\b\d+\s+(people|users|shoppers)\s+(are\s+)?(viewing|watching)\b", re.IGNORECASE),
    ),
)


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _confidence(rule_id: str, match_count: int) -> float:
    """Higher when several phrases in the same category fire (stronger signal)."""
    if match_count <= 0:
        return 0.0
    n = match_count
    if rule_id in ("false_urgency", "confirmshaming"):
        # Extra weight per additional phrase beyond the first
        base = 0.36 + 0.17 * n + 0.07 * max(0, n - 1)
        return min(1.0, base)
    if rule_id == "preselected_checkbox":
        base = 0.38 + 0.15 * n + 0.06 * max(0, n - 1)
        return min(1.0, base)
    base = 0.34 + 0.14 * n + 0.05 * max(0, n - 1)
    return min(1.0, base)


def detect_preselected_checkboxes(html: str) -> list[dict[str, str | None]]:
    """
    Return one dict per ``<input type="checkbox">`` that has a ``checked`` attribute
    (excluding ``checked="false"`` / ``checked="0"``).
    """
    if not html or not html.strip():
        return []
    soup = BeautifulSoup(html, "html.parser")
    found: list[dict[str, str | None]] = []
    for tag in soup.find_all("input"):
        if (tag.get("type") or "").lower() != "checkbox":
            continue
        if not tag.has_attr("checked"):
            continue
        val = tag.get("checked")
        if isinstance(val, str) and val.strip().lower() in ("false", "0"):
            continue
        found.append(
            {
                "name": tag.get("name"),
                "id": tag.get("id"),
                "value": tag.get("value"),
            }
        )
    return found


def _checkbox_phrase(box: dict[str, str | None]) -> str:
    parts: list[str] = []
    if box.get("id"):
        parts.append(f'id="{box["id"]}"')
    if box.get("name"):
        parts.append(f'name="{box["name"]}"')
    val = box.get("value")
    if val not in (None, "") and str(val).lower() not in ("on", "yes"):
        parts.append(f'value="{val}"')
    return ", ".join(parts) if parts else "checkbox (anonymous)"


def analyze_text(
    text: str,
    html: str | None = None,
    image_bytes: bytes | None = None,
) -> tuple[list[dict], int]:
    """
    Return (detections, score) where score is 0–100 (higher = more concerning).
    Pass optional ``html`` for pre-checked checkboxes; optional ``image_bytes`` for OpenCV cues.
    """
    text_stripped = (text or "").strip()
    html_stripped = (html or "").strip()
    has_image = bool(image_bytes)
    if not text_stripped and not html_stripped and not has_image:
        return [], 0

    detections: list[dict] = []
    raw_total = 0

    if text_stripped:
        normalized = _normalize(text_stripped)
        for rule in _RULES:
            matched_phrases: list[str] = []
            for phrase in rule.phrases:
                if phrase in normalized:
                    matched_phrases.append(phrase)

            if matched_phrases:
                detections.append(
                    {
                        "id": rule.id,
                        "name": rule.name,
                        "description": rule.description,
                        "matched_phrases": matched_phrases,
                        "confidence": round(_confidence(rule.id, len(matched_phrases)), 3),
                    }
                )
                raw_total += rule.weight

        for rid, rname, rdesc, weight, rx in _REGEX_RULES:
            m = rx.search(text_stripped)
            if m:
                detections.append(
                    {
                        "id": rid,
                        "name": rname,
                        "description": rdesc,
                        "matched_phrases": [m.group(0).strip()],
                        "confidence": 0.55,
                    }
                )
                raw_total += weight

    if html_stripped:
        boxes = detect_preselected_checkboxes(html_stripped)
        if boxes:
            phrases = [_checkbox_phrase(b) for b in boxes]
            detections.append(
                {
                    "id": "preselected_checkbox",
                    "name": "Pre-selected checkbox",
                    "description": "Checkbox inputs checked by default (opt-out / sneaking).",
                    "matched_phrases": phrases,
                    "confidence": round(_confidence("preselected_checkbox", len(boxes)), 3),
                }
            )
            raw_total += min(50, 16 + 14 * max(0, len(boxes) - 1))

    if image_bytes:
        from image_cv import analyze_brightness_attention

        flag, cv_conf, cv_phrases = analyze_brightness_attention(image_bytes)
        if flag:
            detections.append(
                {
                    "id": "ui_attention_brightness",
                    "name": "Possible UI attention manipulation",
                    "description": "Bright regions detected; may highlight CTAs or distract from alternatives.",
                    "matched_phrases": cv_phrases or ["bright regions detected"],
                    "confidence": cv_conf,
                }
            )
            raw_total += 18

    score = min(100, int(round(raw_total * 0.65)))
    return detections, score
