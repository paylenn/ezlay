# ezlay

A flexible command-line tool that makes laying out new projects easy. Create standardized project structures for various programming languages and frameworks with a single command.

## Features

- 🚀 Multiple project types supported:
  - Python (standard layout)
  - Node.js
  - Bash
  - FastAPI (with SQLAlchemy and Alembic)
  - Next.js (with TypeScript and Tailwind)
  - Go (standard layout)
- 🎨 Beautiful interactive CLI with colorful output
- 📦 Automatic Git initialization
- 📄 License generation (MIT or Apache)
- 🐍 Virtual environment setup for Python projects
- 📦 NPM initialization for Node.js projects (when Node.js is available)
- 🐳 Optional Docker support with docker-compose
- 📝 Comprehensive README generation

## Installation

1. Download the latest release for your platform from the [releases page](https://github.com/yourusername/ezlay/releases)
2. Extract the archive
3. Add the binary to your PATH or run it directly

Linux/macOS:
```bash
chmod +x ezlay
sudo mv ezlay /usr/local/bin/
```

Windows:
- Add the directory containing ezlay.exe to your PATH, or
- Run ezlay.exe from the extracted directory

## Usage

### Interactive Mode (Recommended)

Simply run:
```bash
ezlay create
```

Use arrow keys to navigate through the options and Enter to select. The tool will guide you through:
- Project type selection
- Project name
- License options
- Additional features (Docker, virtual environment, etc.)

### Command Line Mode

For automated scripts or quick project creation:
```bash
ezlay create \
  --project_type=python \
  --project_name=my-app \
  --license=mit \
  --author="John Doe" \
  --docker
```

### Available Options

- `--project_type`: Type of project (python/node/bash/fastapi/nextjs/go)
- `--project_name`: Name of the project
- `--license`: License type (mit/apache)
- `--author`: Author name for license
- `--docker`: Add Docker support
- `--venv`: Create virtual environment (Python projects only)
- `--npm_install`: Run npm install (Node.js projects only)

## Project Types

### Python
- Standard src layout
- Tests directory
- setup.py and requirements.txt
- Optional virtual environment

### Node.js
- Modern project structure
- ESLint and Prettier config
- Jest testing setup
- package.json

### FastAPI
- SQLAlchemy models
- Alembic migrations
- API documentation
- Testing setup

### Next.js
- TypeScript support
- Tailwind CSS
- Testing setup
- Component structure

### Go
- Standard project layout
- cmd and pkg directories
- go.mod (placeholder if Go not installed)
- Makefile

### Bash
- Organized script structure
- Logging utilities
- Configuration handling
- Test framework

## Optional Dependencies

These are not required to create project templates, but needed for full functionality:
- Node.js and npm (for Node.js/Next.js projects)
- Go (for Go projects)
- Docker (for container support)

Note: ezlay can create template directories even if the corresponding language runtime is not installed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
