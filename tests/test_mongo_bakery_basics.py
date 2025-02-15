
def test_mongo_bakery_module_exists():
    from mongo_bakery import baker
    assert baker is not None


def test_baker_has_make_method():
    from mongo_bakery import baker
    assert hasattr(baker, "make") and callable(baker.make)


def test_baker_make_accepts_model():
    from mongo_bakery import baker

    class FakeModel:
        pass

    obj = baker.make(FakeModel)

    assert isinstance(obj, FakeModel)
