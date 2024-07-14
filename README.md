# YTelegraph

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
    - [Token Management](#token-management)
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

## Token Management

YTelegraph offers flexible token management:

1. **Automatic**: If no token is provided, YTelegraph creates a new account and manages the token for you.
2. **Environment Variable**: Set the `TELEGRA_PH_TOKEN` environment variable, and YTelegraph will use it automatically.
3. **Direct Input**: Pass your token directly to the `TelegraphAPI` constructor.

Choose the method that best fits your workflow and security requirements.

## Testing

To run the basic integration tests, execute the examples in the `examples/` directory:

```bash
python examples/basic_usage.py
python examples/advanced_usage.py
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [CHANGELOG.md](CHANGELOG.md) file.

## Support

If you encounter any problems or have any questions, please [open an issue](https://github.com/alterxyz/ytelegraph/issues) on our GitHub repository.

## Contributing

We welcome contributions! Feel free to submit issues or pull requests.

## License

YTelegraph is released under the MIT License. See [LICENSE](LICENSE) for details.