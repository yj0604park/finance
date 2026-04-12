"""
Root conftest.py for the finance project.

Adds SQLite compatibility for PostgreSQL-specific features used in models
(e.g., db_collation="C" on Account.name), so tests can run without a
PostgreSQL instance.
"""

import pytest
from django.db.backends.signals import connection_created


def register_c_collation(sender, connection, **kwargs):
    """Register the 'C' collation in SQLite to match PostgreSQL binary sort order.

    PostgreSQL's C locale compares strings byte-by-byte, which is equivalent
    to Python's default lexicographic comparison.
    """
    if connection.vendor == "sqlite":
        connection.connection.create_collation(
            "C",
            lambda x, y: (x > y) - (x < y),
        )


connection_created.connect(register_c_collation)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db):
    from finance.users.tests.factories import UserFactory

    return UserFactory()
