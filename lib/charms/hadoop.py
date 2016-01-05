from jujubigdata.utils import DistConfig
from jujubigdata.handlers import HadoopBase


def get_dist_config(required_keys):
    return DistConfig(filename='dist.yaml',
                      required_keys=required_keys)


def get_hadoop_base():
    dist_keys = ['vendor', 'hadoop_version', 'packages',
                 'groups', 'users', 'dirs', 'ports']
    return HadoopBase(get_dist_config(dist_keys))
