# swagger_client.SystemApi

All URIs are relative to *http://127.0.0.1:5000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**init_db_post**](SystemApi.md#init_db_post) | **POST** /init-db | Khởi tạo lại cơ sở dữ liệu
[**root_get**](SystemApi.md#root_get) | **GET** / | Kiểm tra trạng thái server

# **init_db_post**
> InlineResponse2001 init_db_post()

Khởi tạo lại cơ sở dữ liệu

Dùng để tạo bảng và dữ liệu mẫu ban đầu.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SystemApi()

try:
    # Khởi tạo lại cơ sở dữ liệu
    api_response = api_instance.init_db_post()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->init_db_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **root_get**
> InlineResponse200 root_get()

Kiểm tra trạng thái server

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SystemApi()

try:
    # Kiểm tra trạng thái server
    api_response = api_instance.root_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemApi->root_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

