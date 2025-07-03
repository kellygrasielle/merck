import base64
import boto3
import csv
from src.scripts.db import save_records
import json
import logging
import os
import re
from typing import Any, Dict
from validation import validate_csv


# Global resources (reuse across Lambda invocations)
S3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def extract_csv_from_multipart(body: bytes, boundary: str) -> bytes:
    """
    Extracts CSV file content from multipart/form-data body.
    Ensures the file is a CSV by checking Content-Type and filename extension.
    """
    parts = body.split(boundary.encode())
    for part in parts:
        if b'Content-Type: text/csv' in part:
            # Check filename extension in Content-Disposition
            disposition_match = re.search(
                b'Content-Disposition:.*filename="([^"]+)"', part)
            if disposition_match:
                filename = disposition_match.group(1).decode()
                if not filename.lower().endswith('.csv'):
                    raise ValueError("Uploaded file is not a .csv file")
            csv_start = part.find(b'\r\n\r\n') + 4
            csv_content = part[csv_start:]
            csv_content = csv_content.strip(b'\r\n--')
            return csv_content
    raise ValueError("CSV file not found in multipart data")

def get_header(event: Dict[str, Any], key: str) -> str:
    """
    Retrieves a header value in a case-insensitive way.
    """
    headers = event.get('headers', {})
    for k, v in headers.items():
        if k.lower() == key.lower():
            return v
    return ""

def handle_upload(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handles the /upload POST route for CSV file uploads.
    """
    try:
        body = event['body']
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body)
        else:
            body = body.encode('utf-8')

        content_type = get_header(event, 'Content-Type')
        if not content_type or "boundary=" not in content_type:
            raise ValueError("Missing or invalid Content-Type header")
        boundary = content_type.split("boundary=")[-1]

        csv_bytes = extract_csv_from_multipart(body, boundary)
        csv_text = csv_bytes.decode('utf-8')

        s3_key = f"uploads/upload_{context.aws_request_id}.csv"
        # Uncomment to save to S3
        S3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=csv_bytes, ContentType='text/csv')

        records = list(csv.DictReader(csv_text.splitlines()))
        validate_csv(records)
        save_records(records)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Upload successful",
                "s3_key": s3_key
            })
        }
    except Exception as e:
        LOGGER.exception("Upload failed")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }