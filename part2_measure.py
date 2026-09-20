"""Part 2 -- the measurement (Gemini version).

1. Token counts for every text in :mod:`texts`, in every language, using the
   free ``count_tokens`` endpoint, plus one combined count per language for
   the real request shape (system prompt + complaint).
2. With --call: one real request per language, to see the answer and the
   billed usage. This is the only part that spends money.

Results are written to ``measurements.json`` for Part 3.

Run (in Colab, with GEMINI_API_KEY set):
    !python part2_measure.py            # count tokens only
    !python part2_measure.py --call     # also answer the complaint in en, ru, kk
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional

from google import genai
from google.genai import errors, types

from prices import MODELS, DEFAULT_MODEL
from texts import CORPUS, LANGUAGES

try:  # optional: only needed if you use a .env file instead of Colab Secrets
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

OUTPUT_PATH = Path(__file__).with_name("measurements.json")

#: Gemini's output limit INCLUDES thinking tokens, and thinking tokens are
#: billed as output but never appear in the reply. Keep generous headroom;
#: do not switch thinking off -- that hides exactly the cost the lab is about.
MAX_TOKENS = 4096


def count_tokens(client: genai.Client, model_id: str, text: str) -> int:
    """Return the number of input tokens ``text`` costs on ``model_id``."""
    result = client.models.count_tokens(model=model_id, contents=text)
    return result.total_tokens


def count_request_tokens(client: genai.Client, model_id: str, lang: str) -> int:
    """Return input tokens for one real request: system prompt + complaint.

    The Gemini API's count_tokens may not accept a system instruction, so the
    system prompt and the complaint are counted as one joined text. This is an
    approximation of the real request shape (a token or two of difference).
    """
    text = CORPUS["system_prompt"][lang] + "\n\n" + CORPUS["complaint"][lang]
    return client.models.count_tokens(model=model_id, contents=text).total_tokens


def one_real_request(
    client: genai.Client, model_id: str, lang: str
) -> Optional[Dict[str, int]]:
    """Send one request and print the answer and its billed usage.

    Returns:
        ``input_tokens`` and ``output_tokens`` as billed (output includes
        thinking tokens), or ``None`` if there was no answer.
    """
    response = client.models.generate_content(
        model=model_id,
        contents=CORPUS["complaint"][lang],
        config=types.GenerateContentConfig(
            system_instruction=CORPUS["system_prompt"][lang],
            max_output_tokens=MAX_TOKENS,
        ),
    )

    usage = response.usage_metadata
    answer = response.text
    if not answer:
        print("  model returned no text (blocked or empty).")
        print(f"  usage: {usage}")
        return None

    finish = None
    if response.candidates:
        finish = response.candidates[0].finish_reason
    print(f"  finish_reason: {finish}")
    print("  --- answer ---")
    print("  " + answer.replace("\n", "\n  "))

    thoughts = usage.thoughts_token_count or 0
    visible = usage.candidates_token_count or 0
    out_tokens = visible + thoughts
    print(
        f"  billed: {usage.prompt_token_count} in, {out_tokens} out "
        f"({visible} visible + {thoughts} thinking)"
    )
    if "MAX_TOKENS" in str(finish):
        print(f"  NOTE: answer was cut off at max_output_tokens={MAX_TOKENS}.")
    return {"input_tokens": usage.prompt_token_count, "output_tokens": out_tokens}


def main() -> int:
    """Count tokens for the whole corpus, optionally make one real request."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=sorted(MODELS),
        help=f"which model to price against (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--call",
        action="store_true",
        help="also answer the complaint in each language (this costs money)",
    )
    args = parser.parse_args()

    model_id = MODELS[args.model].model_id

    try:
        client = genai.Client()  # reads GEMINI_API_KEY from the environment
    except (ValueError, errors.APIError) as exc:
        print(f"could not build a client: {exc}", file=sys.stderr)
        print("set GEMINI_API_KEY (Colab: Secrets -> os.environ).", file=sys.stderr)
        return 1

    counts: Dict[str, Dict[str, int]] = {}
    print(f"counting tokens on {model_id} (free, no model run)")
    try:
        for item_id, versions in CORPUS.items():
            counts[item_id] = {
                lang: count_tokens(client, model_id, versions[lang])
                for lang in LANGUAGES
            }
            row = "  ".join(f"{lang}={counts[item_id][lang]}" for lang in LANGUAGES)
            print(f"  {item_id:<14} {row}")

        request_tokens: Dict[str, int] = {
            lang: count_request_tokens(client, model_id, lang) for lang in LANGUAGES
        }
        row = "  ".join(f"{lang}={request_tokens[lang]}" for lang in LANGUAGES)
        print(f"  {'request':<14} {row}  (system + complaint -- what Part 3 prices)")
    except errors.APIError as exc:
        print(f"API error {exc.code}: {exc}", file=sys.stderr)
        return 1

    billed: Dict[str, Dict[str, int]] = {}
    if args.call:
        print(f"\nanswering the same complaint on {model_id}, in each language:")
        for lang in LANGUAGES:
            print(f"\n[{lang}]")
            try:
                result = one_real_request(client, model_id, lang)
            except errors.APIError as exc:
                print(f"API error {exc.code}: {exc}", file=sys.stderr)
                return 1
            if result is not None:
                billed[lang] = result

    payload = {
        "model": args.model,
        "model_id": model_id,
        "token_counts": counts,
        "request_tokens": request_tokens,
        "one_request_billed": billed or None,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {OUTPUT_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
