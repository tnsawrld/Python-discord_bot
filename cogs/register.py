import discord
import mysql.connector
import random
import configparser
from other.database import Database_Connect
from discord.ext import commands
from discord import app_commands
from other.utils import *

config = configparser.ConfigParser()
config.read("./config.ini")
register_channel = config['channel']['register']

db_connect = Database_Connect()

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
        #Check whether it's on the right channel or not
        if reg_ch != interaction.channel.id:
            await interaction.followup.send(f"Perintah hanya bisa digunakan di <#{register_channel}> ")
            return
        
        try:
            cursor = db_connect.cursor()

            id_discord = interaction.user.id
            pquery = "SELECT * FROM playerucp WHERE DiscordID = %s"

            cursor.execute(pquery, (id_discord,))
            rows = cursor.fetchone()

            if Check_Username(db_connect, name):
                await interaction.followup.send(f"Nama {name} sudah pernah terdaftar dalam database!")
                return
            else:    
                if rows is None:
                    verify = ''.join(random.sample('0123456789', 6))
                    query = "INSERT INTO playerucp (ucp, verifycode, DiscordID) VALUES (%s, %s, %s)"
                    values = (name, verify, id_discord)
                    cursor.execute(query, values)
                    db_connect.commit()

                    #embed message register
                    register_embed = discord.Embed(title="Successfully registered your UCP!", description="Silahkan cek **Private Message** anda untuk mendapatkan kode verify!", color=discord.Color.dark_purple())
                    register_embed.add_field(name=f"Stats UCP user {interaction.user.name}: ", value=f"**UCP** : {name}\n**Status** : Verify!", inline=False)
                    register_embed.set_footer(text=f"Peace, {interaction.guild.name}", icon_url=interaction.guild.icon.url)
                    await interaction.followup.send(embed=register_embed)
                    await interaction.user.send(f"Kode verifikasi mu : `{verify}`")
                else:
                    #Check username if alredy register
                    column_names = ['id', 'ucp', 'verifycode', 'DiscordID']
                    data_dict = dict(zip(column_names, rows))
                    await interaction.followup.send(f"Kamu sudah pernah mendaftarkan akun sebagai : `{data_dict['ucp']}`! discord! id : **{data_dict['DiscordID']}**")

        except mysql.connector.IntegrityError() as err:
            await interaction.response.send_message("Terjadi error, silahkan coba lagi nanti! hubungi atau report jika bug!")
            print(f"Error : {err}")

        except Exception as error:
            print(f"Error : {error}")
            await interaction.response.send_message("Terjadi error, silahkan coba lagi nanti! hubungi atau report jika bug!")
            
        finally:
            if 'database_connection' in locals() and db_connect.is_connected():
                cursor.close()
                db_connect.close()


async def setup(bot):
    await bot.add_cog(register(bot))