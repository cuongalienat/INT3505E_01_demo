# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSystemController(BaseTestCase):
    """SystemController integration test stubs"""

    def test_init_db_post(self):
        """Test case for init_db_post

        Khởi tạo lại cơ sở dữ liệu
        """
        response = self.client.open(
            '/api/v1/init-db',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_root_get(self):
        """Test case for root_get

        Kiểm tra trạng thái server
        """
        response = self.client.open(
            '/api/v1/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
