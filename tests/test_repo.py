try:
    from unittest.mock import patch, MagicMock as Mock
except ImportError:
    from mock import patch, MagicMock as Mock

from gitdb.repo import Repo, Data, YmlRepo, YmlData


@patch('uuid.uuid4')
def test_adding_an_item_returns_an_UUID(uuid4):
    UUID = 'UUID'
    uuid4.return_value = UUID
    assert Repo(Mock()).save('item', 'data', 'message', 'author').id == UUID

@patch('uuid.uuid4')
def test_adding_an_item_commits_to_repo(uuid4):
    UUID = 'UUID'
    uuid4.return_value = UUID
    git_repo_mock = Mock()

    Repo(git_repo_mock).save('item', 'data', 'message', 'author')

    git_repo_mock.commit.assert_called_with([Data('item', UUID, 'data')], 'message', 'author')

def test_list_is_lazy():
    git_repo_mock = Mock()

    result = Repo(git_repo_mock).list('collection')

    git_repo_mock.list.assert_not_called()

    list(result)

    git_repo_mock.list.assert_called_with('collection')

def test_get():
    git_repo_mock = Mock()
    git_repo_mock.get_object.return_value = 'test data'

    assert Repo(git_repo_mock).get('collection', 'sample') == 'test data'

    git_repo_mock.get_object.assert_called_once_with('collection/sample')

@patch('uuid.uuid4')
def test_yml_repo(uuid4):
    UUID = 'UUID'
    uuid4.return_value = UUID
    git_repo_mock = Mock()

    YmlRepo(git_repo_mock).save('collection', {'test': 'data'}, 'message', 'author')

    git_repo_mock.commit.assert_called_once_with([YmlData('collection', UUID, {'test': 'data'})], 'message', 'author')

def test_yml_data():
    assert YmlData('collection', 'uuid', {'test': [1,2,3], 'nested': {'test': 'abc'}}).content == """test:
      - 1
      - 2
      - 3
    nested:
      test: abc"""
