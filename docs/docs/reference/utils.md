---
sidebar_label: utils
title: utils
---

collection of utility functions (adapted from numerapi: https://github.com/uuazed/numerapi)

#### parse\_datetime\_string

```python
def parse_datetime_string(string: str) -> Optional[datetime.datetime]
```

try to parse string to datetime object

#### parse\_float\_string

```python
def parse_float_string(string: str) -> Optional[float]
```

try to parse string to decimal.Decimal object

#### replace

```python
def replace(dictionary: Dict, key: str, function)
```

apply a function to dict item

#### download\_file

```python
def download_file(url: str, dest_path: str, show_progress_bars: bool = True)
```

downloads a file and shows a progress bar. allow resuming a download

#### get\_with\_err\_handling

```python
def get_with_err_handling(url: str, params: Dict = None, headers: Dict = None, timeout: Optional[int] = None) -> Dict
```

send `get` request and handle (some) errors that might occur

#### post\_with\_err\_handling

```python
def post_with_err_handling(url: str, body: str = None, json: str = None, headers: Dict = None, timeout: Optional[int] = None) -> Dict
```

send `post` request and handle (some) errors that might occur

#### encrypt\_file\_object

```python
def encrypt_file_object(file: Union[BinaryIO, BytesIO], key: str)
```

encrypt a file stream

#### decrypt\_file

```python
def decrypt_file(dest_path: str, key_path: str = None, key_base64: str = None)
```

decrypt and overwrite a file

