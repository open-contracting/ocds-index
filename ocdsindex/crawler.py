import os
from collections import defaultdict
from urllib.parse import urljoin

import lxml.html


def true(root, file):
    return True


class Crawler:
    """
    Crawls a directory for documents to index.
    """

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
        Returns the documents to index for each language.

        :returns: a dict in which the key is a language code and the value is the documents to index
        :rtype: dict
        """
        documents = defaultdict(list)

        for entry in os.scandir(self.directory):
            if not entry.is_dir() or len(entry.name) != 2:  # not an ISO 639-1 language code directory
                continue

            for root, dirs, files in os.walk(entry.path):
                for file in files:
                    if self.allow(root, file):
                        documents[entry.name].extend(self.get_documents_from_file(os.path.join(root, file)))

        return documents

    def get_documents_from_file(self, path):
        """
        Parses the file's HTML contents, calculates its remote URL, and returns the documents to index from the file.

        :param str path: a file path
        :returns: the documents to index
        :rtype: list
        """
        if not path.endswith(".html"):
            return []

        with open(path) as f:
            content = f.read()

        url = urljoin(self.base_url, os.path.relpath(path, self.directory).replace(os.sep, "/"))
        if url.endswith("/index.html"):
            url = url[:-10]
        tree = lxml.html.fromstring(content)

        return self.extract(url, tree)
