#!/usr/bin/python

import math
import numpy as np
import os.path
import re
import cgi
import cgitb
cgitb.enable()

BASEDIR='/var/local/AMSR2'
DATADIR=BASEDIR+'/data'


def get_val(d, lat, lng):
	lt = 900 - int(math.floor(lat/0.1))
	lg = int(math.floor(lng/0.1))
	
	d = np.load(filename)
	return d[lt][lg]


def get_values(filename, lat, lng, rng):
	d = np.load(filename, 'r')
	lt = int(math.floor(lat * 10))
	lg = int(math.floor(lng * 10))
	rg = int(math.floor(rng * 10))
	
	ret = []
	for idx_lat in range(lt-rg, lt+rg):
		for idx_lng in range(lg-rg, lg+rg):
			ret.append((idx_lat/10.0, idx_lng/10.0, d[idx_lat][idx_lng]/10.0))
	return tuple(ret)


def toJSON(vals, product):
	elem = lambda val: '{\"lat\":%.1f,\"lng\":%.1f,\"%s\":%.1f}'%(val[0], val[1],product, val[2])
	ret = '{\"result\":\"OK\",\"values\":[' + elem(vals[0])
	for i in vals:
		ret += ',' + elem(i)
	return ret + ']}'
	
		

def getValue(prefix, date, lat, lng, rng):
	errmsg = lambda msg:'{\"result\":\"error\", \"message\":\"%s\"}'%(msg)

	# check arguments
	if(not(lng >= -180 and lng<=180)):
		return errmsg('lng out of range (-180 - +180).')
	if(not(lat >= -90 and lat <= 90)):
		return errmsg('lat out of range (-90 - +90).')
	if(not(rng>=0.1 and rng <=180)):
		return errmsg('range out of range (0.1 - 180)')
	d = re.match('[0-9]{8}',date)
	if(d == None):
		return errmsg('imvalid date format.')
	filename = '%s/%s/%s/%s_%s.npy'%(DATADIR,date[0:4],date[4:6],prefix, date)
	if(os.path.exists(filename) == False):
		return errmsg('no data.:%s')%filename

	val = get_values(filename, lat, lng, rng)
	return toJSON(val, 'snd')
	
	

def printErrMsg():
		print 'Content-type: text/plain\n\n'
		print 'ERROR: date, lat and lng parameters are required.\n'
		print 'Usage http://amsr2.hi-rezclimate.org/snd.py?lat=latitude&lng=longitude&date=YYYYMMDD'
		print form



def main():
	form = cgi.FieldStorage()
	try:
		lat = float(form.getvalue('lat'))
		lng = float(form.getvalue('lng'))
		rng = float(form.getvalue('range'))
		date= form.getvalue('date')
 
	except:
		printErrMsg()
	else:
		print 'Content-type: text/html\n\n'
		print 'Content-type: application/json\n\n'
		#print form
		#print lat, lng, '<br>'
		print getValue('L3SGSN', date, lat, lng, rng)

if __name__ == '__main__':
	main()
