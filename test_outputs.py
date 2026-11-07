"""Check that every step prints exactly the output shown in the article.

The try-it-yourself folder is not in the article; its expected output
is in try-it-yourself/expected.txt.

Run from the repository root:  python test_outputs.py   (or: pytest)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

CASES = [
    ("step-4", "validate.py", "expected.txt"),
    ("step-5", "validate.py", "expected.txt"),
    ("step-6", "validate_before_fix.py", "expected_before_fix.txt"),
    ("step-6", "validate.py", "expected.txt"),
    ("try-it-yourself", "validate.py", "expected.txt"),
]


def run(folder, script):
    result = subprocess.run(
        [sys.executable, script],
        cwd=ROOT / folder,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def test_outputs_match_article():
    for folder, script, expected in CASES:
        want = (ROOT / folder / expected).read_text().strip()
        got = run(folder, script)
        assert got == want, f"{folder}/{script} output changed:\n{got}"


if __name__ == "__main__":
    test_outputs_match_article()
    print(f"All {len(CASES)} outputs match their expected files (4 from the article, 1 from try-it-yourself).")
