import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server import util


def init_db_post():  # noqa: E501
    """Khởi tạo lại cơ sở dữ liệu

    Dùng để tạo bảng và dữ liệu mẫu ban đầu. # noqa: E501


    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def root_get():  # noqa: E501
    """Kiểm tra trạng thái server

     # noqa: E501


    :rtype: InlineResponse200
    """
    return 'do some magic!'
