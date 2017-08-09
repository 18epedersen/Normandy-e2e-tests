from selenium.webdriver.support import expected_conditions as EC
from pages.base import Base
from pages import locators


class ExtensionsListing(Base):
    """Home Class for Normandy Control UI."""

    LOCATORS = locators.ExtensionsListing

    def wait_for_page_to_load(self):
        """Wait for visibility of rows on Normandy's home page to load."""
        self.wait.until(EC.visibility_of_all_elements_located(
            self.LOCATORS.tr))
        return self

    def click_new_extension(self):
        """Click add button to create recipe."""
        from pages.new_extension import NewExtension
        self.find_element(*self.LOCATORS.new_extensions_button).click()
        return NewExtension(self.selenium, self.base_url).wait_for_page_to_load()
