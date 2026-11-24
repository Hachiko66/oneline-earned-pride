#!/usr/bin/env python3
"""One line of earned pride: writes the entry text to /output/entry.txt (deterministic)."""
import os
import tempfile

TEXT = "He fixed the old radio with parts from a broken toaster, and when it crackled back to life, his daughter looked at him like he had invented sound."
# Quiet earned pride: a concrete scene, a real person, a long effort landing in one read.

def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(TEXT)
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
