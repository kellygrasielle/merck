variable "region" { default = "us-east-2" }
variable "region_s3" { default = "sa-east-1" }
variable "account_id" { default = "182274140916" }
variable "s3_bucket_storage" {default = "drug-api-files"}
variable "s3_key"  {default = "76365d88-8c2e-43e6-b2fd-61cd85eb47bd"}
variable "apigateway_role"  {default = "arn:aws:iam::182274140916:role/AmazonAPIGatewayPushToCloudWatchLogs"}
