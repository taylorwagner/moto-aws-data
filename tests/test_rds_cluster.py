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
    """Test operations on mock RDS cluster"""

    def test_create_db_cluster(self, rds_client):
        """Test creation of mock RDS cluster"""

        with create_db_cluster(rds_client):

            res = rds_client.describe_db_clusters(
                DBClusterIdentifier="my-cluster"
            )
            cluster_details = res['DBClusters'][0]

            assert cluster_details['DBClusterIdentifier'] == "my-cluster"


    def test_create_and_delete_db_cluster_snapshot(self, rds_client):
        """Test creation and deletion of mock RDS cluster snapshot"""

        with create_db_cluster(rds_client):

            create_res = rds_client.create_db_cluster_snapshot(
                DBClusterSnapshotIdentifier="my-cluster-snap",
                DBClusterIdentifier="my-cluster"
            )
            describe_snapshot = rds_client.describe_db_cluster_snapshots(
                DBClusterSnapshotIdentifier="my-cluster-snap",
                DBClusterIdentifier="my-cluster"
            )
            
            assert create_res['DBClusterSnapshot']['DBClusterSnapshotIdentifier'] == 'my-cluster-snap'
            assert create_res['DBClusterSnapshot']['SnapshotCreateTime'] != None
            assert describe_snapshot['DBClusterSnapshots'][0]['DBClusterIdentifier'] == 'my-cluster'

            rds_client.delete_db_cluster_snapshot(
                DBClusterSnapshotIdentifier="my-cluster-snap"
            )
            describe_snapshot2 = rds_client.describe_db_cluster_snapshots(
                DBClusterSnapshotIdentifier="my-cluster-snap",
                DBClusterIdentifier="my-cluster"
            )

            assert describe_snapshot2['DBClusterSnapshots'] == []


    def test_delete_db_cluster(self, rds_client):
        """Test deletion of mock RDS cluster"""

        with create_db_cluster(rds_client):

            res = rds_client.delete_db_cluster(
                DBClusterIdentifier="my-cluster"
            )
            
            assert res['DBCluster']['EarliestRestorableTime'] != None