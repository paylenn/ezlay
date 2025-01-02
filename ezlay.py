#!/usr/bin/env python3

import os
import sys
import subprocess
from datetime import datetime
import fire
import questionary
from questionary import Style
import json
import shutil
import click

LICENSES = {
    'mit': '''MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
    'apache': '''                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   Copyright {year} {author}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
}

def run_command(cmd, cwd=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

def init_git(project_path):
    """Initialize a git repository and create .gitignore."""
    return run_command(['git', 'init'], cwd=project_path)

def create_license(project_path, license_type, author):
    """Create a license file in the project directory."""
    if license_type.lower() not in LICENSES:
        return False
    
    license_content = LICENSES[license_type.lower()].format(
        year=datetime.now().year,
        author=author
    )
    
    with open(os.path.join(project_path, 'LICENSE'), 'w') as f:
        f.write(license_content)
    return True

def create_python_project(project_name, args):
    """Create a standard Python project structure."""
    os.makedirs(project_name)
    project_path = os.path.abspath(project_name)
    
    # Create project structure
    os.makedirs(os.path.join(project_path, 'src', project_name.replace('-', '_')))
    os.makedirs(os.path.join(project_path, 'tests'))
    os.makedirs(os.path.join(project_path, 'docs'))
    
    # Create initial files
    with open(os.path.join(project_path, 'README.md'), 'w') as f:
        f.write(f'''# {project_name}

Description of your project goes here.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from {project_name.replace('-', '_')} import main
```

## Development

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Run tests:
```bash
pytest
```
''')
    
    # Create requirements files
    with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
        f.write('')
    
    with open(os.path.join(project_path, 'requirements-dev.txt'), 'w') as f:
        f.write('''pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.900
''')
    
    # Create setup.py
    with open(os.path.join(project_path, 'setup.py'), 'w') as f:
        f.write(f'''from setuptools import setup, find_packages

setup(
    name="{project_name}",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    install_requires=[
        # Add your dependencies here
    ],
    extras_require={{
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
        ],
    }},
    python_requires=">=3.7",
)''')
    
    # Create main module
    module_init = os.path.join(project_path, 'src', project_name.replace('-', '_'), '__init__.py')
    with open(module_init, 'w') as f:
        f.write('"""Main module."""\n\n__version__ = "0.1.0"\n')
    
    with open(os.path.join(project_path, 'src', project_name.replace('-', '_'), 'main.py'), 'w') as f:
        f.write('''"""Main module implementation."""

def main():
    """Main function."""
    print("Hello, World!")

if __name__ == "__main__":
    main()
''')
    
    # Create test file
    with open(os.path.join(project_path, 'tests', 'test_main.py'), 'w') as f:
        f.write('''"""Test main module."""

def test_placeholder():
    """Placeholder test."""
    assert True
''')
    
    # Create virtual environment if requested
    if args.venv:
        run_command(['python', '-m', 'venv', 'venv'], cwd=project_path)
    
    return project_path

def create_node_project(project_name, args):
    """Create a standard Node.js project structure."""
    os.makedirs(project_name)
    project_path = os.path.abspath(project_name)
    
    # Create project structure
    os.makedirs(os.path.join(project_path, 'src'))
    os.makedirs(os.path.join(project_path, 'tests'))
    os.makedirs(os.path.join(project_path, 'public'))
    
    # Create package.json
    with open(os.path.join(project_path, 'package.json'), 'w') as f:
        package_json = {
            "name": project_name,
            "version": "1.0.0",
            "description": "",
            "main": "src/index.js",
            "scripts": {
                "start": "node src/index.js",
                "dev": "nodemon src/index.js",
                "test": "jest",
                "lint": "eslint src/**/*.js"
            },
            "keywords": [],
            "author": args.author if args.author else "",
            "license": args.license.upper() if args.license else "ISC",
            "devDependencies": {
                "jest": "^29.0.0",
                "nodemon": "^3.0.0",
                "eslint": "^8.0.0"
            }
        }
        json.dump(package_json, f, indent=2)
    
    # Create initial files
    with open(os.path.join(project_path, 'README.md'), 'w') as f:
        f.write(f'''# {project_name}

Description of your project goes here.

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Testing

```bash
npm test
```
''')
    
    # Create .gitignore
    with open(os.path.join(project_path, '.gitignore'), 'w') as f:
        f.write('''node_modules/
.env
coverage/
.DS_Store
''')
    
    # Create source files
    with open(os.path.join(project_path, 'src', 'index.js'), 'w') as f:
        f.write('''console.log("Hello, World!");
''')
    
    # Create test file
    with open(os.path.join(project_path, 'tests', 'index.test.js'), 'w') as f:
        f.write('''test('placeholder test', () => {
    expect(true).toBe(true);
});
''')
    
    # Initialize npm if requested
    if args.npm_install:
        run_command(['npm', 'install'], cwd=project_path)
    
    return project_path

def create_bash_project(project_name, args):
    """Create a standard Bash project structure."""
    os.makedirs(project_name)
    project_path = os.path.abspath(project_name)
    
    # Create project structure
    os.makedirs(os.path.join(project_path, 'scripts'))
    os.makedirs(os.path.join(project_path, 'tests'))
    os.makedirs(os.path.join(project_path, 'docs'))
    
    # Create main script
    main_script = os.path.join(project_path, 'scripts', 'main.sh')
    with open(main_script, 'w') as f:
        f.write('''#!/usr/bin/env bash

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Source common functions
source "$SCRIPT_DIR/common.sh"

# Main function
main() {
    echo "Hello, World!"
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
''')
    os.chmod(main_script, 0o755)
    
    # Create common functions file
    with open(os.path.join(project_path, 'scripts', 'common.sh'), 'w') as f:
        f.write('''#!/usr/bin/env bash

# Common functions used across scripts

# Log an error message
log_error() {
    echo "ERROR: $1" >&2
}

# Log an info message
log_info() {
    echo "INFO: $1"
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}
''')
    os.chmod(os.path.join(project_path, 'scripts', 'common.sh'), 0o755)
    
    # Create test script
    test_script = os.path.join(project_path, 'tests', 'test_main.sh')
    with open(test_script, 'w') as f:
        f.write('''#!/usr/bin/env bash

set -euo pipefail

# Add your tests here
test_example() {
    assertTrue true
}

# Source shUnit2 if available
if [ -e "/usr/share/shunit2/shunit2" ]; then
    . /usr/share/shunit2/shunit2
else
    echo "shUnit2 not found. Please install it to run tests."
    exit 1
fi
''')
    os.chmod(test_script, 0o755)
    
    # Create README
    with open(os.path.join(project_path, 'README.md'), 'w') as f:
        f.write(f'''# {project_name}

Description of your bash project goes here.

## Requirements

- Bash 4.0 or later
- shUnit2 (for running tests)

## Usage

```bash
./scripts/main.sh
```

## Testing

```bash
./tests/test_main.sh
```
''')
    
    return project_path

def create_fastapi_project(project_name, args):
    """Create a FastAPI project structure."""
    os.makedirs(project_name)
    project_path = os.path.abspath(project_name)
    
    # Create project structure
    os.makedirs(os.path.join(project_path, 'app'))
    os.makedirs(os.path.join(project_path, 'app', 'api'))
    os.makedirs(os.path.join(project_path, 'app', 'core'))
    os.makedirs(os.path.join(project_path, 'app', 'db'))
    os.makedirs(os.path.join(project_path, 'app', 'models'))
    os.makedirs(os.path.join(project_path, 'app', 'schemas'))
    os.makedirs(os.path.join(project_path, 'tests'))
    os.makedirs(os.path.join(project_path, 'alembic'))
    
    # Create main FastAPI application
    with open(os.path.join(project_path, 'app', 'main.py'), 'w') as f:
        f.write('''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI App",
    description="FastAPI project generated with project_generator",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
''')
    
    # Create database configuration
    with open(os.path.join(project_path, 'app', 'core', 'config.py'), 'w') as f:
        f.write('''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
''')
    
    # Create database setup
    with open(os.path.join(project_path, 'app', 'db', 'session.py'), 'w') as f:
        f.write('''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')
    
    # Create requirements.txt
    with open(os.path.join(project_path, 'requirements.txt'), 'w') as f:
        f.write('''fastapi>=0.100.0
uvicorn>=0.23.0
sqlalchemy>=2.0.0
alembic>=1.11.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
''')
    
    # Create development requirements
    with open(os.path.join(project_path, 'requirements-dev.txt'), 'w') as f:
        f.write('''pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
''')
    
    # Create README
    with open(os.path.join(project_path, 'README.md'), 'w') as f:
        f.write(f'''# {project_name}

FastAPI project with SQLAlchemy and Alembic.

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Development

```bash
# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app tests
```

## API Documentation

After starting the server, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
''')
    
    # Create Docker setup if requested
    if args.docker:
        create_docker_setup(project_path, 'fastapi')
    
    # Create virtual environment if requested
    if args.venv:
        run_command(['python', '-m', 'venv', 'venv'], cwd=project_path)
    
    return project_path

def create_nextjs_project(project_name, args):
    """Create a Next.js project structure."""
    project_path = os.path.abspath(project_name)
    os.makedirs(project_path)
    
    # Create project structure
    os.makedirs(os.path.join(project_path, 'src'))
    os.makedirs(os.path.join(project_path, 'src', 'app'))
    os.makedirs(os.path.join(project_path, 'src', 'components'))
    os.makedirs(os.path.join(project_path, 'src', 'lib'))
    os.makedirs(os.path.join(project_path, 'public'))
    os.makedirs(os.path.join(project_path, 'tests'))
    
    # Create package.json
    package_json = {
        "name": project_name,
        "version": "0.1.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint",
            "format": "prettier --write .",
            "test": "jest",
            "test:watch": "jest --watch",
            "test:coverage": "jest --coverage"
        },
        "dependencies": {
            "next": "^14.0.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "@heroicons/react": "^2.0.0",
            "axios": "^1.0.0",
            "react-query": "^3.39.0"
        },
        "devDependencies": {
            "@types/node": "^20.0.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "typescript": "^5.0.0",
            "tailwindcss": "^3.3.0",
            "autoprefixer": "^10.4.0",
            "postcss": "^8.4.0",
            "@testing-library/jest-dom": "^5.16.0",
            "@testing-library/react": "^13.0.0",
            "@types/jest": "^29.0.0",
            "jest": "^29.0.0",
            "jest-environment-jsdom": "^29.0.0",
            "prettier": "^2.8.0",
            "eslint": "^8.0.0",
            "eslint-config-next": "^14.0.0"
        }
    }
    
    with open(os.path.join(project_path, 'package.json'), 'w') as f:
        json.dump(package_json, f, indent=2)
    
    # Create tsconfig.json
    tsconfig = {
        "compilerOptions": {
            "target": "es5",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "forceConsistentCasingInFileNames": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "node",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "baseUrl": ".",
            "paths": {
                "@/*": ["./src/*"]
            }
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
        "exclude": ["node_modules"]
    }
    
    with open(os.path.join(project_path, 'tsconfig.json'), 'w') as f:
        json.dump(tsconfig, f, indent=2)
    
    # Create next.config.js
    with open(os.path.join(project_path, 'next.config.js'), 'w') as f:
        f.write('''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
}

module.exports = nextConfig
''')
    
    # Create tailwind.config.js
    with open(os.path.join(project_path, 'tailwind.config.js'), 'w') as f:
        f.write('''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
''')
    
    # Create postcss.config.js
    with open(os.path.join(project_path, 'postcss.config.js'), 'w') as f:
        f.write('''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
''')
    
    # Create .env.local
    with open(os.path.join(project_path, '.env.local'), 'w') as f:
        f.write('''# Environment variables
NEXT_PUBLIC_API_URL=http://localhost:3000/api
''')
    
    # Create .prettierrc
    with open(os.path.join(project_path, '.prettierrc'), 'w') as f:
        f.write('''{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
''')
    
    # Create sample app page
    with open(os.path.join(project_path, 'src', 'app', 'page.tsx'), 'w') as f:
        f.write('''export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold">Welcome to {project_name}</h1>
    </main>
  )
}
''')
    
    # Create sample layout
    with open(os.path.join(project_path, 'src', 'app', 'layout.tsx'), 'w') as f:
        f.write('''import './globals.css'

export const metadata = {
  title: '{project_name}',
  description: 'Created with Project Generator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
''')
    
    # Create globals.css
    with open(os.path.join(project_path, 'src', 'app', 'globals.css'), 'w') as f:
        f.write('''@tailwind base;
@tailwind components;
@tailwind utilities;
''')
    
    # Add Docker setup if requested
    if args.docker:
        create_docker_setup(project_path, 'nextjs')
    
    return project_path

def create_go_project(project_name, args):
    """Create a Go project structure."""
    project_path = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_path)

    # Create standard Go project layout
    dirs = [
        'cmd/' + project_name,
        'internal',
        'pkg',
    ]

    for dir_path in dirs:
        os.makedirs(os.path.join(project_path, dir_path))

    # Create main.go
    os.makedirs(os.path.join(project_path, 'cmd', project_name), exist_ok=True)
    with open(os.path.join(project_path, 'cmd', project_name, 'main.go'), 'w') as f:
        f.write(f'''package main

import (
	"fmt"
	"log"
	"os"
)

func main() {{
	if err := run(); err != nil {{
		log.Fatal(err)
		os.Exit(1)
	}}
}}

func run() error {{
	fmt.Println("Hello from {project_name}")
	return nil
}}
''')
    
    # Try to initialize go.mod if Go is installed
    try:
        run_command(['go', 'mod', 'init', project_name], cwd=project_path)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("\nNote: Go is not installed. Skipping go.mod initialization.")
        print("To initialize the Go module later, install Go and run: go mod init", project_name)
        # Create an empty go.mod as a placeholder
        with open(os.path.join(project_path, 'go.mod'), 'w') as f:
            f.write(f'''module {project_name}

go 1.16
''')
    
    # Create Makefile
    with open(os.path.join(project_path, 'Makefile'), 'w') as f:
        f.write(f'''# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get
BINARY_NAME={project_name}
BINARY_UNIX=$(BINARY_NAME)_unix

all: test build

build:
	$(GOBUILD) -o $(BINARY_NAME) -v ./cmd/{project_name}

test:
	$(GOTEST) -v ./...

clean:
	$(GOCLEAN)
	rm -f $(BINARY_NAME)
	rm -f $(BINARY_UNIX)

run: build
	./$(BINARY_NAME)
''')

    # Create README.md
    with open(os.path.join(project_path, 'README.md'), 'w') as f:
        f.write(f'''# {project_name}

A Go project created with Project Generator.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Go 1.16 or higher

### Building

```bash
make build
```

### Running

```bash
make run
```

### Testing

```bash
make test
```

### Cleaning

```bash
make clean
```
''')

    # Initialize git and create license if requested
    if args.license:
        create_license(project_path, args.license, args.author)
    init_git(project_path)

    # Create Docker setup if requested
    if args.docker:
        create_docker_setup(project_path, 'go')

    return project_path

def create_docker_setup(project_path, project_type):
    """Create Docker setup for the project."""
    dockerfile_content = ""
    compose_content = ""
    
    if project_type == 'python':
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
'''
        compose_content = '''version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
    ports:
      - "8000:8000"
'''
    
    elif project_type == 'node':
        dockerfile_content = '''FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "start"]
'''
        compose_content = '''version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
'''
    
    elif project_type == 'fastapi':
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        compose_content = '''version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
  
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app

volumes:
  postgres_data:
'''
    
    elif project_type == 'nextjs':
        dockerfile_content = '''FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

CMD ["npm", "start"]
'''
        compose_content = '''version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
      - /app/.next
    ports:
      - "3000:3000"
'''
    
    elif project_type == 'go':
        dockerfile_content = '''FROM golang:1.20-alpine

WORKDIR /app

COPY go.* ./
RUN go mod download

COPY . .

RUN go build -o main ./cmd/app

CMD ["./main"]
'''
        compose_content = '''version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
    ports:
      - "8080:8080"
'''
    
    with open(os.path.join(project_path, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)
    
    with open(os.path.join(project_path, 'docker-compose.yml'), 'w') as f:
        f.write(compose_content)

class ProjectGenerator:
    """ezlay - A modern project layout generator.

    A command-line tool that creates standardized project structures for various programming languages and frameworks.

    Available Commands:
        create: Generate a new project layout
            Examples:
                ezlay create                     # Interactive mode
                ezlay create --project_type=python --project_name=myapp  # Command line mode

    Project Types:
        python   - Standard Python project with src layout and tests
        node     - Modern Node.js project with ESLint and Jest
        bash     - Organized Bash project with logging and tests
        fastapi  - FastAPI project with SQLAlchemy and Alembic
        nextjs   - Next.js project with TypeScript and Tailwind
        go       - Standard Go project layout

    For more information, visit: https://github.com/yourusername/ezlay
    """

    def create(self, project_type=None, project_name=None, license=None, author=None, 
              venv=False, npm_install=False, docker=False):
        """Create a new project with the specified configuration.

        Args:
            project_type: Type of project to create
                Options: python, node, bash, fastapi, nextjs, go
            project_name: Name of the project (will be used as directory name)
            license: License type to include
                Options: mit, apache
            author: Author name for license
            venv: Create virtual environment (Python projects only)
            npm_install: Run npm install (Node.js projects only)
            docker: Add Docker support with Dockerfile and docker-compose.yml

        Examples:
            ezlay create
            ezlay create --project_type=python --project_name=myapp
            ezlay create --project_type=fastapi --project_name=myapi --docker
            ezlay create --project_type=nextjs --project_name=webapp --license=mit
        """
        if not project_type or not project_name:
            return self.interactive()
        
        if project_type not in ['python', 'node', 'bash', 'fastapi', 'nextjs', 'go']:
            click.secho(f"Error: Invalid project type '{project_type}'", fg='red')
            return
        
        if os.path.exists(project_name):
            click.secho(f"Error: Directory '{project_name}' already exists", fg='red')
            return
        
        # Create project based on type
        click.secho(f"\n🚀 Creating {project_type} project: {project_name}", fg='bright_blue', bold=True)
        
        if project_type == 'python':
            project_path = create_python_project(project_name, self._create_args(locals()))
        elif project_type == 'node':
            project_path = create_node_project(project_name, self._create_args(locals()))
        elif project_type == 'bash':
            project_path = create_bash_project(project_name, self._create_args(locals()))
        elif project_type == 'fastapi':
            project_path = create_fastapi_project(project_name, self._create_args(locals()))
        elif project_type == 'nextjs':
            project_path = create_nextjs_project(project_name, self._create_args(locals()))
        elif project_type == 'go':
            project_path = create_go_project(project_name, self._create_args(locals()))
        
        # Initialize git repository
        if init_git(project_path):
            click.secho("✓ Initialized git repository", fg='green')
        
        # Create license file if requested
        if license and author:
            if create_license(project_path, license, author):
                click.secho(f"✓ Created {license.upper()} license", fg='green')
        
        click.secho(f"\n✨ Created {project_type} project: {project_name}", fg='bright_green', bold=True)
        
        # Show next steps
        self._show_next_steps(project_type, project_name, docker)
    
    def interactive(self):
        """Run the project generator in interactive mode."""
        custom_style = Style([
            ('qmark', 'fg:#673ab7 bold'),       # Question mark
            ('question', 'bold'),               # Question text
            ('answer', 'fg:#2196f3 bold'),      # Submitted answer
            ('pointer', 'fg:#673ab7 bold'),     # Selection pointer
            ('highlighted', 'fg:#673ab7 bold'),  # Selected choice
            ('selected', 'fg:#2196f3'),         # Selected choice
            ('separator', 'fg:#673ab7'),        # Separator
            ('instruction', 'fg:#757575'),      # Help text
        ])

        click.secho("\n🎨 ezlay - Project Layout Generator", fg='bright_blue', bold=True)
        click.secho("Use arrow keys to navigate and Enter to select\n", fg='bright_black')

        # Project Type Selection
        project_types = [
            questionary.Choice('Python Project 🐍', 'python'),
            questionary.Choice('Node.js Project 📦', 'node'),
            questionary.Choice('FastAPI Project 🚀', 'fastapi'),
            questionary.Choice('Next.js Project ⚡', 'nextjs'),
            questionary.Choice('Go Project 🔵', 'go'),
            questionary.Choice('Bash Project 💻', 'bash'),
            questionary.Choice('Cancel ❌', 'cancel')
        ]
        
        project_type = questionary.select(
            "What would you like to create?",
            choices=project_types,
            style=custom_style,
            qmark="🎯",
            use_indicator=True,
            instruction=""
        ).ask()
        
        if not project_type or project_type == 'cancel':
            click.secho("\nProject creation cancelled.", fg='yellow')
            return

        # Project Name Selection
        common_names = [
            questionary.Choice('my-app', 'my-app'),
            questionary.Choice('my-project', 'my-project'),
            questionary.Choice('custom name...', 'custom')
        ]
        
        name_choice = questionary.select(
            "Choose a project name:",
            choices=common_names,
            style=custom_style,
            qmark="📝",
            instruction=""
        ).ask()
        
        if name_choice == 'custom':
            project_name = questionary.text(
                "Enter your custom project name:",
                validate=lambda text: True if text and not os.path.exists(text) and text.replace('-', '').replace('_', '').isalnum() 
                    else "Name must be alphanumeric (hyphens and underscores allowed) and directory must not exist",
                style=custom_style,
                qmark="📝"
            ).ask()
        else:
            project_name = name_choice
            
        if not project_name:
            click.secho("\nProject creation cancelled.", fg='yellow')
            return

        # License Selection
        license_types = [
            questionary.Choice('MIT License', 'mit'),
            questionary.Choice('Apache License 2.0', 'apache'),
            questionary.Choice('No License', 'none')
        ]
        
        license = questionary.select(
            "Choose a license:",
            choices=license_types,
            style=custom_style,
            qmark="📄",
            instruction=""
        ).ask()

        author = None
        if license and license != 'none':
            author_choices = [
                questionary.Choice('Enter custom name...', 'custom'),
                questionary.Choice(os.getenv('USER', 'user'), 'default'),
            ]
            
            author_choice = questionary.select(
                "Choose author name for license:",
                choices=author_choices,
                style=custom_style,
                qmark="👤",
                instruction=""
            ).ask()
            
            if author_choice == 'custom':
                author = questionary.text(
                    "Enter author name:",
                    style=custom_style,
                    qmark="👤"
                ).ask()
            else:
                author = os.getenv('USER', 'user')

        if license == 'none':
            license = None

        # Features Selection
        features = []
        
        if questionary.confirm(
            "Would you like to select additional features?",
            default=True,
            style=custom_style,
            qmark="✨"
        ).ask():
            feature_choices = [
                questionary.Choice('Docker Support 🐳', 'docker'),
            ]
            
            if project_type == 'python':
                feature_choices.append(questionary.Choice('Virtual Environment 🔮', 'venv'))
            elif project_type in ['node', 'nextjs']:
                feature_choices.append(questionary.Choice('Run npm install 📦', 'npm_install'))
            
            features = questionary.checkbox(
                "Select additional features:",
                choices=feature_choices,
                style=custom_style,
                qmark="✨",
                instruction="(Space to select, Enter to confirm)"
            ).ask()

        # Create args dictionary
        args = {
            'project_type': project_type,
            'project_name': project_name,
            'license': license,
            'author': author,
            'docker': 'docker' in features,
            'venv': 'venv' in features,
            'npm_install': 'npm_install' in features
        }

        # Create the project
        click.secho("\n🚀 Creating your project...", fg='bright_blue', bold=True)
        
        if project_type == 'python':
            project_path = create_python_project(project_name, self._create_args(args))
        elif project_type == 'node':
            project_path = create_node_project(project_name, self._create_args(args))
        elif project_type == 'bash':
            project_path = create_bash_project(project_name, self._create_args(args))
        elif project_type == 'fastapi':
            project_path = create_fastapi_project(project_name, self._create_args(args))
        elif project_type == 'nextjs':
            project_path = create_nextjs_project(project_name, self._create_args(args))
        elif project_type == 'go':
            project_path = create_go_project(project_name, self._create_args(args))
        
        # Initialize git repository
        if init_git(project_path):
            click.secho("✓ Initialized git repository", fg='green')
        
        # Create license file if requested
        if license and author:
            if create_license(project_path, license, author):
                click.secho(f"✓ Created {license.upper()} license", fg='green')
        
        click.secho(f"\n✨ Created {project_type} project: {project_name}", fg='bright_green', bold=True)
        
        # Show next steps
        self._show_next_steps(project_type, project_name, args['docker'])
    
    def _create_args(self, params):
        """Convert dictionary of parameters to args object."""
        class Args:
            pass
        
        args = Args()
        for key, value in params.items():
            setattr(args, key, value)
        return args
    
    def _show_next_steps(self, project_type, project_name, docker):
        """Show next steps for the created project."""
        click.secho("\n📝 Next steps:", fg='bright_blue', bold=True)
        
        if project_type in ['python', 'fastapi']:
            click.secho("\n1. Create and activate virtual environment:", fg='yellow')
            click.echo(f"   cd {project_name}")
            click.echo("   python -m venv venv")
            click.echo("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
            click.secho("\n2. Install dependencies:", fg='yellow')
            click.echo("   pip install -r requirements-dev.txt")
        
        elif project_type in ['node', 'nextjs']:
            click.secho("\n1. Install dependencies:", fg='yellow')
            click.echo(f"   cd {project_name}")
            click.echo("   npm install")
            click.secho("\n2. Start development server:", fg='yellow')
            click.echo("   npm run dev")
        
        elif project_type == 'bash':
            click.secho("\n1. Make scripts executable:", fg='yellow')
            click.echo(f"   cd {project_name}")
            click.echo("   chmod +x scripts/*.sh tests/*.sh")
            click.secho("\n2. Run the main script:", fg='yellow')
            click.echo("   ./scripts/main.sh")
        
        elif project_type == 'go':
            click.secho("\n1. Download dependencies:", fg='yellow')
            click.echo(f"   cd {project_name}")
            click.echo("   go mod tidy")
            click.secho("\n2. Run the application:", fg='yellow')
            click.echo("   make run")
        
        if docker:
            click.secho("\n🐳 Docker commands:", fg='bright_blue')
            click.echo("1. Build and run with Docker Compose:")
            click.echo("   docker-compose up --build")

def main():
    fire.Fire(ProjectGenerator)

if __name__ == '__main__':
    main()
