import os
import traceback

from click.testing import CliRunner

from ocdsindex.__main__ import main
from tests import elasticsearch, search


def test_reindex(tmpdir):
    host = os.getenv("ELASTICSEARCH_URL", "https://localhost:9200")

    runner = CliRunner()

    with elasticsearch(host) as es:
        result = runner.invoke(main, ["index", host, os.path.join("tests", "fixtures", "success", "data.json")])
        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)

        index_en_before = next(iter(es.indices.get_alias(name="ocdsindex_en")))
        index_es_before = next(iter(es.indices.get_alias(name="ocdsindex_es")))

        hits_en_before = search(es, "ocdsindex_en")["total"]["value"]
        hits_es_before = search(es, "ocdsindex_es")["total"]["value"]

        result = runner.invoke(main, ["reindex", host])
        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
        assert result.output == ""

        # Old indices were deleted.
        assert not es.indices.exists(index=index_en_before)
        assert not es.indices.exists(index=index_es_before)

        # Documents are copied.
        assert search(es, "ocdsindex_en")["total"]["value"] == hits_en_before
        assert search(es, "ocdsindex_es")["total"]["value"] == hits_es_before

        # Aliases still resolve.
        assert es.indices.exists(index="ocdsindex_en")
        assert es.indices.exists(index="ocdsindex_es")
