# Mongo Bakery

Inspired by [model-bakery](https://model-bakery.readthedocs.io/en/latest/), this project aims to simplify the process
of creating MongoDB documents for testing purposes. The goal is to deliver a maintainable, intuitive, and
developer-friendly API specifically designed for MongoDB. By streamlining the generation of test data, this tool
empowers developers to efficiently create realistic document structures, enhancing the testing workflow for
applications that rely on MongoDB as their primary database.

## Motivation

- To have the conveniences of model_bakery (from the Django world) in Flask with MongoEngine.
- We want more context within the test itself (instead of having fixtures in conftest where we don't know which
  fields are populated).
- We don't want to create a Factory for every Document in the application.

## Installation

```bash
uv add mongo-bakery
```

## Quick usage

```python
from mongo_bakery import baker

instance = baker.make(MyDocument)
instances = baker.make(MyDocument, _quantity=3)

baker.cleanup()
```

See the [API Reference](api.md) for the full `Baker` interface.

## Contributing

Contributions are welcome! See the
[Contributing guide](https://github.com/mongo-bakery/mongo_bakery/blob/main/README.md#contributing) in the project
README for how to get started.
