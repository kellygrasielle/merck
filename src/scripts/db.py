import boto3
import os

# Global resources (reuse across Lambda invocations)
DYNAMODB_TABLE = os.environ.get('TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE)

def save_records(records):
    """
    Batch writes a list of records to the DynamoDB table.

    Args:
        records (list of dict): List of items to be saved to the table.
    """
    with table.batch_writer() as batch:
        for row in records:
            batch.put_item(Item=row)

def get_all_records():
    """
    Retrieves all records from the DynamoDB table.

    Returns:
        list of dict: All items from the table.
    """
    response = table.scan()
    return response.get('Items', [])