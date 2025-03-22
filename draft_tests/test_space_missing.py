from ytelegraph import TelegraphAPI

ph = TelegraphAPI()
content = "- **Bold text:** Use `**text**` to make text **bold**."
ph_link = ph.create_page_md("My First Page", content)
print(f"Your page is live at: {ph_link}")

# https://telegra.ph/My-First-Page-03-22-3