Changelog
=========

0.4.1 (2026-04-01)
------------------

Fixed
~~~~~

-  :ref:`reindex`: Increase request timeout for reindex request.

0.4.0 (2026-03-31)
------------------

Added
~~~~~

-  :ref:`reindex`: New command

Changed
~~~~~~~

-  :ref:`index`: Creates an ``ocdsindex_XX-0001`` index and an ``ocdsindex_XX`` alias, instead of an ``ocdsindex_XX`` index.

0.3.0 (2026-03-27)
------------------

To run tests locally:

-  Run ``docker run`` with ``-e xpack.security.enabled=false -e discovery.type=single-node -p 9200:9200``
-  Run ``pytest`` with ``env ELASTICSEARCH_URL=http://localhost:9200``

Also, add the basic authentication credentials to ``$HOME/.netrc``.

Added
~~~~~

-  Add support for Elasticsearch 9.
-  Add support for Python 3.13, 3.14.

Removed
~~~~~~~

-  Drop support for Elasticsearch 8.
-  Drop support for Python 3.7, 3.8 and 3.9.

0.2.0 (2023-03-13)
------------------

Added
~~~~~

-  Add support for Elasticsearch 8.

Changed
~~~~~~~

-  The ``ELASTICSEARCH_URL`` environment variable must set a scheme.

Removed
~~~~~~~

-  Drop support for Elasticsearch 7.

0.1.1 (2022-12-01)
------------------

Added
~~~~~

-  Log message if section heading not found.

Fixed
~~~~~

-  Extract only within ``role="main"`` element.

0.1.0 (2022-12-01)
------------------

Added
~~~~~

-  Add support for Sphinx 4.x and 5.x.

Removed
~~~~~~~

-  Drop support for Sphinx 3.x.
-  Drop support for Python 3.6.

0.0.7 (2021-04-21)
------------------

Changed
~~~~~~~

-  :ref:`sphinx`: Do not include JSON text in document text.

0.0.6 (2021-04-21)
------------------

Fixed
~~~~~

-  :ref:`sphinx`: Match only the ``section`` class, not the ``tocsection`` class.

0.0.5 (2021-04-10)
------------------

Added
~~~~~

-  Add Python wheels distribution.

0.0.4 (2020-12-23)
------------------

Fixed
~~~~~

-  :ref:`sphinx`: Ignore comment nodes.
-  :ref:`index`, :ref:`copy`, :ref:`expire`: Make netrc file optional.

0.0.3 (2020-12-23)
------------------

Added
~~~~~

-  :ref:`copy`: New command

Changed
~~~~~~~

-  :ref:`index`: ``HOST`` is the first argument, and ``FILE`` is the second argument.
-  :ref:`index`, :ref:`copy`, :ref:`expire`: Added netrc file support.

0.0.2 (2020-11-27)
------------------

Fixed
~~~~~

-  Fix link to ReadTheDocs website.

0.0.1 (2020-11-27)
------------------

First release.
