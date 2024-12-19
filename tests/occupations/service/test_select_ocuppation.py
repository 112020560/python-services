import pytest
from unittest.mock import MagicMock
from src.occupations.domain.ports.fcompras_repository import FComprasRepository
from src.occupations.adapters.fcompras_repository import DynamoFComprasRepository
from src.utils.document_store.adapters.dynamo_db import DynamoDBAdapter
from src.occupations.domain import model
from src.occupations.services.select_occupation import validate_and_process_occupation


@pytest.fixture
def mock_dynamo_adapter():
    # Mock the DynamoDBAdapter
    return MagicMock(spec=DynamoDBAdapter)


@pytest.fixture
def repository(mock_dynamo_adapter):
    # Create an instance of DynamoFComprasRepository with the mocked adapter
    return DynamoFComprasRepository(fcompras_table=mock_dynamo_adapter)


def test_get(repository, mock_dynamo_adapter):
    # Prepare mock data
    mock_customer_id = 123
    mock_data = {"customer_id": mock_customer_id, "occupation": "employee", "is_real_property": True}
    
    # Set the mock to return mock_data when get is called
    mock_dynamo_adapter.get.return_value = mock_data
    
    # Call the method
    result = repository.get(mock_customer_id)
    
    # Assert that the get method was called with the correct arguments
    mock_dynamo_adapter.get.assert_called_once_with(key={"customer_id": mock_customer_id})
    
    # Assert that the result matches the mock data
    assert result == mock_data


def test_persist(repository, mock_dynamo_adapter):
    # Prepare mock data to save
    key = {"customer_id": 123}
    occupation_data = {"occupation": "student", "is_real_property": True}
    
    # Set up the mock for the put method
    mock_dynamo_adapter.put.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    
    # Call persist method
    repository.persist(key, occupation_data)
    
    # Assert that the put method was called with the correct arguments
    mock_dynamo_adapter.put.assert_called_once_with({**key, **occupation_data})
    
    # Optionally, you can check that DynamoDB response is as expected (e.g., status code)
    assert mock_dynamo_adapter.put.return_value["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_validate_and_process_occupation(repository, mock_dynamo_adapter):
    # Mock occupation data
    mock_event = model.OccupationDTO(customer_id=123, occupation="employee")
    
    # Mock repository interaction
    mock_dynamo_adapter.put.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    # Run your validation and process function
    result = validate_and_process_occupation(mock_event, repository)
    
    # Check if the correct occupation was processed and persisted
    assert result["occupation"] == "employee"
    assert result["is_real_property"] is True

    # Assert that persist method was called with the correct data
    mock_dynamo_adapter.put.assert_called_once_with(
        {"customer_id": 123, "occupation": "employee", "is_real_property": True}
    )
