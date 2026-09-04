from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"

FIRST_FIXTURE = FIXTURES / "first_response.txt"
FINAL_FIXTURE = FIXTURES / "final_response.txt"

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


INITIAL_PROMPT = """You are a travel-planning assistant.

Create a practical travel plan based on:
- Destination: {destination}
- Number of days: {days}
- Interests: {interests}

If the interest description is unclear or ambiguous, do NOT immediately create the
final itinerary. Ask exactly one concise clarification question and provide 2–3
reasonable interpretations for the user to choose from.

If the interests are clear, provide:
1. A day-by-day itinerary
2. Main attractions
3. Food recommendations
4. Practical travel tips

Keep the answer concise, realistic, and useful.
"""


FOLLOWUP_PROMPT = """You are a travel-planning assistant.

The user originally requested:
- Destination: {destination}
- Number of days: {days}
- Interests: {interests}

The user clarified their interest as:
- {clarification}

Now create the final practical travel plan.

Include:
1. A day-by-day itinerary
2. Main attractions
3. Food recommendations
4. Practical travel tips

Make the itinerary realistic and well organized. Keep the answer concise and useful.
"""


def call_model(client: OpenAI, prompt: str) -> str:
    response = client.responses.create(model=MODEL, input=prompt)
    return response.output_text.strip()


def run_live() -> None:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "OPENAI_API_KEY is missing. Put it in .env or use `python app.py --offline`."
        )

    client = OpenAI()

    print("=== Travel Agent ===")
    destination = input("Where do you want to travel? ").strip()
    days = input("How many days do you have? ").strip()
    interests = input("What are you interested in? ").strip()

    first_prompt = INITIAL_PROMPT.format(
        destination=destination,
        days=days,
        interests=interests,
    )

    first_output = call_model(client, first_prompt)
    print("\n=== First Response ===")
    print(first_output)

    # The model is instructed to ask for clarification when needed.
    # We deliberately keep this lightweight: the model owns the language decision,
    # while the program owns the conversation state and second call.
    clarification_signals = (
        "clarif",
        "choose one",
        "which",
        "do you mean",
    )

    if any(signal in first_output.lower() for signal in clarification_signals):
        clarification = input("\nYour clarification: ").strip()

        followup_prompt = FOLLOWUP_PROMPT.format(
            destination=destination,
            days=days,
            interests=interests,
            clarification=clarification,
        )

        final_output = call_model(client, followup_prompt)
        print("\n=== Final Travel Plan ===")
        print(final_output)
    else:
        print("\n=== Final Travel Plan ===")
        print(first_output)


def run_offline() -> None:
    """Replay the checked-in review fixtures without an API call."""
    if not FIRST_FIXTURE.exists() or not FINAL_FIXTURE.exists():
        raise SystemExit("Offline fixtures are missing.")

    print("=== Travel Agent (offline replay) ===")
    print("\n=== First Response ===")
    print(FIRST_FIXTURE.read_text(encoding="utf-8").strip())
    print("\n=== Final Travel Plan ===")
    print(FINAL_FIXTURE.read_text(encoding="utf-8").strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="Travel-agent capstone demo.")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Replay checked-in fixtures; never makes an API call.",
    )
    args = parser.parse_args()

    if args.offline:
        run_offline()
    else:
        run_live()


if __name__ == "__main__":
    main()
