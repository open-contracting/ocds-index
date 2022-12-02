class OCDSIndexError(Exception):
    """Base class for exceptions from within this package"""


class MissingHeadingError(OCDSIndexError, IndexError):
    """Raised when a section is missing a heading"""
