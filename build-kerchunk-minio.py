"""Build a Kerchunk zip file without touching the disk"""

import os
import json
import kerchunk.hdf
import fsspec
from io import BytesIO
from urllib.parse import urlparse
from minio import Minio

urls = ["http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/" + f for f in [
    "1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc"]]

# read the access key and secret key from minio resource file (~/.mc/config.json)
with open(os.path.expanduser("~/.mc/config.json")) as fh:
    mc_config = json.load(fh)

# cmip6-zarr alias
cmip6_mc = mc_config["aliases"]["cmip6-zarr"]
# cmip6-zarr connection url
cmip6_host = urlparse(cmip6_mc["url"]).hostname

# create the minio connection - secure=False as we are only using http
mc_client = Minio(cmip6_host, 
                  access_key=cmip6_mc["accessKey"],
                  secret_key=cmip6_mc["secretKey"],
                  secure=False)

so = {}

for u in urls:
    buffer = BytesIO()
    with fsspec.open(u, **so) as inf:
        print(f"Working on: {u}")
        # generate kerchunk and write to buffer
        h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, u, inline_threshold=100)
        buffer.write(json.dumps(h5chunks.translate()).encode())
        # generate the upload name
        url_parts = urlparse(u)
        url_parts = url_parts._replace(path=url_parts.path+".json")
        bucket_name = url_parts.path.split("/")[1]
        object_name = url_parts.path.split("/")[2]
        # reset buffer to beginning
        buffer.seek(0)
        # upload using minio
        mc_client.put_object(bucket_name, object_name, buffer, 
                             buffer.getbuffer().nbytes)
        print(f"Written file: {bucket_name}/{object_name}")
