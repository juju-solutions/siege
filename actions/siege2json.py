#!/usr/bin/env python
"""
Simple script to parse siege's transaction results
and reformat them as JSON for sending back to juju
"""
import sys
import subprocess
import re


def action_set(key, val):
    action_cmd = ['action-set']
    if isinstance(val, dict):
        for k, v in val.iteritems():
            action_set('%s.%s' % (key, k), v)
        return

    action_cmd.append('%s=%s' % (key, val))
    subprocess.check_call(action_cmd)


def parse_siege_output():
    """
    Parse the output from siege and set the action results
    """

    # Throw away the header
    sys.stdin.readline()

    p = re.compile(r'\s+')
    data = re.sub(p, '', sys.stdin.readline()).split(',')

    results = {}
    results['timestamp'] = {'value': data[0], 'units': ''}
    results['transactions'] = {'value': data[1], 'units': 'hits'}
    results['elapsed'] = {'value': data[2], 'units': 'secs'}
    results['transfered'] = {'value': data[3], 'units': 'bytes'}
    results['response-time'] = {'value': data[4], 'units': 'secs'}
    results['transfer-rate'] = {'value': data[5], 'units': 'trans/sec'}
    results['throughput'] = {'value': data[6], 'units': 'bytes/sec'}
    results['concurrent'] = {'value': data[7], 'units': ''}
    results['okay'] = {'value': data[8], 'units': ''}
    results['failed'] = {'value': data[9], 'units': ''}

    for key in results:
        action_set("results.%s" % key, results[key])

    try:
        from charmhelpers.contrib.benchmark import Benchmark
        Benchmark.set_composite_score(
            results['transfer-rate'],
            'trans/second',
            'desc'
        )
    except:
        # Set the composite key
        action_set(
            "meta.composite",
            {
                'value': results['transfer-rate'],
                'units': 'trans/second',
                'direction': 'desc'
            }
        )


if __name__ == "__main__":
    parse_siege_output()
