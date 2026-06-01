from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="your-telegraph",
    version="0.2.1",
    author="alterxyz",
    author_email="88554920+alterxyz@users.noreply.github.com",
    description="A simple Python wrapper for the Telegraph API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alterxyz/ytelegraph",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3,<3.0.0",
        "beautifulsoup4>=4.12.3,<5.0.0",
        "Markdown>=3.6,<4.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    keywords="telegraph api wrapper markdown publishing",
    project_urls={
        "Bug Tracker": "https://github.com/alterxyz/ytelegraph/issues",
        "Documentation": "https://github.com/alterxyz/ytelegraph/blob/main/README.md",
        "Source Code": "https://github.com/alterxyz/ytelegraph",
    },
)
