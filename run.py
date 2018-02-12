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
		Fibot.send_preset_message(chat_id, "start_known", Fibot.chats.get_chat(chat_id)['name'])
	else:
		user_name = update.message.from_user.first_name
		data = {'name': user_name,
				'language': 'Spanish',
				'access_token': None,
				'refresh_token': None,
				'current_state': Fibot.state_machine['MessageHandler'],
				'expire_time_end': None,
				'logged': False,
				'notifications': False,
				'training': False}
		Fibot.chats.update_chat(chat_id, data, compulsory = True)
		Fibot.send_preset_message(chat_id, "start_unknown_1", user_name)
		Fibot.send_preset_message(chat_id, "start_unknown_2")
		Fibot.send_preset_message(chat_id, "start_unknown_3")
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
		Fibot.send_preset_message(chat_id, "send_oauth_url", Fibot.api_raco.get_autho_full_page())
		Fibot.send_preset_message(chat_id, "inform_oauth_procedure")
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine['Wait_authorisation'], overwrite = True)
	else:
		Fibot.send_preset_message(chat_id, "already_login", user_name)
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
		Fibot.send_preset_message(chat_id, "request_oauth_url")
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine['Wait_authorisation'], overwrite = True)
		return MESSAGE_INCOME
	auth_code = url.split('=')[1]
	callback = Fibot.api_raco.authenticate(auth_code)
	if isinstance(callback, dict):
		Fibot.chats.update_chat(chat_id, callback, full_data = False)
		Fibot.send_preset_message(chat_id, "login_done", user_name)
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine['MessageHandler'], overwrite = True)
	else:
		Fibot.send_preset_message(chat_id, "url_error")
		Fibot.chats.update_info(chat_id, 'current_state', Fibot.state_machine_nodes['Wait_authorisation'], overwrite = True)
	return MESSAGE_INCOME


"""
	Function that responds to the /logout command
"""
def logout(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	user_name = Fibot.chats.get_chat(chat_id)['name']
	if Fibot.chats.get_chat(chat_id)['logged']:
		data = {'name': user_name,
				'language': Fibot.chats.get_chat(chat_id)['language'],
				'access_token': None,
				'refresh_token': None,
				'current_state': Fibot.state_machine['MessageHandler'],
				'expire_time_end': None,
				'logged': False,
				'notifications': False,
				'training': False}
		Fibot.chats.update_chat(chat_id, data)
		Fibot.send_preset_message(chat_id, "logout_done", user_name)
	else:
		Fibot.send_preset_message(chat_id, "logout_failed", user_name)


"""
	Function that responds to the /updates_on command
"""
def updates_on(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['logged'] and not Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.chats.update_info(chat_id, 'notifications' , True, overwrite = True)
		Fibot.send_preset_message(chat_id, "notif_active")
	elif Fibot.chats.get_chat(chat_id)['logged'] and Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.send_preset_message(chat_id, "notif_already_active")
	else:
		Fibot.send_preset_message(chat_id, "notif_active_failed")


"""
	Function that responds to the /updates_off command
"""
def updates_off(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['logged'] and Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.chats.update_info(chat_id, 'notifications' , False, overwrite = True)
		Fibot.send_preset_message(chat_id, "notif_inactive")
	elif not Fibot.chats.get_chat(chat_id)['logged']:
		Fibot.send_preset_message(chat_id, "notif_already_inactive")
	elif Fibot.chats.get_chat(chat_id)['notifications']:
		Fibot.send_preset_message(chat_id, "notif_inactive_failed")


"""
	Function that responds to the /train_on command
"""
def training_on(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if not Fibot.chats.get_chat(chat_id)['training']:
		Fibot.chats.update_info(chat_id, 'training' , True, overwrite = True)
		Fibot.send_preset_message(chat_id, "training_active")
		Fibot.send_preset_message(chat_id, "send_me_message")
	else:
		Fibot.send_preset_message(chat_id, "training_already_active")
		return TRAINING


"""
	Function that responds to the /train_off command
"""
def training_off(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	if Fibot.chats.get_chat(chat_id)['training']:
		Fibot.chats.update_info(chat_id, 'training' , False, overwrite = True)
		Fibot.send_preset_message(chat_id, "training_inactive")
	else:
		Fibot.send_preset_message(chat_id, "training_already_inactive")
	return MESSAGE_INCOME


"""
	Function that reads a regular message and decides which mechanism has to answer
"""
def ask(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	text = update.message.text
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
	#Fibot.send_message(chat_id, Fibot.nlg.get_response(text, debug = False), typing = True, reply_to = message_id)
	Fibot.process_income_message(chat_id, text, message_id = message_id)
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
		Fibot.send_preset_message(chat_id, "request_good_answer")
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
	Fibot.send_preset_message(chat_id, "corrected_message")
	Fibot.send_preset_message(chat_id, "send_me_message")
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
