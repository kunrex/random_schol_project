import discord

class ChatCommands:
    dataBase = None
    writeLocation = None
    readWriteService = None

    def __init__(self, data, location, readWrite):
        self.dataBase = data
        self.writeLocation = location
        self.readWriteService = readWrite

    async def registerChannel(self, channelId, serverId):
        if serverId in self.dataBase:
            return "a channel is already registered for you server"
        else:
            self.dataBase[serverId] = channelId
            self.readWriteService.writeCustom(self.writeLocation, self.dataBase)
            return 'registered channel ;)'

    async def changeChannel(self, channelId, serverId):
        if not (serverId in self.dataBase):
            return "a channel is not registered for your server"
        else:
            self.dataBase[serverId] = channelId
            self.readWriteService.writeCustom(self.writeLocation, self.dataBase)
            return 'changed resgitered channel :D'
    
    async def removeChannel(self, serverId):
        if not (serverId in self.dataBase):
            return "a channel is not registered for your server"
        else:
            del self.dataBase[serverId]
            self.readWriteService.writeCustom(self.writeLocation, self.dataBase)
            return 'removed resgitered channel :('

    commands = ['register', 'change',  'remove']
    async def tryMatch(self, content):
        commandArgs = [s.strip() for s in content.split(' ')]
        if len(commandArgs) == 1:
            return (False, "were you trying to tell me something? try using a command sugar plum ;)")

        command = commandArgs[1]
        if command not in self.commands:
            return (False, 'that command was not found... you okay buddy?')
        
        return (True, commandArgs)

    async def channelManagement(self, commandArgs, guild):
        command = commandArgs[1]
        serverId = str(guild.id)
        if command == 'remove':
            print('hi')
            return await self.removeChannel(serverId)
        else:
            if len(commandArgs) < 3 or type(commandArgs[2]) is not str:
                return "invalid command usage. Usage: <prefix> <command name> <channel name/id>"

            channel = discord.utils.get(guild.channels, name = commandArgs[2])
            if channel == None:
                return "the channel you gave me doesn't really exist"
            if command == 'register':
                return await self.registerChannel(channel.id, serverId)
            else:
                return await self.changeChannel(channel.id, serverId)
