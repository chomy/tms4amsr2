

function generate(){
        NPY=$1
        BASENAME=$(basename $NPY .npy)
        PPM=$TMPDIR/$BASENAME.ppm
        TILEDIR=$2
        TMPTIFF=$TMPDIR/tmp_$BASENAME.tiff
        TIFF=$TMPDIR/$BASENAME.tiff
        MAPTIFF=$TMPDIR/map_$BASENAME.tiff

        $BASEDIR/bin/mapgen.py $NPY
        gm convert -transparent black $PPM $TIFF
        gdal_translate -q -gcp 0 0 0 90 \
                -gcp 3600 0 360 90 \
                -gcp 0 1800 0 -90 \
                -gcp 3600 1800 360 -90 $TIFF $TMPTIFF

        gdalwarp -q -s_srs EPSG:4326  $TMPTIFF $MAPTIFF
        gdal2tiles.py -z 0-8 $MAPTIFF $TILEDIR &
}

