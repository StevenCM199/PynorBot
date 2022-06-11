import discord
from datetime import datetime
import pytz
import schedule as schedule
import xlsxwriter
from discord.ext import commands
import time

client = commands.Bot(command_prefix='.')
conectados = []  # lista de conectados
uptime = datetime


def convert(seconds):
    if seconds < 60:
        return time.strftime("%S segundos", time.gmtime(seconds))
    elif seconds < 3600:
        return time.strftime("%M minutos, %S segundos", time.gmtime(seconds))
    elif seconds > 3600:
        return time.strftime("%H horas %M minutos y %S segundos", time.gmtime(seconds))


@client.event
async def on_ready():
    global logChannel
    logChannel = "paynorbot"  # canal de logs


@client.command()
async def logChannel(ctx, logs):
    global logChannel
    logChannel = discord.utils.get(ctx.guild.channels, name=logs)
    await ctx.send(logChannel)


@client.event  # Detecta si alguien ha entrado a un canal
async def on_voice_state_update(member, before, after):
    for channel in member.guild.channels:

        if str(channel) == str(logChannel):
            tz_CR = pytz.timezone('America/Costa_Rica')
            datetime_CR = datetime.now(tz_CR)

            if before.channel is None and after.channel is not None:  # conectarse a voz
                conectados.append([member.name, datetime_CR])
                #print(conectados)
                await channel.send(
                    f' :white_check_mark: {member.name} se unió al canal {after.channel.name} a las {datetime_CR.strftime("%I:%M %p")}')

            if after.channel is None and before.channel is not None:  # desconectarse de voz
                for i in reversed(range(len(conectados))):
                    if conectados[i][0] == member.name:
                        uptime = datetime_CR - conectados[i][1]
                        seconds = uptime.total_seconds()
                        del conectados[i]
                #print(conectados)

                await channel.send(
                    f' :x: {member.name} salió del canal {before.channel.name} a las {datetime_CR.strftime("%I:%M %p")}')
                await channel.send(f' :alarm_clock: {member.name}: tiempo conectado {convert(seconds)}')
                uptime = None
                seconds = None


@client.command()
async def clearLists(ctx):
    conectados.clear()
    await ctx.send('=========Lista vaciada=========')


@client.command()
async def listaconectados(ctx):
    if conectados == []:
        await ctx.send("Lista vacia")
    else:
        for i in reversed(range(len(conectados))):
            await ctx.send(conectados[i])


#schedule.every().day.at("03:30:00").do(clearLists)
client.run('NzM3MjQ0MTQ0MDI3Njk3MTg1.Xx6iHQ.dNgQ-ivU51IMgmqljDTqZrU5J_Y')
