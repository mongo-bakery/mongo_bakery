# mongo_bakery

[![codecov](https://codecov.io/gh/mongo-bakery/mongo_bakery/graph/badge.svg?token=FXA6QEILP6)](https://codecov.io/gh/mongo-bakery/mongo_bakery)
[![mongo-bakery-ci](https://github.com/mongo-bakery/mongo_bakery/actions/workflows/ci.yml/badge.svg)](https://github.com/mongo-bakery/mongo_bakery/actions)
[![GitHub issues](https://img.shields.io/github/issues/mongo-bakery/mongo_bakery.svg)](https://GitHub.com/mongo-bakery/mongo_bakery/issues/)
[![GitHub stars](https://img.shields.io/github/stars/mongo-bakery/mongo_bakery.svg?style=social&label=Star&maxAge=2592000)](https://github.com/mongo-bakery/mongo_bakery/stargazers/)
![GitHub top language](https://img.shields.io/github/languages/top/mongo-bakery/mongo_bakery)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

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

## Installation

```bash
uv add mongo-bakery
```

## Usage

`mongo_bakery` fills in a MongoEngine `Document` (or `EmbeddedDocument`) with realistic fake data so you don't have to
hand-write every field in every test. All the examples below assume:

```python
from mongoengine import BooleanField, Document, IntField, StringField

from mongo_bakery import baker


class Customer(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    company = StringField(required=True)
    phone_number = StringField(required=True)
    loyalty_points = IntField(required=True)
    notes = StringField(required=False)
    newsletter_opt_in = BooleanField(required=False)
```

### Creating a basic Document

`baker.make` instantiates and saves the document, automatically generating values for every **required** field:

```python
customer = baker.make(Customer)
```

### Creating multiple instances with `_quantity`

Pass `_quantity` to create and save several instances at once. `baker.make` returns a list when `_quantity > 1`:

```python
customers = baker.make(Customer, _quantity=5)
len(customers)  # 5
```

### Not-required (optional) fields

Optional fields (`required=False`) are **not** filled in automatically — `baker.make` only generates data for
required fields, leaving optional ones at their MongoEngine default (e.g. `None`). Pass any field, required or not,
as a keyword argument to set it explicitly:

```python
customer = baker.make(Customer, notes="VIP client", newsletter_opt_in=True)
```

Keyword arguments always win over generated data, so this also works to override a required field with a specific
value.

### Fields with realistic values

For `StringField`s, `mongo_bakery` checks whether [Faker](https://faker.readthedocs.io/) has a provider method whose
name matches the field's name, and uses it when available. That's why, on the `Customer` example above,
`email`, `company` and `phone_number` come out looking like real data instead of a random word:

```python
customer = baker.make(Customer)
customer.email         # e.g. "jean23@example.com" instead of a random word
customer.company       # e.g. "Smith, Doe and Partners"
customer.phone_number  # e.g. "+1-555-019-2837"
```

Name your fields after a [Faker provider](https://faker.readthedocs.io/en/master/providers.html) (`address`, `city`,
`job`, `url`, ...) to get more meaningful fake data for free. Fields without a matching provider fall back to a
random word.

### Fields restricted with `choices`

When a field declares `choices`, `baker.make` always picks one of the allowed values, so the generated document
passes MongoEngine's validation:

```python
class Order(Document):
    status = StringField(required=True, choices=["pending", "shipped", "delivered"])


order = baker.make(Order)
order.status in ["pending", "shipped", "delivered"]  # always True
```

### Embedded and referenced Documents

`EmbeddedDocumentField` and `ReferenceField` are resolved recursively with `baker.make`, so nested documents are
created for you as well.

### Cleaning up

`baker.make` keeps track of every instance it saved. Call `baker.cleanup()` (e.g. in a test teardown/fixture) to
delete them all:

```python
baker.cleanup()
```

See the [API Reference](https://mongo-bakery.github.io/mongo_bakery/api/) for the full `Baker` interface.

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

### Contributors

<a href="https://github.com/mongo-bakery/mongo_bakery/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=mongo-bakery/mongo_bakery" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
