from jujubigdata.utils import DistConfig
from jujubigdata.handlers import HadoopBase
from charms.layer import LayerOptions


def get_dist_config(required_keys):
    dist = DistConfig(filename='dist.yaml',
                      required_keys=required_keys)
    opts = LayerOptions('hadoop-base')
    for key in ('vendor', 'hadoop_version'):
        if key in opts:
            dist.dist_config[key] = opts[key]
    for key in ('packages', 'groups'):
        if key in opts:
            dist.dist_config[key] = list(set(dist.dist_config[key]) | set(opts[key]))
    for key in ('users', 'dirs', 'ports'):
        if key in opts:
            dist.dist_config[key].update(opts[key])
    return dist


def get_hadoop_base():
    dist_keys = ['vendor', 'hadoop_version', 'packages',
                 'groups', 'users', 'dirs', 'ports']
    return HadoopBase(get_dist_config(dist_keys))
