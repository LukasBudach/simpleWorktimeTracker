from TrackedMonth import TrackedMonth

import pandas as pd
import unittest


class TestTrackedMonth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._test_data = pd.DataFrame(data={'date': ['04.05.2020', '04.05.2020', '06.05.2020', '10.05.2020'],
                                            'start': ['10:00', '13:00', '09:25', '17;45'],
                                            'end': ['12:30', '17:20', '13:50', ' 19:00'],
                                            'work time': ['02:30', '04:20', '04:25', '01:15'],
                                            'running total': ['02:30', '06:50', '11:15', '12:30'],
                                            'description': ['desc one', 'desc two', 'desc three', 'desc four']})

    def test_validate_valid_header(self):
        self.assertIsNone(TrackedMonth.validate_header(self._test_data))

    def test_validate_invalid_header(self):
        invalid_data = self._test_data.drop(columns=['end'])
        with self.assertRaises(AssertionError):
            TrackedMonth.validate_header(invalid_data)


if __name__ == '__main__':
    unittest.main()
