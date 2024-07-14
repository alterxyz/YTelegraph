from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ytelegraph",
    version="0.1.0",
    author="alterxyz",
    author_email="88554920+alterxyz@users.noreply.github.com",
    description="A simple Python wrapper for the Telegraph API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alterxyz/ytelegraph",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "markdown",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="telegraph api wrapper markdown publishing",
    project_urls={
        "Bug Tracker": "https://github.com/alterxyz/ytelegraph/issues",
        "Documentation": "https://github.com/alterxyz/ytelegraph/blob/main/README.md",
        "Source Code": "https://github.com/alterxyz/ytelegraph",
    },
)
