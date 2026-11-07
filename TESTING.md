# How to test this tutorial

From the repository root:

```bash
pip install -r requirements.txt
python test_outputs.py
python test_rules.py
```

Both files run with plain Python. If you have `pytest` installed, `pytest` runs them too.

Every test must pass before a change is published. GitHub runs them on Linux and Windows for every push (see [`.github/workflows/tests.yml`](.github/workflows/tests.yml)).

## `test_outputs.py`: the outputs match the article

Runs each script and compares what it prints, character for character, with the expected file in its folder.

| Run | Expected file | Article section |
|---|---|---|
| `step-4/validate.py` | `step-4/expected.txt` | Step 4 |
| `step-5/validate.py` | `step-5/expected.txt` | Step 5 |
| `step-6/validate_before_fix.py` | `step-6/expected_before_fix.txt` | Step 6, before the fix |
| `step-6/validate.py` | `step-6/expected.txt` | Step 6, after the fix |
| `try-it-yourself/validate.py` | `try-it-yourself/expected.txt` | Try it yourself (not printed in the article) |

If one fails, either a file was edited or the pySHACL version changed. Check `pip show pyshacl` (it should be 0.40.1).

## `test_rules.py`: each rule on its own

Checks one small record at a time against the step-6 shapes. Each test name is a sentence.

| Rule | Tests |
|---|---|
| Good data | a complete published statistic passes · an internal report on its own is not checked |
| Exactly one publication date | a missing date fails · a date written as text fails · two dates fail |
| A public URL | a missing URL fails · a URL written as text fails · any link passes, even one that does not work |
| Not also an internal report | a record labelled both ways fails |
| The vocabulary (step 6) | a monthly summary is skipped without the vocabulary · it is checked with the vocabulary · a complete monthly summary passes |
| The lesson | empty data passes, so always test with a bad record |

"Any link passes, even one that does not work" is on purpose: as the article says, `sh:nodeKind sh:IRI` checks that the value is a link, not that the link works.
