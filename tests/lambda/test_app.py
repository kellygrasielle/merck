import json
from db import get_all_records
from upload import handle_upload

def lambda_handler(event, context):
    """
    AWS Lambda entry point.
    """
    route = event.get("resource")
    method = event.get("httpMethod")

    if route == "/upload" and method == "POST":
        return handle_upload(event, context)
    elif route == "/data" and method == "GET":
        data = get_all_records()
        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }
    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Not found"})
    }