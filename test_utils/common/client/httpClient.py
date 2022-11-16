import requests

from requests.exceptions import ConnectionError
from .client import Client


class HttpClient(Client):
    """Класс для отправки/приема сообщений по протоколу HTTP.

    """
    PROTOCOL = "http"

    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

        self.__session = requests.Session()
        self.__default_headers = {
            "Host": self._host,
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Origin": f"{self.PROTOCOL}://{self._host}",
        }

    def __repr__(self):
        return f"HttpClient({self._host})"

    def post(self, url: str, extra_headers: dict, body: str) -> str:
        return self.__execute_request(url, "POST", extra_headers, body)

    def get(self, url: str, extra_headers: dict) -> str:
        return self.__execute_request(url, "GET", extra_headers)

    def delete(self, url: str, extra_headers: dict) -> str:
        return self.__execute_request(url, "DELETE", extra_headers)

    def get_cookie(self):
        return requests.utils.dict_from_cookiejar(self.__session.cookies)

    def clear_cookie(self):
        self.__session.cookies.clear()

    def __execute_request(self, url: str, method: str, extra_headers: dict, body: str = None) -> str:
        # раскомментировать для протокола https
        # disable InsecureRequestWarning
        # logging.captureWarnings(True)
        def __prepare_headers() -> dict:
            headers = dict(self.__default_headers)
            headers.update(extra_headers)
            return headers

        request_headers = __prepare_headers()
        try:
            return self.__try_to_execute_request(url, method, request_headers, body)
        except ConnectionError:
            raise AssertionError(f"Unable connect to {self._host}/{url}")

    def __try_to_execute_request(self, url: str, method: str, headers: dict, body: str = None) -> str:
        full_url = f"{self.PROTOCOL}://{self._host}/{url}"
        method_func = {
            "GET": self.__session.get,
            "POST": self.__session.post,
            "DELETE": self.__session.delete
        }

        response = method_func[method](full_url,
                                       headers=headers,
                                       data=body,
                                       allow_redirects=False,
                                       verify=False)
        if response.status_code != 200:
            raise AssertionError(f"Error while sending {method} {url}: response code {response.status_code}")

        return response.text
