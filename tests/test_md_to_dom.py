import unittest

from ytelegraph import md_to_dom


class MarkdownToDomTests(unittest.TestCase):
    def test_preserves_spaces_around_inline_formatting(self) -> None:
        dom = md_to_dom("This is **bold** text and `code`.")

        self.assertEqual(
            dom,
            [
                {
                    "tag": "p",
                    "children": [
                        "This is ",
                        {"tag": "strong", "children": ["bold"]},
                        " text and ",
                        {"tag": "code", "children": ["code"]},
                        ".",
                    ],
                }
            ],
        )

    def test_converts_headings_links_and_lists(self) -> None:
        dom = md_to_dom(
            "# Title\n\n"
            "- **Bold text:** Use `**text**` to make text **bold**.\n\n"
            "[Docs](https://telegra.ph/api)"
        )

        self.assertEqual(dom[0], {"tag": "h3", "children": ["Title"]})
        self.assertEqual(dom[1]["tag"], "ul")
        self.assertEqual(dom[1]["children"][0]["tag"], "li")
        self.assertEqual(
            dom[2],
            {
                "tag": "p",
                "children": [
                    {
                        "tag": "a",
                        "attrs": {"href": "https://telegra.ph/api"},
                        "children": ["Docs"],
                    }
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
