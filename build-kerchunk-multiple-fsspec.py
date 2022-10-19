import os
import json
import kerchunk.hdf
import kerchunk.combine
import fsspec
from urllib.parse import urlparse

suffixes = """185001-186912.nc 187001-188912.nc 189001-190912.nc 191001-192912.nc 
193001-194912.nc 195001-196912.nc 197001-198912.nc 199001-199912.nc""".split()
url_base = "http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115."
out_combined_url = "s3://A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.json"

urls = [url_base + suffix for suffix in suffixes]

# read the access key and secret key from a json file in the directory
with open(os.path.expanduser("./config.json")) as fh:
    config = json.load(fh)

# construct the input options for fsspec
fssopts = {
           "key": config["accessKey"], 
           "secret": config["secretKey"],
           "client_kwargs": {"endpoint_url": config["url"]}
          }

# build / don't build the 
DO_SCAN = False # True

json_urls = []

for u in urls:
    # munge the url name to get the output object path and add .json
    url_parts = urlparse(u)
    url_parts = url_parts._replace(path=url_parts.path+".json")
    bucket_name = url_parts.path.split("/")[1]
    object_name = url_parts.path.split("/")[2]

    # construct the output url and connect to output fsspec
    url_out = f"s3://{bucket_name}/{object_name}"
    http_out = f"http://{url_parts.hostname}/{bucket_name}/{object_name}"

    if DO_SCAN:
        with fsspec.open(u) as infss:
            print(f"Working on: {u}")
            h5chunks = kerchunk.hdf.SingleHdf5ToZarr(infss, u, inline_threshold=100)
            with fsspec.open(url_out, "wb", **fssopts) as out_fss:
                out_fss.write(json.dumps(h5chunks.translate()).encode())
        print(f"Written file: {bucket_name}/{object_name}")
    json_urls.append(http_out)

mzz = kerchunk.combine.MultiZarrToZarr(
    json_urls,
    remote_protocol="s3",
    remote_options=fssopts,
    #preprocess="drop_coords",
    concat_dims={"time"},
    identical_dims={"lat", "lon"}
)

# write out remotely
mzz.translate(out_combined_url, storage_options=fssopts)
