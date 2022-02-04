import os
import json
import zipfile
import kerchunk.hdf
import kerchunk.combine
import fsspec

suffixes = """185001-186912.nc 187001-188912.nc 189001-190912.nc 191001-192912.nc 
193001-194912.nc 195001-196912.nc 197001-198912.nc 199001-199912.nc""".split()
url_base = "http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115."

urls = [url_base + suffix for suffix in suffixes]

#so = dict(anon=True, default_fill_cache=False, default_cache_type='first')
so = {}

DO_SCAN = True
DO_SCAN = False

if DO_SCAN:
  with zipfile.ZipFile("out.zip", mode="w") as zf:
    for u in urls:
        with fsspec.open(u, **so) as inf:
            print(f"Working on: {u}")
            h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, u, inline_threshold=100)
            with zf.open(os.path.basename(u) + ".json", 'w') as outf:
                outf.write(json.dumps(h5chunks.translate()).encode())

print("Merging JSONs...")
mzz = kerchunk.combine.MultiZarrToZarr(
    "zip://*.json::out.zip",
    remote_protocol="http",
    remote_options={'anon': True},
#    preprocess="drop_coords",
    xarray_concat_args={"dim": "time"},
    xarray_open_kwargs={
        "decode_cf": False,
        "mask_and_scale": False,
        "decode_times": True,
        "decode_timedelta": False,
        "use_cftime": True,
        "decode_coords": False
    }
)

# path, remote_protocol, remote_options=None, xarray_open_kwargs=None, xarray_concat_args=None, preprocess=None, storage_options=None):
#mzz.translate("output.zarr")

# This can also be written as a json
mzz.translate("output.json")

