import json


class Cache:
    def cache(self, path, data):
        self.write(path, json.dumps(data))

    def load(self, path):
        data = self.read(path)
        return json.loads(data)

    def read(self, path):
        f = open(path, "r")
        data = f.read()
        f.close()
        return data

    def write(self, path, content):
        f = open(path, "w")
        f.write(content)
        f.close()
