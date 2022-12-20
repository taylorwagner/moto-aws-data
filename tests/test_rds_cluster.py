import pytest

from contextlib import contextmanager


@contextmanager
def create_db_cluster(rds_client):
    """Create mock RDS cluster to test"""

    rds_client.create_db_cluster(
        DBClusterIdentifier="my-cluster",
        Engine="mysql",
        MasterUsername="root-cluster",
        MasterUserPassword="password"
    )
    yield


class TestRDSCluster:
    """Test CRUD operations on mock RDS cluster"""

    def test_create_db_cluster(self, rds_client):
        """Test creation of mock RDS cluster"""

        with create_db_cluster(rds_client):

            res = rds_client.describe_db_clusters(
                DBClusterIdentifier="my-cluster"
            )
            cluster_details = res['DBClusters'][0]

            assert cluster_details['DBClusterIdentifier'] == "my-cluster"