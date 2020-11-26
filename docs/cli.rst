Command-Line Interface
======================

sphinx
------

Prints the URL and the documents to index from the OCDS documentation as JSON.

* ``directory``: the directory to crawl
* ``base-url``: the URL at which the directory will be deployed

Example:

.. code-block:: bash

   ocdsindex sphinx path/to/standard/build/ https://standard.open-contracting.org/staging/1.1-dev/ > data.json

extension-explorer
------------------

Prints the URL and the documents to index from the Extension Explorer as JSON.

* ``directory``: the directory to crawl

.. note::

   ``base_url`` is hardcoded to ``https://extensions.open-contracting.org``.

Example:

.. code-block:: bash

   ocdsindex extension-explorer path/to/extension_explorer/build/ > data.json
