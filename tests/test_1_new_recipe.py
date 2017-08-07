import pytest
from pages.ldap_login import LDAPLogin


@pytest.mark.nondestructive
def test_new_recipe(conf, base_url, selenium, qr_code):
    """Test adding a recipe."""
    ldap_page = LDAPLogin(selenium, base_url)
    home_page = ldap_page.setup(conf, qr_code)
    recipes_listing_page = home_page.click_recipes()
    new_recipe_page = recipes_listing_page.click_new_recipe()
    assert new_recipe_page.heading_two == "Create New Recipe"
    assert new_recipe_page.find_element(
     *new_recipe_page.LOCATORS.save_button).is_displayed()