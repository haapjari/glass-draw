import unittest
from datetime import datetime
from analysis.analysis import normalize_dataset

class TestNormalizeDataset(unittest.TestCase):
    maxDiff = None 

    def test_normalize_dataset(self):
        # Example input dictionary
        dataset_columns = {
            'repository_url': ['https://github.com/user/repo1', 'https://github.com/user/repo2', 'https://github.com/user/repo3'],
            'open_issue_count': [10, 5, 3],
            'closed_issue_count': [50, 30, 10],
            'commit_count': [100, 200, 300],
            'stargazer_count': [500, 1000, 2000],
            'creation_date': ['2021-02-07T21:37:53Z', '2022-02-07T21:37:53Z', '2023-02-07T21:37:53Z'],
            'latest_release': ['2022-02-07T21:37:53Z', '2023-02-07T21:37:53Z', '2024-02-07T21:37:53Z'],
            'original_codebase_size': [10000, 20000, 30000],
            'library_codebase_size': [5000, 10000, 15000]
        }

        # Expected output dictionary
        expected_output = {
            'open_issue_count': [5.0, 2.5, 1.6666666666666667],
            'closed_issue_count': [5.0, 2.5, 0.0],
            'commit_count': [0.0, 2.5, 5.0],
            'stargazer_count': [0.0, 2.5, 5.0],
            'creation_date': [
                datetime(2021, 2, 7, 21, 37, 53),
                datetime(2022, 2, 7, 21, 37, 53),
                datetime(2023, 2, 7, 21, 37, 53)
            ],
            'latest_release': [
                datetime(2022, 2, 7, 21, 37, 53),
                datetime(2023, 2, 7, 21, 37, 53),
                datetime(2024, 2, 7, 21, 37, 53)
            ],
            'original_codebase_size': [0.0, 2.5, 5.0],
            'library_codebase_size': [0.0, 2.5, 5.0]
        }

        # Call the function
        actual_output = normalize_dataset(dataset_columns)

        # Check the output against the expected output
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
