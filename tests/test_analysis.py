import unittest
from datetime import datetime
from analysis.analysis import normalize_date_values

class TestDateNormalization(unittest.TestCase):

    def test_normalize_date_values(self):
        date_list = ["2023-01-15T05:46:17Z", "2023-02-01T10:23:12Z", "2023-03-08T15:01:45Z"]
        expected_output = [0.0, 0.4548944336099585, 1.0]

        # Test with empty list
        result = normalize_date_values([])
        self.assertEqual(result, [])

        # Test with list of one date
        result = normalize_date_values(["2023-02-01T10:23:12Z"])
        self.assertEqual(result, [0.0])

        # Test with list of identical dates
        result = normalize_date_values(["2023-02-01T10:23:12Z", "2023-02-01T10:23:12Z", "2023-02-01T10:23:12Z"])
        self.assertEqual(result, [0.0, 0.0, 0.0])

        # Test with list of non-date strings
#        result = normalize_date_values(["hello", "world"])
        #self.assertEqual(result, [])

        ## Test with list of non-string values
        #result = normalize_date_values([1, 2, 3])
        #self.assertEqual(result, [])

        # Test with original list of dates
        result = normalize_date_values(date_list)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
