# Hadoop Upgrade

Apache Hadoop, when deployed in HA, supports a rolling upgrade to avoid
downtime.  In non-HA, the upgrade steps are the same, but will incur downtime as
services are restarted.

Upgrading will result in the following services being restarted:

  * NameNode
  * DataNode
  * ResourceManager
  * NodeManager
  * JobHistoryServer

However, the following services will *not* be restarted automatically, as doing
so would causing downtime:

  * JournalNode
  * ZKFC

The slave nodes have actions for restarting these services manually.


## Performing an Upgrade

The steps of an upgrade are:

  1. Set the target Hadoop version on each service
  2. Prepare the upgrade, wait until complete
  3. Upgrade each NameNode (starting with the standby will minimize fail-overs)
  4. Upgrade the ResourceManager
  5. Upgrade the slaves (individually, or in groups)
  6. Finalize the upgrade

The Juju commands for performing an upgrade are:

    juju set namenode hadoop_version=2.7.2
    juju set resourcemanager hadoop_version=2.7.2
    juju set slave hadoop_version=2.7.2

    juju action do namenode/0 prepare-upgrade

    # repeat this until the image is ready
    juju action do namenode/0 query
    juju action fetch --wait 0 <query-action-id>

    # once the image is complete, proceed with the upgrade
    juju action do namenode/1 upgrade
    juju action do namenode/0 upgrade

    juju action do resourcemanager/0 upgrade

    juju action do slave/0 upgrade  # for each slave

    juju action do namenode/1 finalize


## Performing a Downgrade

You can also downgrade Hadoop from an in-progress or previous upgrade, as long
as the versions have the same NameNode and DataNode layout format.

The steps for downgrading are very similar to upgrading, but note that slaves
*must* be downgraded before masters:

    juju set namenode hadoop_version=2.7.1
    juju set resourcemanager hadoop_version=2.7.1
    juju set slave hadoop_version=2.7.1

    juju action do namenode/0 prepare-upgrade

    # repeat this until the image is ready
    juju action do namenode/0 query
    juju action fetch --wait 0 <query-action-id>

    # once the image is complete, proceed with the upgrade
    juju action do slave/0 downgrade  # for each slave

    juju action do resourcemanager/0 downgrade

    juju action do namenode/1 downgrade  # standby NN
    juju action do namenode/0 downgrade  # active NN (makes other NN active)

    juju action do namenode/1 finalize


# More Information

More details about the upgrade procedure can be found in the
[Apache Hadoop documentation][upgrade].


# Help

- [Juju mailing list](https://lists.ubuntu.com/mailman/listinfo/juju)
- [Juju Big Data mailing list](https://lists.ubuntu.com/mailman/listinfo/bigdata)
- [Juju community](https://jujucharms.com/community)


[upgrade]: https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsRollingUpgrade.html
