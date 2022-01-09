---
sidebar_position: 1
---

# Ensemble with NumerBay

In this tutorial we are going to make a simple ensemble Numerai predictions file from predictions bought on NumerBay.

Ensembling tends to lower variance and improve accuracy, and we want these for the Numerai tournaments.

Replace with your credentials below and change `products_to_ensemble` to the full names of the prediction files you have bought on NumerBay.
Products you buy need to be listed in `File` mode so that you can download the files.

A working example notebook for this tutorial is available at [https://github.com/councilofelders/numerbay/blob/master/examples/NumerBay%20Ensemble%20Example.ipynb](https://github.com/councilofelders/numerbay/blob/master/examples/NumerBay%20Ensemble%20Example.ipynb)

Checkout the **[Python Client Reference](/docs/reference/numerbay)** docs to learn about all available methods, parameters and returned values.

## Using Python Client

### Install
If you have not installed the `numerbay` client, install by:
```commandline
pip install numerbay
```

### Initialize Python client
```python
import pandas as pd
from numerbay import NumerBay

api = NumerBay(username="myusername", password="mypassword")
```

### Download predictions from NumerBay

Assuming you bought two products: `numerai-predictions-numerbay` and `numerai-predictions-numerbay2`

```python
products_to_ensemble = ["numerai-predictions-numerbay", "numerai-predictions-numerbay2"]

for product_name in products_to_ensemble:
    api.download_artifact(f"{product_name}.csv", product_full_name=product_name)
```

### Read downloaded predictions

```python
all_preds = [pd.read_csv(f"{product_name}.csv", index_col=0).add_suffix(f"_{product_name}") 
             for product_name in products_to_ensemble]

concat_preds = pd.concat(all_preds, axis=1, names=products_to_ensemble).dropna(how='any')
# drop NaNs because one submission file is a legacy file and the other a v2 file
```

### Ensemble by simple average

For demo purpose we do a simple average ensemble here. You can of course try other methods such as rank-averaged predictions, etc.

```python
ensemble_preds = concat_preds.mean(axis=1).rename('prediction').to_frame()
ensemble_preds.to_csv('ensemble.csv')
```
