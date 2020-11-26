OCDS Index |release|
====================

.. include:: ../README.rst

To install:

.. code-block:: bash

   pip install ocdsindex

.. toctree::
   :maxdepth: 2
   :caption: Contents

   cli
   library
   changelog

How it works
------------

1. Build
~~~~~~~~

The repositories for standard documentation, `profiles <https://github.com/open-contracting/standard_profile_template>`__ and the `Extension Explorer <https://github.com/open-contracting/extension-explorer>`__ contain scripts to build HTML files under language directories, like:

.. code-block:: none

   build/
   ├── en
   │   ├── governance
   │   │   ├── deprecation
   │   │   │   └── index.html
   │   │   └── index.html
   …   …
   ├── es
   │   ├── governance
   │   │   ├── deprecation
   │   │   │   └── index.html
   │   │   └── index.html
   …   …

A build is triggered locally, and more commonly as part of continuous integration: for example, as part of a GitHub Actions `workflow <https://github.com/open-contracting/standard_profile_template/blob/master/.github/workflows/ci.yml#L24-L28>`__.

The HTML files are uploaded to a web server, and served as a static website like the `OCDS documentation <https://standard.open-contracting.org/latest/>`__, which includes a search box.

2. Crawl
~~~~~~~~

Once the HTML files are built, this tool crawls the files and extracts the documents to index. This work is performed by the :ref:`sphinx` or :ref:`extension-explorer` command, producing a JSON file for the next step.

An HTML file can contain one or more documents. Heading elements, like ``<h1>``, typically mark the start of a new document. A document follows this format:

url
  The remote URL of the document, which might include a fragment identifier. The tool is provided the base URL of the website whose files are crawled, so that the tool can construct the remote URL of document. For example, a base URL of:

  .. code-block:: none

     https://standard.open-contracting.org/staging/profiles/ppp/1.0-dev/

  yields remote URLs like:

  .. code-block:: none

     https://standard.open-contracting.org/staging/profiles/ppp/1.0-dev/es/overview/#data

title
  The title of the document, which might be the page title and the heading text.
text
  The plain text content of the document.

3. Index
~~~~~~~~

This tool then adds the extracted documents to Elasticsearch indices. This work is performed by the :ref:`index` command.

The tool creates a single index for all documents in a given language: for example, ``ocdsindex_es``. As such, an interface can search across all websites in a given language.

It adds three fields to each indexed document:

_id
  Same as ``url``.
base_url
  The base URL of the website whose files were crawled.
created_at
  The timestamp at which the files were crawled.

As such, an interface can filter on ``base_url`` to limit results to specific websites, and the tool can filter on ``created_at`` to delete documents that are no longer needed.

Copyright (c) 2020 Open Contracting Partnership, released under the BSD license
