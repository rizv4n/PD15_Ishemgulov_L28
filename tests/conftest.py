from pytest_factoryboy import register

from tests.factories import AdFactory, SelectionFactory, CategoryFactory, UserFactory

pytest_plugins = "tests.fixtures"

register(AdFactory)
register(SelectionFactory)
register(CategoryFactory)
register(UserFactory)
