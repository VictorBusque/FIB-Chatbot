# Fibot
Fibot is a telegram bot that is able to help FIB students through conversations. You can try him online by going [here](https://telegram.me/TestTFGbot.)!

<img src="/images_demo/dialog_3.png">

## Libraries
It is written using:
  * python-telegram-bot: https://github.com/python-telegram-bot/python-telegram-bot
  * rasa_nlu: https://github.com/RasaHQ/rasa_nlu
  * rasa_core: https://github.com/RasaHQ/rasa_core

## Table of contents
  * [Quick start](#quick-start)
  * [Setup](#setup)
  * [Architecture](#architecture)

## Quick start
After getting everything set up (more about how in [Setup](#setup) ...) it is only necessary to run the [run.py](./run.py) script.

It will automatically boot up the bot and it will start to be effective and get to respond queries from students.

## Setup
Make sure to have everything installed. Notice it is necessary to have the corpus for both 'en' and 'es' languages on spaCy.
You can download them by using the following commands on your terminal.
```
  python -m spacy download en
```
and
```
  python -m spacy download es
```
Then, there is a step necessary to execute everything correctly, which is to set up several environment variables:
  * client_id: with the client_id value obtained by registering your app in [here](https://api.fib.upc.edu/v2/).
  * client_secret: with the client_secret value obtained by registering your app in [here](https://api.fib.upc.edu/v2/).
  * encryption_key: a 16-character-long number that acts as private key for encrypting sensible data.
  * FibotTOKEN: The Telegram bot Token as obtained by Telegram's BotFather [here](https://telegram.me/BotFather) after creating the bot.

Next, if you have not downloaded the models folder with the pretrained files, it is mandatory to execute first the [train_models.py](./train_models.py), so that it can train the necessary models and store them to be used later.

Also, it is possible to automatically generate the dataset that the rasa_nlu is trained on using the [generate_dataset.py](./generate_dataset.py) python script, that allows to create a dataset for any language of the three of a fixed size randomly (using the data in Data/Professors.txt and Data/Subjects.txt, etc).

## Architecture
Coming soon...
