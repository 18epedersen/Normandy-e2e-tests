"""Expected conditions."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.base import Base
from pages.home import Home
from tests.conftest import generate_QR_code
from pages import locators


class DuoLogin(Base):
    """Duo authenication class."""

    LOCATORS = locators.DuoLogin

    def wait_for_page_to_load(self):
        """Wait for page load method for a0-notloggedin class to load."""
        self.wait.until(EC.visibility_of_element_located(
          self.LOCATORS.a0notloggedin))
        return self

    def login_duo(self, secret):
        """Log into duo."""
        QR_code = generate_QR_code(secret)
        self.selenium.switch_to_frame(
         self.find_element(*self.LOCATORS.duoiframe))
        dropdown_element = self.wait.until(EC.element_to_be_clickable(
          self.LOCATORS.dropdown))
        select = Select(dropdown_element)
        select.select_by_value(self.LOCATORS.value)
        self.find_element(*self.LOCATORS.passcodebutton).click()
        QR_code = generate_QR_code(secret)
        self.find_element(*self.LOCATORS.QRinput).send_keys(QR_code)
        self.find_element(*self.LOCATORS.loginbutton).click()
        self.selenium.switch_to_default_content()
        return Home(self.selenium, self.base_url, 60).wait_for_page_to_load()

    def login_duo_handler(self, conf, selenium, base_url):
        """Login duo handler."""
        secret = conf.get('login', 'secret')
        return self.login_duo(secret)