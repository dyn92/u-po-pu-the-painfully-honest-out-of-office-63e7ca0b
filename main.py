"""The Painfully Honest Out-of-Office — make.fun bounty entry.

One out-of-office auto-reply, at most 200 characters, one sentence, one
line: painfully honest about the sender's inbox, yet polite enough that a
manager would let it stand.

The entry sentence lives in SENTENCE. Running this module validates it
against every rule of the bounty (length, single line, single sentence,
single terminal punctuation mark), prints it to stdout, and writes it to
/output/entry.txt, verifying the write byte-for-byte.

Pure Python standard library only; no network, no third-party packages.
"""

SENTENCE = "I'm out of office until Monday and will return to 847 unread emails I will cheerfully pretend to have read."

MAX_LENGTH = 200
TERMINAL_PUNCTUATION = ".!?"


def validate_sentence(text: str) -> None:
    """Raise unless *text* satisfies every rule of the bounty brief."""
    if not isinstance(text, str) or not text:
        raise ValueError("sentence must be a non-empty string")
    if len(text) > MAX_LENGTH:
        raise ValueError(
            f"sentence is {len(text)} characters, over the {MAX_LENGTH} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("sentence must be exactly one line")
    if text.strip() != text:
        raise ValueError("sentence must not have leading or trailing whitespace")
    if "  " in text:
        raise ValueError("sentence must not contain double spaces")
    if text[-1] not in TERMINAL_PUNCTUATION:
        raise ValueError("sentence must end with a single terminal punctuation mark")
    if text.count(".") + text.count("!") + text.count("?") != 1:
        raise ValueError(
            "sentence must contain exactly one sentence-ending punctuation mark"
        )


def main() -> None:
    validate_sentence(SENTENCE)
    print(SENTENCE)

    import os

    output_dir = "/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.txt")

    payload = (SENTENCE + "\n").encode("utf-8")
    with open(output_path, "wb") as handle:
        handle.write(payload)

    with open(output_path, "rb") as handle:
        written = handle.read()
    if written != payload:
        raise RuntimeError(
            f"{output_path} does not match the sentence byte-for-byte"
        )


if __name__ == "__main__":
    main()
