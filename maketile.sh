#!/bin/bash

BASEDIR='/var/local/AMSR2'
TILEBASE=/var/www/tms/amsr2
TMPDIR=/var/local/AMSR2/tmp

. $BASEDIR/bin/gentile_utils.sh


generate $1 $2

