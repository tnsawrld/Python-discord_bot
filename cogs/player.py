import discord
from other.database import Database_Connect
from discord.ext import commands
from discord import app_commands
from other.utils import *

db_connect = Database_Connect()

class player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[File] : {__name__} berhasil dijalankan!")
    
    @app_commands.command(name="char", description="Menampilkan list karakter player")
    async def char(self, interaction: discord.Interaction, user: discord.User):
        id_discord = user.id
        await interaction.response.defer()
        try:
            cursor = db_connect.cursor()
            rows = Get_UCP(db_connect, id_discord)
            if rows is None:
                await interaction.followup.send("UCP tidak ditemukan!")
                return
            else:
                cursor.execute("SELECT username, level FROM players WHERE ucp = %s LIMIT 3", (rows[0],))
                row_user = cursor.fetchall()
                formatted_players = "\n".join([f"- Username : {player[0]} - Level : {player[1]}" for player in row_user])

                List_Character = discord.Embed(title="List character", description="", color=discord.Color.dark_purple())
                List_Character.add_field(name=f"List karakter dari UCP @{rows[0]}: ", value=f"{formatted_players}", inline=False)
                List_Character.set_footer(text=f"Request by {interaction.user.name}", icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=List_Character)

        except Exception as error:
            print(f"Error : {error}")
            await interaction.response.send_message("Terjadi error, silahkan coba lagi nanti! hubungi atau report jika bug!")
            
        finally:
            if 'database_connection' in locals() and db_connect.is_connected():
                cursor.close()
                db_connect.close()
        
    @app_commands.command(name="statschar", description="Menampilkan statistik karakter player")
    async def statschar(self, interaction: discord.Interaction, user: discord.User, name_character: str):
        discordid = user.id
        cek_user = Check_Username(db_connect, name_character)
        await interaction.response.defer()
        try:
            cursor = db_connect.cursor()
            row_ucp = Get_UCP(db_connect, discordid)
            if row_ucp is None:
                await interaction.followup.send("UCP tidak terdaftar dalam database!")
                return
            else:
                if cek_user is False:
                    await interaction.followup.send("Nama karakter tidak terdaftar dalam database!")
                    return
                else:
                    cursor.execute("SELECT money, skin, gender, level FROM players WHERE username = %s", (name_character,))
                    user_data = cursor.fetchone()
                    column_names = ['money', 'skin', 'gender', 'level']
                    user_dict = dict(zip(column_names, user_data))

                    format_Money = str(f"${user_dict['money']}")
                    if user_dict['gender'] == 1:
                        format_Gender = "Laki-Laki"
                    else:
                        format_Gender = "Perempuan"
                    
                    format_Text = str(f"Nama : {name_character}\nMoney : {format_Money}\nGender : {format_Gender}\nSkin : {user_dict['skin']}\nLevel : {user_dict['level']}")
                    Character_Stats = discord.Embed(title="Stats Character", description="", color=discord.Color.dark_purple())
                    Character_Stats.add_field(name=f"Character", value=f"{format_Text}", inline=False)
                    Character_Stats.set_footer(text=f"Request by {interaction.user.name}", icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=Character_Stats)

        except Exception as error:
            print(f"Error : {error}")
            await interaction.response.send_message("Terjadi error, silahkan coba lagi nanti! hubungi atau report jika bug!")

        finally:
            if 'database_connection' in locals() and db_connect.is_connected():
                cursor.close()
                db_connect.close()
            
async def setup(bot):
    await bot.add_cog(player(bot))