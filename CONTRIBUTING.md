# Contributing Guide

Thank you for your interest in `llama-server-tray`! Contributions are welcome.

## How to Contribute

### Reporting Issues

1. Visit [Issues](https://github.com/Wjavan/llama-server-tray/issues)
2. Click "New Issue"
3. Use the templates:
   - **🐛 Bug Report**: Describe the problem + environment info + steps to reproduce
   - **✨ Feature Request**: Explain what you want + expected usage
   - **📖 Documentation**: Point out unclear documentation
   - **🤔 Other**: Other ideas

### Submitting Pull Requests

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "feat: your feature description"`
4. Push branch: `git push origin feature/your-feature`
5. Submit PR to `main` branch

#### Commit Message Convention

- `feat: ...` - New feature
- `fix: ...` - Bug fix
- `docs: ...` - Documentation update
- `refactor: ...` - Code refactoring (no functional change)
- `chore: ...` - Build/tooling update

## Development Setup

### Local Installation

```bash
git clone https://github.com/Wjavan/llama-server-tray.git
cd llama-server-tray

# Install dependencies
py -m pip install pystray pillow

# Run the launcher
pythonw llama_server_tray.pyw
```

### Build Test

```bash
py -m pip install pyinstaller
pyinstaller --noconsole --onefile --name llama-server-tray llama_server_tray.pyw
```

## Development Guidelines

- **Test edge cases**: Different Windows versions, different llama.cpp versions
- **Maintain backward compatibility**: Don't remove existing configuration options
- **Update documentation**: Update README when changing code
- **Keep it simple**: Minimal changes to solve problems

## Labels Explanation

- `good first issue` - Suitable for newcomers
- `help wanted` - Still looking for help
- `bug` - Something isn't working
- `enhancement` - New feature request

Want to make a PR? Pick an issue tagged with `good first issue`!

## Questions?

- GitHub Discussions: https://github.com/Wjavan/llama-server-tray/discussions
- Open an issue: https://github.com/Wjavan/llama-server-tray/issues
