A simple interface to the RDL AWS Bucket for the GFDRR RDL team

This app is under development and currently only supports Windows.

# Usage guide

## Configuration
Create a `.settings.toml` file with any text editor.

It looks like this at a bare minimum:

```toml
[default]
aws_access_key_id = <your access key>
aws_secret_access_key = <your secret key>

[region]
region = us-east-1  # specify your default region
```

Save the `.settings.toml` file in the same location as the executable `rdl-bucket.exe`

## Running commands

```bash
> rdl-bucket

Usage: rdl-bucket [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.     

  --help                          Show this message and exit.

Commands:
  delete-file      Delete a single file in the datasets/data directory.      
  list-files       List all files in the `risk-data-library-storage` bucket. 
  upload-file      Upload a single file to AWS Bucket, under the...
  upload-folder    Upload all contents of a folder to the `datasets/data`... 
```

### Getting help on specific commands

```bash
> rdl-bucket upload-file --help

Usage: rdl-bucket upload-file [OPTIONS] FILENAME

  Upload a single file to AWS Bucket, under the datasets/data directory.

  Note: Existing files will be overwritten!

Arguments:
  FILENAME  [required]

Options:
  --key-name TEXT
  --help           Show this message and exit.
```

## Upload process

1. Zip individual files if zip files are to be uploaded

```bash
> rdl-bucket zip-files ../some_directory
```

2. Check that files were correctly zipped.

3. Upload to S3 Bucket

```bash
> rdl-bucket upload-folder ../some_directory
```

## Helpful notes

Use the pipe operator to export outputs if needed:

```bash
> rdl-bucket list-files > file_list.txt
```

## Dev notes

This tool uses `pyinstaller` to create the single binary.

```bash
> pyinstaller src/rdl-bucket/rdl-bucket.py --onefile
```
