import json

class ReadWriteService:
    def customOpen(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def writeCustom(self, path, toWrite):
        with open(path, 'w') as file:
            json.dump(toWrite, file)
