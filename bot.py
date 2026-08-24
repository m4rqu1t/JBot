import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# guarda os IDs dos canais que ele mesmo criou
canais_temporarios = []

@bot.event
async def on_ready():
    print(f'Bot online! Conectado como {bot.user}')

@bot.command()
async def criarvoz(ctx, *, nome_canal="Canal Temporário"):
    categoria = ctx.channel.category
    
    try:
        novo_canal = await ctx.guild.create_voice_channel(name=nome_canal, category=categoria)
        # Salva o ID do canal novo na nossa lista de memória
        canais_temporarios.append(novo_canal.id)
        
        await ctx.send(f'Canal de voz **{novo_canal.name}** criado! Ele será apagado em 3 minutos se ninguém entrar.')

        await asyncio.sleep(180)

        canal_atualizado = bot.get_channel(novo_canal.id)

        # Apaga apenas se ainda existir e estiver vazio após os 3 minutos 
        if canal_atualizado and len(canal_atualizado.members) == 0:
            await canal_atualizado.delete()
            
            # Remove o ID da memória já que o canal não existe mais
            if novo_canal.id in canais_temporarios:
                canais_temporarios.remove(novo_canal.id)
                
            await ctx.send(f'O canal **{nome_canal}** foi apagado por inatividade.')
                
    except discord.Forbidden:
        await ctx.send("Eu não tenho permissão para criar ou apagar canais de voz neste servidor.")
    except Exception as e:
        await ctx.send(f'Ocorreu um erro: {e}')

@bot.event
async def on_voice_state_update(member, before, after):
    # Verifica se a pessoa saiu de um canal (o canal anterior não é vazio e é diferente do atual)
    if before.channel is not None and before.channel != after.channel:
        canal = before.channel
        
        # O canal ficou vazio? E o bot foi quem criou esse canal?
        if len(canal.members) == 0 and canal.id in canais_temporarios:
            try:
                await canal.delete()
                canais_temporarios.remove(canal.id)
                print(f'Canal temporário {canal.name} apagado porque o último membro saiu.')
            except discord.NotFound:
                # canal já pode ter sido apagado por inatividade dos 3 minutos
                pass
            except Exception as e:
                print(f'Erro ao tentar apagar o canal automaticamente: {e}')

token = os.getenv('DISCORD_TOKEN')
bot.run(token)