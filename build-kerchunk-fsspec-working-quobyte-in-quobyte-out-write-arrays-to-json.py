"""Build a Kerchunk zip file without touching the disk"""

import os
import json
import kerchunk.hdf
import fsspec
from urllib.parse import urlparse

DEFAULT_BUCKET_NAME = "s3-acclim"
#kerchunk-test/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/1pctCO2/r1i1p1f3/Amon/hus/gn/v20200115/
#urls = ["http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/" + f for f in ["1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc"]]

gws = "/gws/nopw/j04/acclim"
bucket_name = "s3-acclim"
s3_gws_url = f"s3://{bucket_name}"

urls = [s3_gws_url + "/kerchunk-test/CMIP6/CMIP/MOHC/HadGEM3-GC31-MM/1pctCO2/r1i1p1f3/Amon/hus/gn/v20200115/hus_Amon_HadGEM3-GC31-MM_1pctCO2_r1i1p1f3_gn_185001-186912.nc"]

# read the access key and secret key from a json file in the directory
with open(os.path.expanduser("./config.json.quobyte")) as fh:
    config = json.load(fh)

# construct the input options for fsspec
fssopts = {
           "key": config["accessKey"], 
           "secret": config["secretKey"],
           "client_kwargs": {"endpoint_url": config["url"]}
          }


def get_output_url(url):
    url_parts = urlparse(url)
    object_name = "kerchunk-jsons/" + ".".join(url_parts.path.split("/")[2:-1]) + "-V2.json"
    return f"s3://{bucket_name}/{object_name}" 


def check_read_permissions(url, gws=gws):
    fpath = os.path.join(gws, url.replace("s3://s3-acclim/", ""))
    if not int(oct(os.stat(fpath).st_mode)[-1]) > 3:
        raise IOError(f"Must fix global read-access on file system for file: {fpath}")

MAX_BYTES = 10000

for url in urls:    
    check_read_permissions(url)
    url_out = get_output_url(url)
    print(f"Reading: {url}")

    with fsspec.open(url, "rb", **fssopts) as infss:
# For publicly readable endpoints, use:     with fsspec.open(u) as infss:

        # generate kerchunk and write to buffer
        h5chunks = kerchunk.hdf.SingleHdf5ToZarr(infss, url, inline_threshold=MAX_BYTES)

        import pdb; pdb.set_trace()
        with fsspec.open(url_out, "wb", **fssopts) as out_fss:
            out_fss.write(json.dumps(h5chunks.translate()).encode())

    print(f"Written file: {url_out}") 

