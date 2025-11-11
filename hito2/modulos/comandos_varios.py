import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import subir_audios
from discord import Member
import pyttsx3

#$

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True # info de los mensajes
intents.members = True # info de los usuarios

bot = commands.Bot(command_prefix='!', intents = intents)


@bot.event
async def on_member_join(member):
    await member.send(f"ola {member.name}")
@bot.event
async def on_message(message):
    if message.author==bot:
        return
    if "mensaje" in message.content.lower():
        await message.delete()
        await message.channel.send(f"mensaje de {message.author}!")

    if "echame" in message.content.lower():
        await message.author.kick(reason="kick")
    await bot.process_commands(message)


@bot.command()
async def hola(ctx):
    await ctx.send(f"hola {ctx.author.mention}")

@bot.command()
async def respuesta(ctx):
    await ctx.reply("respuesta")

@bot.command()
async def poll(ctx,*,question):
    embed = discord.Embed(title="test",description=question)
    poll_message = await ctx.send(embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")


@bot.command()
async def echar(ctx,*,usuario: Member):
    if ctx.author==bot.user:
        return
    await ctx.send(f"echando {usuario}")
    await usuario.kick(reason="test")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id == 497343885639417868:
        ctx = await bot.get_context(message)
        comando = bot.get_command("h")
        if comando:
            await ctx.invoke(comando, texto=message.content)
    await bot.process_commands(message)

bot.run(token, log_handler=handler,log_level=logging.DEBUG)