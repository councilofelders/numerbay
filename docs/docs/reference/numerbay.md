---
sidebar_label: numerbay
title: numerbay
---

NumerBay API module

Install via:
```commandline
pip install numerbay
```

## NumerBay Objects

```python
class NumerBay()
```

Wrapper around the NumerBay API

### \_\_init\_\_

```python
def __init__(username=None, password=None, verbosity="INFO", show_progress_bars=True)
```

initialize NumerBay API wrapper for Python

**Arguments**:

- `username` _str_ - your NumerBay username
- `password` _str_ - your NumerBay password
- `verbosity` _str_ - indicates what level of messages should be
  displayed. valid values are "debug", "info", "warning",
  "error" and "critical"
- `show_progress_bars` _bool_ - flag to turn of progress bars

### get\_account

```python
def get_account() -> Dict
```

Get all information about your account!

**Returns**:

- `dict` - user information including the following fields:
  
  * email (`str`)
  * id (`int`)
  * is_active (`bool`)
  * is_superuser (`bool`)
  * public_address (`str`)
  * username (`str`)
  * numerai_api_key_public_id (`str`)
  * numerai_api_key_can_read_user_info (`bool`)
  * numerai_api_key_can_read_submission_info (`bool`)
  * numerai_api_key_can_upload_submission (`bool`)
  * numerai_api_key_can_stake (`bool`)
  * numerai_wallet_address (`str`)
  * models (`list`) each with the following fields:
  * id (`str`)
  * name (`str`)
  * tournament (`int`)
  * start_date (`datetime`)
  * coupons (`list`)
  

**Example**:

  ```python
  api = NumerBay(username="..", password="..")
  api.get_account()
  ```
  ```
  {
  "email":"me@example.com",
  "is_active":True,
  "is_superuser":False,
  "username":"myusername",
  "public_address":"0xmymetamaskaddressdde80ca30248e7a8890cacb",
  "id":2,
  "numerai_api_key_public_id":"MYNUMERAIAPIKEYRCXBVB66ACTSLDR53",
  "numerai_api_key_can_upload_submission":True,
  "numerai_api_key_can_stake":True,
  "numerai_api_key_can_read_submission_info":True,
  "numerai_api_key_can_read_user_info":True,
  "numerai_wallet_address":"0x000000000000000000000000mynumeraiaddress",
  "models":[{
  "id":"xxxxxxxx-xxxx-xxxx-xxxx-411487a4d64a",
  "name":"mymodel",
  "tournament":8,
  "start_date":"2021-03-22T17:44:50"
  }, ..],
  "coupons":[..]
  }
  ```

### get\_my\_orders

```python
def get_my_orders() -> List
```

Get all your orders.

**Returns**:

- `list` - List of dicts with the following structure:
  
  * date_order (`datetime`)
  * round_order (`int`)
  * quantity (`int`)
  * price (`decimal.Decimal`)
  * currency (`str`)
  * mode (`str`)
  * stake_limit (`decimal.Decimal`)
  * submit_model_id (`str`)
  * submit_model_name (`str`)
  * submit_state (`str`)
  * chain (`str`)
  * from_address (`str`)
  * to_address (`str`)
  * transaction_hash (`str`)
  * state (`str`)
  * applied_coupon_id (`int`)
  * coupon (`bool`)
  * coupon_specs (`dict`)
  * id (`int`)
  * product (`dict`)
  * buyer (`dict`)
  * buyer_public_key (`str`)
  * artifacts (`list`)

**Example**:

  ```python
  api = NumerBay(username="..", password="..")
  api.get_my_orders()
  ```
  ```
  [{
  "date_order":"2021-12-25T06:34:58.047278",
  "round_order":296,
  "quantity":1,
  "price":9,
  "currency":"NMR",
  "mode":"file",
  "stake_limit":None,
  "submit_model_id":None,
  "submit_model_name":None,
  "submit_state":None,
  "chain":"ethereum",
  "from_address":"0x00000000000000000000000000000fromaddress",
  "to_address":"0x0000000000000000000000000000000toaddress",
  "transaction_hash":"0x09bd2a0f814a745...7a20e5abcdef",
  "state":"confirmed",
  "applied_coupon_id":1,
  "coupon":None,
  "coupon_specs":None,
  "id":126,
  "product":{..},
  "buyer":{
  "id":2,
  "username":"myusername"
  },
  "buyer_public_key":"yqKFQtzss8vRL7devlvZY70v5WUrS3BfKfPFzTnYit4=",
  "artifacts":[...]
  }, ...]
  ```

### get\_my\_sales

```python
def get_my_sales(active_only: bool = False) -> List
```

Get all your sales (including pending and expired sales).

**Arguments**:

- `active_only` _bool, optional_ - whether to fetch only active sale orders

**Returns**:

- `list` - List of dicts with the following structure:
  
  * date_order (`datetime`)
  * round_order (`int`)
  * quantity (`int`)
  * price (`decimal.Decimal`)
  * currency (`str`)
  * mode (`str`)
  * stake_limit (`decimal.Decimal`)
  * submit_model_id (`str`)
  * submit_model_name (`str`)
  * submit_state (`str`)
  * chain (`str`)
  * from_address (`str`)
  * to_address (`str`)
  * transaction_hash (`str`)
  * state (`str`)
  * applied_coupon_id (`int`)
  * coupon (`bool`)
  * coupon_specs (`dict`)
  * id (`int`)
  * product (`dict`)
  * buyer (`dict`)
  * buyer_public_key (`str`)
  * artifacts (`list`)

**Example**:

  ```python
  api = NumerBay(username="..", password="..")
  api.get_my_sales()
  ```
  ```
  [{
  "date_order":"2021-12-25T06:34:58.047278",
  "round_order":296,
  "quantity":1,
  "price":9,
  "currency":"NMR",
  "mode":"file",
  "stake_limit":None,
  "submit_model_id":None,
  "submit_model_name":None,
  "submit_state":None,
  "chain":"ethereum",
  "from_address":"0x00000000000000000000000000000fromaddress",
  "to_address":"0x0000000000000000000000000000000toaddress",
  "transaction_hash":"0x09bd2a0f814a745...7a20e5abcdef",
  "state":"confirmed",
  "applied_coupon_id":1,
  "coupon":None,
  "coupon_specs":None,
  "id":126,
  "product":{..},
  "buyer":{
  "id":2,
  "username":"someusername"
  },
  "buyer_public_key":"yqKFQtzss8vRL7devlvZY70v5WUrS3BfKfPFzTnYit4=",
  "artifacts":[...]
  }, ...]
  ```

### get\_my\_listings

```python
def get_my_listings()
```

Get all your listings.

**Returns**:

- `list` - List of dicts with the following structure:
  
  * avatar (`str`)
  * description (`str`)
  * is_active (`bool`)
  * is_ready (`bool`)
  * expiration_round (`int`)
  * total_num_sales (`int`)
  * last_sale_price (`decimal.Decimal`)
  * last_sale_price_delta (`decimal.Decimal`)
  * featured_products (`list`)
  * id (`int`)
  * name (`str`)
  * sku (`str`)
  * category (`dict`) with the following fields:
  * name (`str`)
  * slug (`str`)
  * tournament (`int`)
  * is_per_round (`bool`)
  * is_submission (`bool`)
  * id (`int`)
  * items (`list`)
  * parent (`dict`)
  * owner (`dict`)
  * model (`dict`)
  * reviews (`list`)
  * options (`list`) each with the following fields:
  * id (`int`)
  * is_on_platform (`bool`)
  * third_party_url (`str`)
  * description (`str`)
  * quantity (`int`)
  * price (`decimal.Decimal`)
  * currency (`str`)
  * wallet (`str`)
  * chain (`str`)
  * stake_limit (`decimal.Decimal`)
  * mode (`str`)
  * is_active (`bool`)
  * coupon (`bool`)
  * coupon_specs (`dict`)
  * special_price (`decimal.Decimal`)
  * applied_coupon (`str`)
  * product_id (`int`)

**Example**:

  ```python
  api = NumerBay(username="..", password="..")
  api.get_my_listings()
  ```
  ```
  [{
  "avatar":"https://example.com/example.jpg",
  "description":"Product description",
  "is_active":True,
  "is_ready":False,
  "expiration_round":None,
  "total_num_sales":0,
  "last_sale_price":None,
  "last_sale_price_delta":None,
  "featured_products":None,
  "id":108,
  "name":"mymodel",
  "sku":"numerai-predictions-mymodel",
  "category":{
  "name":"Predictions",
  "slug":"numerai-predictions",
  "tournament":8,
  "is_per_round":True,
  "is_submission":True,
  "id":3,
  "items":[..],
  "parent":{..}
  },
  "owner":{
  "id":2,
  "username":"myusername"
  },
  "model":{
  "name":"mymodel",
  "tournament":8,
  "nmr_staked":100,
  "latest_ranks":{
  "corr":100,
  "fnc":200,
  "mmc":300
  },
  "latest_reps":{
  "corr":0.01,
  "fnc":0.01,
  "mmc":0.01
  },
  "latest_returns":{
  "oneDay":-5.120798695681796,
  "oneYear":None,
  "threeMonths":-5.915974438808858
  },
  "start_date":"2020-10-25T11:08:30"
  },
  "reviews":[...],
  "options":[{
  "id":6,
  "is_on_platform":True,
  "third_party_url":None,
  "description":None,
  "quantity":1,
  "price":1,
  "currency":"NMR",
  "wallet":None,
  "chain":None,
  "stake_limit":None,
  "mode":"file",
  "is_active":True,
  "coupon":None,
  "coupon_specs":None,
  "special_price":None,
  "applied_coupon":None,
  "product_id":108
  }]
  }, ...]
```

### upload\_artifact

```python
def upload_artifact(file_path: str = "predictions.csv", product_id: int = None, product_full_name: str = None, order_id: int = None, df: pd.DataFrame = None) -> Union[List, Dict]
```

Upload artifact from file.

**Arguments**:

- `file_path` _str_ - file that will get uploaded
- `product_id` _int_ - NumerBay product ID
- `product_full_name` _str_ - NumerBay product full name (e.g. numerai-predictions-numerbay),
  used for resolving product_id if product_id is not provided
- `order_id` _int, optional_ - NumerBay order ID,
  used for encrypted per-order artifact upload
- `df` _pandas.DataFrame_ - pandas DataFrame to upload, if function is
  given df and file_path, df will be uploaded.

**Returns**:

  list or dict: list of artifacts uploaded (for encrypted listing)
  or the artifact uploaded (for unencrypted listing)

**Example**:

  ```python
  api = NumerBay(username="..", password="..")
  product_full_name = "numerai-predictions-numerbay"
  api.upload_predictions("predictions.csv", product_full_name=product_full_name)
  # upload from pandas DataFrame directly:
  api.upload_predictions(df=predictions_df, product_full_name=product_full_name)
  ```

### download\_artifact

```python
def download_artifact(filename: str = None, dest_path: str = None, product_id: int = None, product_full_name: str = None, order_id: int = None, artifact_id: Union[int, str] = None, key_path: str = None, key_base64: str = None) -> None
```

Download artifact file.

**Arguments**:

- `filename` _str_ - filename to store as
- `dest_path` _str, optional_ - complate path where the file should be
  stored, defaults to the same name as the source file
- `product_id` _int, optional_ - NumerBay product ID
- `product_full_name` _str, optional_ - NumerBay product full name
  (e.g. numerai-predictions-numerbay),
  used for resolving product_id if product_id is not provided
- `order_id` _int, optional_ - NumerBay order ID,
  used for encrypted per-order artifact download
- `artifact_id` _str or int, optional_ - Artifact ID for the file to download,
  defaults to the first artifact for your active order for the product
- `key_path` _int, optional_ - path to buyer's exported NumerBay key file
- `key_base64` _int, optional_ - buyer's NumerBay private key base64 string (used for tests)

**Example**:

  ```python
  api = NumerBay(username="..", password="..")
  api.download_artifact("predictions.csv", product_id=2, artifact_id=744)
  ```

### lock\_product

```python
def lock_product(self, product_id: int = None, product_full_name: str = None, round_number: int = None) -> Dict
```

Lock product.

**Arguments**:

- `product_id` _int, optional_ - NumerBay product ID
- `product_full_name` _str, optional_ - NumerBay product full name
  (e.g. numerai-predictions-numerbay),
  used for resolving product_id if product_id is not provided
- `round_number` _int, optional_ - round number to lock, defaults to current selling round

**Example**:

  ```python
  api = NumerBay(username="..", password="..")
  api.lock_product(product_id=2)
  ```

