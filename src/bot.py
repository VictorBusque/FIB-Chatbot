#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
						  ConversationHandler)
import urllib
import requests
import logging
import re

import API_module
import NLU_module
import NLG_module
import feature_module
import db_module

BOT_NAME = "BOT_NAME"
BOT_TOKEN = '464845676:AAG4XGgjfUC_pkuAcJHRDYebQvuTZgx4jUo'


MESSAGE_INCOME, TRAINING, CORR_INCORR, GET_CORRECT = range(4)

##### STATE MACHINE #####
# 0 - Message Handler
### 0.0 - Waiting Question
### 0.1 - Processing Answer
### 0.2 - Missing information (entities)
# 1 - Authorise (via /login)
# 2 - Waiting for autentification
# 3 - Erase user information (via /logout)
# 4 - Push Notification (via push or /update)
#########################
state_machine_nodes = {
	'MessageHandler': '0',
	'Authorise': '1',
	'Wait_authorisation': '2',
	'Erase_user': '3',
	'Push_notification': '4',
}


reply_keyboard = [['Sí','No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def send_chat_action(chat_id, action):
	print("Sending action %s"%action)
	params = {
		'chat_id': chat_id,
		'action': action
	}
	base_url = 'https://api.telegram.org/bot%s/sendChatAction'%BOT_TOKEN#?'%BOT_TOKEN+ urllib.parse.urlencode(params)
	response = requests.get(base_url, params = params)


def send_message(chat_id, message, markup = False):
	print("Sending message %s to %s"%(message, db_module.get_chat(chat_id)['name']) )
	params = {
		'chat_id': chat_id,
		'text': message
	}
	base_url = 'https://api.telegram.org/bot%s/sendMessage'%BOT_TOKEN#?'%BOT_TOKEN+ urllib.parse.urlencode(params)
	response = requests.get(base_url, params = params)



def start(bot, update):
	global state_machine_nodes
	chat_id = update.message.chat_id
	user_name = update.message.from_user.first_name
	if db_module.user_has_data(chat_id):
		update.message.reply_text('Hola %s!'%user_name)
	else:
		data = {'name': user_name,
				'access_token': None,
				'refresh_token': None,
				'current_state': state_machine_nodes['MessageHandler'],
				'expire_time_ini': None,
				'expire_time_end': None,
				'logged': False,
				'notifications': False,
				'training': False}
		db_module.update_chat(chat_id, data, compulsory = not db_module.user_has_data(chat_id))
		update.message.reply_text('Hola %s, bienvenido a %s'%(user_name, BOT_NAME))
		update.message.reply_text('Soy un prototipo de asistente para tí y tus estudios en la FIB, para que puedas centrarte en lo que importa, y no tengas que preocuparte por lo demás.')
		update.message.reply_text('Si quieres autentificarte para que pueda ayudarte aún más, usa el comando "/login"!')#, reply_markup=markup)
	return MESSAGE_INCOME


def done(bot, update):
	return ConversationHandler.END


def start_authentication(bot, update):
	global state_machine_nodes
	print("Starting authentication")
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	logged = db_module.get_chat(chat_id)['logged']
	if (not logged):
		update.message.reply_text('Muy bien %s, autentifícate en la siguiente url: %s.'%(USER_NAME, API_module.get_autho_full_page()))
		update.message.reply_text('Una vez te hayas autentificado, mándame por mensaje la url a la que te llevó.')
		db_module.update_info(chat_id, 'current_state', state_machine_nodes['Wait_authorisation'], overwrite = True)
	else:
		update.message.reply_text('Ya te identificaste con tu cuenta del Racó, %s.'%(USER_NAME))
	return MESSAGE_INCOME


def authenticate(bot, update):
	global state_machine_nodes
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	url = update.message.text
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
	if not urls:
		db_module.update_info(chat_id, 'current_state', state_machine_nodes['MessageHandler'], overwrite = True)
		return ask(bot, update)
	print(url)
	AUTH_CODE = url.split('=')[1]
	print(AUTH_CODE)
	callback = API_module.process_oauth(AUTH_CODE, chat_id)
	if callback:
		update.message.reply_text('Gracias %s, ya podemos empezar!'%USER_NAME)
		db_module.update_info(chat_id, 'current_state', state_machine_nodes['MessageHandler'], overwrite = True)
	else:
		update.message.reply_text('Hubo un error! Mándame la URL de nuevo por favor.')
		db_module.update_info(chat_id, 'current_state', state_machine_nodes['Wait_authorisation'], overwrite = True)
	return MESSAGE_INCOME


def logout(bot, update):
	print("Logging out")
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	if db_module.get_chat(chat_id)['logged']:
		data = {'name': USER_NAME,
				'access_token': None,
				'refresh_token': None,
				'current_state': state_machine_nodes['MessageHandler'],
				'expire_time_ini': None,
				'expire_time_end': None,
				'logged': False,
				'notifications': False}
		db_module.update_chat(chat_id, data)
		update.message.reply_text('Hecho %s. Podrás volver a identificarte cuando quieras usando el comando /login.'%USER_NAME)
	else:
		update.message.reply_text('No te has identificado en el Racó, así que no puedes cerrar sesión %s'%USER_NAME)


def updates_on(bot, update):
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	if db_module.get_chat(chat_id)['logged'] and not db_module.get_chat(chat_id)['notifications']:
		db_module.update_info(chat_id, 'notifications' , True, overwrite = True)
		update.message.reply_text('Hecho! A partir de ahora ya recibirás notificaciones con tus avisos!')
	elif db_module.get_chat(chat_id)['logged'] and db_module.get_chat(chat_id)['notifications']:
		update.message.reply_text('Pero si ya las tenías activadas!')
	else:
		update.message.reply_text('Para recibir notificaciones debes haberte identificado con tu usuario del Racó (usando /login).')


def updates_off(bot, update):
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	if db_module.get_chat(chat_id)['logged'] and db_module.get_chat(chat_id)['notifications']:
		db_module.update_info(chat_id, 'notifications' , False, overwrite = True)
		update.message.reply_text('Hecho! A partir de ahora dejarás de recibir notificaciones con tus avisos!')
	elif not db_module.get_chat(chat_id)['logged']:
		update.message.reply_text('¡Vaya! Ni siquiera te identificaste con tu usuario del Racó. No podía mandarte nada de todas formas.')
	elif db_module.get_chat(chat_id)['notifications']:
		update.message.reply_text('No tenías activadas las notificaciones para los avisos de todas formas.')


def training_on(bot, update):
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	if not db_module.get_chat(chat_id)['training']:
		db_module.update_info(chat_id, 'training' , True, overwrite = True)
		update.message.reply_text('Hecho! modo de entrenamiento activado!')
		update.message.reply_text('Mándame algún mensaje')
	else:
		update.message.reply_text('Modo de entrenamiento está ya activo.')
		return TRAINING


def training_off(bot, update):
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	if db_module.get_chat(chat_id)['training']:
		db_module.update_info(chat_id, 'training' , False, overwrite = True)
		update.message.reply_text('Hecho! modo de entrenamiento desactivado!')
	else:
		update.message.reply_text('Modo de entrenamiento está ya inactivo.')
	return MESSAGE_INCOME


def ask(bot, update):
	chat_id = update.message.chat_id
	query = update.message.text
	'''
	intent = NLU_module.get_intent(query)
	entities = NLU_module.get_entities(query)
	update.message.reply_text('Estoy '+str(intent['confidence']*100)+' porciento seguro de que tu intención es: '+intent['name'])
	for entity in entities:
		update.message.reply_text('Y también me diste el '+entity['entity'] +', que es ' + entity['value'])
	update.message.reply_text('Mis resultados son: ')
	send_chat_action(chat_id, 'typing')
	update.message.reply_text(feature_module.retrieve_data(intent, entities, chat_id = chat_id))
	'''
	update.message.reply_text(NLG_module.get_response(query, debug = False))
	return MESSAGE_INCOME



def train_machine(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text
	print("Hola, estoy en train_machine")
	print(message)
	update.message.reply_text("Procesando el mensaje...", reply_markup = markup)
	NLG_module.process_answer_training(chat_id, message)
	return CORR_INCORR


def feedback_info(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text
	if message == "Sí":
		NLG_module.give_feedback(chat_id, correct = True)
		return TRAINING
	elif message == "No":
		update.message.reply_text("¿Qué respuesta habría sido coherente entonces?")
		return GET_CORRECT
	else:
		update.message.reply_text("¿Fué coherente la última respuesta?", reply_markup = markup)
		return CORR_INCORR


def def_knowledge(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text
	NLG_module.give_feedback(chat_id, correct = False, correct_statement = message)
	update.message.reply_text('Corregido! Muchas gracias!')
	update.message.reply_text('Mándame algún mensaje')
	return TRAINING

##### STATE MACHINE #####
# 0 - Message Handler
### 0.0 - Waiting Question
### 0.1 - Processing Answer
### 0.2 - Missing information (entities)
# 1 - Authorise (via /login)
# 2 - Waiting for autentification
# 3 - Erase user information (via /logout)
# 4 - Push Notification (via push or /update)
#########################
def state_machine(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text

	if (db_module.get_chat(chat_id)['training']):
		return train_machine(bot, update)

	print (message)
	USER_NAME = db_module.get_chat(chat_id)['name']
	current_state = db_module.get_chat(chat_id)['current_state']
	print("está en la state machine, con estado %s"%current_state)
	if current_state == '0':
		print("state , waiting a question")
		return ask(bot, update)
	elif current_state == '2':
		print("state 2, authenticating")
		return authenticate(bot, update)


def main():
	db_module.load_data()
	NLU_module.create_interpreter(False)
	NLG_module.load_bot()
	print("Everything initialisated")
	# Create the Updater and pass it your bot's token.
	updater = Updater(BOT_TOKEN)

	dp = updater.dispatcher

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start), CommandHandler('login', start_authentication),
					CommandHandler('logout', logout), CommandHandler('updates_on', updates_on),
					CommandHandler('updates_off', updates_off), CommandHandler('train_on', training_on),
					CommandHandler('train_off', training_off)],
		states = {
			MESSAGE_INCOME: [MessageHandler(filters = Filters.text, callback = state_machine)],
			TRAINING: [MessageHandler(filters = Filters.text, callback = train_machine)],
			CORR_INCORR: [RegexHandler('^(Sí|No)$', callback = feedback_info)],
			GET_CORRECT: [MessageHandler(filters = Filters.text, callback = def_knowledge)],
		},
		fallbacks=[RegexHandler('^Done$', done)],
		allow_reentry = True #So users can use /login
	)

	dp.add_handler(conv_handler)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()
