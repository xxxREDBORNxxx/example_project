import time
import json

from zeep import Client as ZeepClient
from zeep.plugins import HistoryPlugin
from zeep.exceptions import TransportError, XMLSyntaxError

from requests.exceptions import ConnectionError
from .client import Client


class SoapClient(Client):
    """Класс для отправки/приема сообщений по протоколу SOAP

    """
    TIMEOUT: int = 5

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

        self.__history = HistoryPlugin()
        self.__url = f"http://{self._host}/axis2/services/Iv7Server/?wsdl"
        self.__client = self.__connect()

    def __repr__(self):
        return f"SoapClient({self._host})"

    def __connect(self) -> ZeepClient:
        CONNECTION_LIMIT_ATTEMPTS = 3
        WAIT_TIME = 5

        connection_attempt = 0
        while True:
            connection_attempt += 1
            try:
                return ZeepClient(self.__url, plugins=[self.__history])
            except ConnectionError:
                if connection_attempt == CONNECTION_LIMIT_ATTEMPTS:
                    raise AssertionError(f"Unable connect to {self.__url}")
                time.sleep(WAIT_TIME)
            except XMLSyntaxError:
                raise AssertionError(f"Invalid XML (SOAP): {self.__url}")

    def call_method2(self, method: str, params: dict, sysparams: dict) -> tuple:
        """Метод отправки сообщения и приема ответа по протоколу SOAP.

        :param method: имя ws методa
        :param params: параметры метода;
        :param sysparams: системные параметры;
        :return: словарь, полученный из json ответа.
        """
        try:
            sysparams['timeout'] = self.TIMEOUT
            start_time = time.time()
            response: str = self.__client.service.CallMethod2(
                method,
                json.dumps(params, ensure_ascii=False),
                json.dumps(sysparams))
            response_time = round((time.time() - start_time) * 1000)
            return json.loads(response), response_time

        except ConnectionError:
            raise AssertionError(f"Unable connect to {self.__url}")
        except TransportError as e:
            raise AssertionError(f"Status code is {e.status_code}")
        except json.JSONDecodeError:
            raise AssertionError(f"Invalid JSON: {self.__url}")
