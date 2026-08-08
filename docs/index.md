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

### Reproducible data with `baker.seed`

Call `baker.seed(value)` to seed Faker's random generator, so `baker.make` produces the same mock data across runs
— useful for debugging a flaky test or reproducing a specific failure:

```python
baker.seed(1234)
customer = baker.make(Customer)  # always the same field values for this seed
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

`mongo_bakery` also ships as a pytest plugin, registered automatically once it's installed. Use the `baker` fixture
instead to get this cleanup for free after every test:

```python
def test_something(baker):
    customer = baker.make(Customer)
    ...
# cleanup() is called automatically once the test finishes
```

See the [API Reference](api.md) for the full `Baker` interface.

## Contributing

Contributions are welcome! See the
[Contributing guide](https://github.com/mongo-bakery/mongo_bakery/blob/main/README.md#contributing) in the project
README for how to get started.
