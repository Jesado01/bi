# Code BIAN Module

An intelligent code migration and project generation tool that uses AI to analyze, transform, and generate code across different programming languages and frameworks.

## Features

- **Automated Code Analysis**: Analyzes source code to understand structure, dependencies, and patterns
- **Smart Project Generation**: Generates modern, well-structured projects based on analysis
- **Multi-language Support**: Handles multiple programming languages and frameworks
- **Architecture-Aware**: Understands and implements modern architectural patterns
- **Validation & Testing**: Includes built-in validation and test generation
- **Documentation**: Auto-generates comprehensive project documentation

## Getting Started

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/) for dependency management
- OpenAI API key (or other LLM provider)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/code-bian.git
   cd code-bian
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Usage

### Basic Usage

```bash
# Analyze a project
poetry run python -m agents.analyze --input /path/to/project --output analysis.json

# Generate code from analysis
poetry run python -m agents.generate --input analysis.json --output /output/directory

# Run the full migration pipeline
poetry run python main.py --input /path/to/project --output /output/directory
```

### Configuration

Create a `config.yaml` file to customize the migration:

```yaml
# Example configuration
source:
  language: java
  framework: spring-boot
  version: "2.7.0"

target:
  language: java
  framework: quarkus
  version: "2.15.0.Final"
  architecture: "hexagonal"

llm:
  provider: "anthropic"
  model: "Claude-4.5 Sonnet"
  temperature: 0.1
  max_tokens: 64000
```

## Project Structure

```
code-bian/
├── agents/                  # Core migration agents
│   ├── modules/            # Individual processing modules
│   ├── framework.py        # Main orchestration framework
│   └── state.py            # State management
├── config/                 # Configuration files
├── docs/                   # Documentation
├── examples/               # Example projects
├── templates/              # Code generation templates
├── tests/                  # Test suite
├── .env.example            # Example environment variables
├── config.example.yaml     # Example configuration
├── main.py                 # Entry point
├── poetry.lock             # Dependencies lock file
└── pyproject.toml          # Project configuration
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
   ```bash
   poetry install --with dev
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
poetry run pytest
```

### Adding a New Module

1. Create a new Python file in `agents/modules/`
2. Implement the required interface
3. Register the module in `agents/__init__.py`
4. Add tests in `tests/`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [LangChain](https://python.langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- Inspired by modern code migration patterns and AI-assisted development

## Roadmap

- [ ] Support for more languages and frameworks
- [ ] Enhanced validation and testing
- [ ] Interactive CLI interface
- [ ] Web-based dashboard
- [ ] Plugin system for custom generators

---

**Note**: This project is under active development. Please check back frequently for updates and new features.
