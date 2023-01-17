import discord

from chatCommands import ChatCommands
from services.chatBotService import ChatBot
from services.readWriteService import ReadWriteService

readWrite = ReadWriteService()
config = readWrite.customOpen('file location')

def writeCustom(toWrite):
    readWrite.writeCustom(config["dataBasePath"], toWrite)

dataBase = readWrite.customOpen(config["dataBasePath"])
chatBot = ChatBot(config["GoogleCreedentialsVariable"], config["GoogleCredentialsPath"], config["projectId"], "123456789")

def matchPrefix(content):
    result = content.partition(config["prefix"])
    return [result[1] != '', result[2]]

chatCommands = ChatCommands(dataBase, config["dataBasePath"], readWrite)
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author.id == config["botId"]:
            return

        result = matchPrefix(message.content)
        if result[0]:
            result = await chatCommands.tryMatch(result[1])

            if result[0]:
                await message.channel.send(await chatCommands.channelManagement(result[1], message.guild))
            else:
                await message.channel.send(result[1])
        else:
            guildId = str(message.guild.id)
            if guildId in dataBase and message.channel.id == dataBase[guildId]:
                await message.reply(await chatBot.response(message.content), mention_author = False)
            
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(config["id"])
