import os.path
from contextlib import contextmanager

import lxml.html
from elasticsearch import Elasticsearch

expected = {
    "en": [
        {
            "url": "https://standard.open-contracting.org/dev/en/#about",
            "title": "Open Contracting Data Standard: Documentation - About",
            "text": "The Open Contracting Data Standard",
        },
        {
            "url": "https://standard.open-contracting.org/dev/en/guidance/#guidance",
            "title": "Guidance",
            "text": "Are you new to OCDS?",
        },
        {
            "url": "https://standard.open-contracting.org/dev/en/guidance/page/#design",
            "title": "Design",
            "text": "This phase is about setting up your OCDS implementation to be a success.",
        },
        {
            "url": "https://standard.open-contracting.org/dev/en/schema/#merging",
            "title": "Merging",
            "text": "An OCDS record …",
        },
        {
            "url": "https://standard.open-contracting.org/dev/en/schema/#merging-specification",
            "title": "Merging - Merging specification",
            "text": "",
        },
        {
            "url": "https://standard.open-contracting.org/dev/en/schema/#merge-routine",
            "title": "Merging - Merge routine",
            "text": "To create a compiled or versioned release, you must:\nGet all releases with the same ocid value",
        },
        {
            "url": "https://standard.open-contracting.org/dev/en/schema/#array-values",
            "title": "Merging - Array values",
            "text": "If the input array contains anything other than objects, treat the array as a literal value. "
            "Otherwise, there are two sub-routines for arrays of objects: whole list merge and identifier merge.",
        },
        {
            "url": "https://standard.open-contracting.org/dev/en/schema/#whole-list-merge",
            "title": "Merging - Whole list merge",
            "text": "An input array must be treated as a literal value if the corresponding field in a dereferenced "
            'copy of the release schema has "array" in its type and if any of the following are also true:',
        },
    ],
    "es": [
        {
            "url": "https://standard.open-contracting.org/dev/es/#about",
            "title": "Estándar de Datos de Contrataciones Abiertas: Documentación - Acerca de",
            "text": "El Estándar de Datos de Contratación Abierta",
        }
    ],
}


def parse(*parts):
    with open(os.path.join("tests", "fixtures", *parts)) as f:
        return lxml.html.fromstring(f.read())


@contextmanager
def elasticsearch(host):
    try:
        es = Elasticsearch([host])
        yield es
    finally:
        es.indices.delete(index="ocdsindex_en", ignore=[404])
        es.indices.delete(index="ocdsindex_es", ignore=[404])


def search(es, index):
    es.indices.refresh(index)

    return es.search(index=index)["hits"]
