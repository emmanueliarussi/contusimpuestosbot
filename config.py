# -*- coding: utf-8 -*-
# tweepy-bots/bots/config.py
import tweepy
import logging
import os
from os import environ
import telegram
from telegram.error import NetworkError, Unauthorized
import requests
import re

logger = logging.getLogger()

# Variables del ambiente con las claves de autoenticacion
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
TELEGRAM_KEY = environ['TELEGRAM_KEY']

def create_api():
    # Autenticación a Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Log for debug
    #logger.info("CONSUMER_KEY = {}".format(CONSUMER_KEY))
    #logger.info("CONSUMER_SECRET = {}".format(CONSUMER_SECRET))
    #logger.info("ACCESS_TOKEN = {}".format(ACCESS_TOKEN))
    #logger.info("ACCESS_TOKEN_SECRET = {}".format(ACCESS_TOKEN_SECRET))
    #logger.info("TELEGRAM_KEY = {}".format(TELEGRAM_KEY))

    # Autenticación a Telegram
    bot = telegram.Bot(TELEGRAM_KEY)
    logger.info("API de Telegram lista!")

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error de verificacion en la API de Twitter", exc_info=True)
        raise e
    logger.info("API de Twitter lista!")

    return api,bot


