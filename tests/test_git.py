try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from dulwich.repo import MemoryRepo
from dulwich.objects import Tree, Blob
from gitdb.repo import Data
from gitdb.git import GitRepo


def test_current_commit_is_none_if_repo_is_empty():
    assert GitRepo(MemoryRepo()).current_commit is None


def test_current_commit_is_HEAD_ref_in_repo():
    repo = MemoryRepo()
    tree = Tree()
    repo.do_commit(tree = tree.id, message = b'first commit')
    commit = repo.do_commit(tree = tree.id, message = b'second commit')

    assert GitRepo(repo).current_commit.id == commit


def test_current_tree_should_be_new_if_repo_is_empty():
    tree = GitRepo(MemoryRepo()).current_tree
    assert tree is not None
    assert list(tree) == []

def test_current_tree_should_be_from_current_commit():
    repo = MemoryRepo()
    tree = Tree()
    repo.object_store.add_object(tree)
    repo.do_commit(tree = tree.id, message = b'first commit')
    tree.add(b'test', 0o100644, Blob().id)
    repo.object_store.add_object(tree)
    repo.do_commit(tree = tree.id, message = b'second commit')

    assert GitRepo(repo).current_tree.id == tree.id


def test_commit_new_data():
    data = Data('sample/data.yml', 'test content')
    data2 = Data('sample2/data2.yml', 'test content2')
    data3 = Data('sample2/data3.yml', 'test content3')
    message = 'commit message'
    author = 'commit author'
    repo = MemoryRepo()

    git_repo = GitRepo(repo)
    git_repo.commit([data, data2, data3], message, author)

    assert sorted(list(git_repo.current_tree)) == [b'sample', b'sample2']
    assert git_repo.current_commit.message == message.encode('utf8')
    assert git_repo.current_commit.author.startswith(author.encode('utf8'))
    assert repo.get_object(repo.get_object(git_repo.current_tree[b'sample'][1])[b'data.yml'][1]).data == b'test content'
    assert repo.get_object(repo.get_object(git_repo.current_tree[b'sample2'][1])[b'data2.yml'][1]).data == b'test content2'
    assert repo.get_object(repo.get_object(git_repo.current_tree[b'sample2'][1])[b'data3.yml'][1]).data == b'test content3'


def test_get_object():
    data = Data('sample/data.yml', 'test content')
    data2 = Data('sample2/data2.yml', 'test content2')
    data3 = Data('sample2/data3.yml', 'test content3')
    message = 'commit message'
    author = 'commit author'
    repo = MemoryRepo()

    git_repo = GitRepo(repo)
    git_repo.commit([data, data2, data3], message, author)

    assert git_repo.get_object('sample/data.yml') == 'test content'
