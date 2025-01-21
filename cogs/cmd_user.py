import discord
from discord import app_commands
from discord.ext import commands

class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[File] : {__name__} berhasil dijalankan!")

    @app_commands.command(name="hello", description="Helloo user!!")
    async def halo(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hallo {interaction.user.mention}, ada yang bisaku bantu?")

    @app_commands.command(name="ping", description="Mendapatkan ping bot")
    async def ping(self, interaction: discord.Interaction):
        embed_ping= discord.Embed(title="Pong!", description="Latency bot", color=discord.Color.blurple())
        embed_ping.add_field(name=f"{interaction.user.name} ping : ", value=f"{round(interaction.client.latency * 1000)}ms", inline=False)
        embed_ping.set_footer(text=f"Request by : {interaction.user.name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed_ping)

    @app_commands.command(name="clear", description="Menghapus pesan")
    async def clear(self, interaction: discord.Interaction, ammount: int):
        if ammount < 1 or ammount > 100:
            await interaction.response.send_message("Jumlah pesan yang ingin dihapus harus antara 1 dan 100 yaa.")
            return
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge(limit=ammount)
        await interaction.followup.send(f"{interaction.user.name} menghapus pesan sebanyak {ammount}")

    @app_commands.command(name="dm", description="Private message")
    async def dm(self, interaction: discord.Interaction, user: discord.User, message: str):
        await interaction.response.defer(ephemeral=True)
        try:
            await user.send(message)
            await interaction.followup.send(f"Berhasil mengirim pesan pribadi ke {user.mention}")

        except discord.Forbidden:
            await interaction.followup.send(
                f"Gagal mengirim pesan ke {user.mention}. Pastikan mereka mengizinkan DM dari bot.", ephemeral=True
            )
        except discord.HTTPException:
            await interaction.followup.send(
                "Terjadi kesalahan saat mengirim pesan. Coba lagi nanti.", ephemeral=True
            )
async def setup(bot):
    await bot.add_cog(user(bot))