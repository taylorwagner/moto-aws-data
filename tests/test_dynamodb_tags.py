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
        },
        Tags=[
            {"Key": "TestTag", "Value": "TestValue"},
            {"Key": "TestTag2", "Value": "TestValue2"},
        ]
    )
    yield


class TestDynamoDBTagging:
    """Test tag operations on mock DynamoDB table"""

    def test_list_table_tags(self, dynamodb_client):
        """Test listing the tags on 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            res = dynamodb_client.describe_table(TableName="my-test-table")
            table_arn = res['Table']['TableArn']
            list_tags = dynamodb_client.list_tags_of_resource(ResourceArn=table_arn)

            assert table_arn == "arn:aws:dynamodb:us-east-1:123456789012:table/my-test-table"
            assert list_tags['Tags'][0] == {'Key': 'TestTag', 'Value': 'TestValue'}, {'Key': 'TestTag2', 'Value': 'TestValue2'}
            assert len(list_tags['Tags']) == 2


    def test_add_tags(self, dynamodb_client):
        """Test adding tags to 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            res = dynamodb_client.describe_table(TableName="my-test-table")
            table_arn = res['Table']['TableArn']

            dynamodb_client.tag_resource(
                ResourceArn=table_arn,
                Tags=[
                    {"Key": "NewTag", "Value": "NewValue"},
                    {"Key": "NewestTag", "Value": "NewestValue"},
                ]
            )

            list_tags = dynamodb_client.list_tags_of_resource(ResourceArn=table_arn)

            assert list_tags['Tags'][2] == {'Key': 'NewTag', 'Value': 'NewValue'}
            assert list_tags['Tags'][3] == {'Key': 'NewestTag', 'Value': 'NewestValue'}
            assert len(list_tags['Tags']) == 4


    def test_remove_tags(self, dynamodb_client):
        """Test removing tags from 'my-test-table' DynamoDB table"""

        with create_table(dynamodb_client):

            res = dynamodb_client.describe_table(TableName="my-test-table")
            table_arn = res['Table']['TableArn']

            dynamodb_client.untag_resource(
                ResourceArn=table_arn,
                TagKeys=[
                    'TestTag',
                    'TestTag2'
                ]
            )

            list_tags = dynamodb_client.list_tags_of_resource(ResourceArn=table_arn)

            assert list_tags['Tags'] == []
            assert len(list_tags['Tags']) == 0