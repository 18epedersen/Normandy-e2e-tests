"""Pytest."""
import pytest
from pages.ldap_login import LDAPLogin
from tests.conftest import find_recipe_rest_api
from tests.conftest import create_recipe


@pytest.mark.nondestructive
def test_delete_recipe(conf, base_url, selenium):
    """Confirm recipe deleted on home page."""
    LDAP = LDAPLogin(selenium, base_url)
    duo_page = LDAP.login_handler(conf, selenium, base_url)
    home_page = duo_page.login_duo_handler(conf, selenium, base_url)
    recipe_page = create_recipe(conf, home_page, False)
    found_sucess, recipe_page = home_page.find_recipe_in_table(conf)
    home_page = recipe_page.delete_recipe()
    text = home_page.confirm_deleted_recipe()
    found_failure, recipe_page = home_page.find_recipe_in_table(conf)
    assert found_sucess
    assert text == 'Recipe deleted.'
    assert not found_failure


@pytest.mark.nondestructive
def test_deleted_recipe_at_rest_api(conf):
    """Testing that the deleted recipe is not at the rest api endpoint."""
    found = find_recipe_rest_api(conf)
    assert not found