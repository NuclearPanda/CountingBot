from discord.utils import get
from discord import Game
from discord.ext.commands import Bot

try:
    with open("token.txt") as f:  # read token from file so I don't have to put the token up publicly
        token = f.read().rstrip()
except FileNotFoundError:
    print("Please add the token to the file token.txt in this directory")
    exit()

client = Bot('notneeded')  # 'notneeded' is the bot's command prefix (for example in !help "!" would be the command
# prefix), as this bot has no commands the prefix is not needed and that is reflected in the name

lastMessage = 0  # start counting at 0, so the first message should be 1, will get overwritten with the last message of
# the channel if it was numerical


def increment():  # count up by 1
    global lastMessage
    lastMessage += 1


def reset():  # reset the counter
    global lastMessage
    lastMessage = 0


def check_message(message):  # returns true if the message is correct for the current chain, false otherwise
    global lastMessage
    if message.isnumeric():
        if int(message) == lastMessage + 1:
            return True
    else:
        return False


async def get_last_message():  # returns the last message if it is a number, 0 otherwise
    for server in client.guilds:
        if server.name == "Bot testing":
            for channel in server.channels:
                if channel.name == "counting":
                    async for message in channel.history(limit=1):
                        if message.isnumeric():
                            last = int(message.content)
                        else:
                            member = message.author  # get the user who sent the message
                            role = get(member.guild.roles,
                                       name="Failed")  # get the id of the role with the name "Failed"
                            await member.add_roles(role)  # add the role to the user
                            await message.add_reaction('\U0000274C')  # react with a X
                            last = 0
    print("done", last)
    return last


@client.event
async def on_ready():  # set the "playing:" message and print when the bot is logged in and ready
    global lastMessage
    await client.change_presence(activity=Game(name="Teaching how to count"))
    lastMessage = await get_last_message()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if str(message.channel) == 'counting':  # check the message is in the right channel
        if check_message(message.content):  # check the message is correct
            increment()  # increment the counter
        else:
            print("reset", message.content)  # print the message that reset the counter
            reset()  # reset the counter to 0
            member = message.author  # get the user who sent the message
            role = get(member.guild.roles, name="Failed")  # get the id of the role with the name "Failed"
            await member.add_roles(role)  # add the role to the user
            await message.add_reaction('\U0000274C')  # react with an X
    await client.process_commands(message)


client.run(token)  # start the bot
