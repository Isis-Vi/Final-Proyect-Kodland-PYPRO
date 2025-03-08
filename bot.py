#Importing libraries
import discord
from discord.ext import commands
from db import * 
from db import engine

#Config intents
intents = discord.Intents.default()
intents.message_content = True

#Bot defined as a variable
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#test command
@bot.command()
async def hello(ctx):
    await ctx.send(f'¡Hola! Yo soy {bot.user}, tu asistente ecologico de confianza! ૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა')

#Carbon Footprint estimate command
@bot.command()
async def huella_estimado(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    await ctx.send("¿Cuántos kilometros, en promedio, viajas en vehículos motorizados al mes?")
    km_carro = await bot.wait_for("message", check=check)
    
    await ctx.send("¿Cuántos kWh de electricidad consumes al mes en tu hogar?")
    kwh = await bot.wait_for("message", check=check)
    
    await ctx.send("¿Consumes carne frecuentemente? (sí/no)")
    carne = await bot.wait_for("message", check=check)
    
    await ctx.send("¿Cuántos productos de plástico desechas durante el mes? (aproximado en kilos)")
    plasticos = await bot.wait_for("message", check=check)

#Convert units to estimate the footsprint
    km_carro = float(km_carro.content)
    kwh = float(kwh.content)
    plasticos = int(plasticos.content)
    carne = 1.5 if carne.content.lower() in ["sí"] else 1.0

# Carbon footprint calculation (estimated)
    huella_total = (km_carro * 0.2) + (kwh * 0.5) + (plasticos * 0.3) * carne

    user_id=str(ctx.author.id)
    carbon_foot_print_exists = has_carbonfootprint(user_id,engine)
    if carbon_foot_print_exists == True:
        respuesta_eliminacion = delete_carbon_foot_print(user_id,engine)
        if respuesta_eliminacion == True:
            respuesta = insert_row(user_id,km_carro,kwh,plasticos,carne,huella_total,engine)
    else:
        respuesta = insert_row(user_id,km_carro,kwh,plasticos,carne,huella_total,engine)

    if respuesta == True:
        mensaje_final = {f"Tu huella de carbono estimada es de **{huella_total:.2f} kg CO₂** al mes (๑ᵔ⤙ᵔ๑)"}

    else:
        mensaje_final = f"૮(˶╥︿╥)ა Ocurrió un error y no se pudo estimar tu huella de carbono, vuelve a intentarlo."
        
    await ctx.send(mensaje_final)

#Current fooprint command for each user
@bot.command()
async def huella_registrada(ctx):
    user_id = str(ctx.author.id)
    huella_usuario = get_current_carbon_foot_print(user_id,engine)
    
    if huella_usuario:
        await ctx.send(f'Tu huella de carbono es igual a {huella_usuario}! kg CO₂ al mes (*ᴗ͈ˬᴗ͈)ꕤ*')
    else:
        await ctx.send(f'૮(˶╥︿╥)ა Aun no tienes registrada tu huella de carbono, debes proporcionar tu huella de carbono usando el comando:\n /carbono_comp ')

#Show available commands
@bot.command()
async def ayuda(ctx):
    commands = "**ᕙ( •̀ ᗜ •́ )ᕗ Los comandos disponibles que puedes usar conmigo son:** \n /ayuda \n /huella_estimado \n /huella_regristada \n carbono_comp \n /consejo \n ¡Pruebalos todos ദ്ദി(˵ •̀ ᴗ - ˵ )! "
    await ctx.send(commands)

#Estimate trees to compensate the carbon footprint
@bot.command()
async def carbono_comp(ctx):
    user_id = str(ctx.author.id)
    huella_usuario = get_current_carbon_foot_print(user_id,engine)
    if huella_usuario is None:
        await ctx.send("૮(˶╥︿╥)ა Aun no tienes registrada tu huella de carbono, debes proporcionar tu huella de carbono usando el comando: \n /carbono_comp ")
        return

    # Convertir huella mensual a anual
    huella_anual = huella_usuario * 12
    arboles_necesarios = huella_anual / 22

    await ctx.send(f"🌱 Para compensar tu huella de carbono anual de **{huella_anual:.2f} kg CO₂**, "
                   f"necesitarías plantar aproximadamente **{arboles_necesarios:.2f} árboles** ( ◡̀_◡́)ᕤ")

#Advice on how to decrease carbon footprint command
@bot.command()
async def consejo(ctx):
    user_id = str(ctx.author.id)

    # Obtener datos de la base de datos
    huella_usuario = get_current_carbon_foot_print(user_id, engine)
    carro_usuario = get_current_km_carro(user_id, engine)
    kwh_usuario = get_current_kwh(user_id, engine)
    plastico_usuario = get_current_plastico(user_id, engine)

    consejos = []

    # Evaluar cada aspecto individualmente
    if carro_usuario > 1000:
        consejos.append(f"🚗 **Transporte:** Tu uso del vehículo es más alto de lo ideal, con un total de **{carro_usuario} km/mes**. ( ꩜ ᯅ ꩜;)⁭و - Reduce tu impacto:\n"
                        f"- Usa bicicleta o transporte público \n"
                        f"- Camina más en trayectos cortos \n"
                        )

    if kwh_usuario > 150:
        consejos.append(f"💡 **Electricidad:** Tu consumo es s más alto de lo ideal, con un total de **{kwh_usuario} kWh/mes** (¬`‸´¬) Prueba esto:\n"
                        f"- Apaga luces y desconecta aparatos.\n"
                        f"- Considera fuentes de energía renovable.")

    if plastico_usuario > 2:
        consejos.append(f"🛍️ **Plásticos:** Estás desechando **{plastico_usuario} kilos de plásticos por semana**. (ó﹏ò｡) Reduce esto:\n"
                        f"- Usa bolsas reutilizables. \n"
                        f"- Lleva tu botella y envases reutilizables. \n"
                        f"- Evita productos con empaque plástico.")

    # Si hay consejos, enviarlos uno por uno
    if consejos:
        for consejo in consejos:
            await ctx.send(consejo)

    else:
        await ctx.send(f'૮(˶╥︿╥)ა Aun no tienes registrada tu huella de carbono, debes proporcionar tu huella de carbono usando el comando:\n /carbono_comp')


bot.run("TU TOKEN VA AQUI")