"""Check that each script prints exactly the output shown in the article."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
CASES = [
    ("shacl_check.py", "expected_shacl.txt"),
    ("owl_reason.py", "expected_owl.txt"),
    ("owl_reason_different.py", "expected_owl_different.txt"),
]


def test_outputs_match_article():
    for script, expected in CASES:
        got = subprocess.run([sys.executable, script], cwd=HERE, capture_output=True,
                             text=True, check=True).stdout.strip()
        want = (HERE / expected).read_text().strip()
        assert got == want, f"{script} output changed:\n{got}"


if __name__ == "__main__":
    test_outputs_match_article()
    print(f"All {len(CASES)} outputs match the article.")
