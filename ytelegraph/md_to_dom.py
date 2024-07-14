from bs4 import BeautifulSoup
import markdown
from typing import List, Dict, Any, Union


def md_to_dom(markdown_text: str) -> List[Dict[str, Any]]:
    """Converts Markdown text to a Telegraph-compatible DOM structure.

    Args:
        markdown_text: The input Markdown text to be converted.

    Returns:
        list: A list of dictionaries representing the DOM structure.
            Each dictionary represents a single HTML element and its
            attributes. For example:

            ```python
            [
                {
                    "tag": "p",
                    "children": ["This is a paragraph."]
                },
                {
                    "tag": "a",
                    "attrs": {
                        "href": "https://example.com"
                    },
                    "children": ["Link text"]
                }
            ]
            ```
    """
    html = markdown.markdown(markdown_text, extensions=["extra", "sane_lists"])
    soup = BeautifulSoup(html, "html.parser")
    return [parse_element(element) for element in soup.contents if element.name]


def parse_element(element) -> Dict[str, Any]:
    """Parses an HTML element to a Telegraph-compatible format.

    Args:
        element: The HTML element to parse. This should be a
            `bs4.element.Tag` object.

    Returns:
        dict: A dictionary representing the parsed element.
            The dictionary will have a "tag" key indicating the
            element type, and may have "attrs" and "children" keys
            for attributes and child elements, respectively.
    """
    tag_dict = {"tag": element.name}

    if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        tag_dict = handle_heading(element)
    elif element.name in ["ul", "ol"]:
        tag_dict = handle_list(element)
    elif element.name == "a":
        tag_dict = handle_link(element)
    elif element.name in ["img", "iframe"]:
        return handle_media(element)
    else:
        tag_dict["children"] = parse_children(element)

    return tag_dict


def handle_heading(element) -> Dict[str, Any]:
    """Converts heading elements to Telegraph-compatible format.

    Args:
        element: The heading element to convert.

    Returns:
        dict: A dictionary representing the converted heading.
            H1 and H2 headings are converted to H3 and H4
            respectively, while other headings are converted to
            paragraphs with strong text.
    """
    if element.name == "h1":
        return {"tag": "h3", "children": parse_children(element)}
    elif element.name == "h2":
        return {"tag": "h4", "children": parse_children(element)}
    else:
        return {
            "tag": "p",
            "children": [{"tag": "strong", "children": parse_children(element)}],
        }


def handle_list(element) -> Dict[str, Any]:
    """Converts list elements to Telegraph-compatible format.

    Args:
        element: The list element to convert.

    Returns:
        dict: A dictionary representing the converted list.
    """
    return {
        "tag": element.name,
        "children": [
            {"tag": "li", "children": parse_children(li)}
            for li in element.find_all("li", recursive=False)
        ],
    }


def handle_link(element) -> Dict[str, Any]:
    """Converts link elements to Telegraph-compatible format.

    Args:
        element: The link element to convert.

    Returns:
        dict: A dictionary representing the converted link.
    """
    return {
        "tag": "a",
        "attrs": {"href": element.get("href")},
        "children": parse_children(element),
    }


def handle_media(element) -> Dict[str, Any]:
    """Converts media elements to Telegraph-compatible format.

    Args:
        element: The media element to convert.

    Returns:
        dict: A dictionary representing the converted media element.
    """
    return {"tag": element.name, "attrs": {"src": element.get("src")}}


def parse_children(element) -> List[Union[str, Dict[str, Any]]]:
    """Parses the children of an HTML element.

    Args:
        element: The parent HTML element.

    Returns:
        list: A list of parsed child elements. Each element in the
            list is either a string representing text content, or
            a dictionary representing a child element.
    """
    return [
        parse_element(child) if child.name else child.strip()
        for child in element.children
        if child.name or (isinstance(child, str) and child.strip())
    ]


ALLOWED_TAGS = {
    "a",
    "aside",
    "b",
    "blockquote",
    "br",
    "code",
    "em",
    "figcaption",
    "figure",
    "h3",
    "h4",
    "hr",
    "i",
    "iframe",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "strong",
    "u",
    "ul",
    "video",
}
