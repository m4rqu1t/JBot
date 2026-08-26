import discord
from discord.ext import commands
from discord import app_commands

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}

    @app_commands.command(name="kick", description="Expulsa um membro do servidor.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Nenhum motivo fornecido"):
        cargos = [role.name.lower() for role in member.roles]
        if "regular" not in cargos:
            await interaction.response.send_message("❌ Só tenho permissão para expulsar membros com o cargo @regular.", ephemeral=True)
            return
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(f'👢 {member.mention} foi expulso. Motivo: {reason}')
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não posso expulsar este membro. O cargo dele é maior ou igual ao meu!", ephemeral=True)

    @app_commands.command(name="ban", description="Bane um membro do servidor.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Nenhum motivo fornecido"):
        cargos = [role.name.lower() for role in member.roles]
        if "regular" not in cargos:
            await interaction.response.send_message("❌ Só tenho permissão para banir membros com o cargo @regular.", ephemeral=True)
            return
        try:
            await member.ban(reason=reason)
            await interaction.response.send_message(f'🔨 {member.mention} foi banido. Motivo: {reason}')
        except discord.Forbidden:
            await interaction.response.send_message("❌ Não posso banir este membro. O cargo dele é maior ou igual ao meu!", ephemeral=True)

    @app_commands.command(name="warn", description="Adverte um membro. 3 advertências geram expulsão automática.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Comportamento inadequado"):
        cargos = [role.name.lower() for role in member.roles]
        if "regular" not in cargos:
            await interaction.response.send_message("❌ Só tenho permissão para advertir membros com o cargo @regular.", ephemeral=True)
            return
        
        user_id = member.id
        if user_id not in self.warnings:
            self.warnings[user_id] = 0
            
        self.warnings[user_id] += 1
        total_warns = self.warnings[user_id]
        
        if total_warns >= 3:
            try:
                await member.kick(reason="Atingiu 3 advertências.")
                await interaction.response.send_message(f'👢 {member.mention} foi expulso automaticamente por acumular 3 advertências.')
                self.warnings[user_id] = 0
            except discord.Forbidden:
                await interaction.response.send_message(f"⚠️ {member.mention} atingiu 3 advertências, mas **não posso expulsá-lo** porque o cargo dele é maior ou igual ao meu!", ephemeral=True)
        else:
            await interaction.response.send_message(f'⚠️ {member.mention} recebeu uma advertência. Motivo: {reason}\\nTotal de advertências: {total_warns}')

    @app_commands.command(name="clear", description="Limpa uma quantidade específica de mensagens do chat.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True) 
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f'🧹 {len(deleted)} mensagens foram apagadas com sucesso.', ephemeral=True)

    @app_commands.command(name="lock", description="Bloqueia o canal atual, impedindo envio de novas mensagens.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        default_role = interaction.guild.default_role
        await interaction.channel.set_permissions(default_role, send_messages=False)
        await interaction.response.send_message("🔒 Este canal foi bloqueado temporariamente.")

    @app_commands.command(name="unlock", description="Desbloqueia o canal atual.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        default_role = interaction.guild.default_role
        await interaction.channel.set_permissions(default_role, send_messages=True)
        await interaction.response.send_message("🔓 Canal desbloqueado. Podem voltar a falar!")

async def setup(bot):
    await bot.add_cog(Moderacao(bot))