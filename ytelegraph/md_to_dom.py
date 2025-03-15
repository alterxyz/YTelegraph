from mistletoe import Document, block_token, span_token
from mistletoe.base_renderer import BaseRenderer



class TelegraphDomRenderer(BaseRenderer):
    """
    A custom renderer that converts a mistletoe AST into a DOM list
    of dictionaries for Telegraph. Each dictionary represents a node
    with a tag, optional attributes, and children.
    """
    def render_document(self, token: block_token.Document):
        # The top-level document returns a list of nodes.
        return [self.render(child) for child in token.children]

    def render_paragraph(self, token: block_token.Paragraph):
        return {"tag": "p", "children": self.render_inner(token)}

    def render_heading(self, token: block_token.Heading):
        # Mimic original behavior:
        # - h1 -> h3, h2 -> h4
        # - Other headings -> paragraph with strong text.
        if token.level == 1:
            return {"tag": "h3", "children": self.render_inner(token)}
        elif token.level == 2:
            return {"tag": "h4", "children": self.render_inner(token)}
        else:
            return {"tag": "p", "children": [{"tag": "strong", "children": self.render_inner(token)}]}

    def render_list(self, token: block_token.List):
        # If token.start is not None, we treat it as an ordered list (ol), otherwise unordered (ul).
        tag = "ol" if token.start is not None else "ul"
        # token.children should be ListItem tokens.
        return {"tag": tag, "children": [self.render(child) for child in token.children]}

    def render_list_item(self, token: block_token.ListItem):
        return {"tag": "li", "children": self.render_inner(token)}

    def render_strong(self, token: span_token.Strong):
        return {"tag": "strong", "children": self.render_inner(token)}

    def render_emphasis(self, token: span_token.Emphasis):
        return {"tag": "em", "children": self.render_inner(token)}

    def render_inline_code(self, token: span_token.InlineCode):
        # Return inline code as a code tag.
        # token.content should hold the text.
        return {"tag": "code", "children": [token.children[0].content if token.children else token.content]}

    def render_strikethrough(self, token: span_token.Strikethrough):
        return {"tag": "del", "children": self.render_inner(token)}

    def render_image(self, token: span_token.Image):
        # Build an image element with its src and optional alt/title.
        attrs = {"src": token.src}
        alt_text = self.render_inner(token)
        if alt_text:
            attrs["alt"] = alt_text
        if token.title:
            attrs["title"] = token.title
        return {"tag": "img", "attrs": attrs}

    def render_link(self, token: span_token.Link):
        attrs = {"href": token.target}
        if token.title:
            attrs["title"] = token.title
        return {"tag": "a", "attrs": attrs, "children": self.render_inner(token)}

    def render_auto_link(self, token: span_token.AutoLink):
        # AutoLink tokens are similar to link tokens.
        return {"tag": "a", "attrs": {"href": token.target}, "children": [token.target]}

    def render_raw_text(self, token: span_token.RawText):
        return token.content

    def render_line_break(self, token: span_token.LineBreak):
        # For a soft break, return a newline; otherwise, a <br> element.
        if token.soft:
            return "\n"
        else:
            return {"tag": "br"}

    def render_block_code(self, token: block_token.BlockCode):
        # Return code block as <pre><code> structure.
        code_dict = {"tag": "code", "children": [token.content]}
        if token.language:
            code_dict.setdefault("attrs", {})["class"] = "language-" + token.language
        return {"tag": "pre", "children": [code_dict]}

    def render_quote(self, token: block_token.Quote):
        return {"tag": "blockquote", "children": self.render_inner(token)}

    def render_thematic_break(self, token: block_token.ThematicBreak):
        return {"tag": "hr"}

    def render_html_block(self, token: block_token.HTMLBlock):
        # If raw HTML is encountered, you may choose to either ignore it
        # or return it as plain text. Here we return it as a text node.
        return token.content

    def render_html_span(self, token: span_token.HTMLSpan):
        return token.content

    def render_inner(self, token):
        """
        Helper method that renders all children of a token.
        If a child rendering returns a list, it is flattened.
        """
        result = []
        for child in token.children:
            rendered = self.render(child)
            if isinstance(rendered, list):
                result.extend(rendered)
            else:
                result.append(rendered)
        return result


def md_to_dom(markdown_text: str):
    """
    Converts Markdown text to a Telegraph-compatible DOM structure.

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
    """
    with TelegraphDomRenderer() as renderer:
        # The Document token is the root of the AST.
        ast = renderer.render(Document(markdown_text))
        return ast

