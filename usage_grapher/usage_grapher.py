#!/usr/bin/env python
"""A library for graphing memory usage w/vm_stat"""
import sys
import time
import subprocess
import re
import csv


DATAFILE = '/tmp/usage_grapher.csv'


def run_vm_stat():
    return subprocess.check_output('vm_stat')


def parse_vm_stat_output(output):
    pattern = re.compile(r'^(.*?):\s*(.*?)\.*$')
    data = {}
    for line in output.split('\n'):
        m = pattern.match(line.strip())
        if m:
            data[m.group(1)] = m.group(2)
    return data


def persist_vm_stat_data(data):
    with open(DATAFILE, 'ab') as out:
        writer = csv.DictWriter(out, fieldnames=sorted(data.keys()))
        writer.writerow(data)


def load_vm_stat_data():
    tmp = parse_vm_stat_output(run_vm_stat())  # load the keys
    data = []
    with open(DATAFILE, 'rb') as inf:
        reader = csv.DictReader(inf, fieldnames=sorted(tmp.keys()))
        data = [row for row in reader]
    return data


def create_graph(data, keys=[]):
    if len(data) > 0:
        import pygal
        keys = keys if len(keys) > 0 else data[0].keys()
        lc = pygal.Line()
        lc.title = 'Memory Usage'
        for key in keys:
            lc.add(key, [int(item[key]) for item in data
                         if key != "Mach Virtual Memory Statistics"])
        lc.render_to_file('usage_graph.svg')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE:'
        print '\t%s collect [interval]' % sys.argv[0]
        print '\t%s render [keys]' % sys.argv[0]
        sys.exit(-1)

    if sys.argv[1].strip().lower() == "collect":
        try:
            while True:
                persist_vm_stat_data(parse_vm_stat_output(run_vm_stat()))
                time.sleep(1 if len(sys.argv) == 1 else int(sys.argv[1]))
        except KeyboardInterrupt:
            pass
    elif sys.argv[1].strip().lower() == "render":
        create_graph(load_vm_stat_data(), sys.argv[2:])
