import json
import sys
import time

import click
import elasticsearch

from ocdsindex.allow import allow_sphinx
from ocdsindex.crawler import Crawler
from ocdsindex.extract import extract_sphinx


@click.group()
def main():
    pass


@click.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.argument("base-url")
def sphinx(directory, base_url):
    """
    Crawls the DIRECTORY of the Sphinx build of the OCDS documentation, generates documents to index, assigns documents
    unique URLs from the BASE_URL, and prints the base URL, timestamp, and documents as JSON.
    """
    documents = Crawler(directory, base_url, extract_sphinx, allow=allow_sphinx).get_documents_by_language()
    json.dump({"base_url": base_url, "created_at": int(time.time()), "documents": documents}, sys.stdout)


@click.command()
@click.argument("file", type=click.File())
def extension_explorer(file):
    """
    Crawls the Extension Explorer's `extensions.json` file, generates documents to index, assigns documents unique
    URLs, and prints the base URL, timestamp, and documents as JSON.
    """
    "https://extensions.open-contracting.org"


@click.command()
@click.argument("file", type=click.File())
@click.argument("host")
def index(file, host):
    """
    Adds documents to Elasticsearch indices.

    Reads a JSON file in which the "base_url" key is the remote URL at which the documents will be accessible, and the
    "documents" key is an object in which the key is a language code and the value is the documents to index.

    The `sphinx` and `extension-explorer` commands create such files.

    Connects to Elasticsearch at HOST and, for each language, creates an `ocdsindex_XX` index, deletes existing
    documents matching the base URL, and indexes the new documents in that language.
    """
    language_map = {
        "en": "english",
        "es": "spanish",
        "fr": "french",
        "it": "italian",
    }

    data = json.load(file)

    es = elasticsearch.Elasticsearch([host])

    for language_code, documents in data["documents"].items():
        index = f"ocdsindex_{language_code}"

        if not es.indices.exists(index):
            # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/analysis-lang-analyzer.html
            language = language_map.get(language_code, "standard")

            # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/indices-create-index.html
            es.indices.create(
                index,
                body={
                    # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/mapping.html
                    "mappings": {
                        "properties": {
                            "title": {"type": "text", "analyzer": language},
                            "text": {"type": "text", "analyzer": language},
                            "created_at": {"type": "date"},
                            "base_url": {"type": "keyword"},
                        },
                    },
                },
            )

        # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/docs-delete-by-query.html
        es.delete_by_query(
            index=index,
            body={"query": {"term": {"base_url": data["base_url"]}}},
        )

        # https://www.elastic.co/guide/en/elasticsearch/reference/7.10/docs-bulk.html
        body = []
        for document in documents:
            document["base_url"] = data["base_url"]
            document["created_at"] = data["created_at"]
            body.append({"index": {"_index": index, "_id": document["url"]}})
            body.append(document)
        es.bulk(body)


@click.command()
@click.argument("host")
@click.option(
    "--exclude-file", type=click.File(), help="exclude any document whose base URL is equal to a line in this file"
)
def expire(host, exclude_file):
    """
    Deletes documents from Elasticsearch indices that were crawled more than 180 days ago.
    """
    threshold = int(time.time()) - 15552000  # 180 days

    if exclude_file:
        base_urls = [line.strip() for line in exclude_file]
    else:
        base_urls = []

    es = elasticsearch.Elasticsearch([host])

    for result in es.cat.indices(format="json"):
        es.delete_by_query(
            index=result["index"],
            body={
                "query": {
                    "bool": {
                        "must": {
                            "range": {"created_at": {"lt": threshold}},
                        },
                        "must_not": {
                            "terms": {"base_url": base_urls},
                        },
                    }
                }
            },
        )


main.add_command(sphinx)
main.add_command(extension_explorer)
main.add_command(index)
main.add_command(expire)

if __name__ == "__main__":
    main()
