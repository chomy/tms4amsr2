#!/usr/bin/python

import numpy as np
import os
import os.path
import sys
import zipfile

JSONBASEDIR='/var/www/api/json'

def main():
	generate(sys.argv[1])

def generate(filename):
	factor = 0
#	filename = sys.argv[1]
	product = ''
	date = filename[8:16]
	outdir = ''

	if(filename.find('SND') != -1):
		factor = 0.1
		product = 'snd'
		outdir = JSONBASEDIR + '/snd'
	if(filename.find('SST') != -1):
		factor = 0.01
		product = 'sst'
		outdir = JSONBASEDIR + '/sst'
	if(filename.find('SSW') != -1):
		factor = 0.01
		product = 'ssw'
		outdir = JSONBASEDIR + '/ssw'

	outfilename = outdir + '/' + os.path.basename(filename).split('.')[0] + '.json'
	#d = np.load(sys.argv[1])
	d = np.load(filename)
	with open(outfilename, 'w') as f:
		f.write('\"date\":%s,\"product\":\"%s\",\"values\":['%(date, product))
		for y in range(0, 1800):
			for x in range(0, 3600):
				if(x == 0 and y == 0):
					sep = ''
				else:
					sep = ','

				f.write('%s{\"lng\":%.02f,\"lat\":%.02f,\"value\":%.02f}\n'%(sep, x*0.1, y*0.1, -9999.0 if d[y][x]<-30000 else d[y][x]*factor))

		f.write(']}\n')
	zipfilename = outdir + '/' + os.path.basename(outfilename).split('.')[0] + '.zip'
	with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as z:
		z.write(outfilename)
	os.remove(outfilename)

if __name__ == '__main__':
	main()
