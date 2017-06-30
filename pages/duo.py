"""Expected conditions."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.base import BasePage
from pages.home import HomePage
import pyotp
import pytest
import configparser


@pytest.fixture
def conf():
    """Read config.ini file."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def generate_QR_code(secret):
    """Return the QR code for 2FA."""
    totp = pyotp.TOTP(secret)
    return totp.now()


class DuoLoginPage(BasePage):
    """Duo authenication class."""

    def __init__(self, conf):
        """Create duo login page."""
        self.a0notloggedin_locator = conf.get('duo', 'a0notloggedin_locator')
        self.duoiframe_locator = conf.get('duo', 'duoiframe_locator')
        self.dropdown_locator = conf.get('duo', 'dropdown_locator')
        self.value = conf.get('duo', 'value')
        self.passcodebutton_locator = conf.get('duo', 'passcodebutton_locator')
        self.QRinput_locator = conf.get('duo', 'QRinput_locator')
        self.loginbutton_locator = conf.get('duo', 'loginbutton_locator')

    def wait_for_page_to_load(self):
        """Wait for page load method for a0-notloggedin class to load."""
        self.wait.until(EC.visibility_of_element_located(
          self.a0notloggedin_locator))
        return self

    def login_duo(self, secret):
        """Log into duo."""
        select = Select(self.find_element(*self.dropdown_locator))
        select.select_by_value(*self.value)
        self.find_element(*self.passcodebutton_locator).click()
        QR_code = generate_QR_code(secret)
        self.find_element(*self.QRinput_locator).send_keys(QR_code)
        self.find_element(*self.loginbutton_locator).click()
        return HomePage(self.selenium, self.base_url).wait_for_page_to_load()
