import json


def rest_login(httpconn, login_: str, password: str, login_system: str) -> str:
    """Функция выполнения ws метода users:client_exec с cmd login.

    :param httpconn: объект класса SoapClient;
    :param login_: логин пользователя;
    :param password: пароль пользователя;
    :param login_system: server или client
    :return: токен авторизации/соединения.
    """
    URL = 'api/v1/callmethod'
    HEADERS = {
        "Content-Type": "application/json;charset=utf-8",
    }

    login_system_methods = {
        "server": "users:server_exec",
        "client": "users:client_exec",
    }

    data = {
        "login": login_,
        "password": password,
        "method": login_system_methods[login_system],
        "params": {
            "cmd": "login",
            "params": {
                "login": login_,
                "password": password}
        }}
    payload = json.dumps(data)
    response = json.loads(httpconn.post(URL, HEADERS, payload))

    try:
        return response["result"][0]["data"]["token"]
    except KeyError:
        raise AssertionError("Expected json structure is incorrect!")


def soap_login(soapconn, login_: str, password: str, login_system: str) -> str:
    """Функция выполнения ws метода users:client_exec с cmd login.

    :param soapconn: объект класса SoapClient;
    :param login_: логин пользователя;
    :param password: пароль пользователя;
    :param login_system: server или client
    :return: токен авторизации/соединения.
    """

    login_system_methods = {
        "server": "users:server_exec",
        "client": "users:client_exec",
    }
    params = {
        "cmd": "login",
        "params": {
            "login": login_,
            "password": password}
    }
    sysparams = {
        "login": login_,
        "password": password,
        "session_id": "py_testing",
        "timeout": 50
    }

    response = soapconn.call_method2(login_system_methods[login_system], params, sysparams)

    try:
        return response[0]["result"][0]["data"]["token"]
    except KeyError:
        raise AssertionError("Expected json structure is incorrect!")
