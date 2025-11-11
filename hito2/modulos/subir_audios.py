import aiohttp
import os

async def subirAudio(mensaje,archivo):
    async with aiohttp.ClientSession() as session:
        async with session.get(mensaje) as response:
            if response.status == 200: # codigo de estado http = "ok"
                print("Estatus: ", response.status)
                with open(archivo, 'wb') as f:
                    f.write(await response.read())
                print("Se descargo correctamente")
                return archivo
            else:
                print("Error, status: ", response.status)
                return None