from test_utils.iv7.server.frontend.base_page import BasePage
from test_utils.iv7.server.frontend.locators import LoginPageLocators


class LoginPage(BasePage):

    def should_be_login_page(self, url_content):
        self.should_be_right_url(url_content)
        self.should_be_login_form()
        self.should_be_register_form()
        self.should_be_recovery_form()

    def should_be_login_form(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), 'Login form is not presented'

    def should_be_register_form(self):
        assert self.is_element_present(*LoginPageLocators.PASSWORD_FORM), 'Password form is not presented'

    def should_be_recovery_form(self):
        assert self.is_element_present(*LoginPageLocators.RECOVERY_FORM), 'Recovery form is not presented'

    def authorize_user(self, login, password):
        self.browser.find_element(*LoginPageLocators.LOGIN_FORM).send_keys(login)
        self.browser.find_element(*LoginPageLocators.PASSWORD_FORM).send_keys(password)
        self.browser.find_element(*LoginPageLocators.REG_BUTTON).click()
