# Drug Target CSV Microservice

## Overview
This project is a serverless microservice for uploading, validating, and storing drug target data from CSV files. It is designed to run on AWS Lambda, with data persisted in DynamoDB and files stored in S3. The infrastructure is provisioned using Terraform, located in the infra folder.

## Features
SV Upload: Accepts CSV files via a /upload endpoint, validates required fields, and stores the data. <br>
Data Retrieval: Provides a /data endpoint to fetch all records from DynamoDB.<br>
AWS Integration: Uses S3 for file storage and DynamoDB for data persistence.<br>
Infrastructure as Code: All AWS resources are managed via Terraform scripts.<br>
Clean Code Principles: The codebase follows clean code practices for readability, maintainability, and testability.<br>

## Clean Code Practices

This project adheres to clean code principles, including:

<b>Separation of Concerns:</b> Business logic, data access, and validation are separated into different modules (db.py, upload.py, validation.py). <br>
<b>Descriptive Naming:</b> Functions, variables, and constants use clear, descriptive names.<br>
<b>Single Responsibility:</b> Each function and module has a single, well-defined responsibility.<br>
<b>Error Handling:</b> Exceptions are caught and logged, with meaningful error messages returned to the client.<br>
<b>Reusability: </b>Global resources (e.g., S3 client, DynamoDB table) are initialized once and reused across Lambda invocations.<br>
<b>Testability:</b> The code is structured to facilitate unit testing, with external dependencies easily mockable.<br>

## Requirements

Python 3.8+
Terraform 1.x
AWS CLI configured

## Testing

To run tests use command as example, run:

	python3 -m tests.scripts.test_upload
	
## Terraform

To deploy the infrastructure, run:

```
cd infra
terraform init
terraform apply
```

	
## Folder Structure

. ├── src/ │ └── scripts/ │ ├── app.py ├── db.py │ ├── upload.py │ └── validation.py ├── infra/ │ └── (Terraform files) ├── tests/ │ └── scripts/ │ └── (Test files) └── README.md └── requirements.txt	 
	
## Notes	
	
Single Lambda Handler: Although AWS recommends one Lambda per endpoint, this project uses a single Lambda handler for both /upload and /data for illustration purposes.
