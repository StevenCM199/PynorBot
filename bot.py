import discord
import os
import sys
from datetime import datetime
import pytz
import random
from discord.ext import commands

client = commands.Bot(command_prefix='.')

#txtChnl = client.get_channel(737234405348605996)

#@client.event
#async def on_ready():
#    print("estoy ready")
#    txtChnl = client.get_channel(737234405348605996)
#    await txtChnl.send("hola amiguito")

@client.event
async def on_disconnect():
    txtChnl = client.get_channel(741416524274729021)
    await txtChnl.send("adios amiguito")


@client.event
async def on_member_join(member):
    print(f'{member} ha entrado al server')

@client.event
async def on_member_remove(member):
    print(f'{member} ha salido del server')


@client.event #Detecta si alguien ha entrado a un canal
async def on_voice_state_update(member, before, after):
    tz_CR = pytz.timezone('America/Costa_Rica')
    datetime_CR = datetime.now(tz_CR)
    channel = client.get_channel(741416524274729021)

    if before.channel is None and after.channel is not None:
        await channel.send(f'{member} se ha unido al canal {after.channel.name} a las {datetime_CR.strftime("%H:%M:%S")}')
    if after.channel is None and before.channel is not None:
        await channel.send(f'{member} ha salido del canal {before.channel.name} a las {datetime_CR.strftime("%H:%M:%S")}')


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


#@client.command()
#async def load(ctx, extension):
#    client.load_extension(f'cogs.(extension)')

#@client.command()
#async def unload(ctx, extension):
#    client.unload_extension(f'cogs.(extension)')

#for filename in os.listdir('./cogs'):
#    if filename.endswith('.py'):
#        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def hoy(ctx):
    now = datetime.datetime.now()
    await ctx.send("Dia y Hora actuales:")
    await ctx.send(now.strftime("%Y-%m-%d %H:%M:%S"))


#@client.command()
#async def quit(ctx):
#    await ctx.send(f'me voy')
#    sys.exit()

client.run('NzM3MjQ0MTQ0MDI3Njk3MTg1.Xx6iHQ.dNgQ-ivU51IMgmqljDTqZrU5J_Y')
