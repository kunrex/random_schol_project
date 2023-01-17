import discord

class ChatCommands:
    dataBaseService = None

    def __init__(self, dataBase):
        self.dataBaseService = dataBase

    async def registerChannel(self, channelId, serverId):
        if self.dataBaseService.find(serverId):
            return "a channel is already registered for you server"
        else:
            self.dataBaseService.change(serverId, channelId)
            return 'registered channel ;)'

    async def changeChannel(self, channelId, serverId):
        if not self.dataBaseService.find(serverId):
            return "a channel is not registered for your server"
        else:
            self.dataBaseService.change(serverId, channelId)
            return 'changed resgitered channel :D'
    
    async def removeChannel(self, serverId):
        if not self.dataBaseService.find(serverId):
            return "a channel is not registered for your server"
        else:
            self.dataBaseService.remove(serverId)
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
