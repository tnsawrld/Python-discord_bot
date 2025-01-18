import discord
from discord.ext import commands

class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[File] : {__name__} berhasil dijalankan!")
    
    @commands.command()
    async def halo(self, ctx):
        await ctx.send(f"Hallo {ctx.author.mention}, ada yang bisaku bantu?")

    @commands.command()
    async def ping(self, ctx):
        embed_ping= discord.Embed(title="Ping!", description="Latency bot", color=discord.Color.blurple())
        embed_ping.add_field(name=f"{self.bot.user.name} ping : ", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed_ping.set_footer(text=f"Request by : {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed_ping)

async def setup(bot):
    await bot.add_cog(user(bot))