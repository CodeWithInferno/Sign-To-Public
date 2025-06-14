# Contributing to ASL Recognition Project

Thank you for your interest in contributing to the ASL Recognition project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/asl-recognition.git
   cd asl-recognition
   ```
3. Set up development environment:
   ```bash
   make install-dev
   make install-ui
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Run tests and linting:
   ```bash
   make test
   make lint
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your meaningful commit message"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Code Style Guidelines

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and concise

## Project Structure

- `/Scripts` - Core ML/AI implementation
- `/UI_expo` - Mobile application
- `/server` - Backend server
- `/models` - Trained models
- `/docs` - Documentation

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Add integration tests when appropriate

## Documentation

- Update README.md if adding new features
- Document API changes
- Add inline comments for complex logic
- Update setup instructions if needed

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the requirements.txt if adding dependencies
3. Ensure all tests pass and code is linted
4. Link any relevant issues in the PR description
5. Request review from maintainers

## Questions or Problems?

- Open an issue for bugs
- Use discussions for general questions
- Tag maintainers for urgent issues

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Report inappropriate behavior

Thank you for contributing!