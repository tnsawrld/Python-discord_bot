import discord
import mysql.connector
import random
import configparser
from other.database import Database_Connect
from discord.ext import commands
from discord import app_commands

config = configparser.ConfigParser()
config.read("./config.ini")
register_channel = config['channel']['register']

db_connect = Database_Connect()

def Check_Username(conection_db, username):
    cursor = conection_db.cursor()
    cursor.execute("SELECT COUNT(*) FROM lumibot WHERE BINARY username = %s", (username,))
    result = cursor.fetchone()
    return result[0] > 0  

class register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[File] : {__name__} berhasil dijalankan!")
    
    @app_commands.command(name="register", description="Register your discord!")
    async def register(self, interaction: discord.Interaction, name: str): 
        reg_ch = int(register_channel)
        await interaction.response.defer()
        if reg_ch != interaction.channel.id:
            await interaction.response.send_message(f"Perintah hanya bisa digunakan di <#{register_channel}> ")
            return
        try:
            cursor = db_connect.cursor()

            id_discord = interaction.user.id
            pquery = "SELECT * FROM lumibot WHERE id_discord = %s"
            cursor.execute(pquery, (id_discord,))
            row = cursor.fetchone()
            
            if Check_Username(db_connect, name):
                await interaction.followup.send(f"Nama {name} sudah pernah terdaftar dalam database!")
                return
            else:    
                if row is None:
                    rand = random.randint(100000, 999999)
                    query = "INSERT INTO lumibot (id_discord, username, kode) VALUES (%s, %s, %s)"
                    values = (id_discord, name, rand)
                    cursor.execute(query, values)
                    db_connect.commit()
                    await interaction.followup.send(f"Berhasil terdaftar `{name}` dengan discord id : `{id_discord}`")
                    await interaction.user.send(f"Kode verifikasi mu : `{rand}`")
                else:
                    await interaction.followup.send(f"Kamu sudah pernah mendaftarkan akun discord! `{row[2]}` id : {id_discord}")
        except mysql.connector.IntegrityError() as err:
            await interaction.response.send_message("Kamu sudah terdaftar, silahkan coba lagi nanti!")
            print(f"Error : {err}")

        except Exception as error:
            print(f"Error : {error}")
            await interaction.response.send_message("Kamu sudah terdaftar, silahkan coba lagi nanti!")
        finally:
            if 'database_connection' in locals() and db_connect.is_connected():
                cursor.close()
                db_connect.close()


async def setup(bot):
    await bot.add_cog(register(bot))