"""Check each rule on its own: one small record at a time.

test_outputs.py checks the article's outputs. This file checks that each
rule catches the problem it is meant to catch, and lets good data through.

Run from the repository root:  python test_rules.py   (or: pytest)
"""
from pathlib import Path

from pyshacl import validate
from rdflib import Graph
from rdflib.namespace import SH

STEP_6 = Path(__file__).parent / "step-6"

PREFIXES = """
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:  <http://example.org/> .
"""

GOOD = """
ex:x a ex:PublishedStatistic ;
    ex:publishedOn "2026-03-01"^^xsd:date ;
    ex:publicUrl <https://example.org/stats/x> .
"""

DATE = "A published statistic needs exactly one publication date."
URL = "A published statistic needs a public URL."
BOTH = "A dataset cannot be both a published statistic and an internal report."


def check(turtle, with_vocab=True):
    """Validate a snippet against the step-6 shapes. Return the messages."""
    data = Graph().parse(data=PREFIXES + turtle, format="turtle")
    shapes = Graph().parse(STEP_6 / "shapes.ttl")
    vocab = Graph().parse(STEP_6 / "vocab.ttl") if with_vocab else None
    conforms, report, _ = validate(data, shacl_graph=shapes, ont_graph=vocab)
    messages = sorted(str(m) for m in report.objects(None, SH.resultMessage))
    assert conforms == (not messages)
    return messages


# Good data passes

def test_a_complete_published_statistic_passes():
    assert check(GOOD) == []


def test_an_internal_report_on_its_own_is_not_checked():
    assert check("ex:x a ex:InternalReport .") == []


# Rule 1: exactly one publication date

def test_a_missing_date_fails():
    assert check(GOOD.replace('ex:publishedOn "2026-03-01"^^xsd:date ;', "")) == [DATE]


def test_a_date_written_as_text_fails():
    assert check(GOOD.replace('"2026-03-01"^^xsd:date', '"last spring"')) == [DATE]


def test_two_dates_fail():
    two = '"2026-03-01"^^xsd:date, "2026-04-01"^^xsd:date'
    assert check(GOOD.replace('"2026-03-01"^^xsd:date', two)) == [DATE]


# Rule 2: a public URL

def test_a_missing_url_fails():
    assert check(GOOD.replace("ex:publicUrl <https://example.org/stats/x>", "")) == [URL]


def test_a_url_written_as_text_fails():
    text_url = 'ex:publicUrl "https://example.org/stats/x"'
    assert check(GOOD.replace("ex:publicUrl <https://example.org/stats/x>", text_url)) == [URL]


def test_any_link_passes_even_one_that_does_not_work():
    # As the article says: the rule checks it is a link, not that it works.
    dead = "ex:publicUrl <ftp://nowhere.invalid/x>"
    assert check(GOOD.replace("ex:publicUrl <https://example.org/stats/x>", dead)) == []


# Rule 3: not also an internal report

def test_a_record_labelled_both_ways_fails():
    assert check(GOOD.replace("a ex:PublishedStatistic", "a ex:PublishedStatistic, ex:InternalReport")) == [BOTH]


# Step 6: the vocabulary

def test_a_monthly_summary_is_skipped_without_the_vocabulary():
    assert check("ex:m a ex:MonthlySpendingSummary .", with_vocab=False) == []


def test_a_monthly_summary_is_checked_with_the_vocabulary():
    assert check("ex:m a ex:MonthlySpendingSummary .") == [URL, DATE]


def test_a_complete_monthly_summary_passes():
    assert check(GOOD.replace("ex:PublishedStatistic", "ex:MonthlySpendingSummary")) == []


# The lesson: finding nothing is not the same as correct data

def test_empty_data_passes_so_always_test_with_a_bad_record():
    assert check("") == []


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print("ok  ", test.__name__[len("test_"):].replace("_", " "))
    print(f"All {len(tests)} rule checks passed.")
