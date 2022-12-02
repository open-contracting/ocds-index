import pytest

from ocdsindex.exceptions import MissingHeadingError
from ocdsindex.extract import extract_sphinx
from tests import expected, parse


def test_extract_sphinx():
    documents = extract_sphinx(
        "https://standard.open-contracting.org/dev/en/guidance/",
        parse("success", "en", "guidance", "index.html"),
    )

    assert documents == expected["en"][1:2]


def test_extract_sphinx_deep():
    documents = extract_sphinx(
        "https://standard.open-contracting.org/dev/en/schema/",
        parse("success", "en", "schema", "index.html"),
    )

    assert documents == expected["en"][3:]


def test_extract_sphinx_error(caplog):
    with pytest.raises(MissingHeadingError) as excinfo:
        extract_sphinx(
            "https://standard.open-contracting.org/fail/",
            parse("failure", "index.html"),
        )

    assert str(excinfo.value) == "list index out of range"
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"
    assert caplog.records[0].message == 'No heading found\n<section id="error">\n    No heading.\n  </section>\n'
