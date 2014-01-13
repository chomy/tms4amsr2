#!/usr/bin/python

import numpy as np
import colormap
import datetime
import subprocess
import h5py
import os.path
import sys

BASEDIR='/var/local/AMSR2'
DATADIR='/var/local/AMSR2/data'
TMPDIR=BASEDIR+'/tmp'


def npy2map(filename, offset, factor, mapfunc):
	d = np.load(filename)
	d = np.add(d, offset)
	d = np.multiply(d, factor)
	outfilename = TMPDIR + '/' + os.path.basename(filename).split('.')[0] + '.ppm'
	with open(outfilename,'w') as f:
		f.write('P3\n3600 1800\n255\n')
		for y in range(0,1800):
#			for x in range(-1799,1801):
			for x in range(0,3600):
				f.write('%d %d %d\n'%mapfunc(d[y][x]))
	return outfilename



def npy2map_ave(filename,offset, factor, mapfunc):
	def load_data():
		gen_filename = lambda prefix, date: '%s/%d/%02d/%s_%s.npy'%(DATADIR, 
			date.year, date.month, prefix, date.strftime('%Y%m%d'))
		bname = os.path.basename(filename)
		date = datetime.datetime.strptime(bname[8:16], '%Y%m%d')
		prefix = bname[0:7]
		delta = datetime.timedelta(1)
        
		return (np.load(gen_filename(prefix, date)),
				np.load(gen_filename(prefix, date - delta)),
				np.load(gen_filename(prefix, date - 2 * delta)))

	outfilename = TMPDIR + '/' + os.path.basename(filename).split('.')[0] + '.ppm'
	data = load_data()
	with open(outfilename, 'w') as f:
		f.write('P3\n3600 1800\n255\n')
		for y in range(0,1800):
#			for x in range(-1799,1801):
			for x in range(0,3600):
				s = 0.0
				count = 0
				for i in range(0,3):
					if(data[i][y][x] < -30000):
						continue
					s += data[i][y][x]
					count += 1
				if(count == 0):
					f.write('0 0 0\n')
				else:
					f.write('%d %d %d\n'%mapfunc(s*factor/count))
	return outfilename


def h5_to_map(filename, offset, factor, mapfunc):
	#mapfunc = lambda a:(0,0,0) if a< -30000 else colormap.cool[999] if a>500 else colormap.cool[a]
	h5 = h5py.File(filename, 'r')
	d = h5['Geophysical Data'][:,:,0]
	d = np.add(d, offset)
	d = np.multiply(d, factor)
	data = []
	with open('map.ppm', 'w') as f:
		f.write('P3\n3600 1800\n255\n')
		for y in range(0,1800):
			for x in range(-1799,1801):
				f.write('%d %d %d\n'%mapfunc(d[y][x]))
	h5.close()

def make_mapfunc(colormap, factor):
	def impl(val):
		if(val/factor < -30000):
			return (0,0,0)
		i = int(round(val))
		if(i<0):
			return colormap[0]
		if(i>=1000):
			return colormap[999]
		return colormap[i]

	return lambda val: impl(val)



def main():
	filename = sys.argv[1]
	if(filename.find('SND') != -1):
		npy2map(filename, 0, 5, make_mapfunc(colormap.jet, 5))
	if(filename.find('SST') != -1):
		npy2map_ave(filename, 200, 1000.0/3700.0, make_mapfunc(colormap.jet, 1000.0/3700.0))
	if(filename.find('SSW') != -1):
		npy2map(filename, 0, 1.0/3.0, make_mapfunc(colormap.jet, 1.0/3.0))
		


if __name__ == '__main__':
	main()


