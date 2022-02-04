# can-it-kerchunk

Testing kerchunk with some of our data and services

## TO-DOs

- [ ] Get cf-decoding of times to work - probably just involves passing through kwargs.
- [ ] Need to do a comparison of metadata, bounds, coordinates and values between original and new data.

## Initial test:

### With single NetCDF file

```
put-cmip6-nc.sh

build-kerchunk-single.py

unzip out.zip

jos put -s http://cmip6-zarr-o.s3.jc.rl.ac.uk/ -c ~/.credentials/caringo-credentials.json.cmip6-zarr -b A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM 1pctCO2.r1i1p1f3.Amon.hus.gn.v20200115.185001-186912.nc.json

read-kerchunk-single.py
```

### With multiple NetCDF files

```
put-cmip6-nc.sh # If not run already

build-kerchunk-multiple.py

# writes: output.json # as aggregated kerchunk file

jos put -s http://cmip6-zarr-o.s3.jc.rl.ac.uk/ -c ~/.credentials/caringo-credentials.json.cmip6-zarr -b A-NC-CMIP6.CMIP.MOHC.HadGEM3-GC31-MM output.json

read-kerchunk-multiple.py
```


