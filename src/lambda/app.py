import json
import base64
import csv
import boto3
import os
from validation import validate_csv
from db import save_records, get_all_records

s3 = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET', 'meu-bucket') 

def extract_csv_from_multipart(body, boundary):
    parts = body.split(boundary.encode())
    for part in parts:
        if b'Content-Type: text/csv' in part:
            csv_start = part.find(b'\r\n\r\n') + 4
            csv_content = part[csv_start:]
            csv_content = csv_content.strip(b'\r\n--')
            return csv_content
    raise ValueError("CSV file not found in multipart data")

def lambda_handler(event, context):
    route = event.get("resource")
    method = event.get("httpMethod")
    
    if route == "/upload" and method == "POST":
        try:
            if event.get('isBase64Encoded', False):
                body = base64.b64decode(event['body'])
            else:
                body = event['body'].encode('utf-8')
            
            content_type = event['headers'].get('Content-Type') or event['headers'].get('content-type')
            boundary = content_type.split("boundary=")[-1]
            csv_bytes = extract_csv_from_multipart(body, boundary)
            csv_text = csv_bytes.decode('utf-8')

            # Salva no S3
            s3_key = f"uploads/upload_{context.aws_request_id}.csv"
            s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=csv_bytes, ContentType='text/csv')

            records = list(csv.DictReader(csv_text.splitlines()))
            print(records)
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
            return {"statusCode": 400, "body": json.dumps({"error": str(e)})}
    
    elif route == "/data" and method == "GET":
        data = get_all_records()
        return {"statusCode": 200, "body": json.dumps(data)}
    
    return {"statusCode": 404, "body": json.dumps({"error": "Not found"})}