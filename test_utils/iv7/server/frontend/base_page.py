from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from test_utils.iv7.server.frontend.locators import BasePageLocators


class BasePage:
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.wait_time = timeout
        self.browser.implicitly_wait(self.wait_time)

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, how, what):
        """Method of catching an exception
        Checking the existence of an element"""
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        """Method for negative checks.
        Checking that the item does not appear during timeout.
        """
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def is_disappeared(self, how, what, timeout=4):
        """Method for negative checks.
        Checking that the item will disappear during the timeout.

        """
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).until_not(
                EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def log_off_go_to_login_page(self):
        """Method of logging out and going to the authorization page"""
        self.browser.find_element(*BasePageLocators.LOGIN_LINK).click()

    def should_click_registration_button(self):
        assert WebDriverWait(self.browser, self.wait_time).until(EC.element_to_be_clickable(
            BasePageLocators.LOGIN_LINK))

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"

    def check_authorized_user(self, user_login):
        """Method of checking the registered user"""
        assert self.browser.find_element(
            *BasePageLocators.USER_NAME_LINK).text == user_login, "User icon isn't presented, log or reg new user"

    def should_be_right_url(self, url_content):
        """Method of checking the current url"""
        assert url_content in self.browser.current_url, 'What the??? were am I?'
