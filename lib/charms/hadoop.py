from jujubigdata.utils import DistConfig
from jujubigdata.handlers import HadoopBase


def get_hadoop_base():
    dist_keys = ['vendor', 'hadoop_version', 'packages',
                 'groups', 'users', 'dirs', 'ports']
    dist_config = DistConfig(filename='dist.yaml',
                             required_keys=dist_keys)
    return HadoopBase(dist_config)
