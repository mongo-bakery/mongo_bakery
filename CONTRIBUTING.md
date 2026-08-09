# Contributing to mongo_bakery

Thanks for taking the time to contribute! This document describes how to set up your environment and the
conventions this project follows, so your pull request is easy to review and merge.

## Getting started

1. **Fork the repository**: fork [mongo_bakery](https://github.com/mongo-bakery/mongo_bakery) on GitHub.

2. **Clone your fork**:

    ```bash
    git clone https://github.com/your-username/mongo_bakery.git
    cd mongo_bakery
    ```

3. **Install dependencies**. This project uses [uv](https://docs.astral.sh/uv/) to manage the virtual environment
   and dependencies, so it's a prerequisite.

    ```bash
    uv sync
    ```

    This creates a virtual environment with the project's Python version and installs all runtime and dev
    dependencies (`ruff`, `mypy`, `coverage`, `taskipy`).

4. **Find or open an issue**: every change should be tied to a tracked issue. Check the
   [issue tracker](https://github.com/mongo-bakery/mongo_bakery/issues) for an existing one that matches what you
   want to work on. If your contribution is a new proposal that isn't listed yet, open an issue describing it
   first, and wait for it to be triaged before starting the work.

5. **Create a branch** for your change, named after the issue you're resolving:

    ```bash
    git switch -c mongo_bakery-<issue-number>
    ```

## Development workflow

Common tasks are wired up via [taskipy](https://github.com/taskipy/taskipy) in `pyproject.toml`:

```bash
uv run task lint       # ruff check
uv run task typecheck  # mypy mongo_bakery
uv run task test       # pytest + coverage, then generate an html coverage report
uv run task docs       # serve the documentation site locally
```

Run `lint`, `typecheck` and `test` before opening a pull request — these are exactly the checks run in CI
(`.github/workflows/ci.yml`).

## Code style

- Linting is done with [ruff](https://docs.astral.sh/ruff/); the enabled rule sets are defined in
  `[tool.ruff.lint]` in `pyproject.toml` (bandit, bugbear, comprehensions, simplify, isort, pycodestyle, pyflakes,
  pydocstyle, pyupgrade). Run `uv run task lint` and fix anything it reports.
- Docstrings follow the [Google convention](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
  They aren't mandatory for every function (`D1` rules are disabled), but add one whenever the *why* isn't obvious
  from the name and signature alone.
- Imports are sorted by `ruff`'s isort integration (stdlib / third-party / first-party / local, in that order);
  don't sort them by hand.
- Type hints are required on new and modified code and are enforced by `mypy` in CI
  (`uv run task typecheck`). Untyped code will fail the build.

## Tests

- Tests live under `tests/` in files named `test_*.py` and are run with `pytest`.
- Name tests after the behavior they verify (`test_<subject>_<expected_behavior>`), and prefer a docstring over
  inline comments to describe intent, e.g.:

    ```python
    def test_seq_raises_for_unsupported_value_type():
        """
        Test that `baker.seq()` raises a `ValueError` when used with a value type it doesn't know how to increment.

        Asserts:
        - A `ValueError` mentioning the unsupported type is raised when the sequence is resolved.
        """
        ...
    ```

- Add or update tests for any behavior change — PRs that only add code without covering it with a test are unlikely
  to be merged as-is.

## Commit messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). When a commit
addresses a tracked issue, include the issue number in the scope:

```
feat(issue54): Add baker.seed() for reproducible mock data
fix(issue48): Use word-boundary regex to detect dependency usage
ci(issue56): Add mypy to CI to enforce existing type hints
```

Common types used in this repo: `feat`, `fix`, `refactor`, `chore`, `ci`, `docs`.

## Pull requests

1. All commits in the PR must be signed (GPG, SSH or S/MIME) so they show up as `Verified` on GitHub — the `main`
   branch requires signed commits, and unsigned commits will be rejected on merge. See GitHub's guide on
   [signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
   to set this up.
2. Push your branch and open a pull request against `main`.
3. If the PR is fixing a tracked issue, add a `Closes #<issue-number>` (or `Fixes #<issue-number>`) line in the
   description so the issue is closed automatically when the PR is merged.
4. Give the PR a title following the same Conventional Commits format as commit messages — it's used as the
   squash-merge commit message.
5. Make sure `uv run task lint`, `uv run task typecheck` and `uv run task test` all pass locally; CI runs the same
   three checks.
6. Be ready to address review feedback — a maintainer will review your PR before merging.

## Reporting bugs and requesting features

Open a [GitHub issue](https://github.com/mongo-bakery/mongo_bakery/issues). Issues labeled
[`good first issue`](https://github.com/mongo-bakery/mongo_bakery/labels/good%20first%20issue) are a good place to
start if you're new to the project.

## License

By contributing, you agree that your contributions will be licensed under the project's
[GPL-3.0-or-later](LICENSE) license.
