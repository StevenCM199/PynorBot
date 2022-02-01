import discord
from datetime import datetime
import pytz
from discord.ext import commands
import time

client = commands.Bot(command_prefix='.')
conectados = [] #lista de conectados
dc_time = []
uptime = datetime

def convert(seconds):
    if seconds < 60:
        return time.strftime("%S segundos", time.gmtime(seconds))
    elif seconds < 3600:
        return time.strftime("%M minutos, %S segundos", time.gmtime(seconds))
    elif seconds > 3600:
        return time.strftime("%H Horas %M minutos y %S segundos", time.gmtime(seconds))

@client.event
async def on_ready():
    global logChannel
    logChannel = "paynorbot" #canal de logs

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
                print(conectados)
                await channel.send(
                    f' :white_check_mark: {member.name} se unió al canal {after.channel.name} a las {datetime_CR.strftime("%I:%M %p")}')

            if after.channel is None and before.channel is not None:  # desconectarse de voz
                dc_time.append([member.name, datetime_CR])
                print(dc_time)
                for i in reversed(range(len(conectados))):
                    if conectados[i][0] == member.name and dc_time[i][0] == member.name:
                        uptime = dc_time[i][1] - conectados[i][1]
                        seconds = uptime.total_seconds()
                        del conectados[i]
                        del dc_time[i]
                print(conectados)
                print(dc_time)

                await channel.send(
                    f' :x: {member.name} salió del canal {before.channel.name} a las {datetime_CR.strftime("%I:%M %p")}')
                await channel.send(f' :alarm_clock: {member.name}: tiempo conectado {convert(seconds)}')
                uptime = None
                seconds = None



client.run('NzM3MjQ0MTQ0MDI3Njk3MTg1.Xx6iHQ.dNgQ-ivU51IMgmqljDTqZrU5J_Y')
