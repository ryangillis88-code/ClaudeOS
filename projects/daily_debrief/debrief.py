#!/usr/bin/env python3
"""Daily Debrief — end-of-day reflection in 3 questions."""

import os
import sys
from datetime import datetime
from pathlib import Path
from textwrap import indent

OUTPUTS_DIR = Path(__file__).parent.parent.parent / "outputs" / "debriefs"

QUESTIONS = [
    ("wins", "What were your wins today? (big or small)"),
    ("blockers", "Any blockers or frustrations to note?"),
    ("tomorrow", "What's your #1 priority for tomorrow?"),
]

DIVIDER = "─" * 50


def ask(prompt: str) -> str:
    print(f"\n  {prompt}")
    print("  (press Enter twice when done)\n")
    lines = []
    while True:
        try:
            line = input("  > ")
        except EOFError:
            break
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def build_markdown(date_str: str, answers: dict[str, str]) -> str:
    sections = "\n\n".join(
        f"## {label.capitalize()}\n{answer or '_Nothing noted._'}"
        for label, answer in answers.items()
    )
    return f"# Daily Debrief — {date_str}\n\n{sections}\n"


def print_summary(answers: dict[str, str]) -> None:
    print(f"\n{DIVIDER}")
    print("  DEBRIEF SAVED")
    print(DIVIDER)
    for label, answer in answers.items():
        header = f"  {label.upper()}"
        body = indent(answer or "(nothing noted)", "    ")
        print(f"\n{header}\n{body}")
    print(f"\n{DIVIDER}\n")


def main() -> None:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    print(f"\n{DIVIDER}")
    print(f"  DAILY DEBRIEF  //  {date_str}  {time_str}")
    print(DIVIDER)

    answers: dict[str, str] = {}
    for key, question in QUESTIONS:
        answers[key] = ask(question)

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = OUTPUTS_DIR / f"{date_str}.md"

    # Append if file already exists (multiple debriefs in one day)
    if filename.exists():
        timestamp = now.strftime("%H%M")
        filename = OUTPUTS_DIR / f"{date_str}-{timestamp}.md"

    filename.write_text(build_markdown(date_str, answers))

    print_summary(answers)
    print(f"  Saved to: {filename.relative_to(Path.home())}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Debrief cancelled.\n")
        sys.exit(0)
