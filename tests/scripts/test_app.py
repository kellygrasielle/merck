
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Set the environment variable before importing your module
os.environ['TABLE_NAME'] = 'dummy-table'

with patch('boto3.resource') as mock_boto_resource:
    # Mock the Table object
    mock_table = MagicMock()
    mock_table.scan.return_value = {'Items': [{"id": 1, "name": "test"}]}
    mock_boto_resource.return_value.Table.return_value = mock_table

    # Now import your module (replace 'your_module' with the actual module name)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/scripts')))
    import app

class TestLambdaHandler(unittest.TestCase):
    

    def test_data_route(self):
        event = {
            "resource": "/data",
            "httpMethod": "GET"
        }
        context = MagicMock()
        response = app.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn("test", response['body'])
       

    def test_not_found_route(self):
        event = {
            "resource": "/unknown",
            "httpMethod": "GET"
        }
        context = MagicMock()
        response = app.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 404)
        self.assertIn("Not found", response['body'])

if __name__ == '__main__':
    unittest.main()