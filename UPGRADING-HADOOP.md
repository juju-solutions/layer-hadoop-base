# Hadoop Upgrade

## Actions and Instructions

The hadoop-base layer contains an action called hadoop-upgrade which allows the
administrator to upgrade, downgrade and finalize a hadoop deployment. Currently
rollback is not supported, and HDFS filesystem version upgrade is not supported (but
will be implemented when a new filesystem version is released greater than the version
which comes with 2.7.2)

The actions and the commands they run are in line with the instructions and
recommendations in this document:

http://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-hdfs/HdfsRollingUpgrade.html

Therefore, when upgrading a namenode, datanode or resourcemanager, the following
daemons will be stopped/started:

  - namenode
  - datanode
  - nodemanager
  - resourcemanager
  - jobhistoryserver

While ALL hadoop binaries are upgraded by this process, neither journalnode nor
zkfc (zookeeper) daemons are restarted by the upgrade process, as doing so can
cause an HDFS outage. Further instructions for restarting these daemons after an
upgrade are provided in the action definitions in: the datanode layer (for
journalnode) and the namenode layer for zkfc.

You can run the 'list-versions' action to see which versions are available to upgrade to.


### Upgrade (HA)

The apache documentation suggests the following process for performing a rolling
upgrade - that is, an HDFS upgrade without downtime:

 1. Prepare rolling upgrade
 2. Upgrade namenodes
 3. Upgrade (a subset of) datanodes
 4. Finalize (or downgrade)

There is an additional 'safety' step with our hadoop implementations: you must
config set the version that you would like to upgrade (or downgrade) to for each
service you are going to upgrade.

Here are the general steps:

1. Set `hadoop_version` config value for each service:

    version=2.7.2
    juju set namenode hadoop_version=$version
    juju set resourcemanager hadoop_version=$version
    juju set slave hadoop_version=$version

2. Prepare the rolling upgrade:

    juju action do namenode/0 hadoop-upgrade version=$version prepare=true

At this point HDFS will create a fsimage for rollback. You should wait for this
process to finish before proceeding to the next step. The hadoop-upgrade prepare
action above will report "Upgrade image prepared - proceed with rolling upgrade"
as soon as the rollback image is created.

    juju action fetch <jobId>

3. Upgrade namenodes:

In an HA configuration, zookeeper will handle active/standby states - you
should make the first namenode is 'up' before upgrading the second.

    juju action do namenode/0 hadoop-upgrade version=$version
    juju action do namenode/1 hadoop-upgrade version=$version


4. Upgrade datanodes:

    juju action do slave/0 hadoop-upgrade version=$version
    juju action do slave/1 hadoop-upgrade version=$version
    juju action do slave/2 hadoop-upgrade version=$version


5. Upgrade other components:

The `hadoop-upgrade` action will work with any charm which incorporates it but
you may need to manually restart daemons &mdash; resourcemanager daemons will
be restarted by the `hadoop-upgrade` action.


If data persistence is important to you, you should upgrade a subset of your
slaves/datanodes, perform some tests (e.g. check existing data) and then
continue with the upgrade or rollback.

Once you have have finished upgrading your units (successfully or not) you will
need to do one of the following:

1. finalize - cleans up the HDFS filesystem, and marks the rolling upgrade as
complete
2. downgrade - restores a previous version of hadoop (after which you ***must
still finalize***)


### Upgrade (non-HA)

Upgrading a non-HA deployment requires a more specific sequence of actions to be
executed as the whole cluster will be down - upgrading the namenode after the
datanotes is suggested, or you can follow the instructions for HA as described
above and use the `standalone=true` parameter:

 1. Config set version
 2. Prepare rolling upgrade
 3. Upgrade datanodes and then namenode using the `standalone=true` parameter


### Finalize

This is a fairly straight forward action and can be run on only one of the
namenodes - this restarts the namenode daemons in 'normal' mode, but we
recommend running it on both your namenodes to force those daemons to restart:

    juju action do namenode/0 hadoop-upgrade version=$version postupgrade=finalize

This will commit the upgrade and free up space which is reserved during the
upgrade.


### Downgrade

Slightly more actions are required to downgrade HDFS than to finalize, and the
recommended process is:

1. Set `hadoop_version` config value for each service:

    version=2.7.1
    juju set namenode hadoop_version=$version
    juju set slave hadoop_version=$version

2. Downgrade datanodes:

    juju action do slave/0 hadoop-upgrade version=$version postupgrade=downgrade
    juju action do slave/1 hadoop-upgrade version=$version postupgrade=downgrade
    juju action do slave/2 hadoop-upgrade version=$version postupgrade=downgrade

3. Downgrade both namenodes:

    juju action do namenode/0 hadoop-upgrade version=$version postupgrade=downgrade
    juju action do namenode/1 hadoop-upgrade version=$version postupgrade=downgrade

***Once the downgrade is complete, you must still finalize the rolling upgrade***


### Action parameters

    version:
      type: string
      description: destination hadoop version X.X.X, e.g. 2.7.2
    prepare:
      type: boolean
      description: Must be run first - prepares fsimage backup
      default: false
    query:
      type: boolean
      description: Check if the fsimage backup is ready
      default: false
    postupgrade:
      type: string
      description: Should be specified after an upgrade
      enum: [finalize, downgrade, rollback, rollback_finalize]
    standalone:
      type: boolean
      description: If False, upgrade an HA cluster without downtime. Otherwise perform standalone upgrade.
      default: false
    forceupgrade:
      type: boolean
      description: Does not check if the upgrade has been prepared - just download resource and switch symlink
      default: false


## Contact Information

[bigdata-dev@canonical.com](mailto:bigdata-dev@canonical.com)

## Help

- [Juju mailing list](https://lists.ubuntu.com/mailman/listinfo/juju)
- [Juju community](https://jujucharms.com/community)
