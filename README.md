# YTelegraph

[![PyPi Package Version](https://img.shields.io/pypi/v/your-telegraph.svg)](https://pypi.python.org/pypi/your-telegraph)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/your-telegraph.svg)](https://pypi.python.org/pypi/your-telegraph)
[![PyPi downloads](https://img.shields.io/pypi/dm/your-telegraph.svg)](https://pypi.org/project/your-telegraph/)
[![PyPi status](https://img.shields.io/pypi/status/your-telegraph.svg?style=flat-square)](https://pypi.python.org/pypi/your-telegraph)
![License](https://img.shields.io/github/license/alterxyz/ytelegraph)

YTelegraph is a simple, user-friendly Python wrapper for the Telegraph API. Publish your content to Telegraph with just a few lines of code!

## Table of Contents

- [YTelegraph](#ytelegraph)
    - [Table of Contents](#table-of-contents)
    - [Installation](#installation)
    - [Quick Start](#quick-start)
    - [Key Features](#key-features)
    - [Why YTelegraph?](#why-ytelegraph)
    - [More Examples](#more-examples)
        - [Create a page from a Markdown file](#create-a-page-from-a-markdown-file)
        - [Use your own Telegraph token](#use-your-own-telegraph-token)
        - [Advanced Usage](#advanced-usage)
    - [Token Management](#token-management)
    - [Create Account](#create-account)
    - [Testing](#testing)
    - [Versioning](#versioning)
    - [Support](#support)
    - [Contributing](#contributing)
    - [License](#license)

## Installation

```bash
pip install your-telegraph
```

## Quick Start

Publish a Telegraph page in just 4 lines of code:

```python
from ytelegraph import TelegraphAPI

ph = TelegraphAPI()
content = "# Hello, Telegraph!\n\nThis is my first Telegraph page using YTelegraph."
ph_link = ph.create_page_md("My First Page", content)
print(f"Your page is live at: {ph_link}")
```

That's it! No need to worry about tokens, account creation, or complex API calls.

## Key Features

- **Simple**: Create and publish Telegraph pages with minimal code.
- **Markdown Support**: Write your content in Markdown and let YTelegraph handle the conversion.
- **Flexible Token Management**: Use your own token or let YTelegraph handle account creation.
- **Full API Access**: For advanced users, complete access to Telegraph API features is available.

## Why YTelegraph?

"All you need is a title and content. That's it. Just like <https://telegra.ph/>, but in Python."

YTelegraph brings the simplicity of Telegraph's web interface to your Python projects. Whether you're creating a bot, a content management system, or just want to quickly publish some content, YTelegraph makes it easy.

## More Examples

### Create a page from a Markdown file

```python
from ytelegraph import TelegraphAPI

ph = TelegraphAPI()

with open('my_article.md', 'r') as f:
    content = f.read()

ph_link = ph.create_page_md("My Article", content)
print(f"Article published at: {ph_link}")
```

### Use your own Telegraph token

```python
from os import environ
from ytelegraph import TelegraphAPI

TELEGRA_PH_TOKEN = environ.get("TELEGRA_PH_TOKEN")

ph = TelegraphAPI(TELEGRA_PH_TOKEN)
```

This method is useful if you want to use an existing Telegraph account or manage tokens yourself.

### Advanced Usage

Try and see the `example/second_usage.py` at [here](examples/second_usage.py).

## Token Management

YTelegraph offers flexible token management:

1. **Automatic**: If no token is provided, YTelegraph creates a new account and manages the token for you.
2. **Environment Variable**: Set the `TELEGRA_PH_TOKEN` environment variable, and YTelegraph will use it automatically.
3. **Direct Input**: Pass your token directly to the `TelegraphAPI` constructor.

Choose the method that best fits your workflow and security requirements.

## Create Account

While YTelegraph handles account creation automatically, you might want to create your own Telegraph account for more control. Here's a quick guide:

1. Visit this URL in your browser (feel free to customize the parameters):
   `https://api.telegra.ph/createAccount?short_name=Sandbox&author_name=Anonymous`

   - Replace `Sandbox` with any name to help you remember this account (only visible to you)
   - Change `Anonymous` to your preferred author name (default for your articles)
   - Or keep them as is – it's totally fine!

2. After accessing the link, you'll see a response like this:

   ```json
   {
     "ok": true,
     "result": {
       "short_name": "Sandbox",
       "author_name": "Anonymous",
       "author_url": "",
       "access_token": "abcedfeghijklmnopqrstuvwxyz",
       "auth_url": "https://edit.telegra.ph/auth/qwertyuiop"
     }
   }
   ```

3. The `access_token` (in this example, `abcedfeghijklmnopqrstuvwxyz`) is what you'll use in your code. (Note: This is not a real token!)

For more details, check out the [Telegraph API documentation](https://telegra.ph/api#createAccount).

YTelegraph makes this process super easy, but it's good to know how to do it manually if you ever need to.

## Testing

To run the basic integration tests, execute the examples in the `examples/` directory:

```bash
python examples/basic_usage.py
python examples/second_usage.py
```

## Versioning

For the versions available, see the [CHANGELOG.md](CHANGELOG.md) file.

## Support

If you encounter any problems or have any questions, please [open an issue](https://github.com/alterxyz/ytelegraph/issues) on our GitHub repository.

## Contributing

We welcome contributions! Feel free to submit issues or pull requests.

## License

YTelegraph is released under the MIT License. See [LICENSE](LICENSE) for details.
