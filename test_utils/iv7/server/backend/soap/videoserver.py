from jsonschema import validate
from jsonschema.exceptions import ValidationError

from test_utils.iv7.server.backend import json_schemas


def get_server_name(client, token: str) -> str:
    """Функция ws метода video-server:GetServerName.
    Показывает информацию по всем камерам.

    Входные данные:
    :param client:                             - объект класса SoapClient для отправки и приема ws запросов;
    :param token:                              - токен авторизации;
                                                 то запрос осуществляется по всем камерам.
    :return: кортеж с параметрами метода, системными параметрами и именем метода.
    """

    params = {}
    sysparams = {
        "token": token,
        "session_id": "py_testing",
        "timeout": 50
    }

    response = client.call_method2('video-server:GetServerName', params, sysparams)

    try:
        validate(instance=response, schema=json_schemas.get_server_name)
    except ValidationError:
        raise AssertionError("Invalid json schema!")

    return response['result'][0]['server_name']


def reload_graph(client, token: str, setid: int) -> None:
    """Функция ws метода video-server:GetServerName.
    Показывает информацию по всем камерам.

    Входные данные:
    :param client:                             - объект класса SoapClient для отправки и приема ws запросов;
    :param token:                              - токен авторизации;
                                                 то запрос осуществляется по всем камерам.
    :return: кортеж с параметрами метода, системными параметрами и именем метода.
    """
    params = {
        "setid": setid
    }
    sysparams = {
        "token": token,
        "session_id": "py_testing",
        "timeout": 50
    }

    response = client.call_method2('video_server_info:reload_graph', params, sysparams)

    try:
        validate(instance=response, schema=json_schemas.reload_graph)
    except ValidationError:
        raise AssertionError("Invalid json schema!")

    return None

