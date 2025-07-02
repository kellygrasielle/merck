import pytest

REQUIRED_FIELDS = ['drug_name', 'target', 'efficacy']

def validate_csv(records):
    """
    Validates that each record contains all required fields with non-empty values.

    Args:
        records (list of dict): List of records to validate.

    Raises:
        ValueError: If any required field is missing or empty in a record.
    """
    for row in records:
        for field in REQUIRED_FIELDS:
            if not row.get(field):  # Checks for missing or empty field
                raise ValueError(f"Missing required field: {field}")

def test_validate_csv_success():
    """
    Test that validate_csv passes when all required fields are present and non-empty.
    """
    records = [
        {'drug_name': 'Aspirin', 'target': 'COX', 'efficacy': 'High'},
        {'drug_name': 'Ibuprofen', 'target': 'COX', 'efficacy': 'Medium'}
    ]
    validate_csv(records)  # Should not raise

def test_validate_csv_missing_field():
    """
    Test that validate_csv raises ValueError when a required field is missing.
    """
    records = [
        {'drug_name': 'Aspirin', 'target': 'COX'}  # 'efficacy' is missing
    ]
    with pytest.raises(ValueError, match="Missing required field: efficacy"):
        validate_csv(records)

def test_validate_csv_empty_field():
    """
    Test that validate_csv raises ValueError when a required field is empty.
    """
    records = [
        {'drug_name': 'Aspirin', 'target': '', 'efficacy': 'High'}  # 'target' is empty
    ]
    with pytest.raises(ValueError, match="Missing required field: target"):
        validate_csv(records)