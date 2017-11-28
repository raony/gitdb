try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


@patch('uuid.uuid4')
def test_adding_an_item_returns_an_UUID(uuid4):
    from gitdb.repo import Repo
    UUID = 'UUID'
    uuid4.return_value = UUID
    assert Repo().save('item', 'data') == UUID
