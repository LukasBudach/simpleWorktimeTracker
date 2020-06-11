import datetime


class Month:
    @classmethod
    def from_summary_string(cls, date_str):
        dt = datetime.datetime.strptime(date_str, '%B %Y')
        return cls(dt.month, dt.year)

    def __init__(self, month, year):
        self._month = month
        self._year = year

    def __str__(self):
        return self.as_string()

    def __repr__(self):
        return self.as_string()

    def __le__(self, other):
        assert type(other) == Month
        return (self.year() <= other.year()) and (self.month() <= other.month())

    def __lt__(self, other):
        assert type(other) == Month
        return (self.year() < other.year()) or ((self.year() == other.year()) and (self.month() < other.month()))

    def __ge__(self, other):
        assert type(other) == Month
        return (self.year() >= other.year()) and (self.month() >= other.month())

    def __gt__(self, other):
        assert type(other) == Month
        return (self.year() > other.year()) or ((self.year() == other.year()) and (self.month() > other.month()))

    def __eq__(self, other):
        assert type(other) == Month
        return (self.year() == other.year()) and (self.month() == other.month())

    def __ne__(self, other):
        assert type(other) == Month
        return not self.__eq__(other)

    def as_string(self):
        dt = datetime.date(self._year, self._month, 1)
        return dt.strftime('%B %Y')

    def month(self):
        return self._month

    def year(self):
        return self._year
