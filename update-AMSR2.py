#!/usr/bin/python
# coding:utf-8

import datetime
import difflib
import os
import pexpect
from pprint import pprint
import convert

BASEDIR='/var/local/AMSR2'
DATADIR = BASEDIR + '/data'
TMPDIR = BASEDIR + '/tmp'
USER='USERNAME'
PASSWD='PASSWORD'
SFTPCMD = 'sftp -q -oPort=2051 %s@gcom-w1.jaxa.jp'%(USER)


def update_L3(sens):
	def dump_filename(directory, dumpfilename):
		c = pexpect.spawn(SFTPCMD)
		c.expect("password:")
		c.sendline(PASSWD)
		c.expect("sftp>")
		c.sendline("ls -t " + directory)
		c.expect("sftp>")
		files = c.before
		c.sendline("bye")
		c.expect(pexpect.EOF)
		c.close()
		f = open(dumpfilename, 'w')
		for line in files.split('\r\n'):
			if(line.find('gz') != -1):
				f.write(line.rstrip() + '\n')
		f.close()

	def newfile(oldfile, newfile):
		new = []
		with open(newfile) as f:
			for line in f:
				new.append(line)
		old = []
		with open(oldfile) as f:
			for line in f:
				old.append(line)
		d = list(difflib.Differ().compare(old, new))
		result = []
		for i in d:
			if(i[0] == '+'): 
				result.append(i[2:].rstrip('\n'))
		return tuple(result)

	def download(file_list, directory):
		c = pexpect.spawn(SFTPCMD)
		c.expect("password:")
		c.sendline(PASSWD)
		c.expect('sftp>')
		c.sendline('lcd ' + directory)
		c.expect('sftp>')
		for i in file_list:
			c.sendline('get ' + i)
			c.expect('sftp>')
		c.sendline('bye')
		c.expect(pexpect.EOF)
		c.close()

	for i in sens:
		sensor = i[0]
		rmtdir = i[1]
		dumpfile = '%s/%s.tmp'%(BASEDIR, sensor)
		filelst = '%s/%s.lst'%(BASEDIR, sensor)
		
		dump_filename(rmtdir, dumpfile)
		files = newfile(filelst, dumpfile)
		download(files, TMPDIR)
		os.rename(dumpfile, filelst)
		if len(files) < 1:
			continue
		if (files[0].find('ls') != -1):
			files = files[1:]
		for f in files:
			convert.convert(convert.expand(TMPDIR + '/' + os.path.basename(f)))
			basename = os.path.basename(f).split('_')
			npy = '%s/%s/%s/%s_%s.npy'%(DATADIR,basename[1][0:4],basename[1][4:6],basename[4][0:7],basename[1])

def main():
	today = datetime.date.today()
	y = today.year
	m= today.month
	sens = (('SND_10','AMSR2/%d/%d.%02d/L3/SND_10/1/*EQMA*.gz'%(y,y,m)),
('SSW_10','AMSR2/%d/%d.%02d/L3/SSW_10/1/*EQOA*.gz'%(y,y,m)),
('SST_10','AMSR2/%d/%d.%02d/L3/SST_10/1/*EQOA*.gz'%(y,y,m)))
	update_L3(sens)



if __name__ == "__main__":
	main()

