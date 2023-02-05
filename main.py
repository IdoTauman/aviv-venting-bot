import discord
from random import choice
import time
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

insults = ['bad', 'stupid', 'dumb', 'who asked']

ariel_roasts = ['imagine paying for a free game', 'imagine spoiling an entire anime, also, imagine watching anime']

recipients = ['748981885258170389', '769139609187123240', '633687383660953603']

last_dm = {}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await tree.sync(guild=discord.Object(id=1049253865112997888))

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
            for i in recipients:
                user = await client.fetch_user(i)
                if i not in last_dm or time.time() - last_dm[i] >= 600:
                    await user.send('aviv is venting about his shitass brothers')
                    last_dm[i] = time.time()

@tree.command(name= 'roast_ariel', description= 'roast ariel', guild=discord.Object(id=1049253865112997888))
async def roast_ariel(interaction):
    await interaction.response.send_message(choice(ariel_roasts))

client.run({token})
