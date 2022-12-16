import boto3


class MyDynamoDBClient:
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client("dynamodb", region_name=region_name)
    
    def list_tables(self):
        """Returns a list of table names"""
        res = self.client.list_tables()
        return [table for table in res["TableNames"]]