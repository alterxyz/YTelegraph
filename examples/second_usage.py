# You may wanna try this after you have run the examples/basic_usage.py

from ytelegraph import account

# see the path, and your token

# Since the basic_usage.py has been run, the token file should be created in the current directory


my_ph = account.TelegraphAccount(
    access_token=""
)  # For real usage, you can leave your token there or leave it empty - it will create a temporary account for you automatically

my_token_file_path = my_ph._get_token_file_path()

my_token = my_ph._get_token()

my_info = my_ph.get_account_info()

print(
    f"\nYour token file path: {my_token_file_path}\nYour token: {my_token}\nYour account info: {my_info}"
)

# login to your account by open the link in your browser

my_auth_url = my_ph.get_authorization_url()

print(
    f"\nYour authorization url: {my_auth_url}\nOpen the link in your browser to login. This link only works once.\nAfter you have logged in, try open the page you created by the basic_usage.py\nYou should see the edit button."
)

input("Press Enter to continue...")

# Next, we will try to edit the page

from ytelegraph import TelegraphAPI

ph = TelegraphAPI()  # or `ph = TelegraphAPI(my_token)``
# Unless you delete the token or restart the env, the automatic created account will be used. So you can leave the token empty. For real usage, you can use your token too.


content = "# Hello, Telegraph!\n\nThis is my first Telegraph page using YTelegraph. \n\nI have edited this page using YTelegraph."

# Path or url like <https://telegra.ph/Sample-Page-12-15> are both accepted
my_path = input(
    "Please provide your page url or path"
)  # replace my_path with your path

ph.edit_page_md(path=my_path, title="My First Page", content=content)

print("Now refresh the page you created, you should see the changes.")

input("Press Enter to continue...")

# Lastly, we will try to delete the page
# Unfortunatelly, telegraph does not provide a way to delete a page, but we can replace all content with meaningless text

print(f"{ph.delete_page(my_path)}")

print(
    f"Now refresh the page you created, you should see the changes.\n\nThanks for trying YTelegraph! Hope you enjoy it!\nAlso thanks to Telegram for providing the Telegraph service!\nPlease do not abuse the service so we can keep good things last longer."
)
