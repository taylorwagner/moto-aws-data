import boto3
import os
import pytest

from moto import mock_dynamodb, mock_rds


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb_client(aws_credentials):
    """DynamoDB mock client."""
    with mock_dynamodb():
        conn = boto3.client("dynamodb", region_name="us-east-1")
        yield conn


@pytest.fixture
def rds_client(aws_credentials):
    """RDS mock client."""
    with mock_rds():
        conn = boto3.client("rds", region_name="us-east-1")
        yield conn