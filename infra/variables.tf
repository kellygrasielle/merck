variable "region" { default = "us-east-2" }
variable "account_id" { default = "182274140916" }
variable "s3_bucket_storage" {default = "drug-storage"}
variable "s3_key_arn"  {default = "arn:aws:kms:us-east-2:182274140916:key/c693f19d-0b2a-46ae-aebf-8c61aea67737"}
variable "apigateway_role"  {default = "arn:aws:iam::182274140916:role/AmazonAPIGatewayPushToCloudWatchLogs"}
