"""
``extract_`` methods that return the documents to index as a list of dicts. Each dict sets these keys:

url
  The remote URL of the document, which might include a fragment identifier
title
  The title of the document, which might be the page title and the heading text
text
  The plain text content of the document
"""

from lxml import etree


def _extract_sphinx_section(section):
    lines = []

    for node in section.xpath("node()"):
        if isinstance(node, str):  # lxml.etree._ElementUnicodeResult
            text = str(node)
        # Index each section separately. Don't index the title as part of the text.
        elif "section" in node.get("class", "") or node.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            continue
        else:
            text = node.text_content()

        # Normalize whitespace within a single line.
        lines.extend([" ".join(line.split()) for line in text.splitlines()])

    # Compact newlines.
    return "\n".join(filter(None, lines)), section.attrib["id"]


def extract_sphinx(url, tree):
    """
    Extracts one document per section of the page.

    :param str url: the file's remote URL
    :param tree: the file's root HTML element
    :returns: a list of dicts representing the documents to index
    :rtype: list
    """
    # Don't index the text content of script and style HTML elements.
    for element in ("script", "style"):
        etree.strip_elements(tree, element)

    documents = []
    for section in tree.xpath("//div[contains(@class, 'section')]"):
        # Don't index the text content of jsoninclude Sphinx directives.
        if "expandjson" in section.attrib["class"]:
            continue

        title = tree.xpath("//title/text()")[0].split("—")[0].strip()
        section_title = section.xpath("h1|h2|h3|h4|h5|h6")[0].text_content().rstrip("¶")

        if title != section_title:
            title = f"{title} - {section_title}"

        text, section_id = _extract_sphinx_section(section)

        documents.append(
            {
                "url": f"{url}#{section_id}",
                "title": title,
                "text": text,
            }
        )

    return documents


def extract_extension_explorer(url, tree):
    pass
