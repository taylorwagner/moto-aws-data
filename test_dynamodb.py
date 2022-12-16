import pytest

from dynamodb import MyDynamoDBClient


@pytest.fixture
def table_name():
    return "my-test-table"


@pytest.fixture
def dynamodb_test(dynamodb_client, table_name):
    dynamodb_client.create_table(
        TableName=table_name,
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

def test_list_tables(dynamodb_client, dynamodb_test):
    client = MyDynamoDBClient()
    tables = client.list_tables()
    assert tables == ["my-test-table"]