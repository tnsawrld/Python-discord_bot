import discord
import os
import asyncio
import mysql.connector
import configparser
import logging
from itertools import cycle
from other.database import Database_Connect
from discord.ext import commands, tasks

#--------------------[BOT INTENTS]----------------------------
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app_debug.log"),
        logging.StreamHandler()
    ]
)

#--------------------[LOAD KEY]----------------------------
config = configparser.ConfigParser()
config.read("config.ini")
#token
TOKEN = config['main']['token']
DB_HOST = config['mysql']['host']
DB_NAME = config['mysql']['db_name']
#--------------------[MYSQL CONNECT]----------------------------
database_connetion = Database_Connect()
try:
    if database_connetion.is_connected():
        print(f"[MySQL] : Berhasil tersambung ke : {DB_HOST}, database : {DB_NAME}")
except mysql.connector.Error as e:
    print(f"[MySQL] : Gagal tersambung ke : {DB_HOST}, database : {DB_NAME}")
    print(f"Error : {e}")
#--------------------[ACTIVITY BOT]-----------------------------
bot_status = cycle(["Asistant for Sencillo Roleplay", "Made by TnsaWRLD", "i'm smart :p hehe"])
@tasks.loop(seconds=5)
async def change_status_bot():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

#--------------------[EVENT]-----------------------------
@bot.event
async def on_ready():
    print("[Load] : Server sedang meload\n")  
    print("[Load] : Berhasil") 
    change_status_bot.start()
    #change to slash command
    try:
        synced_commands = await bot.tree.sync()
        print(f"Ditemukan : {len(synced_commands)} commands!")
    except Exception as e:
        print("Error syncing aplication : ", e)

#testing slash
@bot.tree.command(name="tes", description="Testing slash commands bot")
async def tes(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hallo {interaction.user.name}!, ini hanya tes ya!")

#load all files in the /cogs folder
async def CodeLoad():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await CodeLoad()
        await bot.start(TOKEN)

asyncio.run(main())