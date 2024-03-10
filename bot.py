import discord
import datetime as dt
from datetime import datetime
import pytz
import psycopg2
from discord.ext import commands
import time
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
DB_Port = os.getenv("dbconnection")

intents = discord.Intents.default()
intents.members = True 

client = commands.Bot(command_prefix='.', intents=intents)
tz_CR = pytz.timezone('America/Costa_Rica')
datetime_CR = datetime

def convert(seconds):
    if seconds < 60:
        return time.strftime("%S segundos", time.gmtime(seconds))
    elif seconds < 3600:
        return time.strftime("%M minutos, %S segundos", time.gmtime(seconds))
    elif seconds > 3600:
        return time.strftime("%H horas %M minutos y %S segundos", time.gmtime(seconds))



def manage_db(discordId, lasttimeconnected):
    time_connected = 0

    selectQuery = """SELECT * FROM times """
    
    insertQuery = """INSERT INTO times("discordid", lasttimeconnected, connected)
             VALUES(%d, %s, true) 
             """
    
    updateQuery = """UPDATE times
             SET lasttimeconnected = %s, connected = True 
             WHERE "discordid" = %s"""
    
    disconnectQuery = """UPDATE times
             SET lasttimeconnected = %s, seconds= seconds+%s, connected = False
             WHERE "discordid" = %s"""
             
    conn = None
    try:
        #params = dbconnect()
        #conn = psycopg2.connect(**params)
        conn = psycopg2.connect(DB_Port)
        cur = conn.cursor()
        cur.execute(selectQuery)
        tablecur = cur.fetchall()

        for i in range(len(tablecur) + 1):
            if i == len(tablecur):

                cur.execute(insertQuery, (discordId, lasttimeconnected))
                break
            elif discordId in tablecur[i] and tablecur[i][3] == True:
                time_connected = (datetime.now(tz_CR)-tablecur[i][2]).total_seconds()               
                cur.execute(disconnectQuery, (lasttimeconnected, time_connected, discordId))
                break    
            elif discordId in tablecur[i] and tablecur[i][3] == False:
                cur.execute(updateQuery, (lasttimeconnected, discordId))
                break

        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return time_connected

@client.event
async def on_ready():
    global logChannel
    logChannel = "paynor-bot"


@client.command()
async def logChannel(ctx, logs):
    global logChannel
    logChannel = discord.utils.get(ctx.guild.channels, name=logs)
    await ctx.send(logChannel)


@client.event 
async def on_voice_state_update(member, before, after):
    for channel in member.guild.channels:
        if str(channel) == str(logChannel):
            datetime_CR = datetime.now(tz_CR)
            if before.channel is None and after.channel is not None: 
                manage_db(member.name, datetime_CR)
                await channel.send(
                    f' :white_check_mark: {member.name} se unió al canal {after.channel.name} a las {datetime_CR.strftime("%I:%M %p")}')

            if after.channel is None and before.channel is not None: 
                time_connected = manage_db(member.name, datetime_CR)
                await channel.send(
                    f' :x: {member.name} salió del canal {before.channel.name} a las {datetime_CR.strftime("%I:%M %p")}, tiempo conectado: {convert(time_connected)}')


client.run(DISCORD_API_SECRET)