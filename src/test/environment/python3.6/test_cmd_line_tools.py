import os

import subprocess as sp
import shlex
SAMPLE_DATA_DIR = None


def _fpath(fname):
    return os.path.join(SAMPLE_DATA_DIR, fname)

def _run(cmd):
    bytes = sp.check_output(cmd, shell=True, executable='/bin/bash', stderr=sp.STDOUT)
    return bytes.decode('utf-8').replace('\n', '')

def setup():
    import iris_sample_data as isd
    _sample_data_dir = os.path.join(os.path.dirname(isd.__file__), 'sample_data')
    global SAMPLE_DATA_DIR
    SAMPLE_DATA_DIR = _sample_data_dir 


def test_cdo_infov():
    resp = _run('cdo infov {} | grep air_temperature'.format(_fpath('A1B_north_america.nc')))
    match = 'Processed 435120 values from 1 variable over 240 timesteps'
    assert(match in resp)


def test_nco_ncks_subset(tmpdir):
    fin = _fpath('A1B_north_america.nc')
    fout = tmpdir.mkdir("test-outputs").join('fout.nc')
    _run('ncks -d latitude,,,20 -d longitude,,,20 -d time,,,6 {} {}'.format(
                   fin, fout))
    # Check ncdump output
    resp = _run('ncdump -h {}'.format(fout)) 
    assert('latitude = 2 ;' in resp)
    assert('longitude = 3 ;' in resp)
