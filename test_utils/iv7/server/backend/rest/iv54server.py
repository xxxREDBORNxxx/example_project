import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from test_utils.iv7.server.backend import json_schemas

URL = 'api/v1/callmethod'
HEADERS = {
    "Content-Type": "application/json;charset=utf-8",
}


def list_cameras54(client, token: str,  key2: str,
                   id54: int = 0, source_type: str = 'video'):
    """Функция ws метода iv54server:ListCameras54.
    Показывает информацию по всем камерам.

    Входные данные:
    :param source_type:
    :param client:                             - объект класса SoapClient для отправки и приема ws запросов;
    :param token:                              - токен авторизации;
    :param id54: 0,                            - идентификатор камеры по протоколу 5.4 (можно не заполнять);
    :param key2: "Axis P1346 192.168.2.46"     - имя камеры;
                                               - если 'id54' = 0, 'key2' = "",
                                                 то запрос осуществляется по всем камерам.
    :return: кортеж с параметрами метода, системными параметрами и именем метода.
    """
    data = {
        "token": token,
        "method": 'iv54server:ListCameras54',
        "params": {
            "id54": id54,
            "key2": key2,
            "type": source_type
        }
    }

    payload = json.dumps(data)
    response = json.loads(client.post(URL, HEADERS, payload))

    try:
        validate(instance=response, schema=json_schemas.list_cameras54)
    except ValidationError:
        raise AssertionError("Invalid json schema!")

    return response[0]['result'][0]['cameras']
