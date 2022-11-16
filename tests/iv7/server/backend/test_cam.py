import pytest

from test_utils.iv7.server.backend.rest import iv54server as iv54server_rest
from test_utils.iv7.server.backend.soap import iv54server as iv54server_soap


@pytest.mark.critical
@pytest.mark.extended
class TestFps:

    def test_inserted_cam_fps_via_list_cameras_54_soap(self, server_soapconn_with_token, simple_graph_key2: str):
        """Проверка fps созданной напрямую в базе камеры на сервере методом iv54server:ListCameras54
        через SOAP.

        :param server_soapconn_with_token: фикстура в виде кортежа с объектом SoapClient и токеном авторизации;
        :param simple_graph_key2: имя камеры на сервере с простым графом.
        """
        server_soapconn, token = server_soapconn_with_token
        cameras = iv54server_soap.list_cameras54(server_soapconn, token, simple_graph_key2)

        assert len(cameras) > 0, f"Нет подключенных камер с key2 {simple_graph_key2}"
        assert cameras[0]['key2'] == simple_graph_key2
        assert cameras[0]['FPS_2sec'] > 0

    @pytest.mark.skip(reason='skip without module ws.api.dll')
    def test_cam_fps_via_list_cameras_54_rest(self, server_httpconn_with_token, simple_graph_key2):
        """Проверка fps подключенной камеры на сервере методом iv54server:ListCameras54
        через REST.

        :param server_httpconn_with_token: фикстура в виде кортежа с объектом HttpClient и токеном авторизации;
        :param simple_graph_key2: имя камеры на сервере с простым графом.
        """
        server_httpconn, token = server_httpconn_with_token
        cameras: list = iv54server_rest.list_cameras54(server_httpconn, token, simple_graph_key2)

        assert len(cameras) > 0, f"Нет подключенных камер с key2 {simple_graph_key2}"
        assert cameras[0]['key2'] == simple_graph_key2
        assert cameras[0]['FPS_2sec'] > 0
