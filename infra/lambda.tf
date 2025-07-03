data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir = "../src/scripts"
  output_path = "${path.module}/drug_source.zip"
}

resource "aws_lambda_function" "drug_api" {
  function_name = "drug"
  filename      = data.archive_file.lambda_zip.output_path
  handler       = "app.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.drug_data.name,
      BUCKET_NAME = "drug-api-files"
    }
  }
  timeout = 30
}