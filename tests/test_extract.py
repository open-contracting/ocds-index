from ocdsindex.extract import extract_sphinx
from tests import expected, parse


def test_extract_sphinx():
    documents = extract_sphinx(
        "https://standard.open-contracting.org/dev/en/guidance/",
        parse("en", "guidance", "index.html"),
    )

    assert documents == expected["en"][1:2]


def test_extract_sphinx_deep():
    documents = extract_sphinx(
        "https://standard.open-contracting.org/dev/en/schema/",
        parse("en", "schema", "index.html"),
    )

    assert documents == expected["en"][3:]
