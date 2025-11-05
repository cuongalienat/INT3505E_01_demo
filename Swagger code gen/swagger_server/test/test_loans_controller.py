# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2005 import InlineResponse2005  # noqa: E501
from swagger_server.models.loan import Loan  # noqa: E501
from swagger_server.models.loans_body import LoansBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLoansController(BaseTestCase):
    """LoansController integration test stubs"""

    def test_loans_get(self):
        """Test case for loans_get

        Lấy danh sách lượt mượn (có tìm kiếm & phân trang)
        """
        query_string = [('search', 'search_example'),
                        ('page', 1),
                        ('limit', 10)]
        response = self.client.open(
            '/api/v1/loans',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_loans_id_return_patch(self):
        """Test case for loans_id_return_patch

        Trả sách
        """
        response = self.client.open(
            '/api/v1/loans/{id}/return'.format(id=56),
            method='PATCH')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_loans_post(self):
        """Test case for loans_post

        Mượn sách mới
        """
        body = LoansBody()
        response = self.client.open(
            '/api/v1/loans',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
