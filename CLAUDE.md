# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the application

```bash
uv run booklog
```

### Testing

```bash
uv run pytest                    # Run all tests
uv run pytest tests/cli/         # Run CLI tests
uv run pytest -k test_name       # Run specific test
```

### Linting and Type Checking

```bash
uv run ruff check .              # Run linter
uv run ruff format .             # Format Python code
uv run mypy .                    # Run type checker
npm run format                   # Check formatting with Prettier
npm run format:fix               # Fix formatting with Prettier
```

## Architecture

### Core Structure

The application is a console-based book management system with three main layers:

1. **CLI Layer** (`booklog/cli/`): Interactive prompts using prompt-toolkit
   - `main.py`: Entry point with menu system
   - `add_*.py`: Commands for adding authors, works, and readings
   - Uses radio list UI for selection

2. **Repository Layer** (`booklog/repository/`): Data persistence
   - `json_authors.py`, `json_works.py`: JSON-based storage for authors and works
   - `markdown_readings.py`, `markdown_reviews.py`: Markdown-based storage for readings and reviews
   - `api.py`: Unified data access interface with dataclasses

3. **Export Layer** (`booklog/exports/`): Data export functionality
   - Generates JSON exports for web presentation
   - Includes statistics and timeline generation

### Data Model

- **Author**: Name, sort name, slug
- **Work**: Title, subtitle, year, kind (Book, Audiobook, etc.), authors
- **Reading**: Work reference, dates, medium, progress
- **Review**: Work reference, grade, review text in Markdown

### Key Dependencies

- Python 3.13.5 with uv package manager
- prompt-toolkit for CLI interactions
- loguru for logging
- pytest with snapshot testing (syrupy)
- ruff for linting, mypy for type checking

## Important: Pre-PR Checklist

Always perform these steps before creating a PR:

1. `git checkout -b descriptive-branch-name` - Create a new branch for your changes
2. `git pull --rebase origin main` - Rebase on latest main branch
3. `uv run mypy .` - Ensure type safety
4. `uv run ruff check .` - Check for linting issues
5. `npm run format` - Verify formatting is correct
6. `uv run pytest` - Ensure all tests pass
