import discord
from random import choice
import time
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

insults = ['bad', 'stupid', 'dumb', 'who asked', 'a 3 year old', 'an anime kid', 'fat']

ariel_roasts = ['imagine paying for a free game', 'imagine spoiling an entire anime, also, imagine watching anime', 'imagine fighting over ronbleks', 'imagine playing ronbleks when ur over 3']

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

    aviv_venting_about_his_shitass_brothers = client.get_channel(1049386904065409054)
    global last_message
    async for message in aviv_venting_about_his_shitass_brothers.history(limit=1000):
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

    if msg.author.id == 633687383660953603:
        message = f'pimed is {choice(insults)}'
        if message == 'pimed is who asked':
            await msg.channel.send('who asked')
        else:
            await msg.channel.send(message)

    if msg.author.id == 476686545034674176:
        if msg.channel.id == 1049386904065409054:
            global last_message
            last_message = msg
            for i in recipients:
                user = await client.fetch_user(i)
                if i not in last_dm or time.time() - last_dm[i] >= 600:
                    await user.send('aviv is venting about his shitass brothers')
                    last_dm[i] = time.time()

@tree.command(name= 'roast_ariel', description= 'roast ariel', guild=discord.Object(id=1049253865112997888))
async def roast_ariel(interaction):
    log_channel = client.get_channel(1072481763454091314)
    await interaction.response.send_message(f'{choice(ariel_roasts)} <@769139609187123240>')
    await log_channel.send(interaction.user.name)

@tree.command(name= 'last_vent', description= 'when did aviv last vent about his brothers', guild=discord.Object(id=1049253865112997888))
async def last_vent(interaction):
    global last_message
    msg_time = last_message.created_at

    await interaction.response.send_message(f'aviv last vented at {dateToString(msg_time)} <@{interaction.user.id}>')

@tree.command(name= 'ariel_roasting_leaderboard', description= 'show the people that roasted ariel the most', guild=discord.Object(id=1049253865112997888))
async def leaderboard(interaction):
    log_channel = client.get_channel(1072481763454091314)
    log_history = log_channel.history(limit=1000)
    log_list = []
    async for m in log_history:
        log_list.append(m.content)
    log_authors = set(log_list)
    leaderboard_list = []
    for author in log_authors:
        leaderboard_list.append(f'{author}: {log_list.count(author)}')
    await interaction.response.send_message('\n'.join(leaderboard_list))

client.run({token})
