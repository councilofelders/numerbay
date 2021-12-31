---
sidebar_position: 2
---

# API Automation

NumerBay provides REST APIs at the backend endpoint `https://numerbay.ai/backend-api/v1`

Interactive Swagger API docs are available at [https://numerbay.ai/docs](https://numerbay.ai/docs)

## Automated submission

A working example notebook for API automated submission to NumerBay is available at [https://github.com/councilofelders/numerbay/blob/master/NumerBay%20Example.ipynb](https://github.com/councilofelders/numerbay/blob/master/NumerBay%20Example.ipynb)

:::caution

This example code only submits product artifact files to NumerBay. **You still need to submit your files to Numerai** in your own code.

:::

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
