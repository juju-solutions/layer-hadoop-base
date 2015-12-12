from charms.layer import LayerOptions
from jujubigdata.utils import DistConfig
from jujubigdata.handlers import HadoopBase


def get_hadoop_base():
    layer_opts = LayerOptions('hadoop-base')
    dist_config = DistConfig(filename='dist.yaml',
                             required_keys=layer_opts['dist_keys'])
    return HadoopBase(dist_config)
