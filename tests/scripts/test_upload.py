import base64
import json
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
os.environ['TABLE_NAME'] = 'dummy-table'

with patch('boto3.resource') as mock_boto_resource, patch('boto3.client') as mock_boto_client:
    # Mock the Table object
    mock_table = MagicMock()
    mock_table.scan.return_value = {'Items': [{"id": 1, "name": "test"}]}
    mock_boto_resource.return_value.Table.return_value = mock_table
    
    # Mock the S3 client
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    # Now import your module (replace 'your_module' with the actual module name)
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/scripts')))
    import upload


# Importe suas funções do módulo correto
class TestUploadFunctions(unittest.TestCase):

    def test_extract_csv_from_multipart_success(self):
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        filename = 'test.csv'
        csv_content = 'col1,col2\nval1,val2'
        multipart_body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f'Content-Type: text/csv\r\n\r\n'
            f'{csv_content}\r\n'
            f'--{boundary}--\r\n'
        ).encode()
        result = upload.extract_csv_from_multipart(multipart_body, boundary)
        self.assertEqual(result.decode(), csv_content)

    def test_extract_csv_from_multipart_not_csv(self):
        boundary = 'boundary'
        multipart_body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="file.txt"\r\n'
            f'Content-Type: text/csv\r\n\r\n'
            f'data\r\n'
            f'--{boundary}--\r\n'
        ).encode()
        with self.assertRaises(ValueError):
            upload.extract_csv_from_multipart(multipart_body, boundary)

    def test_extract_csv_from_multipart_no_csv(self):
        boundary = 'boundary'
        multipart_body = b'--boundary--\r\n'
        with self.assertRaises(ValueError):
            upload.extract_csv_from_multipart(multipart_body, boundary)

    def test_get_header_case_insensitive(self):
        event = {'headers': {'content-type': 'abc', 'X-Test': '123'}}
        self.assertEqual(upload.get_header(event, 'Content-Type'), 'abc')
        self.assertEqual(upload.get_header(event, 'x-test'), '123')
        self.assertEqual(upload.get_header(event, 'missing'), '')

 
    def test_handle_upload_success(self):
        boundary = 'boundary'
        csv_content = {'drug_name': 'A', 'target': 'B', 'efficacy': 'High'}
        multipart_body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="file.csv"\r\n'
            f'Content-Type: text/csv\r\n\r\n'
            f'{csv_content}\r\n'
            f'--{boundary}--\r\n'
        ).encode()
        event = {
            'body': base64.b64encode(multipart_body).decode(),
            'isBase64Encoded': True,
            'headers': {'Content-Type': f'multipart/form-data; boundary={boundary}'}
        }
        context = MagicMock()
        context.aws_request_id = 'abc123'
        response = upload.handle_upload(event, context)
        self.assertEqual(response['statusCode'], 201)
        body = json.loads(response['body'])
        self.assertIn('Upload successful', body['message'])
        self.assertIn('abc123', body['s3_key'])
        mock_s3.put_object.assert_called_once()
     
       

    def test_handle_upload_invalid_content_type(self):
        event = {
            'body': '',
            'isBase64Encoded': False
        }
        context = MagicMock()
        response = upload.handle_upload(event, context)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Missing or invalid Content-Type header', response['body'])

if __name__ == '__main__':
    unittest.main()