# Contributing to PDF Tools

Thank you for considering contributing to PDF Tools! Here's how you can help:

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/pdf_tools.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

## Adding New Tools

1. Create a new Python file in the project root
2. Follow the same pattern as existing tools:
   - Use argparse for CLI arguments
   - Include comprehensive documentation
   - Handle errors gracefully
3. Update the README.md to document your new tool

## Pull Request Process

1. Create a branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test your changes thoroughly
4. Update documentation if needed
5. Push to your fork: `git push origin feature/your-feature-name`
6. Submit a pull request

## Code Style

- Follow PEP 8 guidelines
- Include docstrings for functions and modules
- Use meaningful variable names
- Add comments for complex logic

## Reporting Issues

If you find a bug or have a feature request, please create an issue on GitHub with:

- A clear description of the bug or feature
- Steps to reproduce (for bugs)
- Expected behavior
- Screenshots if applicable
- System information
