import pytest

from contextlib import contextmanager


@contextmanager
def create_db_instance(rds_client):
    """Create mock RDS instance to test full CRUD operations"""

    rds_client.create_db_instance(
        AllocatedStorage=10,
        DBName="my-test-db",
        DBInstanceIdentifier="my-aurora-instance",
        DBInstanceClass="db.t2.micro",
        Engine="aurora",
        MasterUsername="root",
        MasterUserPassword="123456789",
        Port=3306,
        VpcSecurityGroupIds=["sg-7fa4d512"]
    )
    yield


class TestRDS:
    """Test CRUD operations on mock RDS instance"""

    def test_create_db_instance(self, rds_client):
        """Test creation of mock RDS instance"""

        with create_db_instance(rds_client):

            res = rds_client.describe_db_instances(DBInstanceIdentifier="my-aurora-instance")
            instance_details = res['DBInstances'][0]

            assert instance_details['AllocatedStorage'] == 10
            assert instance_details['DBName'] == "my-test-db"
            assert instance_details['DBInstanceIdentifier'] == "my-aurora-instance"
            assert instance_details['DBInstanceClass'] == "db.t2.micro"
            assert instance_details['Engine'] == "aurora"
            assert instance_details['Endpoint']['Port'] == 3306


    def test_modify_instance(self, rds_client):
        """Test modification of mock RDS instance"""

        with create_db_instance(rds_client):

            res = rds_client.modify_db_instance(
                DBInstanceIdentifier="my-aurora-instance",
                MultiAZ=True,
                EnableIAMDatabaseAuthentication=True
            )

            assert res['DBInstance']['MultiAZ'] == True
            assert res['DBInstance']['IAMDatabaseAuthenticationEnabled'] == True


    def test_delete_db_instance(self, rds_client):
        """Test deletion of mock RDS instance"""

        with create_db_instance(rds_client):

            res = rds_client.delete_db_instance(
                DBInstanceIdentifier="my-aurora-instance",
                SkipFinalSnapshot=False,
                FinalDBSnapshotIdentifier="final-snap",
                DeleteAutomatedBackups=False
            )

            assert res['DBInstance']['DBInstanceIdentifier'] == "my-aurora-instance"

            