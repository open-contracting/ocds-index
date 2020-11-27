import os
import traceback
from collections import defaultdict

from click.testing import CliRunner

from ocdsindex.cli.__main__ import main
from tests import elasticsearch, search


def test_copy(tmpdir):
    host = os.getenv("ELASTICSEARCH_URL", "localhost:9200")

    runner = CliRunner()

    with elasticsearch(host) as es:
        result = runner.invoke(main, ["index", host, os.path.join("tests", "fixtures", "data.json")])

        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
        assert result.output == ""

        es.indices.refresh("ocdsindex_en")
        es.indices.refresh("ocdsindex_es")

        source = "https://standard.open-contracting.org/dev/"
        destination = "https://standard.open-contracting.org/copy/"

        result = runner.invoke(main, ["copy", host, source, destination])

        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
        assert result.output == ""

        for index, value in (("ocdsindex_en", 8), ("ocdsindex_es", 1)):
            hits = search(es, index)
            counts = defaultdict(int)

            for hit in hits["hits"]:
                counts[hit["_source"]["base_url"]] += 1

            assert counts == {
                source: value,
                destination: value,
            }
            assert hits["total"]["value"] == value * 2
