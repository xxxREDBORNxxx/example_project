import pytest

from test_utils.iv7.client.desktop.rest import iv54client as iv54client_rest
from test_utils.iv7.client.desktop.soap import iv54client as iv54client_soap


@pytest.mark.critical
@pytest.mark.extended
class TestFps:
    @pytest.mark.skip(reason='skip without module ws.api.dll')
    def test_cam_fps_via_list_connection_54_rest(self, client_httpconn_with_token, simple_graph_key2):
        """Проверка fps подключенной камеры на клиенте методом iv54client:ListConnection
        через REST.

        :param client_httpconn_with_token: фикстура в виде кортежа с объектом HttpClient и токеном авторизации;
        :param simple_graph_key2: имя камеры на сервере с простым графом.
        """

        client_httpconn, token = client_httpconn_with_token
        cameras: list = iv54client_rest.list_connection(client_httpconn, token, simple_graph_key2)
        assert len(cameras) > 0, f"Нет подключенных камер с key2 {simple_graph_key2}"
        assert cameras[0]['key2'] == simple_graph_key2
        assert cameras[0]['fps'] > 0

    def test_cam_fps_via_list_connection_54_soap(self, client_soapconn_with_token, simple_graph_key2):
        """Проверка fps подключенной камеры на клиенте методом iv54client:ListConnection
        через SOAP.

        :param client_soapconn_with_token: фикстура в виде кортежа с объектом SoapClient и токеном авторизации;
        :param simple_graph_key2: имя камеры на сервере с простым графом.
        """

        client_soapconn, token = client_soapconn_with_token
        cameras: list = iv54client_soap.list_connection(client_soapconn, token, simple_graph_key2)
        assert len(cameras) > 0, f"Нет подключенных камер с key2 {simple_graph_key2}"
        assert cameras[0]['key2'] == simple_graph_key2
        assert cameras[0]['fps'] > 0
