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

## Webhook Trigger
All products can set a webhook to trigger uploads for orders, but this is mostly useful for products using client-side encryption as the uploads for those are done per-order.

The webhooks are triggered when:
- On new round open, and the product has active sale orders
- On each new order that is confirmed after round open and before round close

The webhooks are muted when tournament rounds are not open.

The webhook sends a `POST` request when triggered with the following json body:
```json
{
    "date": "2022-04-02T13:25:32.893448",
    "product_id": 4206,
    "product_category": "numerai-predictions",
    "product_name": "myproduct",
    "product_full_name": "numerai-predictions-myproduct",
    "model_id": "adabxxx-3acf-470e-8733-e4283261xxxx",
    "tournament": 8,
    "order_id": 52,
    "round_tournament": 327
}
```

* date: ISO 8601 timestamp
* product_id: NumerBay product ID
* product_category: NumerBay product category
* product_name: NumerBay product name
* product_full_name: NumerBay product full name (category-name)
* model_id: Numerai model ID
* tournament: Numerai tournament ID
* order_id: (Optional) NumerBay order ID, present when triggered on new order, null when triggered on round open
* round_tournament: Currently selling tournament round
