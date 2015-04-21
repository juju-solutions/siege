from charmhelpers.core import hookenv
from charmhelpers.core.services import helpers
import os.path


def log_start(service_name):
    hookenv.log('benchmark-siege starting')
