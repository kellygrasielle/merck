resource "aws_api_gateway_rest_api" "drug_api" {
  name        = "drug-api"
  description = "API for drug discovery data"
}

resource "aws_api_gateway_resource" "upload" {
  rest_api_id = aws_api_gateway_rest_api.drug_api.id
  parent_id   = aws_api_gateway_rest_api.drug_api.root_resource_id
  path_part   = "upload"
}

resource "aws_api_gateway_resource" "data" {
  rest_api_id = aws_api_gateway_rest_api.drug_api.id
  parent_id   = aws_api_gateway_rest_api.drug_api.root_resource_id
  path_part   = "data"
}

resource "aws_api_gateway_method" "upload_post" {
  rest_api_id   = aws_api_gateway_rest_api.drug_api.id
  resource_id   = aws_api_gateway_resource.upload.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "data_get" {
  rest_api_id   = aws_api_gateway_rest_api.drug_api.id
  resource_id   = aws_api_gateway_resource.data.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "upload_post" {
  rest_api_id             = aws_api_gateway_rest_api.drug_api.id
  resource_id             = aws_api_gateway_resource.upload.id
  http_method             = aws_api_gateway_method.upload_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.drug_api.invoke_arn
  credentials             = var.apigateway_role
}

resource "aws_api_gateway_integration" "data_get" {
  rest_api_id             = aws_api_gateway_rest_api.drug_api.id
  resource_id             = aws_api_gateway_resource.data.id
  http_method             = aws_api_gateway_method.data_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.drug_api.invoke_arn
  credentials             = var.apigateway_role
}


resource "aws_api_gateway_deployment" "drug_api" {
  depends_on = [
    aws_api_gateway_integration.upload_post,
    aws_api_gateway_integration.data_get
  ]
  rest_api_id = aws_api_gateway_rest_api.drug_api.id
}



resource "aws_cloudwatch_log_group" "apigw_logs" {
  name = "/aws/apigateway/drug_api"
}

data "aws_caller_identity" "current" {}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.drug_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.drug_api.id}/*/*/*"
}



