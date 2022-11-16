import json
import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options_chrome
from selenium.webdriver.firefox.options import Options as Options_firefox

from test_utils.common.client.httpClient import HttpClient
from test_utils.common.client.soapClient import SoapClient

from test_utils.iv7.server.backend.sqlite import db
from test_utils.iv7.server.backend.soap import videoserver as videoserver_soap

from test_utils.iv7 import users

CONFIG_PATH = '/home/videosrv7/config_tests/night_build_config.json'
DEFAULT_WAIT_TIME = 10


def pytest_addoption(parser):
    parser.addoption('--language', action='store', default=None,
                     help="Choose correct language for site, default='ru'")
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--config', action='store', default="./config.json",
                     help="Config file path with all settings for tests")


@pytest.fixture(scope="session")
def browser(pytestconfig):
    browser_name = pytestconfig.getoption("browser_name")
    user_language = pytestconfig.getoption("language")

    if browser_name == "chrome":

        print("\nstart chrome browser for test..")

        options = Options_chrome()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        # Suppressing any console message either from the Selenium driver or from the browser itself,
        # including the first DevTools message listening to ws://127.0.0.1 at the very beginning.
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        browser = webdriver.Chrome(options=options)

    elif browser_name == "firefox":

        print("\nstart firefox browser for test..")

        options = Options_firefox()
        options.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(options=options)

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()


@pytest.fixture(scope='session')
def client_host(request, config):
    return config['client']['host']


@pytest.fixture(scope='session')
def client_login(request, config):
    return config['client']['login']


@pytest.fixture(scope='session')
def client_password(request, config):
    return config['client']['password']


@pytest.fixture(scope='session')
def client_rest_port(request, config):
    return config['client']['rest_port']


@pytest.fixture(scope="session")
def client_soapconn_with_token(request, client_host, client_soap_port, client_login, client_password):
    client_soapconn = SoapClient(client_host, client_soap_port)
    token = users.soap_login(client_soapconn, client_login, client_password, 'client')
    assert token
    return client_soapconn, token


@pytest.fixture(scope='session')
def client_soap_port(request, config):
    return config['client']['soap_port']


@pytest.fixture(scope='session')
def config(pytestconfig):
    with open(pytestconfig.getoption("config")) as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture(scope='session')
def db_conn(request, server_sqlite_path):
    def teardown():
        db.disconnect(db_conn)

    request.addfinalizer(teardown)
    db_conn = db.connect(server_sqlite_path)


@pytest.fixture(scope='session')
def server_host(request, config):
    return config['server']['host']


@pytest.fixture(scope='session')
def server_login(request, config):
    return config['server']['login']


@pytest.fixture(scope='session')
def server_password(request, config):
    return config['server']['password']


@pytest.fixture(scope="session")
def server_httpconn_with_token(request, server_host, server_rest_port, server_login, server_password):
    server_httpconn = HttpClient(server_host, server_rest_port)
    token = users.rest_login(server_httpconn, server_login, server_password, 'server')
    assert token
    return server_httpconn, token


@pytest.fixture(scope='session')
def server_soap_port(request, config):
    return config['server']['soap_port']


@pytest.fixture(scope='session')
def server_rest_port(request, config):
    return config['server']['rest_port']


@pytest.fixture(scope='session')
def server_sqlite_path(request, config):
    return config['server']['sqlite_path']


@pytest.fixture(scope="session")
def server_soapconn_with_token(request, server_host, server_soap_port, server_login, server_password):
    server_soapconn = SoapClient(server_host, server_soap_port)
    token = users.soap_login(server_soapconn, server_login, server_password, 'server')
    assert token
    return server_soapconn, token


@pytest.fixture(scope="session", params=[
    "D:\\config_tests\\web_cam_graf.json",
    # "./test_env/graphs/simple/samsung_s12312_212.json",
    # "./test_env/graphs/simple/rvi_i3131_153.json"
])
def simple_graph_key2(request, server_soapconn_with_token, db_conn):
    def teardown():
        setting.delete()

    server_soapconn, token = server_soapconn_with_token

    server_name = videoserver_soap.get_server_name(server_soapconn, token)
    setting, key2 = db.insert_graph_from_file(request.param, server_name, 'Quality')
    videoserver_soap.reload_graph(server_soapconn, token, setting.setid)

    request.addfinalizer(teardown)
    time.sleep(15)
    return key2
