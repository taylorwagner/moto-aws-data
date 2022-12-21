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

    TABLE_NAME = "my-test-table"

    def test_create_table(self, dynamodb_client):
        """Test creation of 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            res = dynamodb_client.describe_table(TableName=self.TABLE_NAME)
            res2 = dynamodb_client.list_tables()

            assert res['Table']['TableName'] == self.TABLE_NAME
            assert res2['TableNames'] == [self.TABLE_NAME]


    def test_put_item(self, dynamodb_client):
        """Test adding an item to 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            add_item = dynamodb_client.put_item(
                TableName=self.TABLE_NAME,
                Item={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                },
            )

            res = dynamodb_client.get_item(
                TableName=self.TABLE_NAME,
                Key={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                },
            )

            assert add_item['ResponseMetadata']['HTTPStatusCode'] == 200
            assert res['Item']['attribute1'] == {"S": "attribute1_value"}
            assert len(res['Item']) == 2


    @pytest.mark.skip
    def test_update_item(self, dynamodb_client):
        """Test updating an item to 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            ## Add an item to update
            dynamodb_client.put_item(
                TableName=self.TABLE_NAME,
                Item={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                    "attribute3": {"S": "attribute3_value"}
                },
            )

            ## Update previously added item
            dynamodb_client.update_item(
                TableName=self.TABLE_NAME,
                Key={"attribute1": "attribute1_value", "attribute2": "attribute2_value", "attribute3": "attribute3_value"},
                UpdateExpression="REMOVE attribute3",
                ReturnValues="UPDATED_NEW"
            )

            res = dynamodb_client.get_item(
                TableName=self.TABLE_NAME,
                Key={
                    "attribute1": {"S": "attribute1_value"}
                },
            )
            print(res)


    def test_delete_item(self, dynamodb_client):
        """Test deleting an item from 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            ## Add an item to delete
            dynamodb_client.put_item(
                TableName=self.TABLE_NAME,
                Item={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                },
            )

            ## Delete previously added item
            dynamodb_client.delete_item(
                TableName=self.TABLE_NAME,
                Key={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                },
            )

            res = dynamodb_client.get_item(
                TableName=self.TABLE_NAME,
                Key={
                    "attribute1": {"S": "attribute1_value"},
                    "attribute2": {"S": "attribute2_value"},
                },
            )

            if 'Item' not in res:
                assert res['ResponseMetadata']['HTTPStatusCode'] == 200


    def test_delete_table(self, dynamodb_client):
        """Test deletion of 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            dynamodb_client.delete_table(TableName=self.TABLE_NAME)
            res = dynamodb_client.list_tables()

            assert res['TableNames'] != [self.TABLE_NAME]