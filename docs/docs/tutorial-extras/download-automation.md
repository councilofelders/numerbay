---
sidebar_position: 1
---

# Automate Downloads (buyer)
As a buyer, you can use the Python client, its command line interface or the REST APIs for automating downloads from NumerBay.

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

# exported NumerBay key file used for decryption, optional
export NUMERBAY_KEY_PATH=./numerbay.json
```

### Download (and Decrypt)
To download file for your order:

```python
api.download_artifact(
    dest_path=FILE_PATH,
    product_full_name="numerai-predictions-somemodel",
    key_path=NUMERBAY_KEY_PATH, 
    # exported NumerBay key file used for decryption, optional. 
    # Alternatively, specify the key path in env variables.
)
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

# exported NumerBay key file used for decryption, optional
export NUMERBAY_KEY_PATH=./numerbay.json
```

### Download (and Decrypt)

To download file for your order: 
```commandline
numerbay download --product_full_name="numerai-predictions-somemodel" --filename=predictions.csv
```
