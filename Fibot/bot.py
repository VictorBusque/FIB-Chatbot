#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
						  ConversationHandler)
import urllib
import requests
import logging
import re

from Fibot.chats import Chats
from Fibot.api_raco import API_raco
from Fibot.NLP.nlu import NLU_unit
from Fibot.NLP.nlg import NLG_unit


class Fibot(object):

	""" This object contains information and methods to manage the BOT_NAME

	Attributes:
		name(:obj:`str`): Unique identifier for the bot
		bot_token(:obj:`str`): Token to access the bot
		chats(:class:`Fibot.Chat`): Object that represents the chats
		api_raco(:class:`Fibot.API_raco`): Object that interacts with Raco's api
		nlu(:class:`Fibot.NLP.nlu.NLU_unit`): Object that interprets querys
		nlg(:class:`Fibot.NLP.nlg.NLG_unit`): Object that interacts with non FIB messages
		query_answer(:class:`Fibot.NLP.nlg.Query_answer_unit`): Object that responds to FIB-related queries
		state_machine(:obj:`dict`): Object that simplifies the state machine management
	"""
	def __init__(self, name = 'Fibot'):
		self.name = name
		self.bot_token = '464845676:AAG4XGgjfUC_pkuAcJHRDYebQvuTZgx4jUo'#os.getenv('FibotTOKEN')
		self.chats = Chats()
		self.api_raco = API_raco()
		self.nlu = NLU_unit()
		self.nlg = NLG_unit()
		self.state_machine = {
			'MessageHandler': '0',
			'Authorise': '1',
			'Wait_authorisation': '2',
			'Erase_user': '3',
			'Push_notification': '4',
		}

	"""
		Loads the following components:
			chats: Loads the chats information from persistence
			nlu: Loads the trained model
			nlg: Loads the trained model
	"""
	def load_components(self):
		self.chats.load()
		self.nlu.load()
		self.nlg.load()

	"""
		Sends a message to the chat with chat_id with content text
	"""
	def send_message(self, chat_id, text):
		params = {
			'chat_id': chat_id,
			'text': text
		}
		base_url = 'https://api.telegram.org/bot%s/sendMessage'%self.bot_token
		response = requests.get(base_url, params = params)

	"""
		Sends an action to a chat (using ChatAction helper)
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		params = {
			'chat_id': chat_id,
			'action': action
		}
		base_url = 'https://api.telegram.org/bot%s/sendChatAction'%self.bot_token
		response = requests.get(base_url, params = params)

	"""
		Returns the bot's name
	"""
	def name(self):
		return self.name

	"""
		Returns the bot's token
	"""
	def bot_token(self):
		return self.bot_token

	"""
		Returns the object chats
	"""
	def chats(self):
		return self.chats

	"""
		Returns the object api_raco
	"""
	def api_raco(self):
		return self.api_raco

	"""
		Returns the object nlu
	"""
	def nlu(self):
		return self.nlu

	"""
		Returns the object nlg
	"""
	def nlg(self):
		return self.nlg

	"""
		Returns the object query_answer
	"""
	def query_answer(self):
		return self.query_answer

	"""
		Returns the object state_machine
	"""
	def state_machine(self):
		return self.state_machine


MESSAGE_INCOME, TRAINING, CORR_INCORR, GET_CORRECT = range(4)
reply_keyboard = [['Sí','No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
Fibot = Fibot()

def start(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.user_has_data(chat_id):
		update.message.reply_text('Hola %s!'%Fibot.chats.get_chat(chat_id)['name'])
	else:
		user_name = update.message.from_user.first_name
		data = {'name': user_name,
				'access_token': None,
				'refresh_token': None,
				'current_state': Fibot.state_machine['MessageHandler'],
				'expire_time_ini': None,
				'expire_time_end': None,
				'logged': False,
				'notifications': False,
				'training': False}
		Fibot.chats.update_chat(chat_id, data, compulsory = True)
		update.message.reply_text('Hola %s, bienvenido a %s'%(user_name, Fibot.name))
		update.message.reply_text('Soy un prototipo de asistente para tí y tus estudios en la FIB, para que puedas centrarte en lo que importa, y no tengas que preocuparte por lo demás.')
		update.message.reply_text('Si quieres autentificarte para que pueda ayudarte aún más, usa el comando "/login"!')
	return MESSAGE_INCOME


def done(bot, update):
	return ConversationHandler.END


def start_authentication(bot, update):
	global Fibot
	print("Starting authentication")
	chat_id = update.message.chat_id
	user_name = Fibot.chats.get_chat(chat_id)['name']
	print(user_name)
	logged = Fibot.chats.get_chat(chat_id)['logged']
	print(logged)
	if (not logged):
		update.message.reply_text('Muy bien %s, autentifícate en la siguiente url: %s.'%(user_name, Fibot.api_raco.get_autho_full_page()))
		update.message.reply_text('Una vez te hayas autentificado, mándame por mensaje la url a la que te llevó.')
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine['Wait_authorisation'], overwrite = True)
	else:
		update.message.reply_text('Ya te identificaste con tu cuenta del Racó, %s.'%(user_name))
	return MESSAGE_INCOME


def authenticate(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	user_name = Fibot.chats.get_chat(chat_id)['name']
	url = update.message.text
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
	if not urls:
		update.message.reply_text('Por favor, mándame por mensaje la URL a la que te llevó.')
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine['Wait_authorisation'], overwrite = True)
		return MESSAGE_INCOME
	auth_code = url.split('=')[1]
	callback = Fibot.api_raco.authenticate(auth_code)
	if isinstance(callback, dict):
		Fibot.chats.update_info(chat_id, 'access_token', callback['access_token'])
		Fibot.chats.update_info(chat_id, 'refresh_token', callback['refresh_token'])
		Fibot.chats.update_info(chat_id, 'expire_time_end', callback['expire_time_end'])
		Fibot.chats.update_info(chat_id, 'logged', callback['logged'], overwrite = True)
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine['MessageHandler'], overwrite = True)
		update.message.reply_text('Gracias %s, ya podemos empezar!'%user_name)
	else:
		update.message.reply_text('Hubo un error! Mándame la URL de nuevo por favor.')
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine_nodes['Wait_authorisation'], overwrite = True)
	return MESSAGE_INCOME


def logout(bot, update):
	global Fibot
	print("Logging out")
	chat_id = update.message.chat_id
	user_name = Fibot.chats.get_chat(chat_id)['name']
	if Fibot.chats.get_chat(chat_id)['logged']:
		data = {'name': USER_NAME,
				'access_token': None,
				'refresh_token': None,
				'current_state': Fibot.state_machine()['MessageHandler'],
				'expire_time_ini': None,
				'expire_time_end': None,
				'logged': False,
				'notifications': False}
		Fibot.chats.update_chat(chat_id, data)
		update.message.reply_text('Hecho %s. Podrás volver a identificarte cuando quieras usando el comando /login.'%user_name)
	else:
		update.message.reply_text('No te has identificado en el Racó, así que no puedes cerrar sesión %s'%user_name)


def updates_on(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['logged'] and not Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.chats.update_info(chat_id, 'notifications' , True, overwrite = True)
		update.message.reply_text('Hecho! A partir de ahora ya recibirás notificaciones con tus avisos!')
	elif Fibot.chats.get_chat(chat_id)['logged'] and Fibot.chats.get_chat(chat_id)['notifications']:
		update.message.reply_text('Pero si ya las tenías activadas!')
	else:
		update.message.reply_text('Para recibir notificaciones debes haberte identificado con tu usuario del Racó (usando /login).')


def updates_off(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['logged'] and Fibot.chats().get_chat(chat_id)['notifications']:
		Fibot.chats.update_info(chat_id, 'notifications' , False, overwrite = True)
		update.message.reply_text('Hecho! A partir de ahora dejarás de recibir notificaciones con tus avisos!')
	elif not Fibot.chats.get_chat(chat_id)['logged']:
		update.message.reply_text('¡Vaya! Ni siquiera te identificaste con tu usuario del Racó. No podía mandarte nada de todas formas.')
	elif Fibot.chats.get_chat(chat_id)['notifications']:
		update.message.reply_text('No tenías activadas las notificaciones para los avisos de todas formas.')


def training_on(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if not Fibot.chats.get_chat(chat_id)['training']:
		Fibot.chats.update_info(chat_id, 'training' , True, overwrite = True)
		update.message.reply_text('Hecho! modo de entrenamiento activado!')
		update.message.reply_text('Mándame algún mensaje')
	else:
		update.message.reply_text('Modo de entrenamiento está ya activo.')
		return TRAINING


def training_off(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['training']:
		Fibot.chats.update_info(chat_id, 'training' , False, overwrite = True)
		update.message.reply_text('Hecho! modo de entrenamiento desactivado!')
	else:
		update.message.reply_text('Modo de entrenamiento está ya inactivo.')
	return MESSAGE_INCOME


def ask(bot, update):
	global Fibot
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
	update.message.reply_text(Fibot.nlg.get_response(query, debug = False))
	return MESSAGE_INCOME



def train_machine(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text
	update.message.reply_text("Procesando el mensaje...", reply_markup = markup)
	Fibot.nlg().process_answer_training(chat_id, message)
	return CORR_INCORR


def feedback_info(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text
	if message == "Sí":
		Fibot.nlg().give_feedback(chat_id, correct = True)
		return TRAINING
	elif message == "No":
		update.message.reply_text("¿Qué respuesta habría sido coherente entonces?")
		return GET_CORRECT
	else:
		update.message.reply_text("¿Fué coherente la última respuesta?", reply_markup = markup)
		return CORR_INCORR


def def_knowledge(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text
	Fibot.nlg().give_feedback(chat_id, correct = False, correct_statement = message)
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
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text

	if (Fibot.chats.get_chat(chat_id)['training']):
		return train_machine(bot, update)

	print (message)
	current_state = Fibot.chats.get_chat(chat_id)['current_state']
	if current_state == Fibot.state_machine['MessageHandler']:
		print("state , waiting a question")
		return ask(bot, update)
	elif current_state == Fibot.state_machine['Wait_authorisation']:
		print("state 2, authenticating")
		return authenticate(bot, update)


def main():
	global Fibot
	#Fibot = Fibot()
	Fibot.load_components()
	print("Everything initialisated")
	# Create the Updater and pass it your bot's token.

	updater = Updater(Fibot.bot_token)

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
