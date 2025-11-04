# swagger_client.UsersApi

All URIs are relative to *http://127.0.0.1:5000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**users_get**](UsersApi.md#users_get) | **GET** /users | Lấy danh sách người dùng (có tìm kiếm &amp; phân trang)
[**users_post**](UsersApi.md#users_post) | **POST** /users | Tạo người dùng mới

# **users_get**
> InlineResponse2003 users_get(search=search, page=page, limit=limit)

Lấy danh sách người dùng (có tìm kiếm & phân trang)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.UsersApi(swagger_client.ApiClient(configuration))
search = 'search_example' # str | Từ khóa tìm kiếm theo tên hoặc username (optional)
page = 1 # int | Số trang (bắt đầu từ 1) (optional) (default to 1)
limit = 10 # int | Số bản ghi mỗi trang (optional) (default to 10)

try:
    # Lấy danh sách người dùng (có tìm kiếm & phân trang)
    api_response = api_instance.users_get(search=search, page=page, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| Từ khóa tìm kiếm theo tên hoặc username | [optional] 
 **page** | **int**| Số trang (bắt đầu từ 1) | [optional] [default to 1]
 **limit** | **int**| Số bản ghi mỗi trang | [optional] [default to 10]

### Return type

[**InlineResponse2003**](InlineResponse2003.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_post**
> User users_post(body)

Tạo người dùng mới

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UsersApi()
body = swagger_client.UserCreate() # UserCreate | 

try:
    # Tạo người dùng mới
    api_response = api_instance.users_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UsersApi->users_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserCreate**](UserCreate.md)|  | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

