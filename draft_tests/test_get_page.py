# `python setup.py develop` to install the package locally
# https://telegra.ph/Answer-it-07-16-2

from ytelegraph import TelegraphAPI

ph = TelegraphAPI()

import json


def print_json(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))


get_path = ph.get_page("Answer-it-07-16-3")

print_json(get_path)

input("Press Enter to continue...\nNext is link rather than path\n")

get_link = ph.get_page("https://telegra.ph/Answer-it-07-16-2")

print_json(get_link)

input("Press Enter to continue...\nNext is max_retries and retry_delay. Should fail\n")

get_fail = ph.get_page("your-page-path", max_retries=3, retry_delay=0.1)

print(get_fail)

print_json(get_fail)
