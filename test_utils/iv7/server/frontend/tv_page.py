from test_utils.iv7.server.frontend.base_page import BasePage
from test_utils.iv7.server.frontend.locators import TvPageLocator


class TvPage(BasePage):

    def should_be_tv_page(self, url_content):
        self.should_be_right_url(url_content)
        self.should_end_user_session_link()
        self.should_be_user_settings_form()
        self.should_be_settings_form()

    def should_end_user_session_link(self):
        assert self.is_element_present(*TvPageLocator.END_USER_SESSION_LINK), 'No authorized user'

    def should_be_user_settings_form(self):
        assert self.is_element_present(*TvPageLocator.USER_SETTINGS_LINK), 'User settings form is not presented'

    def should_be_settings_form(self):
        assert self.is_element_present(*TvPageLocator.SETTINGS_LINK), 'Settings form is not presented'
