import boto3
import os

# Global resources (reuse across Lambda invocations)
DYNAMODB_TABLE = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE)

def save_records(records):
    with table.batch_writer() as batch:
        for row in records:
            batch.put_item(Item=row)

def get_all_records():
    response = table.scan()
    return response.get('Items', [])