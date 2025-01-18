import discord
from discord.ext import commands, tasks
import os
import asyncio
from itertools import cycle

#--------------------[BOT INTENTS]-----------------------------
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)

#--------------------[ACTIVITY BOT]-----------------------------
bot_status = cycle(["Asistant for Sencillo Roleplay", "Made by TnsaWRLD", "i'm smart :p hehe"])
@tasks.loop(seconds=5)
async def change_status_bot():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

#--------------------[MAIN]-----------------------------
@bot.event
async def on_ready():
    print("[Load] : Server sedang meload\n")  
    print("[Load] : Berhasil") 
    change_status_bot.start()   

#just token
with open("topsecret.txt") as file:
    TOKEN = file.read()

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