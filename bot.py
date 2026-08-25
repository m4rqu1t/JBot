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

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'👢 {member.mention} foi expulso do servidor. Motivo: {reason}')

# Comando para banir (!ban @usuario Motivo)
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'🔨 {member.mention} foi banido do servidor. Motivo: {reason}')

# Comando para apagar mensagens (!clear 10)
@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    # amount + 1 para apagar também a mensagem do próprio comando
    deleted = await ctx.channel.purge(limit=amount + 1)
    # Mostra uma mensagem temporária que some após 5 segundos
    await ctx.send(f'🧹 {len(deleted) - 1} mensagens foram apagadas.', delete_after=5)

# Comando para bloquear o canal (!lock)
@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Este canal foi bloqueado temporariamente.")

# Comando para desbloquear o canal (!unlock)
@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Canal desbloqueado. Podem voltar a falar!")
    
token = os.getenv('DISCORD_TOKEN')
bot.run(token)