#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- General imports --#
import re
import datetime

#-- 3rd party imports --#
from telegram import ChatAction
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
						  ConversationHandler)

#-- Local imports --#
from Fibot.fibot import Fibot


# States of the ConversationHandler
MESSAGE_INCOME, CORR_INCORR, GET_CORRECT = range(3)


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
				'language': 'English',
				'access_token': None,
				'refresh_token': None,
				'current_state': Fibot.state_machine['MessageHandler'],
				'expire_time_end': None,
				'logged': False,
				'notifications': False,
				'last_notif_polling': None}
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
		Fibot.send_preset_message(chat_id, "send_oauth_url", Fibot.oauth.get_autho_full_page())
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
	callback = Fibot.oauth.authenticate(auth_code)
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
				'last_notif_polling': None}
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
	Function that reads a regular message and decides which mechanism has to answer
"""
def ask(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	text = update.message.text
	message_id = update.message.message_id
	if Fibot.chats.get_chat(chat_id)['logged'] & Fibot.chats.token_has_expired(chat_id):
		print("This token has expired!!")
		r_t = Fibot.chats.get_chat(chat_id)['refresh_token']
		print("This is the rt {}".format(r_t))
		callback = Fibot.oauth.refresh_token(r_t)
		Fibot.chats.update_chat(chat_id, callback, full_data = False)
	Fibot.process_income_message(chat_id, text)
	return MESSAGE_INCOME

"""
	Function that manages the state machine
"""
def state_machine(bot, update):
	global Fibot
	chat_id = update.message.chat_id
	message = update.message.text
	print (message)
	current_state = Fibot.chats.get_chat(chat_id)['current_state']
	if current_state == Fibot.state_machine['MessageHandler']:
		return ask(bot, update)
	elif current_state == Fibot.state_machine['Wait_authorisation']:
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
					CommandHandler('updates_off', updates_off)],
		states = {
			MESSAGE_INCOME: [MessageHandler(filters = Filters.text, callback = state_machine)],
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
