#!/usr/bin/env python

from os import environ
from flask import Flask
import tweepy
import logging
from config import create_api
import json
import time
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import requests
import re
import urllib.request

# Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Tiempo de espera entre updates
sleep_time_sec = 5 

update_id = None
link      = None

# Patron de los links de Twitter 
url_pattern = re.compile("https://twitter.com/([a-zA-Z0-9_]+)/status/([0-9_]+).*")

# Obtener link desde el bot de telegram
def getLink(bot):

    global update_id

    # Obtener ultimos updates del bot
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        # Verifico que el mensaje contenga texto (podrían ser de otro tipo los updates)
        if update.message:  
            if update.message.text:
                if url_pattern.match(update.message.text):
                    try:
                        logger.info(update.message.text)
			#html = urllib.request.urlopen(update.message.text)
                        # Respuesta automatica para el usuario que envio el link
                        update.message.reply_text("Con tus impuestos twiteamos el link. Gracias!")
                        # Retorno el link
                        return update.message.text
                    except:
                        logger.info("Link inválido")
                        update.message.reply_text("El link no es válido, la dirección del tweet no existe.")
                        return None 
                else:
                    logger.info("Link inválido")
                    update.message.reply_text("El link no es válido. Recordá enviar links a tweets que comiencen con 'https://twitter.com/'")
                    return None 

    # Si no hay nada, retorno None
    return None

# Twitear un link
def tweet_link(api,tweet_ref):
    # Log 
    logger.info(f"Procesando el tweet..") 
    logger.info(tweet_ref)
    # Tweet "Con tus impuestos [LINK]"
    try:
        api.update_status("Con tus impuestos {}".format(tweet_ref))
        logger.info(f"Twiteado!")
    except:
        logger.info(f"No se pudo twittear, probablemente es un tweet duplicado.")

# Main del bot
def index():
    logger.info(f"Bienvenido a @contusimpuestos BOT") 
    global update_id
    global link
    
    # Init APIs de Telegram y Twitter
    api,telegramBot = create_api()

    # Loop del bot
    while True:
        # Chequear si hay links disponibles para twitear
        try:
            link = getLink(telegramBot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1

        # Si hay link...
        if(link != None):
            # Lo twiteamos!
            tweet_link(api,link)
            link = None
        
        # Espero un poco antes de volver a chequear
        logger.info("keep waiting..")
        time.sleep(sleep_time_sec)

    return 0
        
if __name__ == "__main__":
    index()

    

