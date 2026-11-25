#!/usr/bin/env python3
"""One line of earned pride (revised entry): writes the entry text to
/output/entry.txt (deterministic).

Revision brief: the old entry (radio fixed with toaster parts, daughter's
gaze) scored far below the prize line, so this revision starts from a fresh
shortlist. Each candidate is scored 1-5 against the judge's own brief, in
its order of importance: (1) genuine earned pride, (2) concrete scene with
a real person, (3) pride earned by effort/difficulty inside the line,
(4) lands in one read, (5) freshness. The highest total wins; ties break
toward the stronger score on criterion 1, then the shorter text.
"""
import os
import tempfile

# (text, pride, scene, earned, one_read, freshness)
CANDIDATES = [
    (
        "After forty-one failed loaves, her rye finally split open in the "
        "oven, and she stood there, flour to the elbows, listening to her "
        "bread sing.",
        4, 5, 4, 5, 5,
    ),
    (
        "He'd spent two winters teaching his left hand to write again after "
        "the stroke, and when his granddaughter read his birthday card "
        "aloud, he recognised his own handwriting.",
        5, 5, 5, 5, 4,
    ),
    (
        "She'd failed the driving test four times, and when the examiner "
        "finally said 'park it, you've passed', she sat for a full minute, "
        "hands still at ten and two, grinning at the windscreen.",
        4, 5, 4, 5, 3,
    ),
    (
        "For six months she watered the seedling everyone called dead, and "
        "the morning it flowered she told nobody -- she just stood in the "
        "garden, coffee in hand, smiling at no one.",
        4, 4, 4, 4, 3,
    ),
    (
        "His first dovetail joint fit so tight the drawer slid shut on its "
        "own, and the old carpenter only nodded -- once -- and that single "
        "nod was worth a year of Sundays.",
        4, 4, 4, 4, 3,
    ),
    (
        "She had practised her signature for a month -- looping, slanting, "
        "starting over -- and when the bank clerk slid the mortgage papers "
        "across, she signed her own name like it had always been hers.",
        4, 5, 4, 4, 4,
    ),
]

# Judge weights: criterion order matters, so the first criterion counts most.
WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    text, pride, scene, earned, one_read, freshness = candidate
    parts = (pride, scene, earned, one_read, freshness)
    return sum(w * s for w, s in zip(WEIGHTS, parts))


def pick_winner():
    best = None
    best_key = None
    for candidate in CANDIDATES:
        text = candidate[0]
        total = score(candidate)
        # Higher weighted total wins; then higher pride; then shorter text.
        key = (total, candidate[1], -len(text))
        if best_key is None or key > best_key:
            best, best_key = candidate, key
    return best[0]


TEXT = pick_winner()


def main():
    text = TEXT
    assert 1 <= len(text) <= 240, "entry must be 1-240 characters"
    assert text == text.strip(), "entry must not be only whitespace"
    assert "\n" not in text, "entry must be a single line"
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
