#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions
from charmhelpers.core import hookenv


class BenchmarkRelation(helpers.RelationContext):
    """
    Add documentation and examples of using this, before submitting to CH

    i.e.,

    BenchmarkRelation(actions=['my', 'list', 'of', 'benchmark', 'actions'])

    """

    interface = 'benchmark'
    name = 'benchmark'

    required_keys = [
        'hostname',
        'port',
        'graphite_port',
        'graphite_endpoint',
        'api_port'
    ]

    def __init__(self, name=None, additional_required_keys=None, actions=None):
        # Store actions
        if actions:
            for action in actions:
                hookenv.log("Action: %s" % action)
        super(BenchmarkRelation, self).__init__(
            name, additional_required_keys
        )

    def is_ready(self):
        ready = super(BenchmarkRelation, self).is_ready()
        if ready:
            f = open('/etc/benchmark.conf', 'w')
            data = self['benchmark'][0]
            for key in data:
                f.write("%s=%s\n" % (key, data[key]))
            f.close()
        return ready


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
                BenchmarkRelation(actions=['list', 'of', 'actions']),
            ],
            'data_ready': [
                helpers.render_template(
                    source='siegerc',
                    target='%s/.siegerc' % hookenv.charm_dir()),
                actions.log_start,
            ],
            'data_lost': [
            ],
        },
    ])
    manager.manage()
