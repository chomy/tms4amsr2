#!/bin/bash

BASEDIR='/var/local/AMSR2'
TILEBASE=/var/www/tms/amsr2
DATADIR=/var/local/AMSR2/data
TMPDIR=/var/local/AMSR2/tmp

export GDAL_CACHEMAX=1024

. $BASEDIR/bin/gentile_utils.sh


for i in `find /var/local/AMSR2/data -mtime -1|grep npy`
do
	if [ `echo $i | grep SST` ] ;then
		generate $i $TILEBASE/sst
	fi
	if [ `echo $i | grep SSW` ] ;then
		generate $i $TILEBASE/ssw
	fi
	if [ `echo $i | grep SND` ] ;then
		generate $i $TILEBASE/snd
	fi
	/var/local/AMSR2/bin/genJSON.py $i
done



