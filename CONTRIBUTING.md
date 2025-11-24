# Contributing to AI Procrastination Detector

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, GPU/CPU)
- Relevant logs (set `log_level: "DEBUG"` in config.yaml)

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists or is planned
- Describe the use case and benefits
- Provide examples if applicable

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the existing code style
   - Add type hints to new functions
   - Include docstrings (Google style)
   - Update constants.py for new configuration values
   - Add logging where appropriate
4. **Test your changes**:
   - Ensure the app runs without errors
   - Test with and without CUDA
   - Verify configuration changes work
5. **Update documentation**:
   - Update README.md if needed
   - Update config.yaml template
   - Add comments for complex logic
6. **Commit your changes**: Use clear, descriptive commit messages
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Add docstrings to all public functions
- Keep functions focused and single-purpose
- Use meaningful variable names

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hourse-of-wisdom.git
cd hourse-of-wisdom

# Install dependencies
uv sync

# Create config file
uv run python config.py

# Add test images to horse of wisdom/ folder

# Run the app
uv run app.py
```

## Testing

Before submitting a PR, test:
- ✅ App starts without errors
- ✅ Camera detection works
- ✅ Alert system displays correctly
- ✅ Configuration changes are respected
- ✅ Error handling works (test with missing files, no camera, etc.)

## Questions?

Feel free to open an issue for questions or discussions!

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Help others learn and grow

Thank you for contributing! 🐴
