from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_LINK = (By.CSS_SELECTOR, "#menu_login_btn")
    MENU_FORM = (By.CSS_SELECTOR, ".gears_icon")
    USER_FORM = (By.CSS_SELECTOR, "#user[url='/user_settings']")
    USER_NAME_LINK = (By.CSS_SELECTOR, ".icon-user_w + span")


class LoginPageLocators:
    LOGIN_FORM = (By.CSS_SELECTOR, ".form-1 .field [name='login']")
    PASSWORD_FORM = (By.CSS_SELECTOR, ".form-1 .field [name='passwd']")
    RECOVERY_FORM = (By.CSS_SELECTOR, '.form-1 .recovery')
    REG_BUTTON = (By.CSS_SELECTOR, ".enter button")


class TvPageLocator:
    END_USER_SESSION_LINK = (By.CSS_SELECTOR, ".exit .a-master-btn-text")
    USER_SETTINGS_LINK = (By.CSS_SELECTOR, ".settings .a-master-btn-text")
    SETTINGS_LINK = (By.CSS_SELECTOR, ".menu_item[href='/wizard']")
    SEARCH_CAMERAS_LINK = (By.CSS_SELECTOR, ".menu_item[href='/cameras_search']")
    CAMERAS_SETTINGS_LINK = (By.CSS_SELECTOR, ".menu_item[href='/cameras_settings']")
    EVENTS_LINK = (By.CSS_SELECTOR, ".menu_item[href='/events']")
    DISK_FORMAT_LINK = (By.CSS_SELECTOR, ".menu_item[href = '/disk_format']")
