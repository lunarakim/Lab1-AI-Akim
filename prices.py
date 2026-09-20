"""Gemini API list prices, in US dollars per million tokens (text input/output).

CHECK every number below against the source before you quote it: prices and
model ids change. Set PRICE_CHECKED to the day you actually checked.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

PRICE_SOURCE = "https://ai.google.dev/gemini-api/docs/pricing"
PRICE_CHECKED = "2026-09-20"  # CHECK: put the date you verified the prices

BATCH_DISCOUNT = 0.50  # CHECK on the pricing page
CACHE_READ_FRACTION: Dict[str, float] = {}  # not used in this lab


@dataclass(frozen=True)
class Model:
    """One model's list price and headline limits."""

    model_id: str
    input_per_mtok: float
    output_per_mtok: float
    context_tokens: int


MODELS: Dict[str, Model] = {
    # CHECK model_id with client.models.list() and prices on the pricing page.
    "flash-lite-3.1": Model("gemini-3.1-flash-lite", 0.25, 1.50, 1_000_000),
    "flash-3": Model("gemini-3-flash-preview", 0.50, 3.00, 1_000_000),
    "pro-3.1": Model("gemini-3.1-pro-preview", 2.00, 12.00, 1_000_000),
}

DEFAULT_MODEL = "flash-3"


def cost_usd(model_key: str, input_tokens: int, output_tokens: int) -> float:
    """Return the list-price cost of one request, in US dollars."""
    model = MODELS[model_key]
    return (
        input_tokens * model.input_per_mtok
        + output_tokens * model.output_per_mtok
    ) / 1_000_000
