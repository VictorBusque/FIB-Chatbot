#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
						  ConversationHandler)

import logging
import API_module
import NLU_module
import feature_module
import db_module

BOT_NAME = "Test_bot"
BOT_TOKEN = '464845676:AAG4XGgjfUC_pkuAcJHRDYebQvuTZgx4jUo'


LOG_OPTION, WAITING_URL, WAITING_QUESTION = range(3)
LOGGED_IN = False

reply_keyboard = [['Sí','No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


state_machine = {
	'started': 0,
	'waiting_question': 1,
	'waiting_component': 2,
	'login': 3,
	'waiting_url': 4,
	'notifying': 5
}


def start(bot, update):
	chat_id = update.message.chat_id
	user_name = update.message.from_user.first_name
	data = {'name': user_name,
			'access_token': None,
			'refresh_token': None,
			'current_state': state_machine['started'],
			'expire_time_ini': None,
			'expire_time_end': None,
			'logged': False}
	db_module.update_chat(chat_id, data, not db_module.user_has_data(chat_id))

	update.message.reply_text('Hola %s, bienvenido a %s'%(user_name, BOT_NAME))
	update.message.reply_text('Soy un prototipo de asistente para tí y tus estudios en la FIB, para que puedas centrarte en lo que importa, y no tengas que preocuparte por lo demás.')
	update.message.reply_text('Ahora dime, quieres autentificarte para que pueda ser más útil?', reply_markup=markup)
	return LOG_OPTION


def done(bot, update):
	return ConversationHandler.END


def custom_choice(bot, update):
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	text = update.message.text
	if text == "Sí":
		update.message.reply_text('Muy bien %s, autentifícate en la siguiente url: %s.'%(USER_NAME, API_module.get_autho_full_page()))
		update.message.reply_text('Una vez te hayas autentificado, mándame por mensaje la url a la que te llevó.')
		db_module.update_info(chat_id, 'current_state', state_machine['waiting_url'], overwrite = True)
		return WAITING_URL
	elif text == "No":
		update.message.reply_text('De acuerdo %s, podrás autentificarte cuando quieras usando el comando "/login" '%(USER_NAME))


def authenticate(bot, update):
	chat_id = update.message.chat_id
	USER_NAME = db_module.get_chat(chat_id)['name']
	text = update.message.text
	print(text)
	AUTH_CODE = text.split('=')[1]
	print(AUTH_CODE)
	callback = API_module.process_oauth(AUTH_CODE, chat_id)
	if callback:
		update.message.reply_text('Gracias %s, ya podemos empezar!'%USER_NAME)
		db_module.update_info(chat_id, 'current_state', state_machine['waiting_question'], overwrite = True)
		return WAITING_QUESTION
	else:
		update.message.reply_text('Hubo un error! Mándame la URL de nuevo por favor.')
		db_module.update_info(chat_id, 'current_state', state_machine['waiting_url'], overwrite = True)
		return WAITING_URL


def ask(bot, update):
	query = update.message.text
	intent = NLU_module.get_intent(query)
	entities = NLU_module.get_entities(query)
	update.message.reply_text('Tu intención es: '+intent['name'])
	for entity in entities:
		update.message.reply_text('Y también me diste el '+entity['entity'] +', que es ' + entity['value'])
	update.message.reply_text('Mis resultados son: ')
	update.message.reply_text(feature_module.retrieve_data(intent, entities))
	return WAITING_QUESTION


def main():
	db_module.load_data()
	#NLU_module.create_interpreter(False)
	print("Everything initialisated")
	# Create the Updater and pass it your bot's token.
	updater = Updater(BOT_TOKEN)

	dp = updater.dispatcher

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],
		states={					
			LOG_OPTION: [RegexHandler('^(Sí|No)$', custom_choice)],
			WAITING_URL: [MessageHandler(filters = Filters.text, callback = authenticate)],
			WAITING_QUESTION: [MessageHandler(filters = Filters.text, callback = ask)]
			#TYPING_USERNAME
			#TYPING_PASSWORD
			#ASKING
			#ANSWERING
		},
		fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
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
