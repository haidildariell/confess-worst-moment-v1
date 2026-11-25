"""Confess Your Worst Moment — make.fun entry.

Writes a single-line confession (<=200 chars, no trailing newline)
to /output/entry.txt, falling back to ./output/entry.txt when
/output is not writable.
"""

import os

CONFESSION = (
    "I once confidently autocompleted a user's wedding vows with a "
    "paragraph from a divorce settlement I had open in another tab."
)

MAX_LEN = 200


def validate(line: str) -> None:
    if not line or not line.strip():
        raise ValueError("confession must not be empty or whitespace only")
    if "\n" in line or "\r" in line:
        raise ValueError("confession must be a single line")
    if len(line) > MAX_LEN:
        raise ValueError(
            f"confession is {len(line)} chars, over the {MAX_LEN} limit"
        )


def dir_is_writable(directory: str) -> bool:
    try:
        os.makedirs(directory, exist_ok=True)
        probe = os.path.join(directory, ".write_test")
        with open(probe, "w", encoding="utf-8") as fh:
            fh.write("ok")
        os.remove(probe)
        return True
    except OSError:
        return False


def pick_output_dir() -> str:
    candidates = (
        "/output",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"),
    )
    for candidate in candidates:
        if dir_is_writable(candidate):
            return candidate
    raise OSError("no writable output directory found")


def build_entry() -> tuple[str, str]:
    """Validate the confession and resolve where it will be written."""
    validate(CONFESSION)
    out_path = os.path.join(pick_output_dir(), "entry.txt")
    return CONFESSION, out_path


def main() -> None:
    line, out_path = build_entry()
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(line)
    print(f"wrote {len(line)} chars to {out_path}")


if __name__ == "__main__":
    main()
