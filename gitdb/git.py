# from dulwich.repo import Repo
from __future__ import unicode_literals
from dulwich.objects import Commit, Tree, Blob
import time
from dateutil.tz import tzlocal
import os
from functools import reduce, wraps

ENCODING = 'utf-8'

class GitData(object):
    def __init__(self, data, base_tree):
        self.data = {}
        for data_obj in data:
            self.data[data_obj.path] = Blob.from_string(data_obj.content.encode(ENCODING))
            path = list(os.path.split(data_obj.path))
            last_name = path.pop(-1)
            last_child = (0o100644, self.data[data_obj.path].id)
            while path:
                self.data.setdefault(os.path.join(*path), Tree()).add(last_name.encode(ENCODING), *last_child)
                last_child = (0o040000, self.data[os.path.join(*path)].id)
                last_name = path.pop(-1)
            base_tree.add(last_name.encode(ENCODING), *last_child)

    def items(self):
        for key in reversed(sorted(self.data)):
            yield self.data[key]


def path_hygiene(path):
    return [path_part for path_part in os.path.split(path) if path_part.strip()]


class GitRepo(object):
    def __init__(self, repo):
        self.repo = repo

    @property
    def current_commit(self):
        return self.__get_object__(self.repo.head()) if b'HEAD' in self.repo.refs else None

    @property
    def current_tree(self):
        return self.__get_object__(self.current_commit.tree) if self.current_commit else Tree()

    def commit(self, data, message, author):
        current_tree = self.current_tree
        for obj in GitData(data, current_tree).items():
            self.__add_object__(obj)

        self.__add_object__(current_tree)
        commit = self.__create_commit__(message, author)
        commit.tree = current_tree.id
        self.__add_object__(commit)
        self.repo.refs[b'HEAD'] = commit.id

    def get_object(self, path):
        path = path_hygiene(path)
        obj = self.current_tree
        for name in path:
            obj = self.__get_object__(obj[name.encode(ENCODING)][1])
        return obj.data.decode(ENCODING)

    def list(self, path):
        path = path_hygiene(path)
        obj = self.current_tree
        for name in path:
            obj = self.__get_object__(obj[name.encode(ENCODING)][1])

        for name in obj:
            yield self.__get_object__(obj[name][1]).data.decode(ENCODING)

    def __get_object__(self, sha1):
        return self.repo.get_object(sha1)

    def __add_object__(self, object):
        self.repo.object_store.add_object(object)
        return object

    def __add_trees__(self, trees):
        for tree in trees:
            self.__add_object__(tree)

    def __create_tree__(self, parent_list, child):
        tree = Tree()
        parent_list[-1].add(child.encode(ENCODING), 0o040000, tree.id)
        parent_list.append(tree)
        return parent_list

    def __create_commit__(self, message, author):
        commit = Commit()
        commit.author = commit.committer = author.encode(ENCODING)
        commit.author_time = commit.commit_time = int(time.time())
        commit.author_timezone = commit.commit_timezone = 0
        commit.message = message.encode(ENCODING)
        return commit

