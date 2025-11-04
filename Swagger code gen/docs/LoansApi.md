# swagger_client.LoansApi

All URIs are relative to *http://127.0.0.1:5000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**loans_get**](LoansApi.md#loans_get) | **GET** /loans | Lấy danh sách lượt mượn (có tìm kiếm &amp; phân trang)
[**loans_id_return_patch**](LoansApi.md#loans_id_return_patch) | **PATCH** /loans/{id}/return | Trả sách
[**loans_post**](LoansApi.md#loans_post) | **POST** /loans | Mượn sách mới

# **loans_get**
> InlineResponse2005 loans_get(search=search, page=page, limit=limit)

Lấy danh sách lượt mượn (có tìm kiếm & phân trang)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LoansApi(swagger_client.ApiClient(configuration))
search = 'search_example' # str | Tìm kiếm theo tên người dùng hoặc tiêu đề sách (optional)
page = 1 # int | Số trang (bắt đầu từ 1) (optional) (default to 1)
limit = 10 # int | Số bản ghi mỗi trang (optional) (default to 10)

try:
    # Lấy danh sách lượt mượn (có tìm kiếm & phân trang)
    api_response = api_instance.loans_get(search=search, page=page, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoansApi->loans_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| Tìm kiếm theo tên người dùng hoặc tiêu đề sách | [optional] 
 **page** | **int**| Số trang (bắt đầu từ 1) | [optional] [default to 1]
 **limit** | **int**| Số bản ghi mỗi trang | [optional] [default to 10]

### Return type

[**InlineResponse2005**](InlineResponse2005.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **loans_id_return_patch**
> loans_id_return_patch(id)

Trả sách

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LoansApi(swagger_client.ApiClient(configuration))
id = 56 # int | 

try:
    # Trả sách
    api_instance.loans_id_return_patch(id)
except ApiException as e:
    print("Exception when calling LoansApi->loans_id_return_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **loans_post**
> Loan loans_post(body)

Mượn sách mới

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LoansApi(swagger_client.ApiClient(configuration))
body = swagger_client.LoansBody() # LoansBody | 

try:
    # Mượn sách mới
    api_response = api_instance.loans_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoansApi->loans_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**LoansBody**](LoansBody.md)|  | 

### Return type

[**Loan**](Loan.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

