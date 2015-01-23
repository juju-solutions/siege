from charmhelpers.core import hookenv
from charmhelpers.core.services import helpers


def debug_my_hook(service_name):
    hookenv.log('not enough data?!')


def write_config(service_name):
    """
    Write $HOME/.siegerc
    """
    host = helpers.HttpRelation()[0]['hostname']
    port = helpers.HttpRelation()[0]['port']
    hookenv.log('write_config(%s): %s:%d' % (service_name, host, port))


def log_start(service_name):
    hookenv.log('benchmark-siege starting')
