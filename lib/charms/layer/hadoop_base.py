from jujubigdata import utils
from jujubigdata.handlers import HadoopBase
from charms import layer
from charms.reactive import is_state
from charmhelpers.core import hookenv


def get_dist_config(required_keys=None):
    required_keys = required_keys or [
        'vendor', 'hadoop_version', 'packages',
        'groups', 'users', 'dirs', 'ports']
    dist = utils.DistConfig(filename='dist.yaml',
                            required_keys=required_keys)
    opts = layer.options('hadoop-base')
    for key in ('packages', 'groups'):
        if key in opts:
            dist.dist_config[key] = list(
                set(dist.dist_config[key]) | set(opts[key])
            )
    for key in ('users', 'dirs', 'ports'):
        if key in opts:
            dist.dist_config[key].update(opts[key])
    if is_state('hadoop.installed'):
        hadoop_version = utils.run_as('hdfs', 'hadoop', 'version',
                                      capture_output=True)
        dist.hadoop_version = hadoop_version.splitlines()[0].split()[1]
    else:
        dist.hadoop_version = hookenv.config('hadoop_version')
    return dist


def get_hadoop_base():
    return HadoopBase(get_dist_config())


def reconfigure_hdfs():
    cfg = hookenv.config()
    hdfs_site = get_dist_config().path('hadoop_conf') / 'hdfs-site.xml'
    with utils.xmlpropmap_edit_in_place(hdfs_site) as props:
        props['dfs.replication'] = cfg['dfs_replication']
        props['dfs.blocksize'] = int(cfg['dfs_blocksize'])
