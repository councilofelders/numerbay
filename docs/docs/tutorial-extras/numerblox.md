---
sidebar_position: 4
---

# NumerBlox Integration

[NumerBlox](https://crowdcent.github.io/numerblox/) is a library that offers Numerai specific functionality, so you can worry less about software/data engineering and focus more on building great Numerai models.

NumerBay provides basic integration with NumerBlox for downloading and submission of file artifacts.

A working example notebook for this tutorial is available at [https://github.com/restrading/numerblox/blob/feature/numerbay-edu-nbs/nbs/edu_nbs/numerbay_integration.ipynb](https://github.com/restrading/numerblox/blob/feature/numerbay-edu-nbs/nbs/edu_nbs/numerbay_integration.ipynb)

## NumerBay download with NumerFrame

This part of the tutorial demonstrates how to use `NumerFrame` to download predictions bought on NumerBay community marketplace.

### Numerai Classic

First, we download tournament data using `NumeraiClassicDownloader`.

```python
from numerblox.numerframe import create_numerframe, NumerFrame
from numerblox.download import NumeraiClassicDownloader
from numerblox.key import Key
from numerblox.model import NumerBayCSVs
from numerblox.submission import NumerBaySubmitter, NumeraiClassicSubmitter, NumeraiSignalsSubmitter

downloader = NumeraiClassicDownloader("numerframe_edu")
# Path variables
tournament_file = "numerai_tournament_data.parquet"
tournament_save_path = f"{str(downloader.dir)}/{tournament_file}"
# Download only tournament parquet file
downloader.download_single_dataset(tournament_file, dest_path=tournament_save_path)
```

Loading in data and initializing a `NumerFrame` takes one line of code. It will automatically recognize the data format such as `.csv` or `.parquet`. You have the option to add metadata, which is stored in the `meta` attribute.

```python
# Initialize NumerFrame from parquet file path
dataf = create_numerframe(tournament_save_path, metadata={"version": 3, "type": "tournament"})
```

Next, we create a NumerBayCSVs model object with a list of products we bought and NumerBay credentials. `numerbay_key_path` may be required for products that use client-side encryption. You can learn more about encryption [here](https://docs.numerbay.ai/updates/encryption)

```python
nb_model = NumerBayCSVs(data_directory='/app/notebooks/tmp',
                        numerbay_product_full_names=['numerai-predictions-numerbay'],  # change to the full names of products you bought
                        numerbay_username="your_username",  # change to your own username
                        numerbay_password="your_password",  # change to your own password
                        numerbay_key_path="/app/notebooks/tmp/numerbay.json")
```

Call the `predict` method on the `NumerFrame` to fetch the prediction file from NumerBay. If the file already exists in the `data_directory`, that file will be loaded without re-downloading.

```python
preds = nb_model.predict(dataf)
```

The predictions are concatenated to the `NumerFrame` with column name `prediction_numerai-predictions-numerbay`.

In this part of the tutorial we have downloaded a prediction file from NumerBay with `NumerFrame`. This makes things easier for post processing such as ensembling and neutralization.

### Numerai Signals

Currently only the main tournament is supported. Signals support will be added in future.

## NumerBay submission
This part of the tutorial is for sellers who want to upload their predictions to NumerBay to fulfill sale orders. Using `NumerBaySubmitter`, a seller can choose to submit to both Numerai and NumerBay or just NumerBay.

### Numerai Classic

Assume we have some prediction column to upload for the Numerai main tournament, in this case the `prediction` column which simply takes the value of a feature.

```python
dataf = create_numerframe(tournament_save_path, metadata={"version": 3, "type": "tournament"})
dataf['prediction'] = dataf['feature_dichasial_hammier_spawner']  # delete this line to use your own columns
```

Next, we create a `NumerBaySubmitter` object which wraps on top of a `NumeraiClassicSubmitter` object that you would normally use if you are only submitting to Numerai.

```python
key = Key(pub_id='YOUR_PUBLIC_KEY', secret_key='YOUR_PRIVATE_KEY')  # change to your own Numerai API key
numerai_submitter = NumeraiClassicSubmitter(directory_path="/app/notebooks/tmp", key=key)
```

Set `upload_to_numerai` to True (default) if you want to submit to both Numerai and NumerBay, set to False to submit only to NumerBay.

```python
nb_submitter = NumerBaySubmitter(tournament_submitter=numerai_submitter, upload_to_numerai=True, numerbay_username="numerbay", numerbay_password="your_password")
```

Finally, we call the `full_submission` method to perform the submission

```python
nb_submitter.full_submission(dataf, file_name='upload-full.csv', model_name='numerbay', numerbay_product_full_name='numerai-predictions-numerbay', cols='prediction')
```

### Numerai Signals

The process for Signals submission is very similar and is omitted for brevity, just do the following:
- Use Signals NumerFrame
- Change `NumeraiClassicSubmitter` to `NumeraiSignalsSubmitter` for the `tournament_submitter` argument
- When calling `full_submission`, change the `cols` argument to the list of Signals column to submit (e.g. `['bloomberg_ticker', 'signal']`)

