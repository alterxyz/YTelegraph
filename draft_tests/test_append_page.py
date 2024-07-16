from ytelegraph import md_to_dom, TelegraphAPI

ph = TelegraphAPI()

init_md = "# Initial Markdown\n\nThis is the initial markdown content.\n\nWe will test get_page and edit_page by appending content to both the front and back of this page."

ph_link = ph.create_page_md("Append testing", init_md)

print(f"{ph_link}\n has been created.\nPlease check,")

ph.edit_page_md(ph_link, "Hello, World!")

append_to_front = (
    md_to_dom("# Title\n\nThis should at the front") + ph.get_page(ph_link)["content"]
)

ph.edit_page(path=ph_link, content=append_to_front)

input(
    f"{ph_link}\n has been appended to at the front.\nPlease check,\nthen press Enter to continue...\n"
)

append_to_back = ph.get_page(ph_link)["content"] + md_to_dom(
    "# End\n\nThis should be at the end"
)

ph.edit_page(ph_link, append_to_back)

input(
    f"{ph_link}\n has been appended to at the back.\nPlease check\nPress CTRL+C to exit.\nOr press Enter to continue to display the page content...\n"
)

import json


def print_json(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))


print_json(ph.get_page(ph_link))

input("Try again with more direct way? Press Enter to continue...\n")

init_md = "# Initial Markdown\n\nThis is the initial markdown content.\n\nWe will test get_page and edit_page by appending content to both the front and back of this page."

ph_link = ph.create_page_md("Append testing", init_md)

print(f"{ph_link}\n has been created.\nPlease check,")

ph.edit_page_md(ph_link, init_md)

ph.edit_page_md_append_to_front(ph_link, "# Appended to front")

ph.edit_page_md_append_to_back(ph_link, "\nAppended to back")

print(f"Appended to front.\nPlease check,")
