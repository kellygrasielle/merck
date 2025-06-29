resource "aws_dynamodb_table" "payments" {
  name           = "${var.project_name}-payments-${var.resource_suffix_identification}"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "status"
  range_key      = "due_payment_date_contract"

    attribute {
      name = "due_payment_date_contract"
      type = "S"
    }

    attribute {
      name = "status"
      type = "S"
    }



}


