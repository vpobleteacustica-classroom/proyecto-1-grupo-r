import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import subir_audios
from discord import Member
from gtts import gTTS
import requests
from pydub import AudioSegment
import math
import pyttsx3


#$aaaaa

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True # info de los mensajes
intents.members = True # info de los usuarios

bot = commands.Bot(command_prefix='!', intents = intents)


# Para indicar las voces cuando se pidan para generarTTS
voces = ["en", "es", "ja", "fr", "de", "zh-CN", "pt", "ru", "it", "ko"]


# Esto es del tts de linux
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'es')
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)




@bot.event
async def on_ready():
    print("LISTO: BOT EN EJECUCIÓN")

# Para cambiar el volumen
@bot.command()
async def vol(ctx, link, volumen: int):
        print("recibido")
        if ctx.author == bot.user:
            return
        print(f"buscando {link}")
        archivo = await subir_audios.subirAudio(link, "audio.mp3")
        audio = AudioSegment.from_file("audio.mp3")
        if (audio):
            audioMod = audio + (20 * math.log10(volumen / 100))
            audioMod.export(f"audio_volumen_{volumen}.mp3", format="mp3")
            await ctx.send(file=discord.File(f"audio_volumen_{volumen}.mp3"))         
            os.remove(archivo)
            os.remove(f"audio_volumen_{volumen}.mp3")
        else:
            print("fail")
            await ctx.send("error")

# Cambiar la velocidad de un audio
@bot.command()
async def vel(ctx, link, vel = 1.0):
        print("recibido")
        if ctx.author == bot.user:
            return
        print(f"buscando {link}")
        archivo = await subir_audios.subirAudio(link, "audio.mp3")
        audio = AudioSegment.from_file("audio.mp3")
        if(audio):
            audioV = audio._spawn(audio.raw_data, overrides={
                "frame_rate": int(audio.frame_rate*vel)})
            audioV.export(f"audio_a_{vel}.mp3", format = "mp3")
            await ctx.send(file=discord.File(f"audio_a_{vel}.mp3"))
            os.remove(archivo)
            os.remove(f"audio_a_{vel}.mp3")
        else:
            await ctx.send("error")

# Ponerf un audio en reversa
@bot.command()
async def reversa(ctx, link):
        print("recibido")
        if ctx.author == bot.user:
            return
        print(f"buscando {link}")
        archivo = await subir_audios.subirAudio(link, "audio.mp3")
        audio = AudioSegment.from_file("audio.mp3")
        if(audio):
            audioR = audio.reverse()
            audioR.export("audio_reversa.mp3",format = "mp3")
            await ctx.send(file=discord.File("audio_reversa.mp3"))
            os.remove(archivo)
            os.remove("audio_reversa.mp3")
        else:
            await ctx.send("error")
        
# Efecto de fade (como degradado)
@bot.command()
async def fade(ctx,link, fin: int, fout: int):
        print("recibido")
        if ctx.author == bot.user:
            return
        print(f"buscando {link}")
        if fin < 0 or fout < 0:
            await ctx.send("No pueden haber tiempos negativos.")
            return
        archivo = await subir_audios.subirAudio(link, "audio.mp3")
        audio = AudioSegment.from_file("audio.mp3")
        print(f'{fin} y {fout}')
        if(audio):
            audioF = audio.fade_in(fin).fade_out(fout)
            audioF.export("audio_fade.mp3", format = "mp3")
            await ctx.send(file=discord.File("audio_fade.mp3"))
            os.remove(archivo)
            os.remove("audio_fade.mp3")
        else:
            await ctx.send("error")

# Cortar un audio con los seg proporcionados
@bot.command()
async def cortar(ctx, link, ini: int, fin: int):
        print("recibido")
        if ctx.author == bot.user:
            return
        print(f"buscando {link}")
        if ini < 0 or fin < 0:
            return
        archivo = await subir_audios.subirAudio(link, "audio.mp3")
        audio = AudioSegment.from_file("audio.mp3")
        if (audio):
            audioTr = audio[ini:fin]
            audioTr.export(f"audio_{ini}_a_{fin}.mp3", format = "mp3")
            await ctx.send(file=discord.File(f"audio_{ini}_a_{fin}.mp3"))
            os.remove(archivo)
            os.remove(f"audio_{ini}_a_{fin}.mp3")
        else:
            await ctx.send("error")


# Crear un audio tts con la voz de google    
@bot.command()
async def generartts(ctx,*,texto):
    if "#" in texto:
        if ctx.author == bot.user:
            return
        if len(texto) > 300:
            await ctx.send(f"{ctx.author}, tu texto supera los 300, inténtalo denuevo.")
            return
        idioma = texto.split("#")
        if len(idioma) == 2:
            if idioma[1] in voces:
                lang = idioma[1]
                await ctx.send("preparando tts..")
            else:
                await ctx.send(f"Debes especificar uno de estos idiomas: {voces}")
                return
        else:
            lang = "es"
        archivo = os.path.join("temp_tts", f"tts_{ctx.author}_{idioma[0]}_{idioma[1]}.mp3")
        if(archivo):
            tts = gTTS(text = idioma[0], lang=lang)
            tts.save(archivo)
            await ctx.send(file=discord.File(archivo))
            os.remove(archivo)
        else:
            await ctx.send("error")
            return
    else:
        await ctx.send("Debes especificar el idioma terminando tu mensaje con #(idioma)")
        await ctx.send(f"Estos son los idiomas disponibles: {voces}")
        return
        
# Para que el bot hable en llamada usando la tts de google
@bot.command()
async def h(ctx,*,texto):
    if ctx.voice_client:
            if ctx.voice_client.is_playing() == False:
                if ctx.author == bot.user:
                    return
                if len(texto) > 300:
                    await ctx.send(f"{ctx.author}, tu texto supera los 300, inténtalo denuevo.")
                    return
                def borrar(a):
                    print("callback after:", a)
                    os.remove(archivo)
                archivo = os.path.join("temp_tts", f"tts.mp3")
                if(archivo):
                    tts = gTTS(text = texto, lang="es")
                    tts.save(archivo)
                    ctx.voice_client.play(
                        discord.FFmpegPCMAudio(source=archivo),
                        after=lambda e: borrar(archivo))
            else: return
    else:
        await ctx.invoke(bot.get_command("entrar"))


# Para que el bot pueda hablar en llamada usando la voz TTS de linux
@bot.command()
async def tts(ctx,*,texto):
    if ctx.voice_client:
            if ctx.voice_client.is_playing() == False:
                if ctx.author == bot.user:
                    return
                if len(texto) > 300:
                    await ctx.send(f"{ctx.author}, tu texto supera los 300, inténtalo denuevo.")
                    return
                def borrar(a):
                    print("callback after:", a)
                    os.remove(archivo)
                archivo = os.path.join("temp_tts", f"ttsR.mp3")
                if(archivo):
                    engine.save_to_file(texto, archivo)
                    engine.runAndWait()
                    ctx.voice_client.play(
                        discord.FFmpegPCMAudio(source=archivo),
                        after=lambda e: borrar(archivo))
                else:
                    await ctx.send("error")


                     

# --------------   Técnico   ------------------   

# Estos son comandos para manipular al bot en sí

@bot.command()
async def entrar(ctx):
    canal = ctx.author.voice.channel
    if canal:
        await canal.connect()
    else:
        await ctx.send(f"no voice xd")
        return

@bot.command()
async def salir(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        return
    
@bot.command()
async def para(ctx):
    if ctx.voice_client:
            if ctx.voice_client.is_playing() == True:
                ctx.voice_client.stop()
    

@bot.command()
async def status(ctx):
    if ctx.author==bot.user:
        return
    await ctx.send(f"sigue andando el bot -> {ctx.author}")

@bot.command()
async def sacarid(ctx, usuario: discord.User):
    if ctx.author==bot.user:
        return
    idusuario = usuario.id
    await ctx.send(f"La id de {usuario} es {idusuario}")



bot.run(token, log_handler=handler,log_level=logging.DEBUG)