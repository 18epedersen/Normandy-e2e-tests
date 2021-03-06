"""Expected conditions method for selenium webdriver."""
from selenium.webdriver.support import expected_conditions as EC
from pages.base import Base
from pages import locators


class Home(Base):
    """Home Class for Normandy Control UI."""

    LOCATORS = locators.Home

    def wait_for_page_to_load(self):
        """Wait for visibility of rows on Normandy's home page to load."""
        self.wait.until(EC.visibility_of_all_elements_located(
         self.LOCATORS.tr))
        return self

    def click_add_recipe(self):
        """Click add button to create recipe."""
        from pages.recipe import Recipe
        self.find_element(*self.LOCATORS.add_button).click()
        return Recipe(self.selenium, self.base_url).wait_for_page_to_load()

    def create_approved_recipe(self, conf):
        """Create and approve recipe."""
        """Return recipe page object, and notications."""
        recipe_page = self.click_add_recipe()
        recipe_page, recipe_name, messages_list = recipe_page.save_recipe(conf)
        recipe_page, messages_list = recipe_page.approve_new_recipe(conf)
        return recipe_page, messages_list

    def create_approved_and_enabled_recipe(self, conf):
        """Create, approve, and enable recipe."""
        """Return recipe page object, recipe name, and notications."""
        recipe_page = self.click_add_recipe()
        recipe_page, recipe_name, messages_list = recipe_page.save_recipe(conf)
        recipe_page, messages_list = recipe_page.approve_new_recipe(conf)
        recipe_page, messages_list = recipe_page.enable_recipe()
        return recipe_page, recipe_name, messages_list

    def find_recipe_in_table(self, recipe_name):
        """Find recipe name in home page recipe table."""
        """Return boolean, recipe page object, and the text of recipe's row."""
        from pages.recipe import Recipe
        recipe_page = None
        row_content = []
        rows = self.wait.until(EC.visibility_of_all_elements_located(
         self.LOCATORS.tr))
        found = False
        for row in rows:
            cols = row.find_elements(*self.LOCATORS.td)
            for col in cols:
                if col.text == recipe_name:
                    found = True
                    row_content = self.get_row_content(row)
                    col.click()
                    recipe_page = Recipe(self.selenium,
                                         self.base_url).wait_for_save_draft_button() # noqa
                    break
            if found:
                break
        return found, recipe_page, row_content

    def get_row_content(self, row):
        """Get the text of the selected recipe."""
        row_content_texts = []
        cols = row.find_elements(*self.LOCATORS.td)
        for col in cols:
            row_content_texts.append(col.text)
        return row_content_texts
