import pytest

from contextlib import contextmanager


@contextmanager
def create_table(dynamodb_client):
    """Create mock DynamoDB table to test full CRUD operations"""

    dynamodb_client.create_table(
        TableName="my-test-table",
        KeySchema=[
            {
                'AttributeName': 'attribute1',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'attribute2',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'attribute1',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'attribute2',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    yield

class TestDynamoDB:
    """Test CRUD operations on mock DynamoDB table"""

    def test_create_table(self, dynamodb_client):
        """Test creation of DynamoDB table"""

        with create_table(dynamodb_client):

            res = dynamodb_client.describe_table(TableName="my-test-table")
            assert res['Table']['TableName'] == "my-test-table"