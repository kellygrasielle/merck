import unittest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/scripts')))
import validation


class TestValidateCSV(unittest.TestCase):
    def test_valid_records(self):
        records = [
            {'drug_name': 'A', 'target': 'B', 'efficacy': 'High'},
            {'drug_name': 'C', 'target': 'D', 'efficacy': 'Low'}
        ]
        # Should not raise
        validation.validate_csv(records)

    def test_missing_field(self):
        records = [
            {'drug_name': 'A', 'target': 'B'},  # Missing 'efficacy'
        ]
        with self.assertRaises(ValueError) as cm:
            validation.validate_csv(records)
        self.assertIn('Missing or empty required field \'efficacy\' in row 1', str(cm.exception))

    def test_empty_field(self):
        records = [
            {'drug_name': 'A', 'target': '', 'efficacy': 'High'},  # Empty 'target'
        ]
        with self.assertRaises(ValueError) as cm:
            validation.validate_csv(records)
        self.assertIn('Missing or empty required field \'target\' in row 1', str(cm.exception))

    def test_multiple_records(self):
        records = [
            {'drug_name': 'A', 'target': 'B', 'efficacy': 'High'},
            {'drug_name': '', 'target': 'D', 'efficacy': 'Low'},  # Empty 'drug_name'
        ]
        with self.assertRaises(ValueError) as cm:
            validation.validate_csv(records)
        self.assertIn('Missing or empty required field \'drug_name\' in row 2', str(cm.exception))

if __name__ == '__main__':
    unittest.main()