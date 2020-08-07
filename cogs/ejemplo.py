import discord
from discord.ext import commands

class Ejemplo(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Eventos
    @commands.Cog.listener()
    async def on_ready(self):
        print('estoy ready')

    #Comandos
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


def setup(client):
    client.add_cog(Ejemplo(client))