#!/usr/bin/env python

import json
import sys
import argparse


config = '../etc/minicondas.json'


    
def _get(py_version, miniconda_version, attribute):

    with open(config) as reader:
        data = json.load(reader)

    if miniconda_version == 'latest':
        _all_versions = [i.split('-')[1] for i in data['minicondas'][py_version].keys()]
        m_start = 'm' + py_version.replace('py', '')[0]

        _av_ints = sorted([[int(i) for i in item.split('.')] for item in _all_versions])
        _av_ints.reverse()
        _all_verisons = ['.'.join([str(item) for item in items]) for items in _av_ints] 

        miniconda_version = m_start + '-' + _all_versions[-1] 

    try:
        attr = data['minicondas'][py_version][miniconda_version][attribute]
    except:
        print('Could not find {} attribute for python version: "{}"'.format(attribute, py_version))

    return attr


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("py_version", type=str, help="Python version")
    parser.add_argument("attribute", type=str, choices=['url', 'md5', 'short_id'],
                        help="Attribute")

    parser.add_argument('-m', '--miniconda-version', default='latest',
                        help='Add Miniconda version (or use "latest").',
                        type=str)
    args = parser.parse_args()
    print(_get(args.py_version, args.miniconda_version, args.attribute))
