import connexion
import six

from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_create import UserCreate  # noqa: E501
from swagger_server import util


def users_get(search=None, page=None, limit=None):  # noqa: E501
    """Lấy danh sách người dùng (có tìm kiếm &amp; phân trang)

     # noqa: E501

    :param search: Từ khóa tìm kiếm theo tên hoặc username
    :type search: str
    :param page: Số trang (bắt đầu từ 1)
    :type page: int
    :param limit: Số bản ghi mỗi trang
    :type limit: int

    :rtype: InlineResponse2003
    """
    return 'do some magic!'


def users_post(body):  # noqa: E501
    """Tạo người dùng mới

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:
        body = UserCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
