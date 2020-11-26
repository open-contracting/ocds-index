import json
import sys
from urllib.parse import urljoin

import click
import elasticsearch

from ocdsindex.crawler import Crawler
from ocdsindex.extract import extract_extension_explorer, extract_sphinx


def dump(directory, base_url, extract, **kwargs):
    documents = Crawler(directory, base_url, extract, **kwargs).get_documents_by_language()
    json.dump({"base_url": base_url, "documents": documents}, sys.stdout)


@click.group()
def main():
    pass


@click.command()
@click.argument("directory")
@click.argument("base-url")
def sphinx(directory, base_url):
    """
    Crawls the DIRECTORY of the Sphinx build of the OCDS documentation, generates documents to index, assigns documents
    unique URLs from the BASE_URL, and prints the base URL and documents as JSON.
    """
    dump(directory, base_url, extract_sphinx)


@click.command()
@click.argument("directory")
def extension_explorer(directory):
    """
    Crawls the DIRECTORY containing the Extension Explorer's built documentation, generates documents to index, assigns
    documents unique URLs, and prints the base URL and documents as JSON.
    """
    base_url = "https://extensions.open-contracting.org"
    dump(directory, base_url, extract_extension_explorer)


@click.command()
@click.argument("filename")
@click.argument("host")
def index(filename, host):
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

    with click.open_file(filename) as f:
        data = json.load(f)

    for language_code, documents in data["documents"].items():
        es = elasticsearch.Elasticsearch([host])

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
            body.append({"index": {"_index": index, "_id": document["url"]}})
            body.append(document)
        es.bulk(body)


main.add_command(sphinx)
main.add_command(extension_explorer)
main.add_command(index)

if __name__ == "__main__":
    main()
