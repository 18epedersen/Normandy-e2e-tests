"""By method."""
from selenium.webdriver.support import expected_conditions as EC
from pages.base import Base
from pages.duo_login import DuoLogin
from pages import locators


class LDAPLogin(Base):
    """Login class for demo LDAP account."""

    URL_TEMPLATE = "/control/recipe/"
    LOCATORS = locators.LDAPLogin

    def wait_for_page_to_load(self):
        """Wait for page load method for submit."""
        self.wait.until(EC.visibility_of_element_located(self.LOCATORS.submit))
        return self

    def login(self, username, password):
        """Return Duo class after logging in with demo LDAP."""
        self.find_element(*self.LOCATORS.username).send_keys(username)
        self.find_element(*self.LOCATORS.password).send_keys(password)
        self.find_element(*self.LOCATORS.submit).click()
        duo_page = DuoLogin(self.selenium, self.base_url)
        return duo_page.wait_for_page_to_load()

    def login_handler(self, conf, selenium, base_url):
        """Login handler."""
        username = conf.get('login', 'username')
        password = conf.get('login', 'password')
        self.open()
        return self.login(username, password)