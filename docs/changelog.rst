Changelog
=========

0.2.0 (2023-03-13)
------------------

To run tests locally, set the ``REQUESTS_CA_BUNDLE`` environment variable to e.g. ``path/to/elasticsearch/config/certs/http_ca.crt``, and add the basic authentication credentials to ``$HOME/.netrc``.

Added
~~~~~

-  Add support for Elasticsearch 8.

Changed
~~~~~~~

-  The ``ELASTICSEARCH_URL`` environment variable must set a scheme.
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

Changed
~~~~~~~

-  Drop support for Sphinx 3.x.
-  Drop support for Python 3.6 (end-of-life 2021-12-23).

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
