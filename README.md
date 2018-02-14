# Fibot
Fibot is a telegram bot that is able to help FIB students through conversations. You can try him online by going to https://telegram.me/TestTFGbot.

<img src="/images_demo/demo_2.jpg">

Don't mind the translation too much...
## Libraries
It is written using:
  * python-telegram-bot: https://github.com/python-telegram-bot/python-telegram-bot
  * rasa_nlu: https://github.com/RasaHQ/rasa_nlu
  * rasa_core: https://github.com/RasaHQ/rasa_core
  * chatterbot: https://github.com/gunthercox/ChatterBot

## Table of contents
  * [Quick start](#quick-start)
  * [Setup](#setup)
  * [Architecture](#architecture)

## Quick start
After getting everything set up (more about how in [Setup](#setup) ...) it is only necessary to run the [run.py](./run.py) script.

## Setup
There is a step necessary to execute everything correctly.
If you have not downloaded the models folder with the pretrained files, then it is mandatory to execute first the [train_models.py](./train_models.py).
It will pop a message like the following
```
Do you wish to input stories by hand? [y/n]
```
By saying "n", it will train the models and save them into persistence (in the models folder).

By saying "y", it will train the dialog model, and also will allow you to add new stories to the rasa_core knowledge.


Also, it is possible to automatically generate the dataset that the rasa_nlu is trained on using the [generate_dataset.py](./generate_dataset.py) python script, that allows to create a dataset of a fixed size randomly (using the data in Data/Professors.txt and Data/Subjects.txt).

## Architecture
Coming soon...
