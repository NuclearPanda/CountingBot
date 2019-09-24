from discord.utils import get
from discord import Game
from discord.ext.commands import Bot

with open("token.txt") as f:
    token = f.read().rstrip()

client = Bot('notneeded')

lastMessage = 0


def counter():
    global lastMessage
    lastMessage += 1


def reset():
    global lastMessage
    lastMessage = 0


@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="Teaching how to count"))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if str(message.channel) == 'counting':
        if message.content.startswith(str(lastMessage + 1)):
            counter()
            return
        else:
            print("reset")
            reset()
            member = message.author
            role = get(member.guild.roles, name="Failed")
            await member.add_roles(role)
            await message.add_reaction('\U0000274C')





client.run(token)
