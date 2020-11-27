"""
``allow_`` methods that return whether to crawl a file.
"""

import os


def allow_sphinx(root, file):
    """
    :param str root: a directory path
    :param str file: a file basename
    :returns: whether to crawl the file
    :rtype: bool
    """
    return os.path.split(root)[1] not in ("404", "privacy-notice")
