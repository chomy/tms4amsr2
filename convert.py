#!/usr/bin/python
# -*- coding: UTF-8 -*-

import gzip
import h5py
import numpy as np
import os
import sys

BASEDIR='/var/local/AMSR2'
DATADIR=BASEDIR + '/data'
TMPDIR= BASEDIR + '/tmp'


def expand(filename):
	fgz = gzip.open(filename, 'r')
	outfilename = '%s/%s'%(TMPDIR, os.path.basename(filename))
	outfilename = outfilename.replace('.gz','')
	fout= open(outfilename, 'wb')
	fout.writelines(fgz)
	fgz.close()
	fout.close()
	return outfilename

def convert(filename):
	f = h5py.File(filename, 'r')
	dset = f['Geophysical Data']
	gid = f.attrs['GranuleID'][0].split('_')
	year= gid[1][0:4]
	mon = gid[1][4:6]
	out = '%s/%s/%s/%s_%s.npy'%(DATADIR,year,mon,gid[4][0:7],gid[1])
	if(len(dset.shape)==3):
		data = dset[:,:,0]
	else:
		data = dset[:,:]
	np.save(out, data)
	f.close()
	return out


def main():
	if(len(sys.argv) != 2):
		print 'convert.py HDF5'
		return 0

	convert(expand(sys.argv[1]))

if __name__ == '__main__':
	main()
