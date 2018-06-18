#
# Config pytest
# Reference
# - https://pytest-django.readthedocs.io/en/latest/database.html#
#   std:fixture-django_db_setup
#
import pytest


@pytest.yield_fixture(scope='session')
def django_db_setup():
    """Just a no-op django_db_setup to attach an existing database"""
    pass
