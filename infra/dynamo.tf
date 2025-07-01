resource "aws_dynamodb_table" "drug_data" {
  name           = "DrugData"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "drug_name"
  
    attribute {
      name = "drug_name"
      type = "S"
    }s

   
}

