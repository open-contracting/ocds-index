import json
import sys

import click

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


main.add_command(sphinx)
main.add_command(extension_explorer)

if __name__ == "__main__":
    main()
