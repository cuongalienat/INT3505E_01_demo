# swagger_client.AuthsApi

All URIs are relative to *http://127.0.0.1:5000/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auths_post**](AuthsApi.md#auths_post) | **POST** /auths | Đăng nhập

# **auths_post**
> InlineResponse2002 auths_post(body)

Đăng nhập

Đăng nhập bằng username và password để nhận JWT token.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AuthsApi()
body = swagger_client.AuthsBody() # AuthsBody | 

try:
    # Đăng nhập
    api_response = api_instance.auths_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthsApi->auths_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuthsBody**](AuthsBody.md)|  | 

### Return type

[**InlineResponse2002**](InlineResponse2002.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

