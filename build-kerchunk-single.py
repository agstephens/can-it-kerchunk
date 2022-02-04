import os
import json
import zipfile
import kerchunk.hdf
import fsspec

urls = ["http://cmip6-zarr-o.s3.jc.rl.ac.uk/A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM/" + f for f in [
    "1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc"]]

so = dict(
   # anon=True, 
#    default_fill_cache=False, default_cache_type='first'
)

help(fsspec.open)
with zipfile.ZipFile("out.zip", mode="w") as zf:
    for u in urls:
        with fsspec.open(u, **so) as inf:
            print(f"Working on: {u}")
            h5chunks = kerchunk.hdf.SingleHdf5ToZarr(inf, u, inline_threshold=100)
            with zf.open(os.path.basename(u) + ".json", 'w') as outf:
                outf.write(json.dumps(h5chunks.translate()).encode())

