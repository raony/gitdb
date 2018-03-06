import uuid
import os
import yaml

class Data(object):
    def __init__(self, collection, id, content):
        self.collection = collection
        self.id = id
        self._content = content

    def __hash__(self):
        return hash(self.path + self.content)

    def __eq__(self, obj):
        return hash(self) == hash(obj)

    @property
    def path(self):
        return os.path.join(self.collection, self.id)

    @property
    def content(self):
        return self._content

class YmlData(Data):
    @property
    def content(self):
        return yaml.dump(self._content)


class LazyCollection(object):
    def __init__(self, git_repo, collection):
        self.git_repo = git_repo
        self.collection = collection

    def __iter__(self):
        for item in self.git_repo.list(self.collection):
            yield item

class Repo(object):
    data_class = Data

    def __init__(self, git_repo):
        self.git_repo = git_repo

    def save(self, collection, data, message, author):
        id = self._new_id()
        data = self.data_class(collection, id, data)
        return self._save(data, message, author)

    def list(self, collection):
        return LazyCollection(self.git_repo, collection)

    def get(self, collection, uuid):
        return self.git_repo.get_object(Data(collection, uuid, None).path)

    def _new_id(self):
        return uuid.uuid4()

    def _save(self, data, message, author):
        self.git_repo.commit([data], message, author)
        return data

class YmlRepo(Repo):
    data_class = YmlData


