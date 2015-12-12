from charms.reactive import when, when_not, set_state
from charms.hadoop import get_hadoop_base


@when_not('hadoop.installed')
def fetch_resources():
    hadoop = get_hadoop_base()
    if hadoop.verify_resources():
        set_state('resources.available')


@when('resources.available')
@when_not('hadoop.installed')
def install_hadoop():
    hadoop = get_hadoop_base()
    hadoop.install()
    set_state('hadoop.installed')
