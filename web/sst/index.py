#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os.path
import string
import xml.etree.ElementTree


BASEDIR='/var/www/tms/amsr2/sst'
XML='/var/www/tms/amsr2/sst/tilemapresource.xml'

def read_tile_date():
	if(os.path.exists(XML) == False):
		return ''
	elem = xml.etree.ElementTree.parse(XML).getroot()
	return datetime.datetime.strptime(elem.find('.//Title').text[12:20], '%Y%m%d').strftime('%Y-%m-%d')
	

def index():
	now = datetime.datetime.now()
	html = []
	with open('%s/index.html'%BASEDIR,'r') as f:
		for line in f:
			html.append(line)

	tmpl = string.Template(''.join(html))
	return tmpl.safe_substitute(DATE=read_tile_date()+' (UTC)')


read_tile_date()
