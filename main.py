import discord
from random import choice
import time
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

recipients = ['748981885258170389', '769139609187123240', '633687383660953603']

last_dm = {}

last_message = None

def dateToString(date):

    minute = date.minute

    if len(str(date.minute)) == 1:
        minute = "0" + str(minute)

    return f'{date.day}/{date.month} {date.hour + 2}:{minute}'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await tree.sync(guild=discord.Object(id=1049253865112997888))

    aviv_venting_about_his_brothers = client.get_channel(1049386904065409054)
    global last_message
    async for message in aviv_venting_about_his_brothers.history(limit=1000):
        if message.author.id == 476686545034674176:
            last_message = message

            if last_message is None:
                print('no messages found')
            elif last_message.content == None:
                print('invalid message')
            else:
                print(f'found message {last_message.content}')
                break

@client.event
async def on_message(msg):
    # Ignore messages sent by the bot itself
    if msg.author == client.user:
        return

    if msg.author.id == 476686545034674176:
        if msg.channel.id == 1049386904065409054:
            global last_message
            last_message = msg
            for i in recipients:
                user = await client.fetch_user(i)
                if i not in last_dm or time.time() - last_dm[i] >= 600:
                    await user.send('aviv is venting about his brothers')
                    last_dm[i] = time.time()

@tree.command(name= 'last_vent', description= 'when did aviv last vent about his brothers', guild=discord.Object(id=1049253865112997888))
async def last_vent(interaction):
    global last_message
    msg_time = last_message.created_at

    await interaction.response.send_message(f'aviv last vented at {dateToString(msg_time)} <@{interaction.user.id}>')

client.run({token})
