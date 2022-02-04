import xarray as xr
import fsspec
import os

ref = "http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc.json"

mapper = fsspec.get_mapper('reference://', fo=ref, target_protocol='http')

ds = xr.open_zarr(mapper)

subset = ds.sel(time=slice("1855-01-01", "1856-01-01"), lat=slice(20, 40), lon=slice(20, 40))
print("subset shape", subset.hus.shape)

