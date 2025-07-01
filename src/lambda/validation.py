REQUIRED_FIELDS = ['drug_name', 'target', 'efficacy']

def validate_csv(records):
    for row in records:
        for field in REQUIRED_FIELDS:
            if field not in row or not row[field]:
                raise ValueError(f"Missing required field: {field}")