from telegram import Update
from telegram.ext import Application, CommandHandler
import requests
import os
import logging

# Configurar el registro de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Función para el comando /dni
async def dni(update: Update, context):
    if len(context.args) != 2:
        await update.message.reply_text("Por favor, proporciona el DNI y el sexo. Ejemplo: /dni 95847512 M")
        return

    dni = context.args[0]
    sexo = context.args[1].upper()

    url = f"https://ricardoaplicaciones-qu4k.onrender.com/api/federador/{dni}/{sexo}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if "data" in data and "sisa" in data["data"]:
            sisa_data = data["data"]["sisa"]
            respuesta = f"Nombre: {sisa_data['nombre']}\n" \
                        f"Apellido: {sisa_data['apellido']}\n" \
                        f"DNI: {sisa_data['nroDocumento']}\n" \
                        f"Sexo: {sisa_data['sexo']}\n" \
                        f"Fecha de Nacimiento: {sisa_data['fechaNacimiento']}\n" \
                        f"Fallecido: {sisa_data['fallecido']}\n" \
                        f"Domicilio: {sisa_data['domicilio']}\n"
        else:
            respuesta = "No se encontró información para ese DNI y sexo."

        await update.message.reply_text(respuesta)
    
    except Exception as e:
        await update.message.reply_text(f"Error al obtener datos: {e}")

# Función principal
async def main():
    # Token del bot
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("El token del bot no está configurado en las variables de entorno.")

    # Crear la aplicación de Telegram
    application = Application.builder().token(token).build()

    # Añadir el manejador de comando /dni
    application.add_handler(CommandHandler("dni", dni))

    # Imprimir que el bot se ha iniciado
    logging.info("Bot Iniciado")

    # Ejecutar el bot
    await application.start()
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
