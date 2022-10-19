"""Build a Kerchunk zip file without touching the disk"""

import os
import json
import kerchunk.hdf
import fsspec
from urllib.parse import urlparse

urls = ["http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/" + f for f in [
    "1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc"]]

# read the access key and secret key from a json file in the directory
with open(os.path.expanduser("./config.json")) as fh:
    config = json.load(fh)

# construct the input options for fsspec
fssopts = {
           "key": config["accessKey"], 
           "secret": config["secretKey"],
           "client_kwargs": {"endpoint_url": config["url"]}
          }

for u in urls:    
    # munge the url name to get the output object path and add .json
    url_parts = urlparse(u)
    url_parts = url_parts._replace(path=url_parts.path+".json")
    bucket_name = url_parts.path.split("/")[1]
    object_name = url_parts.path.split("/")[2]

    # construct the output url and connect to output fsspec
    url_out = f"s3://{bucket_name}/{object_name}"

    with fsspec.open(u) as infss:
        print(f"Working on: {u}")
        # generate kerchunk and write to buffer
        h5chunks = kerchunk.hdf.SingleHdf5ToZarr(infss, u, inline_threshold=100)
        with fsspec.open(url_out, "wb", **fssopts) as out_fss:
            out_fss.write(json.dumps(h5chunks.translate()).encode())
    print(f"Written file: {bucket_name}/{object_name}")
