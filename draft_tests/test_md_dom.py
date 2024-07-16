import json


def print_json(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))


from ytelegraph import md_to_dom, TelegraphAPI

ph = TelegraphAPI()

attempts = 3
dom = md_to_dom(f"# Error\n\nAttempted {attempts} times")
print(dom)


old_content = ph.get_page("Answer-it-07-16-3")
append_front = dom + old_content["content"]  # This is now
# append_front = dom + old_content # This is desired
print(append_front)
print_json(append_front)

dom = [
    {"tag": "h3", "children": ["Appended to front"]},
    {
        "tag": "h3",
        "attrs": {"id": "Initial-Markdown"},
        "children": ["Initial Markdown"],
    },
    {"tag": "p", "children": ["This is the initial markdown content."]},
    {
        "tag": "p",
        "children": [
            "We will test get_page and edit_page by appending content to both the front and back of this page."
        ],
    },
]

print_json(dom)
