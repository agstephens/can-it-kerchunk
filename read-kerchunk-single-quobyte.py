import os
import json

import set_configs

# read the access key and secret key from a json file in the directory
with open(os.path.expanduser("./config.json.quobyte")) as fh:
    config = json.load(fh)

# construct the input options for fsspec
fssopts = {
           "key": config["accessKey"],
           "secret": config["secretKey"],
           "client_kwargs": {"endpoint_url": config["url"]}
}


set_configs.setup_configs(config["accessKey"], config["secretKey"], config["url"])

for key in ("AWS_ACCESS_KEY_ID", "FSSPEC_CONFIG_DIR"): print(f"{key} -> {os.environ[key]}")
print("HAVE TO SET CONFIG BEFORE IMPORTING xarray??????")

import xarray as xr
import fsspec


ref = "http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc.json"
ref = "s3://s3-acclim/kerchunk-jsons/CMIP6.CMIP.MOHC.HadGEM3-GC31-MM.1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115-V2.json"
ref = "s3://s3-acclim/kerchunk-jsons/CMIP6.CMIP.MOHC.HadGEM3-GC31-MM.1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115-V2-fixed-fill_value.json"

import s3fs
s3fs  = s3fs.S3FileSystem(**fssopts)
ref = s3fs.open(ref)


for key in ("AWS_ACCESS_KEY_ID", "FSSPEC_CONFIG_DIR"): print(f"{key} -> {os.environ[key]}")

mapper = fsspec.get_mapper('reference://', fo=ref, target_protocol="http", 
                           **fssopts)
for key in ("AWS_ACCESS_KEY_ID", "FSSPEC_CONFIG_DIR"): print(f"{key} -> {os.environ[key]}")

ds = xr.open_zarr(mapper) #, **fssopts) #, backend_kwargs={'consolidated': False})

for key in ("AWS_ACCESS_KEY_ID", "FSSPEC_CONFIG_DIR"): print(f"{key} -> {os.environ[key]}")


subset = ds.sel(time=slice("1855-01-01", "1856-01-01"), lat=slice(20, 40), lon=slice(20, 40))
print("subset shape", subset.hus.shape)

print(f"MAX: {float(subset.hus.max())}")

