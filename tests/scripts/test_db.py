import unittest, os, sys
from unittest.mock import patch, MagicMock
os.environ['TABLE_NAME'] = 'dummy-table'

with patch('boto3.resource') as mock_boto_resource:
    # Mock the Table object
    mock_table = MagicMock()
    mock_table.scan.return_value = {'Items': [{"id": 1, "name": "test"}]}
    mock_boto_resource.return_value.Table.return_value = mock_table

    # Now import your module (replace 'your_module' with the actual module name)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/scripts')))
    import db


class TestDynamoDBRepository(unittest.TestCase):
 

    def test_save_records(self):
        records = [{'id': 1}, {'id': 2}]
        db.save_records(records)
        
        mock_table.batch_writer.assert_called_once()

    def test_get_all_records_single_page(self):
        result = db.get_all_records()
        self.assertEqual(result, [{"id": 1, "name": "test"}])
        mock_table.scan.assert_called_once()

   

if __name__ == '__main__':
    unittest.main()