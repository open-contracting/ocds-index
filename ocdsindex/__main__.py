import json
import sys
import time
from netrc import netrc
from urllib.parse import urlsplit

import click
import elasticsearch

from ocdsindex.allow import allow_sphinx
from ocdsindex.crawler import Crawler
from ocdsindex.extract import extract_sphinx


def connect(host, **kwargs):
    try:
        credentials = netrc().authenticators(urlsplit(host).hostname)
    except FileNotFoundError:
        pass
    else:
        if credentials:
            kwargs["basic_auth"] = (credentials[0], credentials[2])

    return elasticsearch.Elasticsearch([host], node_class="requests", **kwargs)


@click.group()
def main():
    pass


@main.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.argument("base-url")
def sphinx(directory, base_url):
    """
    Crawl the DIRECTORY of the Sphinx build of the OCDS documentation, generate documents to index, assign documents
    unique URLs from the BASE_URL, and print the base URL, timestamp, and documents as JSON.
    """
    documents = Crawler(directory, base_url, extract_sphinx, allow=allow_sphinx).get_documents_by_language()
    json.dump({"base_url": base_url, "created_at": int(time.time()), "documents": documents}, sys.stdout)


@main.command()
@click.argument("file", type=click.File())
def extension_explorer(file):
    """
    Crawl the Extension Explorer's `extensions.json` file, generate documents to index, assign documents unique
    URLs, and print the base URL, timestamp, and documents as JSON.
    """
    "https://extensions.open-contracting.org"


@main.command()
@click.argument("host")
@click.argument("file", type=click.File())
def index(file, host):
    """
    Add documents to Elasticsearch indices.

    Read a JSON file in which the "base_url" key is the remote URL at which the documents will be accessible, and the
    "documents" key is an object in which the key is a language code and the value is the documents to index.

    The `sphinx` and `extension-explorer` commands create such files.

    Connect to Elasticsearch at HOST and, for each language, create an `ocdsindex_XX` index, delete existing
    documents matching the base URL, and index the new documents in that language.
    """
    language_map = {
        "en": "english",
        "es": "spanish",
        "fr": "french",
        "it": "italian",
    }

    data = json.load(file)

    with connect(host) as es:
        body = []

        for language_code, documents in data["documents"].items():
            index = f"ocdsindex_{language_code}"

            if not es.indices.exists(index=index):
                # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/analysis-lang-analyzer.html
                language = language_map.get(language_code, "standard")

                # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/indices-create-index.html
                es.indices.create(
                    index=index,
                    # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/mapping.html
                    mappings={
                        "properties": {
                            "title": {"type": "text", "analyzer": language},
                            "text": {"type": "text", "analyzer": language},
                            "created_at": {"type": "date"},
                            "base_url": {"type": "keyword"},
                        },
                    },
                )

            # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/docs-delete-by-query.html
            es.delete_by_query(index=index, query={"term": {"base_url": data["base_url"]}})

            # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/docs-bulk.html
            for document in documents:
                document["base_url"] = data["base_url"]
                document["created_at"] = data["created_at"]

                body.append({"index": {"_index": index, "_id": document["url"]}})
                body.append(document)

        es.bulk(operations=body)


@main.command()
@click.argument("host")
@click.argument("source")
@click.argument("destination")
def copy(host, source, destination):
    """Add a document with a DESTINATION base URL for each document with a SOURCE base URL."""
    with connect(host) as es:
        body = []

        for index_result in es.cat.indices(format="json"):
            index = index_result["index"]
            for hit in es.search(index=index, size=10000, query={"term": {"base_url": source}})["hits"]["hits"]:
                document = hit["_source"]
                for field in ("url", "base_url"):
                    document[field] = document[field].replace(source, destination)

                body.append({"index": {"_index": index, "_id": document["url"]}})
                body.append(document)

        es.bulk(operations=body)


@main.command()
@click.argument("host")
@click.option(
    "--exclude-file", type=click.File(), help="exclude any document whose base URL is equal to a line in this file"
)
def expire(host, exclude_file):
    """Delete documents from Elasticsearch indices that were crawled more than 180 days ago."""
    threshold = int(time.time()) - 15552000  # 180 days

    base_urls = [line.strip() for line in exclude_file] if exclude_file else []

    with connect(host) as es:
        for index_result in es.cat.indices(format="json"):
            es.delete_by_query(
                index=index_result["index"],
                query={
                    "bool": {
                        "must": {
                            "range": {"created_at": {"lt": threshold}},
                        },
                        "must_not": {
                            "terms": {"base_url": base_urls},
                        },
                    }
                },
            )


if __name__ == "__main__":
    main()
