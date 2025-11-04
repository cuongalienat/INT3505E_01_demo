# swagger_client.BooksApi

All URIs are relative to *http://127.0.0.1:5000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**books_get**](BooksApi.md#books_get) | **GET** /books | Lấy danh sách tất cả sách (có tìm kiếm &amp; phân trang)
[**books_id_delete**](BooksApi.md#books_id_delete) | **DELETE** /books/{id} | Xóa sách
[**books_id_get**](BooksApi.md#books_id_get) | **GET** /books/{id} | Lấy thông tin sách theo ID
[**books_id_put**](BooksApi.md#books_id_put) | **PUT** /books/{id} | Cập nhật thông tin sách
[**books_post**](BooksApi.md#books_post) | **POST** /books | Thêm sách mới

# **books_get**
> InlineResponse2004 books_get(search=search, page=page, limit=limit)

Lấy danh sách tất cả sách (có tìm kiếm & phân trang)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BooksApi()
search = 'search_example' # str | Từ khóa tìm kiếm theo tiêu đề hoặc tác giả (optional)
page = 1 # int | Số trang (bắt đầu từ 1) (optional) (default to 1)
limit = 10 # int | Số bản ghi mỗi trang (optional) (default to 10)

try:
    # Lấy danh sách tất cả sách (có tìm kiếm & phân trang)
    api_response = api_instance.books_get(search=search, page=page, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BooksApi->books_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| Từ khóa tìm kiếm theo tiêu đề hoặc tác giả | [optional] 
 **page** | **int**| Số trang (bắt đầu từ 1) | [optional] [default to 1]
 **limit** | **int**| Số bản ghi mỗi trang | [optional] [default to 10]

### Return type

[**InlineResponse2004**](InlineResponse2004.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_id_delete**
> books_id_delete(id)

Xóa sách

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.BooksApi(swagger_client.ApiClient(configuration))
id = 56 # int | 

try:
    # Xóa sách
    api_instance.books_id_delete(id)
except ApiException as e:
    print("Exception when calling BooksApi->books_id_delete: %s\n" % e)
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

# **books_id_get**
> Book books_id_get(id)

Lấy thông tin sách theo ID

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BooksApi()
id = 56 # int | 

try:
    # Lấy thông tin sách theo ID
    api_response = api_instance.books_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BooksApi->books_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Book**](Book.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_id_put**
> books_id_put(body, id)

Cập nhật thông tin sách

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.BooksApi(swagger_client.ApiClient(configuration))
body = swagger_client.BookCreate() # BookCreate | 
id = 56 # int | 

try:
    # Cập nhật thông tin sách
    api_instance.books_id_put(body, id)
except ApiException as e:
    print("Exception when calling BooksApi->books_id_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BookCreate**](BookCreate.md)|  | 
 **id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **books_post**
> Book books_post(body)

Thêm sách mới

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.BooksApi(swagger_client.ApiClient(configuration))
body = swagger_client.BookCreate() # BookCreate | 

try:
    # Thêm sách mới
    api_response = api_instance.books_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BooksApi->books_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BookCreate**](BookCreate.md)|  | 

### Return type

[**Book**](Book.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

