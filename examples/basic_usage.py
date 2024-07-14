from ytelegraph import TelegraphAPI

ph = TelegraphAPI()
content = "# Hello, Telegraph!\n\nThis is my first Telegraph page using YTelegraph."
ph_link = ph.create_page_md("My First Page", content)
print(
    f"Your page is live at: \nYou may wanna save this somewhere\n{ph_link}\nAnd you may wanna try the second example too!"
)
