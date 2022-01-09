---
sidebar_position: 2
---

# Automate Submissions (seller)
As a seller, you can use the Python client, its command line interface or the REST APIs for automating submissions to NumerBay.

:::caution

This tutorial only submits product artifact files to NumerBay. **You still need to submit your files to Numerai** in your own code.

:::

## Using Python Client (Recommended)
Python client API reference is available at [https://docs.numerbay.ai/docs/reference/numerbay](https://docs.numerbay.ai/docs/reference/numerbay)

### Install
If you have not installed the `numerbay` client, install by:
```commandline
pip install numerbay
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

## Using Command Line (Recommended)
To see command Line help message:
```commandline
numerbay --help
```

### Install
If you have not installed the `numerbay` client, install by:
```commandline
pip install numerbay
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


## Using REST API

NumerBay provides REST APIs at the backend endpoint `https://numerbay.ai/backend-api/v1`

Interactive Swagger API docs are available at [https://numerbay.ai/docs](https://numerbay.ai/docs)

A working example notebook for using REST API is available at [https://github.com/councilofelders/numerbay/blob/master/examples/NumerBay%20Example.ipynb](https://github.com/councilofelders/numerbay/blob/master/examples/NumerBay%20Example.ipynb)

### Login to get authentication token

```python
from requests import Session
BASE_API_URL = "https://numerbay.ai/backend-api/v1"

client = Session()

login_data = {
    "username": NUMERBAY_USERNAME,
    "password": NUMERBAY_PASSWORD
}

r = client.post(f"{BASE_API_URL}/login/access-token", data=login_data)

access_token = r.json()['access_token']

# Add the token header to the client for all subsequent queries
client.headers = {"Authorization": f"Bearer {access_token}"}
```

### Generate upload URL for product artifact

```python
artifact_data = {
    "filename": os.path.basename(PRODUCT_ARTIFACT_FILE)
}

r = client.post(
    f"{BASE_API_URL}/products/{PRODUCT_ID}/artifacts/generate-upload-url",
    data=artifact_data,
)

content = r.json()
artifact_id = content['id']
upload_url = content['url']
```

### Upload the file to the generated URL

```python
r = client.put(upload_url, 
               data=open(PRODUCT_ARTIFACT_FILE, 'rb'), 
               headers={"Content-type": "application/octet-stream"})
# The header override is important
```

### Validate the upload

:::caution

This step is **required**. If not performed, your upload may not be confirmed immediately.

:::

```python
r = client.post(
    f"{BASE_API_URL}/products/{PRODUCT_ID}/artifacts/{artifact_id}/validate-upload",
)
```
