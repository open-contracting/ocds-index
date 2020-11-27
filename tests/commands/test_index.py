import json
import os
import traceback
from contextlib import contextmanager

from click.testing import CliRunner
from elasticsearch import Elasticsearch

from ocdsindex.cli.__main__ import main


@contextmanager
def elasticsearch(host):
    try:
        es = Elasticsearch([host])
        yield es
    finally:
        es.indices.delete(index="ocdsindex_en", ignore=[404])
        es.indices.delete(index="ocdsindex_es", ignore=[404])


def search(es):
    # Force refresh.
    es.indices.refresh("ocdsindex_en")
    es.indices.refresh("ocdsindex_es")

    return es.search(index="ocdsindex_en")["hits"], es.search(index="ocdsindex_es")["hits"]


def test_index(tmpdir):
    runner = CliRunner()

    filename = tmpdir.join("data.json")
    with open(os.path.join("tests", "fixtures", "data.json")) as f:
        data = json.load(f)

    host = os.getenv("ELASTICSEARCH_URL", "localhost:9200")

    with elasticsearch(host) as es:
        filename.write(json.dumps(data))
        result = runner.invoke(main, ["index", str(filename), host])

        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
        assert result.output == ""

        assert es.indices.exists("ocdsindex_en")
        assert es.indices.exists("ocdsindex_es")

        assert es.indices.get("ocdsindex_en")["ocdsindex_en"]["mappings"] == {
            "properties": {
                "title": {"analyzer": "english", "type": "text"},
                "text": {"analyzer": "english", "type": "text"},
                "base_url": {"type": "keyword"},
                "created_at": {"type": "date"},
                "url": {"fields": {"keyword": {"ignore_above": 256, "type": "keyword"}}, "type": "text"},
            }
        }
        assert es.indices.get("ocdsindex_es")["ocdsindex_es"]["mappings"] == {
            "properties": {
                "title": {"analyzer": "spanish", "type": "text"},
                "text": {"analyzer": "spanish", "type": "text"},
                "base_url": {"type": "keyword"},
                "created_at": {"type": "date"},
                "url": {"fields": {"keyword": {"ignore_above": 256, "type": "keyword"}}, "type": "text"},
            }
        }

        hits_en, hits_es = search(es)

        assert hits_en["total"]["value"] == 8
        assert hits_es["total"]["value"] == 1

        assert {
            "_id": "https://standard.open-contracting.org/dev/en/#about",
            "_index": "ocdsindex_en",
            "_score": 1.0,
            "_source": {
                "title": "Open Contracting Data Standard: " "Documentation - About",
                "text": "The Open Contracting Data Standard",
                "base_url": "https://standard.open-contracting.org/dev/",
                "created_at": 1577880000,
                "url": "https://standard.open-contracting.org/dev/en/#about",
            },
            "_type": "_doc",
        } in hits_en["hits"]
        assert {
            "_id": "https://standard.open-contracting.org/dev/es/#about",
            "_index": "ocdsindex_es",
            "_score": 1.0,
            "_source": {
                "title": "Estándar de Datos de Contrataciones Abiertas: " "Documentación - Acerca de",
                "text": "El Estándar de Datos de Contratación Abierta",
                "base_url": "https://standard.open-contracting.org/dev/",
                "created_at": 1577880000,
                "url": "https://standard.open-contracting.org/dev/es/#about",
            },
            "_type": "_doc",
        } in hits_es["hits"]

        # Re-index

        data["documents"]["en"] = [data["documents"]["en"][-1]]
        data["documents"].pop("es")

        filename.write(json.dumps(data))
        result = runner.invoke(main, ["index", str(filename), host])

        assert result.exit_code == 0, traceback.print_exception(*result.exc_info)
        assert result.output == ""

        hits_en, hits_es = search(es)

        assert hits_en["total"]["value"] == 1
        assert hits_es["total"]["value"] == 1