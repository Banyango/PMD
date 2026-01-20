# PMD

[![PyPI version](https://badge.fury.io/py/pmd.svg)](https://badge.fury.io/py/pmd)
[![Python Support](https://img.shields.io/pypi/pyversions/pmd.svg)](https://pypi.org/project/pmd/)

Pmd is a lightweight markup language and Python library for writing, composing, and rendering structured LLM prompts.

Pmd targets prompt engineering workflows where clarity, versioning, and correctness matter.

## Features

- ✨ Framework agnostic — works with any LLM or API
- 🚀 Composable — prompts can be split, reused, and nested
- 🎯 Static-first — templates are validated before execution
- 📦 Metadata — version, and provide metadata alongside your prompts.

## Get Started

Here's a Hello World example. helloworld.pmd contains the template, and helloworld.json contains the data.

```markdown:helloworld.pmd
// file:helloworld.pmd

Hello, {{name}}!
Welcome to Pmd templating.
```

```json:helloworld.json
// file:helloworld.json

{
    "name": "World"
}
```

**Run the following command:**
```shell
pmd render helloworld.pmd
```

**Output:**

```markdown
Hello, World!
Welcome to Pmd templating.
```


## Python Library

TBD

## Documentation

Full documentation is available at [https://banyango.github.io/pmd/latest](https://www.banyango.com/PMD/latest/)

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Setup Development Environment

```bash
uv sync # Install dependencies
```

### Running Tests

```bash
# Run tests with pytest
uv run pytest

# Run tests with coverage
uv run pytest --cov=pmd --cov-report=html
```

### Code Quality

```bash
# Format code with ruff
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking with mypy
uv run mypy src/pmd
```

### Building the Package

```bash
# Build the package
uv build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to:
- Update tests as appropriate
- Follow the existing code style
- Update documentation for any changed functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Kyle Reczek** - *Initial work* - [Banyango](https://github.com/Banyango)

## Acknowledgments

- Markdown

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes to this project.

## Support

If you encounter any problems or have questions, please [open an issue](https://github.com/yourusername/pmd/issues).

