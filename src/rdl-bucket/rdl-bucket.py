from typing import Optional

import os
import glob
import zipfile
from pathlib import Path

import typer
import boto3
from tqdm import tqdm

try: 
    import zlib
    compression = zipfile.ZIP_DEFLATED
except Exception:
    print("Could not load zlib library, any zipped files will not be compressed")
    compression = zipfile.ZIP_STORED


os.environ['AWS_CONFIG_FILE'] = ".settings.toml"
app = typer.Typer()


@app.command()
def zip_files(dir_path: Path):
    """Zip individual files in given directory.
    
    Note: Only top-level files are zipped. Nested folders are not supported."""
    all_files = dir_path.glob('*.*')
    for fn in tqdm(all_files):
        zipfile.ZipFile(fn.with_name(fn.name+'.zip'), mode='w').write(fn, arcname=fn.name, compress_type=compression)


@app.command()
def upload_folder(dir_path: Path):
    """Upload all contents of a folder to the `datasets/data` directory in the AWS Bucket."""
    all_files = dir_path.glob('*.*')
    for fn in tqdm(all_files):
        upload_file(fn, fn.name)


@app.command()
def upload_file(filename: str, key_name: Optional[str] = None):
    """Upload a single file to AWS Bucket, under the datasets/data directory.
    
    Note: Existing files will be overwritten!
    """
    if not key_name:
        key_name = filename

    with open(filename, 'rb') as fp:
        client.upload_fileobj(fp, 'risk-data-library-storage', f"datasets/data/{key_name}")


@app.command()
def download_file(filename: str):
    """Download a single file from the AWS Bucket, under the datasets/data directory.
    """
    client.download_file('risk-data-library-storage', f"datasets/data/{filename}", filename)


@app.command()
def delete_file(filename: str):
    """Delete a single file in the datasets/data directory."""
    client.delete_object(Bucket='risk-data-library-storage', Key=f"datasets/data/{filename}")


@app.command()
def list_files():
    """List all files in the AWS Bucket."""
    new_file_list = s3.Bucket('risk-data-library-storage')
    for fn in new_file_list.objects.all():
        print(fn)


if __name__ == '__main__':
    s3 = boto3.resource("s3")
    client = boto3.client('s3')
    app()
