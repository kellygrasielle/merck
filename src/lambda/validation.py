# Global resources (reuse across Lambda invocations)
REQUIRED_FIELDS = ['drug_name', 'target', 'efficacy']

def validate_csv(records):
    """
    Validates that each record contains all required fields and that they are not empty.
    Raises ValueError with details if any required field is missing or empty.
    """
    for idx, row in enumerate(records, start=1):
        for field in REQUIRED_FIELDS:
            value = row.get(field, '').strip() if isinstance(row.get(field), str) else row.get(field)
            if not value:
                raise ValueError(f"Missing or empty required field '{field}' in row {idx}")