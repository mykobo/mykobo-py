# Release Process

This project uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) to automate versioning and releases.

## How It Works

Semantic Release automatically:
1. Analyzes your git commit messages
2. Determines the next version number (major, minor, or patch)
3. Updates version in `pyproject.toml` and `mykobo_py/__init__.py`
4. Generates/updates `CHANGELOG.md`
5. Creates a git commit and tag
6. Optionally builds and publishes to PyPI

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>: <description>

[optional body]

[optional footer]
```

### Types that trigger releases:

- `feat:` - New feature (bumps **minor** version: 0.4.9 → 0.5.0)
- `fix:` - Bug fix (bumps **patch** version: 0.4.9 → 0.4.10)
- `perf:` - Performance improvement (bumps **patch** version)

### Breaking changes:

Add `BREAKING CHANGE:` in the commit body or use `!` after type to bump **major** version:

```
feat!: redesign API

BREAKING CHANGE: Changed the API structure
```

### Other types (no version bump):

- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test changes
- `build:` - Build system changes
- `ci:` - CI configuration changes
- `chore:` - Other changes

## Release Commands

### 1. Check what the next version will be (dry run)

```bash
poetry run semantic-release version --print
```

### 2. Create a new release

```bash
poetry run semantic-release version
```

This will:
- Calculate the next version
- Update version in files
- Generate CHANGELOG
- Create a commit and tag

### 3. Push the release to GitHub

```bash
git push && git push --tags
```

### 4. Build and publish to PyPI (optional)

```bash
poetry build
poetry publish
```

Or use semantic-release to do it all:

```bash
poetry run semantic-release publish
```

## Full Release Workflow

1. Make your changes following conventional commits
2. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add new message bus models with validation"
   ```

3. Check what version will be released:
   ```bash
   poetry run semantic-release version --print
   ```

4. Create the release:
   ```bash
   poetry run semantic-release version
   ```

5. Push to remote:
   ```bash
   git push && git push --tags
   ```

6. (Optional) Publish to PyPI:
   ```bash
   poetry publish
   ```

## Configuration

The semantic release configuration is in `pyproject.toml` under `[tool.semantic_release]`:

- **version_toml**: Updates version in pyproject.toml
- **version_variables**: Updates __version__ in __init__.py
- **branch**: Only releases from main branch
- **major_on_zero**: Don't auto-bump to 1.0.0
- **tag_format**: Git tag format (just the version number)

## Examples

### Patch Release (0.4.9 → 0.4.10)
```bash
git commit -m "fix: resolve validation error in MetaData"
poetry run semantic-release version
```

### Minor Release (0.4.9 → 0.5.0)
```bash
git commit -m "feat: add convenience function for creating messages"
poetry run semantic-release version
```

### Major Release (0.4.9 → 1.0.0)
```bash
git commit -m "feat!: redesign message bus API

BREAKING CHANGE: Removed deprecated methods"
poetry run semantic-release version
```

## Troubleshooting

### No version bump triggered
- Ensure your commits follow the conventional commits format
- Check that you're on the main branch
- Use `--print` to see what semantic-release detected

### Version mismatch
If `pyproject.toml` and `__init__.py` are out of sync, manually update them to match before running semantic-release.
