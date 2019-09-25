from discord.utils import get
from discord import Game
from discord.ext.commands import Bot

with open("token.txt") as f:  # read token from file so I don't have to put the token up publicly
    token = f.read().rstrip()

client = Bot('notneeded')  # 'notneeded' is the bot command prefix, as this bot has no commands the prefix is notneeded
# and that is reflected in the name

lastMessage = 0  # start counting at 0, so the first message should be 1, could make this read the last message sent
# to the channel, that would enable restarting the bot while a count is going


def counter():  # count up by 1
    global lastMessage
    lastMessage += 1


def reset():  # reset the counter
    global lastMessage
    lastMessage = 0


@client.event
async def on_ready():  # set the "playing:" message and print when the bot is logged in and ready
    await client.change_presence(activity=Game(name="Teaching how to count"))
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if str(message.channel) == 'counting':  # check the message is in the right channel
        if message.content == (str(lastMessage + 1)):  # check the message is correct
            counter()  # increment the counter
        else:
            print("reset", message.content)  # print the message that reset the counter
            reset()  # reset the counter to 0
            member = message.author  # get the user who sent the message
            role = get(member.guild.roles, name="Failed")  # get the id of the role with the name "Failed"
            await member.add_roles(role)  # add the role to the user
            await message.add_reaction('\U0000274C')  # react with a X


client.run(token)  # start the bot
