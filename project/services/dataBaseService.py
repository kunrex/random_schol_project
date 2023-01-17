class DataBaseService:
    dataBase = None
    writeLocation = None
    readWriteService = None

    def __init__(self, location, readWrite):
        self.writeLocation = location
        self.readWriteService = readWrite

        self.dataBase = self.readWriteService.customOpen(location)

    def find(self, serverId):
        return serverId in self.dataBase
    
    def result(self, serverId, channelId):
        return self.dataBase[serverId] == channelId

    def change(self, serverId, channelId):
        self.dataBase[serverId] = channelId
        self.readWriteService.writeCustom(self.writeLocation, self.dataBase)
    
    def remove(self, serverId):
        del self.dataBase[serverId]
        self.readWriteService.writeCustom(self.writeLocation, self.dataBase)