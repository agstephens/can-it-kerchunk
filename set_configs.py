import os
import tempfile
import importlib


def setup_configs(key, secret, url):
    tmpdir = tempfile.mkdtemp(prefix="s3-config-")
    aws_file = os.path.join(tmpdir, "aws.conf")

    with open(aws_file, "w") as aws:
        aws.write(f"""[default]
aws_access_key_id = {key}
aws_secret_access_key = {secret}
""")

    fsspec_file = os.path.join(tmpdir, "fsspec.json")
    with open(fsspec_file, "w") as fss:
        fss.write(f"""{{
    "s3": {{
        "client_kwargs": {{
            "endpoint_url": "{url}"
        }}
    }}
}}
""")
 
    os.environ["AWS_CONFIG_FILE"] = aws_file
    os.environ["FSSPEC_CONFIG_DIR"] = tmpdir

# AWS_CONFIG_FILE=/home/users/astephens/xarray-zarr-deep-dive/tmpconf/aws.conf FSSPEC_CONFIG_DIR=/home/users/astephens/xarray-zarr-deep-dive/tmpconf
    return tmpdir

def test_setup_configs():
    tmpdir = setup_configs(key="key", secret="secret", url="url")
    print(tmpdir)
    assert os.path.isdir(tmpdir)


#test_setup_configs()

