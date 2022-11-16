import pytest

from test_utils.iv7.server.frontend.login_page import LoginPage


@pytest.mark.critical_path
def test_authorization(browser, server_host, server_login, server_password):
    link = f"https://{server_host}/tv"
    page = LoginPage(browser, link)
    page.open()
    page.should_be_login_page(link)
    page.authorize_user(server_login, server_password)
    page.check_authorized_user(server_login)
