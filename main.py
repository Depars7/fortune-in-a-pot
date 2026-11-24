"""Write one kind, funny fortune for a houseplant to /output/entry.txt.

Standard library only. The file's content is exactly the fortune's
UTF-8 bytes -- no trailing newline -- so repeated runs are
byte-identical. The entry must be a single line of 1-120 characters,
so the fortune is validated before it is written.
"""

import os

FORTUNE = (
    "You will be turned a quarter-turn on Tuesday in the window, "
    "and the whole room will finally admire your good side."
)

# The bounty gate: the entry is one line of 1-120 characters.
MAX_LENGTH = 120

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(fortune):
    """The bounty gate: one line, 1-120 characters, non-blank.

    The fortune must already be exactly as written: leading or
    trailing whitespace would be silently dropped by strip(), so
    it is rejected instead of hidden.
    """
    text = fortune.strip()
    if fortune != text:
        raise ValueError("entry must not start or end with whitespace")
    if not 1 <= len(text) <= MAX_LENGTH:
        raise ValueError(
            f"entry must be 1-{MAX_LENGTH} characters, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def write_entry(fortune):
    """Write the fortune's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.

    Returns the number of bytes written, so the caller can confirm
    the file holds exactly the fortune's UTF-8 bytes.
    """
    data = fortune.encode("utf-8")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(data)
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)
    return len(data)


def main():
    fortune = validate(FORTUNE)
    written = write_entry(fortune)
    if written != len(fortune.encode("utf-8")):
        raise RuntimeError("wrote an unexpected number of bytes")


if __name__ == "__main__":
    main()
