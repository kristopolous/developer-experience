# HackerNews CLI

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Read HackerNews like a hacker, directly from your terminal.

## Installation

You can install the HackerNews CLI directly from the source:

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

## Usage

List top stories:
```bash
hn stories
```

List newest stories:
```bash
hn stories --sort_by new
```

Show comments for a story:
```bash
hn comments <story_id>
```

Open a story in your default browser:
```bash
hn go <story_id>
```

Open the discussion page for a story in your browser:
```bash
hn comment <story_id>
```

## Development

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run tests:
```bash
pytest
```

## License
Apache License 2.0
