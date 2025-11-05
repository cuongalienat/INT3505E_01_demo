# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.auths_body import AuthsBody  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAuthsController(BaseTestCase):
    """AuthsController integration test stubs"""

    def test_auths_post(self):
        """Test case for auths_post

        Đăng nhập
        """
        body = AuthsBody()
        response = self.client.open(
            '/api/v1/auths',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
