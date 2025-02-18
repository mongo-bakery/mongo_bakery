# mongo_bakery

[![codecov](https://codecov.io/gh/mongo-bakery/mongo_bakery/graph/badge.svg?token=FXA6QEILP6)](https://codecov.io/gh/mongo-bakery/mongo_bakery)
![mongo-bakery-ci](https://github.com/mongo-bakery/mongo_bakery/actions/workflows/ci.yml/badge.svg)

Inspired by [model-bakery](https://model-bakery.readthedocs.io/en/latest/), this project aims to simplify the process of
creating MongoDB documents for testing purposes. The goal is to deliver a maintainable, intuitive, and
developer-friendly API specifically designed for MongoDB. By streamlining the generation of test data, this tool will
empower developers to efficiently create realistic document structures, enhancing the testing workflow for applications
that rely on MongoDB as their primary database.

## Motivation

- To have the conveniences of model_bakery (from the Django world) in Flask with MongoEngine.
- We want more context within the test itself (instead of having fixtures in conftest where we don't know which fields
are populated).
- We don't want to create a Factory for every Document in the application.

## Alternatives

- <https://factoryboy.readthedocs.io/en/stable/>
- <https://github.com/klen/mixer>

## Draft Solution

- <https://gist.github.com/huogerac/57d2ecc15b1ba8fc16af41a697065f24>

## Contributing

We welcome contributions to the mongo_bakery project! Here are the steps to get started:

1. **Fork the Repository**: Fork the [mongo_bakery repository](https://github.com/mongo-bakery/mongo_bakery) on GitHub.

2. **Clone Your Fork**: Clone your forked repository to your local machine.

    ```bash
    git clone https://github.com/your-username/mongo_bakery.git
    cd mongo_bakery
    ```

3. **Create a Branch**: Create a new branch for your feature or bugfix.

    ```bash
    git checkout -b branch-name
    ```

4. **Install Dependencies**: Install the required dependencies. We use the [uv](https://docs.astral.sh/uv/) tool to
manage our prject dependencies and vitualenv. So it is a prerequisite to the project.

    ```bash
    uv sync
    ```

    This command will create the Python virtual environment with the Python version of the project and install all
    dependencies.

5. **Make Changes**: Implement your feature or bugfix.

6. **Run Tests and Lint**: Ensure all tests and lint pass before submitting your changes.

    ```bash
    uv run task test
    ```

    This command runs `ruff check` as a lint, `pytest` to run all tests, and `coverage html` to generate an html report of test coverage. This html report is for the development side only. On our CI with Github Actions, it runs `pytest --cov=mongo_bakery --cov-report=xml` to generate a report that is send to
    [codecov.io](https://app.codecov.io/gh/mongo-bakery/mongo_bakery)

7. **Commit Changes**: Commit your changes with a descriptive commit message. Use
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) to write your commit messages.

    ```bash
    git add .
    git commit -m "feat(issue4): Description of your changes"
    ```

8. **Push to GitHub**: Push your changes to your forked repository.

    ```bash
    git push origin branch-name
    ```

9. **Create a Pull Request**: Open a pull request on the original repository. Provide a clear description of your
changes and any relevant information.

10. **Review Process**: Your pull request will be reviewed by the maintainers. Be prepared to make any necessary
changes based on feedback.
