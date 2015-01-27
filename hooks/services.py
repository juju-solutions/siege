#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions
from charmhelpers.core import hookenv


class HttpRelation(helpers.HttpRelation):
    """
    Override HttpRelation to fix the required keys, and return the port
    provided by the relation, rather than the hard-coded port 80
    """
    required_keys = ['hostname', 'port']

    def provide_data(self):
        return {
            'host': hookenv.unit_get('hostname'),
            'port': hookenv.unit_get('port'),
        }


def manage():
    manager = ServiceManager([
        {
            'service': 'benchmark-siege',
            'ports': [],  # ports to after start
            'provided_data': [
                # context managers for provided relations
                # e.g.: helpers.HttpRelation()
            ],
            'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
                # helpers.RequiredConfig('hostname', 'port'),
                HttpRelation(),
            ],
            'data_ready': [
                # actions.write_config,
                helpers.render_template(
                    source='siegerc',
                    target='%s/.siegerc' % hookenv.charm_dir()),
                actions.log_start,
            ],
            'data_lost': [
                actions.debug_my_hook
            ],
        },
    ])
    manager.manage()
