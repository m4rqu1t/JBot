import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

class JBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        initial_extensions = ['cogs.moderacao', 'cogs.voz', 'cogs.geral']
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"✅ Cog carregado: {extension}")
            except Exception as e:
                print(f"❌ Erro ao carregar {extension}: {e}")
        
        synced = await self.tree.sync()
        print(f"Sincronizados {len(synced)} comandos de barra.")

bot = JBot()

@bot.event
async def on_ready():
    print(f'JBot online e operando! Conectado como {bot.user}')
    
    atividade = discord.Game(name="JBot v1.0.1 | /status")
    await bot.change_presence(status=discord.Status.online, activity=atividade)

token = os.getenv('DISCORD_TOKEN')
bot.run(token)