#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

__version__ = '1.0'

install_requires = [
    "requests",
    "python-telegram-bot",
    "urllib",
    "re",
    "json",
    "datetime",
    "threading",
    "time",
    "rasa_nlu",
    "spacy",
    "chatterbot",
    "pypandoc",
    "tensorflow",
]

setup(
    name = 'Fibot',
    packages = [
        'Fibot',
        'Fibot.NLP'
    ],
    version = __version__,
    install_requires = install_requires,
    description = "Fibot, el bot para los estudiantes de la FIB",
    author = "Victor Busque",
    author_email = "victorbusque@gmail.com",
    url = "https://github.com/VictorBusque",
    keywords=["nlp", "machine-learning", "bot",
                  "bots",
                  "botkit", "rasa", "conversational-agents",
                  "conversational-ai",
                  "chatbot", "chatbot-framework", "bot-framework", "FIB", "Query"],
    download_url="https://codeload.github.com/VictorBusque/FIB-Chatbot/zip/master"
)
import os
os.system("python -m spacy download en")
print("\nBienvenido a Fibot!!")
