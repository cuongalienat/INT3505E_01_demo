import connexion
import six

from swagger_server.models.auths_body import AuthsBody  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server import util


def auths_post(body):  # noqa: E501
    """Đăng nhập

    Đăng nhập bằng username và password để nhận JWT token. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2002
    """
    if connexion.request.is_json:
        body = AuthsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
