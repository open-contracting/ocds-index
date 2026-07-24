import os
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

import lxml.html


def true(_root, _file):
    return True


class Crawler:
    """Crawl a directory for documents to index."""

    def __init__(self, directory, base_url, extract, *, allow=true):
        """
        :param str directory: the directory to crawl
        :param str base_url: the remote URL at which the files will be available
        :param extract: a function that accepts a file's remote URL and its root HTML element, and returns the
                        documents to index as a list of dicts
        :param allow: a function that accepts a directory path and a file basename, and returns whether to crawl the
                      file as a boolean
        """
        self.directory = directory
        self.base_url = base_url
        self.extract = extract
        self.allow = allow

    def get_documents_by_language(self):
        """
        Return the documents to index for each language.

        :returns: a dict in which the key is a language code and the value is the documents to index
        :rtype: dict
        """
        documents = defaultdict(list)

        # The entries are sorted to make it easier to manually test whether output has changed.
        for entry in sorted(Path(self.directory).iterdir()):
            if not entry.is_dir() or len(entry.name) != 2:  # not an ISO 639-1 language code directory
                continue

            for root, _, files in os.walk(entry):
                for file in files:
                    if self.allow(root, file):
                        documents[entry.name].extend(self.get_documents_from_file(Path(root) / file))

        return documents

    def get_documents_from_file(self, path):
        """
        Parse the file's HTML contents, calculate its remote URL, and return the documents to index from the file.

        :param path: a file path
        :type path: pathlib.Path
        :returns: the documents to index
        :rtype: list
        """
        if path.suffix != ".html":
            return []

        content = path.read_text()

        url = urljoin(self.base_url, path.relative_to(self.directory).as_posix())
        if url.endswith("/index.html"):
            url = url[:-10]
        tree = lxml.html.fromstring(content)

        return self.extract(url, tree)
