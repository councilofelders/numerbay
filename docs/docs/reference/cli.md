---
sidebar_label: cli
title: cli
---

Access the numerai API via command line

## CommonJSONEncoder Objects

```python
class CommonJSONEncoder(json.JSONEncoder)
```

Common JSON Encoder
json.dumps(jsonString, cls=CommonJSONEncoder)

#### prettify

```python
def prettify(stuff)
```

prettify json

#### cli

```python
@click.group()
def cli()
```

Wrapper around the NumerBay API

#### account

```python
@cli.command()
def account()
```

Get all information about your account!

#### orders

```python
@cli.command()
def orders()
```

Get all your orders!

#### listings

```python
@cli.command()
def listings()
```

Get all your listings!

#### submit

```python
@cli.command()
@click.option("--product_id", type=int, default=None, help="NumerBay product ID")
@click.option(
    "--product_full_name",
    type=str,
    default=None,
    help="NumerBay product full name (e.g. numerai-predictions-numerbay), \
    used for resolving product_id if product_id is not provided",
)
@click.argument("path", type=click.Path(exists=True))
def submit(path, product_id, product_full_name)
```

Upload artifact from file.

#### download

```python
@cli.command()
@click.option("--product_id", type=int, default=None, help="NumerBay product ID")
@click.option(
    "--product_full_name",
    type=str,
    default=None,
    help="NumerBay product full name (e.g. numerai-predictions-numerbay), \
    used for resolving product_id if product_id is not provided",
)
@click.option(
    "--artifact_id",
    type=int,
    default=None,
    help="Artifact ID for the file to download, \
    defaults to the first artifact for your active order for the product",
)
@click.option("--filename", help="filename to store as")
@click.option(
    "--dest_path",
    help="complate path where the file should be stored, \
    defaults to the same name as the source file",
)
def download(filename, dest_path, product_id, product_full_name, artifact_id)
```

Download artifact file.

#### version

```python
@cli.command()
def version()
```

Installed numerbay version.

