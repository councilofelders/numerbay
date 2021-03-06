---
sidebar_position: 2
---

# Automate Submissions (seller)
As a seller, you can use the Python client, its command line interface or the REST APIs for automating submissions to NumerBay.

:::caution

This tutorial only submits product artifact files to NumerBay. **You still need to submit your files to Numerai** in your own code.

:::

## Using Python Client
Python client API reference is available at [https://docs.numerbay.ai/docs/reference/numerbay](https://docs.numerbay.ai/docs/reference/numerbay)

### Install
If you have not installed the `numerbay` client, install by:
```commandline
pip install -U numerbay
```

### Authentication
```python
from numerbay import NumerBay

api = NumerBay(username="myusername", password="mypassword")
```

Alternatively, set the env variables in command line for authentication:
```commandline
export NUMERBAY_USERNAME=myusername
export NUMERBAY_PASSWORD=mypassword
```

### Submit
To submit file to your listing:
```python
artifact = api.upload_artifact(FILE_PATH, product_full_name="numerai-predictions-mymodel")
```

If you have a pandas DataFrame, you can also submit it directly:
```python
api.upload_artifact(df=df, product_full_name="numerai-predictions-mymodel")
```

## Using Command Line
To see command Line help message:
```commandline
numerbay --help
```

### Install
If you have not installed the `numerbay` client, install by:
```commandline
pip install -U numerbay
```

### Authentication
Set the env variables in command line for authentication:
```commandline
export NUMERBAY_USERNAME=myusername
export NUMERBAY_PASSWORD=mypassword
```

### Submit

To submit file to your listing: 
```commandline
numerbay submit --product_full_name="numerai-predictions-mymodel" ./predictions.csv
```
