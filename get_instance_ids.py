#!/usr/bin/env python

__author__ = "Matthew Bach"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "mbach@redhat.com"
__status__ = "Production"

"""
The purpose of this script is to extract all aws
ec2 instance id's from an aws inventory output.
The input file for this script is generated using
ec2.py like so:
# python ec2.py > inventory.json
The result is a json formatted file with one key,
labeled instances that contains a list of all aws
instance id's. This file can be processed by ansible
for tasks performed on all instances selected by
ec2.py's filters.
"""

import json
import sys

jsonf = sys.argv[1]
outf = 'instance_inventory.json'

with open(jsonf, 'r') as f:
    raw_data = f.read()

jdata = json.loads(raw_data)

def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.iteritems():
            if k == lookup_key:
                yield v
            else:
                for child_val in item_generator(v, lookup_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_key):
                yield item_val

instances = []

for i in item_generator(jdata, 'ec2_id'):
    instances.append(str(i))

for i in instances:
    print i

print '-'*20
print 'Instance Count: {}'.format(len(instances))


with open('instance_inventory.json', 'w') as f:
    f.write('instances: ')
    f.write(json.dumps(instances))

print 'created: instance_inventory.json'
