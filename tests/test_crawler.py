import os.path

from ocdsindex.crawler import Crawler
from ocdsindex.extract import extract_sphinx
from tests import expected


def test_get_documents_by_language():
    crawler = Crawler(os.path.join("tests", "fixtures"), "https://standard.open-contracting.org/dev/", extract_sphinx)
    documents = crawler.get_documents_by_language()

    assert set(documents) == set(expected)
