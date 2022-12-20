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
        """Test creation of 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            res = dynamodb_client.describe_table(TableName="my-test-table")
            res2 = dynamodb_client.list_tables()
            assert res['Table']['TableName'] == "my-test-table"
            assert res2['TableNames'] == ["my-test-table"]

    def test_put_item(self, dynamodb_client):
        """Test adding an item to 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            add_item = dynamodb_client.put_item(
                TableName="my-test-table",
                Item={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                },
            )

            res = dynamodb_client.get_item(
                TableName="my-test-table",
                Key={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                },
            )

            assert add_item['ResponseMetadata']['HTTPStatusCode'] == 200
            assert res['Item']['attribute1'] == {"S": "attribute1_value"}

    def test_delete_table(self, dynamodb_client):
        """Test deletion of 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            dynamodb_client.delete_table(TableName="my-test-table")
            res = dynamodb_client.list_tables()
            assert res['TableNames'] != ["my-test-table"]