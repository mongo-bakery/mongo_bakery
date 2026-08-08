import datetime


class Sequence:
    """Produces an incrementing value on each call, for use as a `baker.make` kwarg."""

    def __init__(self, value, increment_by=1, start=None):
        self.value = value
        self.increment_by = increment_by
        self._step = start if start is not None else increment_by

    def __call__(self):
        if isinstance(self.value, str):
            result = f"{self.value}{self._step}"
        elif isinstance(self.value, (int, float, datetime.date, datetime.datetime)):
            result = self.value + self._step
        else:
            raise ValueError(f"No sequence strategy defined for value type: {type(self.value).__name__}")

        self._step += self.increment_by
        return result
