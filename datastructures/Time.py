from math import floor

class Time:
    @classmethod
    def from_string(cls, input_str: str):
        # check whether the string is negative
        time_start = 1 if input_str[0] == '-' else 0
        is_negative = input_str[0] == '-'
        hours = int(input_str[time_start:-3])
        minutes = int(input_str[-2:])
        return cls(hours, minutes, is_negative)

    @classmethod
    def required_time_calculation(cls, days: int, hours_per_week: float):
        req_as_minutes = floor(days * hours_per_week * 60 / 7)
        minutes = req_as_minutes % 60
        hours = floor((req_as_minutes - minutes) / 60)
        return cls(hours, minutes, False)

    def __init__(self, hours: int, minutes: int, is_negative: bool):
        self._hours = hours
        self._minutes = minutes
        self._is_negative = is_negative

    def __add__(self, other):
        assert type(other) == Time
        sum = self.value() + other.value()
        s_is_neg = sum < 0
        sum = abs(sum)
        minutes = sum % 60
        hours = floor((sum - minutes) / 60)
        return Time(hours, minutes, s_is_neg)

    def __sub__(self, other):
        assert type(other) == Time
        return self.__add__(Time(other.hours(), other.minutes(), not other.is_negative()))

    def __eq__(self, other):
        assert type(other) == Time
        return self.value() == other.value()

    def __ne__(self, other):
        assert type(other) == Time
        return not self.__eq__(other)

    def __lt__(self, other):
        assert type(other) == Time
        return self.value() < other.value()

    def __le__(self, other):
        assert type(other) == Time
        return self.value() <= other.value()

    def __gt__(self, other):
        assert type(other) == Time
        return self.value() > other.value()

    def __ge__(self, other):
        assert type(other) == Time
        return self.value() >= other.value()

    def __str__(self):
        return self.as_string()

    def __repr__(self):
        return self.as_string()

    def __hash__(self):
        return hash(self.value())

    def hours(self):
        return self._hours

    def minutes(self):
        return self._minutes

    def value(self):
        return (self._hours * 60 + self._minutes) * (-1 if self._is_negative else 1)

    def is_positive(self):
        return not self.is_negative()

    def is_negative(self):
        return self._is_negative

    def as_string(self):
        return '{}{:02d}:{:02d}'.format('-' if self._is_negative else '', self._hours, self._minutes)
