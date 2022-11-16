from abc import ABC


class Client(ABC):
    def __init__(self, host: str, port):
        super().__init__()

        self._host = f"{host}:{port}"

    def get_host(self) -> str:
        return self._host


