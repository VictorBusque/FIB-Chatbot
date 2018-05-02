#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-- General imports --#
from os import getenv
import requests
import json
import re
from pprint import pprint
from time import time

#-- 3rd party imports --#
from telegram import ChatAction

#-- Local imports --#
from Fibot.chats import Chats
from Fibot.api.oauth import Oauth
from Fibot.NLP.nlg import Query_answer_unit
from Fibot.message_handler import Message_handler
from Fibot.multithreading.threads import Notification_thread, Refresh_token_thread

class Fibot(object):

	""" This object contains information and methods to manage the bot, and interact with
		its users.

	Attributes:
		name (:obj:`str`): Unique identifier for the bot
		bot_token (:obj:`str`): Token to access the bot
		chats (:class:`Fibot.Chat`): Object that represents the chats
		oauth (:class:`Fibot.api.Oauth`): Object that does the oauth communication necessary
		qa (:class:`Fibot.NLP.nlg.Query_answer_unit`): Object that responds to FIB-related queries
		message_handler (:class:`Fibot.message_handler.Message_handler`): Object that handles messages
		delay (:obj:`int`): Cantidad de segundos entre escaneos en los threads
		notification_thread (:class:`Fibot.multithreading.threads.Notification_thread`): Object that enables a thread to scan for notifications.
		refresh_token_thread(:class:`Fibot.multithreading.threads.Refresh_token_thread`): Object that enables a thread to scan for tokens to refresh.
		messages (:obj:`dict`): Object that contains the Fibot configuration messages
		state_machine (:obj:`dict`): Object that simplifies the state machine management
	"""
	def __init__(self, name = 'Fibot'):
		self.name = name
		self.bot_token = getenv('FibotTOKEN')
		self.chats = Chats()
		self.oauth = Oauth()
		self.qa = Query_answer_unit()
		self.message_handler = None
		self.delay = 60
		self.notification_thread = None
		self.refresh_token_thread = Refresh_token_thread(self.delay)
		self.messages = {}
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
			message_handler: Enables it to send messages to users
			notification_thread: Starts its activation and defines the polling interval
			refresh_token_thread: Starts its activation and defines the polling interval (and the offset)
			nlu: Loads the trained models
			qa: Loads the trained models
			messages: Loads the preset messages to memory
	"""
	def load_components(self):
		self.chats.load()
		print("Chats loaded")
		self.message_handler = Message_handler(self.chats)
		print("Message handler loaded")
		self.notification_thread = Notification_thread(self.message_handler, self.delay)
		self.notification_thread.run()
		self.refresh_token_thread.run(initial_offset = 30)
		self.qa.load(train=False)
		print("Query answering model loaded")
		with open('./Data/messages.json', 'r') as fp:
			self.messages = json.load(fp)
		print("Preset messages loaded")

	"""
		Parameters:
			chat_id (:obj:`int`): chat id of the user to send the message to
			action (:obj:`str`): defines the action to send the user (default is typing)

		This function sends an action to the chat with chat_id (using ChatAction helper)
	"""
	def send_chat_action(self, chat_id, action = ChatAction.TYPING):
		self.message_handler.send_chat_action(chat_id, message, typing, reply_to)

	"""
		Parameters:
			chat_id (:obj:`int`): chat id of the user to send the message to
			message (:obj:`str`): content of the message to be sent
			typing (:obj:`bool`): value that defines whether to send typing action or not
			reply_to (:obj:`int` or None): If defined, it is the message_id of the message
				that will be replied to, else no message will be replied.
			parse_mode (:obj:`str`): The parse mode to use (normally Markdown or None)

		This function sends a message to the chat with chat_id with content text,
		and depending on the rest of the parameters it might do extra functionality.
	"""
	def send_message(self, chat_id, message, typing = False, reply_to = None, parse_mode = 'Markdown'):
		self.message_handler.send_message(chat_id, message, typing, reply_to, parse_mode)


	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the user to send the message to
			preset (:obj:`str`): the preset of the message to send
			param (:obj:`str` or None): the parameter of the messages

		This function sends a preset message to the user with user id.
		See /Data/messages.json to see the preset messages.
	"""
	def send_preset_message(self, chat_id, preset, param = None):
		print("#### SENDING PRESET MESSAGE: {} #####".format(preset))
		user_lang = self.chats.get_chat(chat_id)['language']
		if param:
			message = self.messages[user_lang][preset].format(param)
		else:
			message = self.messages[user_lang][preset]
		if 'set_lang' in message: self.send_message(chat_id, message, typing=True, parse_mode = None)
		else: self.send_message(chat_id, message, typing=True)

	"""
		Parameters:
			chat_id (:obj:`str`): chat_id of the user that sent the messages
			message (:obj:`str`): text the user sent
			message_id (:obj:`int`): message_id of the message to reply to


		This function receives a message from a user and decides which mechanism is responsible
		for responding the message.
	"""
	def process_income_message(self, chat_id, message, message_id = None):
		print("##### USER SAID: {} #####".format(message))
		user_language = self.chats.get_chat(chat_id)['language']
		response = self.qa.get_response(message, sender_id = chat_id, language = user_language)
		print("##### RESPONSE IS: {} #####".format(response))
		self.send_message(chat_id, response, typing=True, reply_to = message_id, parse_mode = None)
