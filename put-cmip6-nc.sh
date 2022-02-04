#!/bin/bash

dsid=CMIP6.CMIP.MOHC.HadGEM3-GC31-MM.1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115
bucket_id=A-NC-$(echo $dsid | cut -d. -f1-4)
dr=/badc/cmip6/data/$(echo $dsid | sed 's/\./\//g')
files=$dr/*.nc

STORE_URL=http://cmip6-zarr-o.s3.jc.rl.ac.uk/
CREDS_FILE=${HOME}/.credentials/caringo-credentials.json.cmip6-zarr
COMMON_ARGS="-s $STORE_URL -c $CREDS_FILE"

echo "[INFO] Creating bucket: $bucket_id"
jos create-bucket $COMMON_ARGS $bucket_id

sleep 3
echo "[INFO] Listing..."
jos list-buckets $COMMON_ARGS  

for f in $files; do
    file_id="$(echo $f | cut -d/ -f9-14 | sed 's/\//\./g').$(echo $f | cut -d_ -f7)"
    echo "[INFO] Working on: $file_id"
    jos put $COMMON_ARGS -b $bucket_id -n $file_id $f
done

