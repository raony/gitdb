import uuid


class Data(object):
    def __init__(self, path, content):
        self.path = path
        self.content = content


class Repo(object):
    def save(self, collection, data):
        return uuid.uuid4()
