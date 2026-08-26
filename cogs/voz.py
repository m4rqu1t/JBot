import discord
from discord.ext import commands
from discord import app_commands
import asyncio 

class Voz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is not None:
            if len(before.channel.members) == 0 and before.channel.name.startswith("Sala de"):
                
                await asyncio.sleep(180)
                
                canal_atualizado = self.bot.get_channel(before.channel.id)
                
                if canal_atualizado is not None and len(canal_atualizado.members) == 0:
                    try:
                        await canal_atualizado.delete()
                    except discord.NotFound:
                        pass 

    @app_commands.command(name="criarvoz", description="Cria um canal de voz temporário para você.")
    async def criarvoz(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        categoria = interaction.channel.category 
        
        novo_canal = await guild.create_voice_channel(
            name=f"Sala de {member.display_name}",
            category=categoria
        )
        
        await interaction.response.send_message(f"✅ Seu canal temporário foi criado: {novo_canal.mention}", ephemeral=True)
        
        if member.voice:
            try:
                await member.move_to(novo_canal)
            except discord.HTTPException:
                pass

async def setup(bot):
    await bot.add_cog(Voz(bot))