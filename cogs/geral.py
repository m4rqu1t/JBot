import discord
from discord.ext import commands
from discord import app_commands

VERSAO_BOT = "v1.0.0"

class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Mostra o status atual e a versão do bot.")
    async def status(self, interaction: discord.Interaction):
        ping = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🤖 Status do JBot",
            description="Todos os sistemas operando perfeitamente!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Versão Atual", value=f"`{VERSAO_BOT}`", inline=True)
        embed.add_field(name="Latência", value=f"`{ping}ms`", inline=True)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Geral(bot))