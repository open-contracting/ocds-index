Command-Line Interface
======================

The netrc file is supported by commands that interact with Elasticsearch.

.. _sphinx:

sphinx
------

Prints the URL and the documents to index from the OCDS documentation as JSON.

.. code-block:: bash

   ocdsindex sphinx DIRECTORY BASE_URL

-  ``DIRECTORY``: the directory to crawl, containing language directories and HTML files
-  ``BASE_URL``: the URL of the website whose files are crawled

Example:

.. code-block:: bash

   ocdsindex sphinx path/to/standard/build/ https://standard.open-contracting.org/staging/1.1-dev/ > data.json

The output looks like:

.. code-block:: json

   {
     "base_url": "https://standard.open-contracting.org/staging/1.1-dev/",
     "created_at": 1577880000,
     "documents": {
       "en": [
         {
           "url": "https://standard.open-contracting.org/staging/1.1-dev/en/#about",
           "title": "Open Contracting Data Standard: Documentation - About",
           "text": "The Open Contracting Data Standard …"
         },
         ...
       ],
       ...
     }
   }

.. _extension-explorer:

extension-explorer
------------------

Prints the URL and the documents to index from the Extension Explorer as JSON.

.. code-block:: bash

   ocdsindex extension-explorer FILE

-  ``FILE``: the Extension Explorer's `extensions.json <https://github.com/open-contracting/extension-explorer#get-extensions-data>`__ file

Example:

.. code-block:: bash

   ocdsindex extension-explorer path/to/extension_explorer/data/extensions.json > data.json

.. _index:

index
-----

Adds documents to Elasticsearch indices.

.. code-block:: bash

   ocdsindex index HOST FILE

-  ``HOST``: the connection URI for Elasticsearch, like ``https://user:pass@host:9200``
-  ``FILE``: the file containing the output of the ``sphinx`` or ``extension-explorer`` command

Example:

.. code-block:: bash

   ocdsindex index https://user:pass@host:9200 data.json

.. _copy:

copy
----

Adds a document with a DESTINATION base URL for each document with a SOURCE base URL.

.. code-block:: bash

   ocdsindex copy HOST SOURCE DESTINATION

-  ``HOST``: the connection URI for Elasticsearch, like ``https://user:pass@host:9200``
-  ``SOURCE``: the base URL of the documents to copy
-  ``DESTINATION``: the base URL of the documents to create

Example:

.. code-block:: bash

   ocdsindex copy https://user:pass@host:9200 https://standard.open-contracting.org/staging/latest/ https://standard.open-contracting.org/latest/

.. _expire:

expire
------

Deletes documents from Elasticsearch indices that were crawled more than 180 days ago.

.. code-block:: bash

   ocdsindex expire HOST --exclude-file FILENAME

-  ``HOST``: the connection URI for Elasticsearch, like ``https://user:pass@host:9200``
-  ``--exclude-file FILENAME``: exclude any document whose base URL is equal to a line in this file

Example:

.. code-block:: bash

   ocdsindex expire https://user:pass@host:9200 --exclude-file exclude.txt

Where ``exclude.txt`` contains:

.. code-block:: none

   https://standard.open-contracting.org/latest/
   https://standard.open-contracting.org/1.1/
