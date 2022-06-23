import discord
from datetime import datetime
import pytz
import psycopg2
from config import config
from discord.ext import commands
import time

intents = discord.Intents.default() # or .all() if you ticked all, that is easier
intents.members = True # If you ticked the SERVER MEMBERS INTENT

client = commands.Bot(command_prefix='.', intents=intents)
conectados = []  # lista de conectados
uptime = datetime
tz_CR = pytz.timezone('America/Costa_Rica')
datetime_CR = datetime


def convert(seconds):
    if seconds < 60:
        return time.strftime("%S segundos", time.gmtime(seconds))
    elif seconds < 3600:
        return time.strftime("%M minutos, %S segundos", time.gmtime(seconds))
    elif seconds > 3600:
        return time.strftime("%H horas %M minutos y %S segundos", time.gmtime(seconds))


def insert_ez(discordId, hours, lasttimeconnected):
    # INSERTA O ACTUALIZA UNA ENTRADA EN LA BASE DE DATOS
    selectQuery = """SELECT * FROM public.times_test
                ORDER BY discordid ASC """
    insertQuery = """INSERT INTO TIMES_TEST(discordID, hours, lasttimeconnected)
             VALUES(%s, %s, %s) """
    updateQuery = """UPDATE TIMES_TEST
             SET hours = hours+%s, lasttimeconnected = %s 
             WHERE discordID = %s"""
    conn = None
    try:
        # LEER LOS PARAMETROS Y CONECTAR
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(selectQuery)
        tablecur = cur.fetchall()

        # RECORRER LOS IDS EN LA BASE DE DATOS
        for i in range(len(tablecur) + 1):
            if i == len(tablecur):
                # print("No se encontro el valor en la lista, insertando nuevo valor")
                cur.execute(insertQuery, (discordId, hours, lasttimeconnected))
            elif discordId in tablecur[i]:
                # print("ID detectado, actualizando entrada y saltando el codigo")
                cur.execute(updateQuery, (hours, lasttimeconnected, discordId))
                break
            # else:
            # print("ID no detectado, recorriendo lista...")

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return discordId, hours, lasttimeconnected


async def insertarConectados(member, date):
    conectados.append([member, date])


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

            datetime_CR = datetime.now(tz_CR)
            if before.channel is None and after.channel is not None:  # conectarse a voz
                try:
                    await insertarConectados(member.name, datetime_CR)
                except:
                    await channel.send(f':sob::sob::sob::sob::sob::sob::sob:Hubo un problema registrando a {member.name} :sob::sob::sob::sob::sob::sob::sob::sob:')

                await channel.send(
                    f' :white_check_mark: {member.name} se unió al canal {after.channel.name} a las {datetime_CR.strftime("%I:%M %p")}')

            if after.channel is None and before.channel is not None:  # desconectarse de voz
                for i in reversed(range(len(conectados))):
                    if conectados[i][0] == member.name:
                        uptime = datetime_CR - conectados[i][1]
                        seconds = uptime.total_seconds()
                        insert_ez(member.name, (seconds / 3600), datetime_CR)
                        del conectados[i]
                try:
                    await channel.send(
                        f' :x: {member.name} salió del canal {before.channel.name} a las {datetime_CR.strftime("%I:%M %p")}, tiempo conectado: {convert(seconds)}')

                except UnboundLocalError:
                    await channel.send(f':sob: No sé a que hora se conectó {member.name}, ignorando...')
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


# schedule.every().day.at("03:30:00").do(clearLists)
client.run('NzM3MjQ0MTQ0MDI3Njk3MTg1.GqOySh.6gCZf5sULGWnGtonXgBg5godJi8mHNVXWE91Og')
