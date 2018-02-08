#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
import os
import urllib
import requests
import re

#-- 3rd party imports --#
from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
						  ConversationHandler)

#-- Local imports --#
from Fibot.fibot import Fibot


# States of the ConversationHandler
MESSAGE_INCOME, TRAINING, CORR_INCORR, GET_CORRECT = range(4)

#Custom Keyboard for training models
reply_keyboard = [['Sí','No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

#The main object of the bot, see Fibot/fibot.py to understand the implementation
Fibot = Fibot()


"""
	Function that responds to the /start command
"""
def start(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.user_has_data(chat_id):
		Fibot.send_message(chat_id, 'Hola %s!'%Fibot.chats.get_chat(chat_id)['name'])
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
		Fibot.send_message(chat_id, 'Hola %s, bienvenido a %s'%(user_name, Fibot.name))
		Fibot.send_message(chat_id, 'Soy un prototipo de asistente para tí y tus estudios en la FIB, para que puedas centrarte en lo que importa, y no tengas que preocuparte por lo demás.')
		Fibot.send_message(chat_id, 'Si quieres autentificarte para que pueda ayudarte aún más, usa el comando "/login"!')
	return MESSAGE_INCOME


"""
	Function that ends a conversation
"""
def done(bot, update):
	return ConversationHandler.END


"""
	Function that responds to the /login command
"""
def start_authentication(bot, update):
	global Fibot
	print("Starting authentication")
	chat_id = update.message.chat_id
	user_name = Fibot.chats.get_chat(chat_id)['name']
	print(user_name)
	logged = Fibot.chats.get_chat(chat_id)['logged']
	print(logged)
	if (not logged):
		Fibot.send_message(chat_id, 'Muy bien %s, autentifícate en la siguiente url: %s.'%(user_name, Fibot.api_raco.get_autho_full_page()))
		Fibot.send_message(chat_id, 'Una vez te hayas autentificado, mándame por mensaje la url a la que te llevó.')
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine['Wait_authorisation'], overwrite = True)
	else:
		Fibot.send_message(chat_id,'Ya te identificaste con tu cuenta del Racó, %s.'%(user_name))
	return MESSAGE_INCOME


"""
	Function that does the 2nd part of the oauth2.0 process
"""
def authenticate(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	user_name = Fibot.chats.get_chat(chat_id)['name']
	url = update.message.text
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
	if not urls:
		Fibot.send_message(chat_id, 'Por favor, mándame por mensaje la URL a la que te llevó.')
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
		Fibot.send_message(chat_id, 'Gracias %s, ya podemos empezar!'%user_name)
	else:
		Fibot.send_message(chat_id, 'Hubo un error! Mándame la URL de nuevo por favor.')
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine_nodes['Wait_authorisation'], overwrite = True)
	return MESSAGE_INCOME


"""
	Function that responds to the /logout command
"""
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
		Fibot.send_message(chat_id, 'Hecho %s. Podrás volver a identificarte cuando quieras usando el comando /login.'%user_name)
	else:
		Fibot.send_message(chat_id, 'No te has identificado en el Racó, así que no puedes cerrar sesión %s'%user_name)


"""
	Function that responds to the /updates_on command
"""
def updates_on(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['logged'] and not Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.chats.update_info(chat_id, 'notifications' , True, overwrite = True)
		Fibot.send_message(chat_id, 'Hecho! A partir de ahora ya recibirás notificaciones con tus avisos!')
	elif Fibot.chats.get_chat(chat_id)['logged'] and Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.send_message(chat_id, 'Pero si ya las tenías activadas!')
	else:
		Fibot.send_message(chat_id, 'Para recibir notificaciones debes haberte identificado con tu usuario del Racó (usando /login).')


"""
	Function that responds to the /updates_off command
"""
def updates_off(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['logged'] and Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.chats.update_info(chat_id, 'notifications' , False, overwrite = True)
		Fibot.send_message(chat_id, 'Hecho! A partir de ahora dejarás de recibir notificaciones con tus avisos!')
	elif not Fibot.chats.get_chat(chat_id)['logged']:
		Fibot.send_message(chat_id, '¡Vaya! Ni siquiera te identificaste con tu usuario del Racó. No podía mandarte nada de todas formas.')
	elif Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.send_message(chat_id, 'No tenías activadas las notificaciones para los avisos de todas formas.')


"""
	Function that responds to the /train_on command
"""
def training_on(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if not Fibot.chats.get_chat(chat_id)['training']:
		Fibot.chats.update_info(chat_id, 'training' , True, overwrite = True)
		Fibot.send_message(chat_id, 'Hecho! modo de entrenamiento activado!')
		Fibot.send_message(chat_id, 'Mándame algún mensaje')
	else:
		Fibot.send_message(chat_id, 'Modo de entrenamiento está ya activo.')
		return TRAINING


"""
	Function that responds to the /train_off command
"""
def training_off(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['training']:
		Fibot.chats.update_info(chat_id, 'training' , False, overwrite = True)
		Fibot.send_message(chat_id, 'Hecho! modo de entrenamiento desactivado!')
	else:
		Fibot.send_message(chat_id, 'Modo de entrenamiento está ya inactivo.')
	return MESSAGE_INCOME


"""
	Function that reads a regular message and decides which mechanism has to answer
"""
def ask(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	query = update.message.text
	message_id = update.message.message_id
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
	Fibot.send_message(chat_id, Fibot.nlg.get_response(query, debug = False), typing = True, reply_to = message_id)
	return MESSAGE_INCOME



"""
	Function that responds to the training messages
"""
def train_machine(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text
	update.message.reply_text("Procesando el mensaje...", reply_markup = markup)
	Fibot.nlg.process_answer_training(chat_id, message)
	return CORR_INCORR


"""
	Function that does the feedback part of the training
"""
def feedback_info(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text
	if message == "Sí":
		Fibot.nlg.give_feedback(chat_id, correct = True)
		return TRAINING
	elif message == "No":
		Fibot.send_message(chat_id,"¿Qué respuesta habría sido coherente entonces?")
		return GET_CORRECT
	else:
		update.message.reply_text("¿Fué coherente la última respuesta?", reply_markup = markup)
		return CORR_INCORR


"""
	Function that applies a new rule defined by the user
"""
def def_knowledge(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text
	Fibot.nlg.give_feedback(chat_id, correct = False, correct_statement = message)
	Fibot.send_message(chat_id, 'Corregido! Muchas gracias!')
	Fibot.send_message(chat_id, 'Mándame algún mensaje')
	return TRAINING


"""
	Function that manages the state machine
"""
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


"""
	Main function, polls waiting for messages
"""
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
