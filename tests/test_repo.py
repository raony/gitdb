try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from gitdb.repo import Repo


@patch('uuid.uuid4')
def test_adding_an_item_returns_an_UUID(uuid4):
    UUID = 'UUID'
    uuid4.return_value = UUID
    assert Repo().save('item', 'data') == UUID
